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

- **Django**
- **Python**
- **SQLite** 
- **Bootstrap **
- **ReportLab** (para geração de PDFs)
- **Email via SMTP** 

## 📸 Interface

Tela de Cadastro:
<img src="https://github.com/user-attachments/assets/395d0ad7-5c99-4375-90b3-f12bfa800b21" alt="Tela de cadastro" width="340">
Tela de Home:
<img src="https://github.com/user-attachments/assets/c689f791-7ba5-4284-a9cb-eed95bed9d8b" alt="Tela de home" width="340">
Aba de eventos:
<img src="https://github.com/user-attachments/assets/2ff52e8b-b2d5-4704-bafc-66ff8a2a6d32" alt="Tela de meus_eventos" width="340">
Tela de Perfil:
<img src="https://github.com/user-attachments/assets/e33ded36-d1a5-44b4-b46e-1359b84db6f6" alt="Tela de perfil" width="340">

## 📦 Como rodar o projeto localmente

1. **Clone o repositório:**

```python
git clone https://github.com/ndamasc/django-eventix.git
cd django-eventix
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
