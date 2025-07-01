from django.shortcuts import render, redirect, get_object_or_404
from .forms import CadastroUsuarioForm
from django.contrib import messages
from django.core.mail import send_mail
from io import BytesIO
from .models import Evento, Inscricao, Token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings
import hashlib
import time
from django.urls import reverse

def lista_eventos(request):
    
    eventos = Evento.objects.all().order_by('data')

    data = request.GET.get('data')
    local = request.GET.get('local')

    if data:
        eventos = eventos.filter(data__date=data)

    if local:
            eventos = eventos.filter(local__icontains=local)

    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})


def cadastro(request):
    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Cadastro realizado com sucesso! Agora faça login.")
            return redirect('login')

    else:
        form = CadastroUsuarioForm()
    return render(request, 'eventos/cadastro.html', {'form': form})


@login_required
def inscrever(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    usuario = request.user

    inscricao, created = Inscricao.objects.get_or_create(participante=usuario, evento=evento)

    if created:
        send_mail(
            subject='Confirmação de Inscrição - Eventix',
            message=f'Olá {request.user.first_name},\n\nVocê se inscreveu no evento: {evento.titulo} no dia {evento.data.strftime("%d/%m/%Y %H:%M")}.\n\nLocal: {evento.local}\n\nObrigado por usar o Eventix!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

    return redirect('meus_eventos')



def meus_eventos(request):
    inscricoes = Inscricao.objects.filter(participante=request.user).select_related('evento')
    return render(request, 'eventos/meus_eventos.html', {'inscricoes': inscricoes})


def gerar_ingresso(request, id):
    evento = get_object_or_404(Evento, pk=id)
    participante = request.user
    nome_completo = request.user.perfil.nome_completo

    if not Inscricao.objects.filter(participante=participante, evento=evento).exists():
        return HttpResponse('Você não está inscrito nesse evento!', status=403)
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Conteúdo do ingresso
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 800, "Ingresso - {}".format(evento.titulo))

    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Nome: {nome_completo}")
    p.drawString(100, 750, f"Email: {participante.email}")
    p.drawString(100, 730, f"Data: {evento.data.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(100, 710, f"Local: {evento.local}")
    p.drawString(100, 690, f"Código: EVT-{evento.id}-USR-{participante.id}")
    p.drawString(100, 670, "Apresente este ingresso na entrada do evento.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')


def gerar_token_cancelamento(user_id, evento_id):

    raw = f'{user_id}{evento_id}{time.time()}'.encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def solicitar_cancelamento(request, id):
    evento = get_object_or_404(Evento, pk=id)
    token = gerar_token_cancelamento(user_id=request.user.id, evento_id=evento.id)

    Token.objects.create(
        token=token,
        user=request.user,
        evento = evento
    )

    link = request.build_absolute_uri(
        reverse('confirmar_cancelamento', args=[evento.id]) + f'?token={token}'
    )

    send_mail(
        subject='Confirmação de Cancelamento - Eventix',
        message=f'Olá {request.user.first_name},\n\nClique no link abaixo para confirmar o cancelamento da sua inscrição no evento "{evento.titulo}":\n\n{link}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email]
    )

    return redirect('meus_eventos')


def confirmar_cancelamento(request, id):
    token_str = request.GET.get('token')
    evento = get_object_or_404(Evento, id=id)

    try:
        token = Token.objects.get(token=token_str, user=request.user, evento=evento)
    except Token.DoesNotExist:
        return HttpResponse("Token inválido ou expirado.", status=403)

    # Cancela inscrição
    Inscricao.objects.filter(participante=request.user, evento=evento).delete()
    token.delete()  # Remove o token após uso

    return HttpResponse("Inscrição cancelada com sucesso!")
