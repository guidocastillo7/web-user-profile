from django.shortcuts import render, redirect
from .forms import LoginForm, RegistroForm, RegistroPrueba, RegistroUser, RegistroOriginal, EditarPerfilUsuario
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from usuario.models import Usuario
from django.contrib.auth.decorators import login_required
from datetime import datetime
from PIL import Image

# Create your views here.

#En la misma vista donde esta el formulario pa iniciar sesion puedo hacer de una vez el metodo login con los datos q agarra del POST
def inicio(request):

    if request.user.is_authenticated:
        return redirect('/perfil')

    form = LoginForm()

    context = {
        'form':form
    }

    if request.method == 'POST':
        dataUsuario = request.POST['username']
        dataPass = request.POST['password']

        usuarioAuth = authenticate(request, username= dataUsuario, password= dataPass)
        if usuarioAuth is not None:
            login(request, usuarioAuth)
            return redirect('/perfil')

        else:
            context = {
                'form':form,
                'msj':'Datos incorrectos'
            }


    return render(request, 'inicio.html', context)



def cerrarSesion(request):
    logout(request)
    return redirect('/')




def registroUsuario(request):
    form = RegistroForm()
    formPrueba = RegistroPrueba()
    formUser = RegistroUser()
    formOriginal = RegistroOriginal()



    context = {
        'form':form,
        'formPrueba':formPrueba,
        'formUser':formUser,
        'formOriginal':formOriginal
    }

    if request.method == 'POST':
        pass



    return render(request, 'registro.html', context)


'''Registrar el usuario con el RegistroForm'''
def registrando1(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            nvUser = User.objects.create_user(username= data['username'], email= data['email'], password= data['passw'])
            nvUser.first_name = data['nombre']
            nvUser.last_name = data['apellido']
            nvUser.save()

        else:
            context = {
                'form':form
            }

            return render(request, 'registro.html', context)

    return redirect('/')



'''Registrar el usuario con el RegistroOriginal'''
def registrando2(request):
    if request.method == 'POST':
        form = RegistroOriginal(request.POST)
        

        if form.is_valid():
            data = form.cleaned_data

            usuario = User.objects.create_user(username= data['username'], email= data['email'], password= data['password2'])

        else:
            errores = form.errors
            context = {
                'formOriginal':form,
                'errores':errores
            }
            
            return render(request, 'registro.html', context)

    return redirect('/')


@login_required(login_url='/')
def perfil(request):

    username = request.user.username
    email = request.user.email
    nombre = request.user.first_name
    apellido = request.user.last_name

    
    try:
        persona = Usuario.objects.get(usuario= request.user)
        pais = persona.pais
        fecha_nacimiento = persona.fecha_nacimiento
        imagen = persona.imagen

    except:
        #Pongo esto pa q lo obligue a completar su perfil y no se vea sin datos
        return redirect('/editarPerfil')

    context = {
        'username':username,
        'email':email,
        'nombre':nombre,
        'apellido':apellido,
        'pais':pais,
        'fecha':fecha_nacimiento,
        'imagen':imagen
    }

    return render(request, 'perfil.html', context)


@login_required(login_url='/')
def editarPerfil(request):
    '''Quede aqui en terminar el formulario pa q haga el chequeo
    del username q ya existe, terminar de configurar lo de la imagen,
    q cuando no seleccione imagen no me salga error'''


    try:
        persona = Usuario.objects.get(usuario= request.user)
        formu = EditarPerfilUsuario()
        formu['fecha_editar'].field.required = False

        '''Con el formu.initial cargo el formulario con los datos del usuario, pa q no tenga q escribilos todos de nuevo
       en tal caso de q quiera cambiar una sola cosa'''

        formu.initial = {
        'username':request.user.username,
        'email':request.user.email,
        'nombre':request.user.first_name,
        'apellido':request.user.last_name,
        'pais':persona.pais,
        'fecha_nacimiento':persona.fecha_nacimiento,
    }
        context = {
            'formu':formu
        }
        

    except:
        formu = EditarPerfilUsuario()
        mensaje = 'Por favor completa tu perfil para continuar..'

        formu.initial = {
        'username':request.user.username,
        'email':request.user.email,
        'nombre':request.user.first_name,
        'apellido':request.user.last_name
    }

        context = {
            'formu':formu,
            'msj':mensaje
        }

    if request.method == 'POST':
        formulario2 = EditarPerfilUsuario(request.POST, request.FILES)
        formulario2['fecha_editar'].field.required = False
        
        
        if formulario2.is_valid():
            data = formulario2.cleaned_data

            actUser = User.objects.get(pk= request.user.id)

            try:
                actUser.username = data['username']
                actUser.email = data['email']
                actUser.first_name = data['nombre']
                actUser.last_name = data['apellido']
                actUser.save()
            except:
                formulario2.add_error('username', 'El username ya esta en uso!')
                context = {
                    'formu':formulario2
                }
                return render(request, 'editarPerfil.html', context)
            

            try:
                actUsuario = Usuario.objects.get(usuario= actUser)
                actUsuario.pais = data['pais']

                if data['imagen'] == None:
                    actUsuario.imagen = actUsuario.imagen
                else:
                    actUsuario.imagen = data['imagen']
                

                if data['fecha_editar'] is None:
                    actUsuario.fecha_nacimiento = data['fecha_nacimiento']
                    actUsuario.save()             

                else:
                    actUsuario.fecha_nacimiento = data['fecha_editar']
                    actUsuario.save()

            except:
                nvoUsuario = Usuario()
                nvoUsuario.usuario = actUser
                nvoUsuario.pais = data['pais']
                nvoUsuario.fecha_nacimiento = data['fecha_editar']
                if data['imagen'] is not None:
                    nvoUsuario.imagen = data['imagen']
                nvoUsuario.save()

            return redirect('/perfil')
            

        else:
            context = {
                'formu':formulario2
            }

        
    '''if request.method == 'POST':

        actUser = User.objects.get(pk= request.user.id)
        actUser.username = request.POST['username']
        actUser.email = request.POST['email']
        actUser.first_name = request.POST['nombre']
        actUser.last_name = request.POST['apellido']
        actUser.save()

        try:
            actUsuario = Usuario.objects.get(usuario= actUser)
            actUsuario.pais = request.POST['pais']
            actUsuario.imagen = request.FILES['imagen']

            if request.POST['fechaEditada'] == '':
                actUsuario.save()
            else:
                actUsuario.fecha_nacimiento = request.POST['fechaEditada']
                actUsuario.save()
            
        except:
            nvoUser = Usuario()
            nvoUser.usuario = request.user
            nvoUser.pais = request.POST['pais']
            
            
            if request.POST['fechaEditada'] == '':
                nvoUser.save()
            else:
                nvoUser.fecha_nacimiento = request.POST['fechaEditada']
                nvoUser.save()

        return redirect('/perfil')'''


    return render(request, 'editarPerfil.html', context)