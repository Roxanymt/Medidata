from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group, User
from .forms import * 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    return render(request, 'core/index.html')

def base(request):
    return render(request, 'core/base.html')

def admin(request):
    return render(request, 'core/admin.html')

@login_required
def medico(request):
    return render(request, 'core/medico.html', {'nombre_usuario': request.user.get_full_name() or request.user.username})

@login_required
def paciente(request):
    return render(request, 'core/paciente.html', {'nombre_usuario': request.user.get_full_name() or request.user.username})

def quienessomos(request):
    return render(request, 'core/quienessomos.html')

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Administradores').exists(): #si el usuario está en el grupo administradores
                    return redirect('admin')  # Redirige a la URL del administrador
                elif user.groups.filter(name='Medicos').exists():
                    return redirect('medico')  # Redirige a la URL del médico
                elif user.groups.filter(name='Pacientes').exists():
                    return redirect('paciente')  # Redirige a la URL del paciente
    else:
        form = CustomAuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def admin(request):
    return render(request, 'core/admin.html')

#CRUD

@login_required

def registrar_paciente(request):
    if request.method == 'POST':
        formulario = PacienteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            #messages.success(request, "Paciente registrado correctamente")
            return redirect('registro_exitoso')  # Redirige a la vista de éxito
        else:
            messages.error(request, "Error al registrar el paciente. Por favor, verifica los datos ingresados.")
    else:
        formulario = PacienteForm()
    return render(request, 'core/paciente/registrar_paciente.html', {'form': formulario})
            


@login_required
def listar_pacientes(request):
    listaPacientes = Paciente.objects.all()
    paginator = Paginator(listaPacientes, 10)

    # Obtén el número de página desde la solicitud GET
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # Obtener la página actual

    datos = {'page_obj': page_obj}  # Pasar la página al template

    return render(request, 'core/paciente/listar_pacientes.html',datos)


@login_required
def editar_paciente(request,id):
    paciente = Paciente.objects.get(id=id)
    datos = { 'form' : EditarPacienteForm (instance = paciente), 'paciente': paciente }

    if request.method == 'POST':
        formulario = EditarPacienteForm(data = request.POST, instance = paciente)
        if formulario.is_valid():
            formulario.save();
            messages.success(request, "Paciente modificado correctamente")
            datos['form'] = formulario

    return render(request, 'core/paciente/editar_paciente.html',datos)


@login_required
def registrar_atencion(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    medico = request.user
    ficha_medica = FichaMedica.objects.filter(paciente=paciente).first()
    especialidad = medico.medico_profile.especialidad.descripcion if hasattr(medico, 'medico_profile') else 'Sin especialidad'
    datos = {'form': AtencionForm(initial={
        'paciente': paciente.rut,
        'ficha_medica': ficha_medica.id if ficha_medica else None,
        'medico': medico.get_full_name() or medico.username,  # Utilizar el nombre completo del usuario
        'fecha_atencion': date.today(),  # Inicializar la fecha de atención
        'especialidad': especialidad
        }),
        'especialidad': especialidad  # Agregar la especialidad al contexto para la plantilla
    }
    previsualizar = False

    if request.method == 'POST':
        formulario = AtencionForm(data=request.POST)
        if 'preview' in request.POST:
            if formulario.is_valid():
                previsualizar = True
                datos['form'] = formulario
                datos['previsualizar'] = True
        elif 'confirm' in request.POST:
            if formulario.is_valid():
                atencion = formulario.save(commit=False)
                atencion.medico = medico  # Asignar la instancia del Medico (User)
                atencion.paciente = paciente  # Asignar la instancia del Paciente
                atencion.ficha_medica = ficha_medica  # Asociar FichaMedica
                atencion.fecha_atencion = date.today()  # Asignar la fecha de atención
                atencion.save()
                #messages.success(request, "Atención registrada correctamente!")
                return redirect('atencion_exito')
        elif 'edit' in request.POST:
            # El caso 'edit' puede simplemente permitir al usuario editar de nuevo
            datos['form'] = formulario
            messages.info(request, "Edite la información antes de confirmar.")

    return render(request, 'core/atencion/registrar_atencion.html', {
        'form': datos['form'],
        'previsualizar': previsualizar,
        'msj': datos.get('msj', None),
        'paciente': paciente,
        'ficha_medica': ficha_medica,
        'medico': medico.get_full_name() or medico.username,
        'especialidad': especialidad  # Pasar la especialidad al contexto
    })

def atencion_exito(request):
    return render(request, 'core/atencion/atencion_exito.html')


from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def listar_fichasmedicas(request):
    # Obtener todas las fichas médicas con el uso de select_related para optimizar consultas
    fichas_medicas = FichaMedica.objects.select_related('paciente').all()

    # Paginación: Mostrar 10 fichas por página
    paginator = Paginator(fichas_medicas, 10)  # Cambia el 10 al número deseado de fichas por página
    page_number = request.GET.get('page')  # Obtener el número de página de los parámetros de la URL
    page_obj = paginator.get_page(page_number)  # Obtener la página correspondiente

    return render(request, 'core/ficha_medica/listar_fichasmedicas.html', {
        'page_obj': page_obj,  # Pasar la página actual al contexto
    })



def ficha_paciente(request, id):
    ficha = get_object_or_404(FichaMedica, id=id)
    atenciones = Atencion.objects.filter(ficha_medica=ficha)

    return render(request, 'core/ficha_medica/ficha_paciente.html', {
    'ficha': ficha,
    'atenciones': atenciones,
    })

@login_required
def detalle_atencion(request, id):
    atencion = get_object_or_404(Atencion, id=id)
    ficha_medica = atencion.ficha_medica  # Obtener la ficha médica asociada a la atención
    medico_profile = getattr(atencion.medico, 'medico_profile', None)
    especialidad = medico_profile.especialidad.descripcion if medico_profile else 'Sin especialidad'

    return render(request, 'core/atencion/detalle_atencion.html', {
        'atencion': atencion,
        'ficha_medica': ficha_medica,
        'especialidad': especialidad
    })

@login_required
def registro_exitoso(request):
    return render(request, 'core/paciente/registro_exitoso.html')

@login_required
def buscar_paciente(request):
    form = BuscarPacienteForm()
    paciente = None

    if request.method == 'POST':
        form = BuscarPacienteForm(request.POST)
        if form.is_valid():
            rut_formateado = form.cleaned_data['rut']
            try:
                paciente = Paciente.objects.get(rut=rut_formateado)
            except Paciente.DoesNotExist:
                paciente = None

    return render(request, 'core/paciente/buscar_paciente.html', {
        'form': form,
        'paciente': paciente,
    })

@login_required
def soporte(request):
    return render(request, 'core/soporte.html')