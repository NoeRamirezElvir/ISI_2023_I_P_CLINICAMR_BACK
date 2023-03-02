from django.urls import path
from .views.cargo_views import *
from .views.documento_views import *
from .views.especialidad_views import *
from .views.empleado_views import *
from .views.usuario_views import *


urlpatterns = [
    path('cargos/', CargosView.as_view() , name='cargo_list'),
    path('cargos/busqueda/<str:criterio>/<str:campo>', CargosView.as_view() , name='cargos_process'),
    path('cargos/id/<int:id>', CargosView.as_view() , name='cargos_process_id'),
    path('documentos/', DocumentoViews.as_view() , name='documento_list'),
    path('documentos/busqueda/<str:criterio>/<str:campo>', DocumentoViews.as_view() , name='documento_process'),
    path('documentos/id/<int:id>', DocumentoViews.as_view() , name='documento_process_id'),
    path('especialidades/', EspecialidadViews.as_view() , name='especialidad_list'),
    path('especialidades/busqueda/<str:criterio>/<str:campo>', EspecialidadViews.as_view() , name='especialidad_process'),
    path('especialidades/id/<int:id>', EspecialidadViews.as_view() , name='especialidad_process_id'),
    path('empleados/', EmpleadoViews.as_view() , name='empleado_list'),
    path('empleados/busqueda/<str:criterio>/<str:campo>', EmpleadoViews.as_view() , name='empleado_process'),
    path('empleados/id/<int:id>', EmpleadoViews.as_view() , name='empleado_process_id'),
    path('usuarios/', UsuarioViews.as_view() , name='usuario_list'),
    path('usuarios/busqueda/<str:criterio>/<str:campo>', UsuarioViews.as_view() , name='usuario_process'),
    path('usuarios/id/<int:id>', UsuarioViews.as_view() , name='usuario_process_id'),
]