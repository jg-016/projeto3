from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render

from ..forms import UserForm, UserUsuarioForm
from ..models import Usuario


def list_usuario_view(request):
    usuarios = Usuario.objects.filter(perfil=Usuario.PERFIL_USUARIO).select_related('usuario')
    context = {
        'usuarios': usuarios,
        'quantidade': usuarios.count(),
    }
    return render(request, 'usuario/usuario.html', context)


def edit_usuario_view(request, usuario_id):
    usuario_obj = get_object_or_404(Usuario, pk=usuario_id)
    user_instance = usuario_obj.usuario
    message = None

    if request.method == 'POST':
        usuarioForm = UserUsuarioForm(request.POST, instance=usuario_obj, current_user=request.user)
        userForm = UserForm(request.POST, instance=user_instance)

        if usuarioForm.is_valid() and userForm.is_valid():
            email = userForm.cleaned_data.get('email')
            if User.objects.filter(email=email).exclude(pk=user_instance.pk).exists():
                message = {
                    'text': 'O e-mail já está sendo utilizado por outro usuário.',
                    'type': 'warning',
                }
            else:
                user_instance = userForm.save(commit=False)
                user_instance.email = email
                user_instance.save()

                usuario_obj = usuarioForm.save(commit=False)
                usuario_obj.usuario = user_instance
                usuario_obj.save()

                message = {
                    'text': 'Dados atualizados com sucesso.',
                    'type': 'success',
                }
        else:
            message = {
                'text': 'Existem dados inválidos no formulário. Verifique os campos abaixo.',
                'type': 'danger',
            }
    else:
        usuarioForm = UserUsuarioForm(instance=usuario_obj, current_user=request.user)
        userForm = UserForm(instance=user_instance)

    context = {
        'usuarioForm': usuarioForm,
        'userForm': userForm,
        'message': message,
    }
    return render(request, 'loja/usuario-edit.html', context)
