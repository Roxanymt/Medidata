from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

class TipoMedico(models.Model):
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medico_profile', null=True, blank=True)
    especialidad = models.ForeignKey(TipoMedico, on_delete=models.CASCADE)    

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.especialidad.descripcion}"

class Paciente(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    rut = models.CharField(max_length = 12, blank=False, unique= True)
    nombre = models.CharField(max_length = 40, blank=False)
    apellido = models.CharField(max_length = 40, blank=False)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, blank=False)
    telefono = models.CharField(max_length = 12, blank=False) 
    correo = models.EmailField(blank=False)

    def __str__(self):
        return f"{self.rut}"

class FichaMedica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"

class Atencion(models.Model):
    ficha_medica = models.ForeignKey(FichaMedica, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(User, on_delete=models.CASCADE)
    especialidad = models.ForeignKey(TipoMedico, on_delete=models.SET_NULL, null=True, blank=True)  # Nueva relación a TipoMedico
    fecha_atencion = models.DateField()
    anamesis = models.TextField()
    medicamentos_recetados = models.TextField(blank=True, null=True)
    examenes_indicados = models.TextField(blank=True, null=True)
    diagnostico = models.TextField()

    def __str__(self):
        return f"Atención de {self.paciente} por {self.medico} el {self.fecha_atencion}"

@receiver(post_save, sender=Paciente)
def crear_ficha_medica(sender, instance, created, **kwargs):
    if created:
        FichaMedica.objects.create(paciente=instance)
