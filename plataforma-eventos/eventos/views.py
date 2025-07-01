from django.shortcuts import render, redirect, get_object_or_404
from .forms import CadastroUsuarioForm
from django.contrib import messages
from django.core.mail import send_mail
from io import BytesIO
from .models import Evento, Inscricao
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas


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
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Agora faça login.")
            return redirect('login')

    else:
            form = CadastroUsuarioForm()
    return render(request, 'eventos/cadastro.html', {'form': form})


@login_required
def inscrever(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    usuario = request.user

    inscrito = Inscricao.objects.filter(evento=evento, participante=request.user).exists()

    if not inscrito:
        Inscricao.objects.create(evento=evento, participante=request.user)

        send_mail(
            subject='Confirmação de Inscrição - {}'.format(evento.titulo),
            message=f'Olá {usuario.first_name},\n\nVocê se inscreveu no evento "{evento.titulo}" em {evento.data.strftime("%d/%m/%Y %H:%M")}, no local: {evento.local}.\n\nObrigado!',
            from_email=None,
            recipient_list=[usuario.email],
            fail_silently=False,
        )

    return render(request, 'eventos/inscricao_confirmada.html', {'evento': evento})

def meus_eventos(request):
    inscricoes = Inscricao.objects.filter(participante=request.user).select_related('evento')
    return render(request, 'eventos/meus_eventos.html', {'inscricoes': inscricoes})


def gerar_ingresso(request, id):
    evento = get_object_or_404(Evento, pk=id)
    participante = request.user

    if not Inscricao.objects.filter(participante=participante, evento=evento).exists():
        return HttpResponse('Você não está inscrito nesse evento!', status=403)
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Conteúdo do ingresso
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, 800, "Ingresso - {}".format(evento.titulo))

    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Nome: {participante.get_full_name() or participante.username}")
    p.drawString(100, 750, f"Email: {participante.email}")
    p.drawString(100, 730, f"Data: {evento.data.strftime('%d/%m/%Y %H:%M')}")
    p.drawString(100, 710, f"Local: {evento.local}")
    p.drawString(100, 690, f"Código: EVT-{evento.id}-USR-{participante.id}")
    p.drawString(100, 670, "Apresente este ingresso na entrada do evento.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def cancelar_inscricao(request, id):
    evento = get_object_or_404(Evento, pk=id)
    participante = request.user
    inscricao = Inscricao.objects.filter(participante=participante, evento=evento)

    if inscricao:
        inscricao.delete()
        messages.success(request, f'Você cancelou sua inscrição no evento "{evento.titulo}".')
    else:
        messages.warning(request, 'Você não está inscrito nesse evento.')

    return redirect('meus_eventos')
