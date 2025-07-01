from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from django.conf import settings


caminho_fonte = os.path.join(settings.BASE_DIR, 'eventos', 'static', 'fonts', 'Montserrat-Light.ttf')
caminho_imagem = os.path.join(settings.BASE_DIR, 'eventos', 'static', 'images', 'background.jpg')

imagem_fundo = ImageReader(caminho_imagem)
nome_fonte_titulo = "Montserrat-Light"


pdfmetrics.registerFont(TTFont(nome_fonte_titulo, caminho_fonte))

def gerar_ingresso_pdf(evento, participante, nome_completo):
    buffer = BytesIO()
    largura = 750  
    altura = 300   
    p = canvas.Canvas(buffer, pagesize=(largura, altura))

    p.drawImage(imagem_fundo, 0, 0, width=largura, height=altura)

    azul_escuro = colors.HexColor("#0e3950")
    cinza = colors.HexColor("#F4F4F4")
    branco = colors.white

    # Carregar imagem de fundo personalizada
    caminho_fundo = os.path.join(settings.BASE_DIR, 'eventos', 'static', 'images', 'background.jpg')
    fundo = ImageReader(caminho_fundo)
    p.drawImage(fundo, 0, 0, width=largura, height=altura)

    # Texto no cabeçalho (mantido por cima da imagem)

    texto = "Eventix - Ingresso"
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(azul_escuro)
    largura_texto = p.stringWidth(texto, "Helvetica-Bold", 24)
    x = (largura - largura_texto) / 2
    y = altura - 35 
    
    # Desenha o texto centralizado
    p.drawString(x, y, texto)

    altura_cabecalho = 40

    y_atual = altura - altura_cabecalho - 30
    espaco_linhas = 30

    p.setFont(nome_fonte_titulo, 20)
    p.setFillColor(azul_escuro)
    p.drawString(40, y_atual, evento.titulo.upper())

    y_atual -= espaco_linhas
    p.setFont("Helvetica-Bold", 18)
    p.drawString(40, y_atual, evento.data.strftime("%Hh%M"))
    p.drawString(180, y_atual, evento.data.strftime("%d.%B").upper())

    y_atual -= espaco_linhas - 4
    p.setFont("Helvetica", 11)
    p.drawString(40, y_atual, "Horário")
    p.drawString(180, y_atual, evento.data.strftime("%A").capitalize())

    y_atual -= espaco_linhas
    p.setFont("Helvetica-Bold", 14)
    p.drawString(40, y_atual, f"Local: {evento.local}")

    y_atual -= espaco_linhas
    p.setFont("Helvetica", 13)
    p.drawString(40, y_atual, f"Participante: {nome_completo}")

    y_atual -= espaco_linhas - 6
    p.drawString(40, y_atual, f"E-mail: {participante.email}")

    y_atual -= espaco_linhas
    codigo = f"EVT-{evento.id}-USR-{participante.id}"
    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, y_atual, f"Código do ingresso: {codigo}")

    p.setFont("Helvetica-Oblique", 9)
    p.drawString(40, 40, "Apresente este ingresso na entrada do evento.")



    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer