from django import forms
from usuario.models import Usuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de Usuario', max_length=150, required=True)
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)

class DateInput(forms.DateInput):
    input_type = 'date'

class RegistroForm(forms.Form):
    '''Este modo solo me verifica q el username no se puede repetir
    pero cuando manda el error tengo q crear yo el error manualmente
    y q se vea en el template'''

    username = forms.CharField(label='Nombre de Usuario', max_length=150, required=True)
    email = forms.EmailField(label='Email', max_length=255, required=True)
    nombre = forms.CharField(label='Nombre', max_length=150)
    apellido = forms.CharField(label='Apellido', max_length=150)
    passw = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput)


'''Prueba de formulario heredando del modelo de usuario'''
class RegistroPrueba(forms.ModelForm):   #Se hereda de ModelForm cuando el formulario va a estar basado en un modelo
    class Meta:                          #En este caso seria el modelo de Usuario
        model = Usuario
        fields = ('__all__')



'''Prueba de formulario heredando del modelo User por defecto de Django'''
class RegistroUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')



'''Prueba de formulario heredando el original User Creation Form'''
class RegistroOriginal(UserCreationForm):

    '''Este metodo es mejor pq sigue haciendo sus validaciones por defecto
    de las 2 contraseñas, q tengan sus caracteristicas y q no se puedan duplicar
    los campos Unicos y muestra los errores en el template automaticamente'''

    username = forms.CharField(label='Nombre de Usuario', help_text='Aqui pongo los requisitos de este campo')
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmación de contraseña', widget=forms.PasswordInput)



'''Prueba de Formulario para editar el perfil.
Asi es la mejor forma, automaticamente no me deja quedar los campos en blanco, no tengo q hacer el html de 0,
y hace la validacion de el email por ejemplo.
Me falta hacer la validacion del nombre de usuario, pa q cuando se ponga uno ya en uso muestre el error'''
class EditarPerfilUsuario(forms.Form):
    username = forms.CharField(label='Username', required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    nombre = forms.CharField(label='Nombre', initial='nombre',required=True, max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    apellido = forms.CharField(label='Apellido', required=True,max_length=150, widget=forms.TextInput(attrs={'class':'form-control'}))
    pais = forms.CharField(label='Pais', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    fecha_nacimiento = forms.CharField(label='Fecha de nacimiento', required=False, widget=forms.TextInput(attrs={'readonly':'readonly', 'class':'form-control'}))
    fecha_editar = forms.DateField(label='Fecha a editar', widget=DateInput(attrs={'class':'form-control'}))
    imagen = forms.FileField(label='Foto de perfil', required=False, widget=forms.FileInput(attrs={'class':'form-control'}))


    #Prueba de crear la verificacion del username, pa q me de el error si ya existe
    '''def clean_username(self):
        username2 = self.cleaned_data['username']
        todos = User.objects.filter(username= username2)

        if todos.exists():
            raise forms.ValidationError('Este nombre de usuario ya esta en uso!')
        return username2'''