from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from .validators import *

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PacienteForm(ModelForm):
    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'apellido', 'fecha_nacimiento', 'genero', 'telefono', 'correo']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el rut sin puntos y con guión'
            }),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9XXXXXXXX '
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@correo.cl'
            }),
        }

    #validaciones con importaciones
    #rut

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        try:
            rut_chile = RutChile(rut)
            if not rut_chile.es_rut:
                raise ValidationError("El RUT ingresado no es válido.")
            return rut_chile.rut
        except ValidationError as e:
            raise ValidationError(e)
        
    #NOMBRE
        
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        try:
            return validar_nombre(nombre)
        except ValidationError as e:
            raise ValidationError(e)
        
    #APELLIDO
        
    def clean_apellido(self):
        apellido = self.cleaned_data.get('apellido')
        try:
            return validar_apellido(apellido)
        except ValidationError as e:
            raise ValidationError(e)
        
    #TELEFONO

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        try:
            return validar_telefono(telefono)
        except ValidationError as e:
            raise ValidationError(e)


class AtencionForm(forms.ModelForm):
    paciente = forms.CharField(
        max_length=12,
        widget=forms.HiddenInput(),  # Ocultar el campo de RUT del Paciente
        label="RUT del Paciente"
    )

    ficha_medica = forms.CharField(
        widget=forms.HiddenInput(),  # Ocultar el campo de Ficha Médica
        required=False,
        label="Ficha Médica"
    )
    
    medico = forms.CharField(
        widget=forms.HiddenInput(),  # Ocultar el campo de Médico
        required=False,
        label="Médico"
    )

    fecha_atencion = forms.DateField(
        widget=forms.HiddenInput(),  # Ocultar el campo de Fecha de Atención
        label="Fecha de Atención"
    )

    especialidad = forms.CharField(
        widget=forms.HiddenInput(),  # Ocultar el campo de Especialidad
        required=False,
        label="Especialidad"
    )

    class Meta:
        model = Atencion
        fields = ['anamesis', 'medicamentos_recetados', 'examenes_indicados', 'diagnostico']
        widgets = {
            'anamesis': forms.Textarea(attrs={'class': 'form-control'}),
            'medicamentos_recetados': forms.Textarea(attrs={'class': 'form-control'}),
            'examenes_indicados': forms.Textarea(attrs={'class': 'form-control'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Llamar al constructor padre para inicializar el formulario
        initial_data = kwargs.get('initial', {})
        super(AtencionForm, self).__init__(*args, **kwargs)

        # Establecer valores iniciales para los campos ocultos
        self.fields['fecha_atencion'].initial = date.today()
        self.fields['paciente'].initial = initial_data.get('paciente')
        self.fields['ficha_medica'].initial = initial_data.get('ficha_medica')
        self.fields['medico'].initial = initial_data.get('medico')

        # Establecer el valor inicial de la especialidad según el médico proporcionado
        medico = initial_data.get('medico')
        if medico and hasattr(medico, 'medico_profile'):
            self.fields['especialidad'].initial = medico.medico_profile.especialidad.descripcion


    def clean_paciente(self):
        rut = self.cleaned_data['paciente']
        try:
            paciente = Paciente.objects.get(rut=rut)
            return paciente
        except Paciente.DoesNotExist:
            raise forms.ValidationError('No existe un paciente con el RUT ingresado.')

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['especialidad']
        widgets = {
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
        }

def __init__(self, *args, **kwargs):
        paciente_rut = kwargs.pop('paciente_rut', None)
        super(AtencionForm, self).__init__(*args, **kwargs)
        
        if paciente_rut:
            # Buscar el paciente y la ficha médica correspondiente
            paciente = Paciente.objects.filter(rut=paciente_rut).first()
            if paciente:
                ficha_medica = FichaMedica.objects.filter(paciente=paciente).first()
                if ficha_medica:
                    # Establecer el valor inicial de la ficha médica
                    self.fields['ficha_medica'] = forms.ModelChoiceField(
                        queryset=FichaMedica.objects.filter(paciente=paciente),
                        initial=ficha_medica,
                        widget=forms.HiddenInput()
                    )
                else:
                    self.fields['ficha_medica'] = None
            else:
                self.fields['ficha_medica'] = None
        else:
            self.fields['ficha_medica'] = None

class EditarPacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'genero', 'telefono', 'correo']  # Excluir el campo 'rut'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditarPacienteForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['fecha_nacimiento'].initial = self.instance.fecha_nacimiento

class BuscarPacienteForm(forms.Form):
    rut = forms.CharField(
        max_length=12, 
        label='RUT', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el RUT sin puntos ni guión'})
    )

    def clean_rut(self):
        rut_sin_formato = self.cleaned_data['rut']

        try:
            rut_validador = RutChile(rut_sin_formato)
        except ValidationError as e:
            raise forms.ValidationError(e)

        rut_formateado = rut_validador.rut

        if not Paciente.objects.filter(rut=rut_formateado).exists():
            raise forms.ValidationError('No existe un paciente con el RUT ingresado.')

        return rut_formateado