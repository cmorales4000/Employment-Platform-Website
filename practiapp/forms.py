from django import forms
from django.forms import ModelForm
from .models import oferta, Usuario, aplicantes
from django.contrib.auth.forms import UserCreationForm



class formusuario(forms.ModelForm):
    """
    variables:
    password1: contraseña
    password2: verificacion contraseña
    """
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Ingrese contraseña',
            'required':'required'
        }
    ))

    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Confirme su contraseña',
            'required':'required'
        }
    ))

    class Meta:
        model=Usuario
        fields=['is_empresa','username','nombre','dni','email','contacto','imagen','password1','password2']
        exclude=['imagen','contacto']
        widgets={
            'is_empresa': forms.CheckboxInput(
                attrs={
                    'class':'form-control'
                    }),
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Username'
                }),
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre Completo'
                }),
            'dni': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Identificación'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo Electrónico'
                }),
            'contacto': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Teléfono'
                }),
            'imagen': forms.FileInput(
                attrs={
                    'class':'form-control'
                })
               
        }

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user


class formperfil(forms.ModelForm): 

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Confirme su Contraseña',
            'required':'required'
        }
    ))

    
    class Meta:
        model = Usuario
        fields = ['is_empresa','username','nombre','dni','email','contacto','imagen','hdv','password1']
        widgets={
            'is_empresa': forms.CheckboxInput(
                attrs={
                    'class':'form-control'
                    }),
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Username'
                }),
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre Completo'
                }),
            'dni': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Identificación'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo Electrónico'
                }),
            'contacto': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Teléfono'
                }),
            'imagen': forms.FileInput(
                attrs={
                    'class':'form-control'
                }),
            'hdv': forms.FileInput(
                attrs={
                    'class':'form-control'
                })
               
        }
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            if user.is_empresa:
                user.hdv=""
                user.save()
        return user


class formoferta(forms.ModelForm):
    
    class Meta:
        model = oferta
        fields = ['titulo', 'area', 'ciudad', 'contenido', 'salario', 'horario']
        widgets={
            'titulo': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Titulo'
                }),
            'area': forms.Select(
                attrs={
                    'class':'form-control',
                    'placeholder':'Area'
                }),
            'ciudad': forms.Select(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ciudad'
                }),
            'contenido': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Contenido de la oferta'
                }),
            'salario': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Salario'
                }),
            'horario': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Horario'
                }),
        }


class formaplicar(forms.ModelForm):

    class Meta:
        model = aplicantes
        fields = []





