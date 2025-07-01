from django.db import models

from django.contrib.auth.models import User

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    data = models.DateTimeField()
    local = models.CharField(max_length=100)
    vagas = models.PositiveIntegerField()
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
    

class Inscricao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscricoes')
    participante = models.ForeignKey(User, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.participante.username} em {self.evento.titulo}'