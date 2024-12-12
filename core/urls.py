from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', index, name="index"), # PAGINA DE INICIO
    path('index/', index, name="index"),
    path('admin/', admin, name="admin"),
    path('medico/', medico, name="medico"),
    path('paciente/', paciente, name="paciente"),
    path('quienessomos/' , quienessomos, name="quienessomos"),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    #CRUD
    path('registrar_paciente/', registrar_paciente, name='registrar_paciente'),
    path('listar_pacientes/', listar_pacientes, name='listar_pacientes'),
    path('editar_paciente/<id>/', editar_paciente, name='editar_paciente'),
    path('buscar_paciente/', buscar_paciente, name='buscar_paciente'),
    path('registrar_atencion/<id>/', registrar_atencion, name='registrar_atencion'),
    path('atencion_exito/', atencion_exito, name='atencion_exito'),
    path('detalle_atencion/<id>/', detalle_atencion, name='detalle_atencion'),
    path('listar_fichasmedicas/', listar_fichasmedicas, name='listar_fichasmedicas'),
    path('ficha_paciente/<id>/', ficha_paciente, name='ficha_paciente'),
    path('registro_exitoso/', registro_exitoso, name='registro_exitoso'),
    path('soporte/', soporte, name='soporte'),
]
