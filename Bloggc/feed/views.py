from django.shortcuts import render, redirect
from .models import Publicacion
from django.contrib.auth.models import User
from usuario.models import Usuario
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/')
def feed(request):

    publi = Publicacion.objects.all()
    usuario = Usuario.objects.get(usuario= request.user)
    img = usuario.imagen

    context = {
        'publi':publi,
        'img':img
    }

    return render(request, 'feed.html', context)


def publicar(request):

    if request.method == 'POST':

        #user = User.objects.get(pk= request.user.id)

        publi = Publicacion()
        publi.autor = request.user
        publi.contenido = request.POST['contenido']
        publi.save()

    return redirect('/feed')