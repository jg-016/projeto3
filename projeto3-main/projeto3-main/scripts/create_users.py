import datetime
from django.contrib.auth.models import User
from loja.models import Usuario

users = [
    ('usuario1', 'usuario1@example.com', 'usuario1pass', Usuario.PERFIL_USUARIO),
    ('usuario2', 'usuario2@example.com', 'usuario2pass', Usuario.PERFIL_USUARIO),
    ('admin', 'admin@example.com', 'adminpass', Usuario.PERFIL_ADMIN),
]

for username, email, password, perfil in users:
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    if created:
        user.set_password(password)
        if username == 'admin':
            user.is_staff = True
            user.is_superuser = True
        user.save()

    usuario_obj, created_usuario = Usuario.objects.get_or_create(
        usuario=user,
        defaults={'perfil': perfil, 'aniversario': datetime.date(2000, 1, 1)},
    )
    if not created_usuario and usuario_obj.perfil != perfil:
        usuario_obj.perfil = perfil
        usuario_obj.save()

    print(username, 'created' if created else 'exists', 'perfil', usuario_obj.get_perfil_display())
