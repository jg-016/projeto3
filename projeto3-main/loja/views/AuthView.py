from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from loja.forms.AuthForm import LoginForm, RegisterForm


def login_view(request):
    login_form = LoginForm()
    message = None

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('/')

            message = {
                'type': 'danger',
                'text': 'Dados de usuário incorretos'
            }

    context = {
        'form': login_form,
        'message': message,
        'title': 'Login',
        'button_text': 'Entrar',
        'link_text': 'Registrar',
        'link_href': '/register',
    }

    return render(request, 'auth/auth.html', context, status=200)


def logout_view(request):
    logout(request)
    return redirect('/login')


def register_view(request):
    register_form = RegisterForm()
    message = None

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']

            if User.objects.filter(username=username).first() is not None:
                message = {
                    'type': 'danger',
                    'text': 'Já existe um usuário com este username!'
                }
            elif User.objects.filter(email=email).first() is not None:
                message = {
                    'type': 'danger',
                    'text': 'Já existe um usuário com este e-mail!'
                }
            else:
                user = User.objects.create_user(username, email, password)
                message = {
                    'type': 'success' if user is not None else 'danger',
                    'text': (
                        'Conta criada com sucesso!'
                        if user is not None
                        else 'Um erro ocorreu ao tentar criar o usuário.'
                    )
                }

    context = {
        'form': register_form,
        'message': message,
        'title': 'Registrar',
        'button_text': 'Registrar',
        'link_text': 'Login',
        'link_href': '/login',
    }

    return render(request, 'auth/auth.html', context, status=200)