# 🎟️ Eventix - Plataforma de Gerenciamento de Eventos

Eventix é uma aplicação web desenvolvida com Django que permite que usuários visualizem eventos, façam inscrições, cancelem participação e gerem ingressos em PDF. É ideal para quem deseja organizar eventos e permitir controle de participantes de forma simples e intuitiva.

## 🚀 Funcionalidades

- Cadastro e login de usuários
- Perfil de usuário com dados pessoais e senha editáveis
- Listagem de eventos com filtros por data e local
- Inscrição e cancelamento com confirmação por e-mail
- Geração de ingresso em PDF com design personalizado
- Administração dos dados pelo painel do Django Admin

## 🛠 Tecnologias utilizadas

- **Django 5.2**
- **Python 3.x**
- **SQLite** 
- **Bootstrap 5**
- **ReportLab** (para geração de PDFs)
- **Email via SMTP** 

## 📸 Interface

![Tela de Cadastro](C:\Users\DELL\Documents\alura-cursos\django\plataforma-eventos\django-eventix\plataforma-eventos\docs\cadastro.png)
![Tela de Home](C:\Users\DELL\Documents\alura-cursos\django\plataforma-eventos\django-eventix\plataforma-eventos\docs\home.png)
![Tela de Perfil](C:\Users\DELL\Documents\alura-cursos\django\plataforma-eventos\django-eventix\plataforma-eventos\docs\perfil.png)
![Tela de Eventos do Usuário](C:\Users\DELL\Documents\alura-cursos\django\plataforma-eventos\django-eventix\plataforma-eventos\docs\meus_eventos.png)

## 📦 Como rodar o projeto localmente

1. **Clone o repositório:**

```python
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo
```

2. **Instale as dependencias:**

```python
pip -r requirements.txt
```

3. **Faça as migrações para o banco de dados:**
```python
python manage.py migrate
```

4. **Crie o superusuario:**

```python
python manage.py createsuperuser
```

5. **Rode o servidor:**

```python
python manage.py runserver
```
