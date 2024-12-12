from django.contrib import admin
from . models import *
# Register your models here.

class MedicoAdmin(admin.ModelAdmin):
    list_display = ['nombre_medico', 'apellido_medico', 'especialidad']
    search_fields = ['nombre_medico', 'apellido_medico']
    list_per_page = 10

    def nombre_medico(self, obj):
        return obj.user.first_name  # Accede al nombre del usuario relacionado

    def apellido_medico(self, obj):
        return obj.user.last_name  # Accede al apellido del usuario relacionado

class PacienteAdmin(admin.ModelAdmin):
    list_display = ['nombre','apellido', 'rut']
    search_fields = ['nombre', 'apellido','rut']
    list_per_page = 10

class FichaMedicaAdmin(admin.ModelAdmin):
    list_display = ['paciente']
    search_fields = ['rut']
    list_per_page = 10

class AtencionAdmin(admin.ModelAdmin):
    list_display = ['paciente','medico','fecha_atencion']
    search_fields = ['paciente','medico','fecha_atencion']
    list_per_page = 10

admin.site.register(TipoMedico)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(FichaMedica, FichaMedicaAdmin)
admin.site.register(Atencion, AtencionAdmin)
