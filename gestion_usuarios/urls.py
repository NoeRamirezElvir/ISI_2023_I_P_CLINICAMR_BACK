from django.urls import path


from .views.cargo_views import *
from .views.documento_views import *
from .views.especialidad_views import *
from .views.empleado_views import *
from .views.usuario_views import *
from .views.Impuesto_views import *
from .views.Paciente_views import *
from .views.login_views import *


urlpatterns = [
    path('login/', LoginViews.as_view() , name='login_view'),
    path('cargos/', CargosView.as_view() , name='cargo_list'),
    path('cargos/busqueda/<str:criterio>/<str:campo>', CargosView.as_view() , name='cargos_process'),
    path('cargos/id/<int:id>', CargosView.as_view() , name='cargos_process_id'),
    path('documentos/', DocumentoViews.as_view() , name='documento_list'),
    path('documentos/busqueda/<str:criterio>/<str:campo>', DocumentoViews.as_view() , name='documento_process'),
    path('documentos/id/<int:id>', DocumentoViews.as_view() , name='documento_process_id'),
    path('especialidad/', EspecialidadViews.as_view() , name='especialidad_list'),
    path('especialidad/busqueda/<str:criterio>/<str:campo>', EspecialidadViews.as_view() , name='especialidad_process'),
    path('especialidad/id/<int:id>', EspecialidadViews.as_view() , name='especialidad_process_id'),
    path('empleados/', EmpleadoViews.as_view() , name='empleado_list'),
    path('empleados/busqueda/<str:criterio>/<str:campo>', EmpleadoViews.as_view() , name='empleado_process'),
    path('empleados/id/<int:id>', EmpleadoViews.as_view() , name='empleado_process_id'),
    path('usuarios/', UsuarioViews.as_view() , name='usuario_list'),
    path('usuarios/busqueda/<str:criterio>/<str:campo>', UsuarioViews.as_view() , name='usuario_process'),
    path('usuarios/id/<int:id>', UsuarioViews.as_view() , name='usuario_process_id'),
    path('Impuestos/', ImpuestoViews.as_view() , name='Impuestos_list'),
    path('Impuestos/busqueda/<str:criterio>/<str:campo>', ImpuestoViews.as_view() , name='Impuestos_process'),
    path('Impuestos/id/<int:id>', ImpuestoViews.as_view() , name='Impuestos_process_id'),
    path('pacientes/', PacienteViews.as_view() , name='paciente_list'),
    path('pacientes/busqueda/<str:criterio>/<str:campo>', PacienteViews.as_view() , name='paciente_process'),
    path('pacientes/id/<int:id>', PacienteViews.as_view() , name='paciente_process_id'),
    path('muestras/', PacienteViews.as_view() , name='muestra_list'),
    path('muestras/busqueda/<str:criterio>/<str:campo>', PacienteViews.as_view() , name='muestra_process'),
    path('muestras/id/<int:id>', PacienteViews.as_view() , name='muestra_process_id'),
]