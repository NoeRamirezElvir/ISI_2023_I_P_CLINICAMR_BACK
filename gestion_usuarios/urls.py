from django.urls import path


from .views.cargo_views import *
from .views.documento_views import *
from .views.especialidad_views import *
from .views.empleado_views import *
from .views.usuario_views import *
from .views.Impuesto_views import *
from .views.Paciente_views import *
from .views.login_views import *
from .views.TipoMuestra_views import *
from .views.SubTipo_views import *
from .views.Tipo_views import *
from .views.impuesto_historico_views import *
from .views.cita_views import *
from .views.Muestra_views import *
from .views.medicamento_views import *
from .views.proveedor_views import *
from .views.costo_historico_medicamento_views import *
from .views.precio_historico_medicamento_views import *
from .views.laboratorio_views import *
from .views.sintoma_views import *
from .views.enfermedad_views import *
from .views.enfermedad_detalle_views import *
from .views.metodoPago_views import *
from .views.diagnostico_views import *
from .views.parametros_generales_views import *
from .views.diagnostico_detalle import *
from .views.tratamiento_views import *
from .views.Resultado_views import *
from .views.precio_historico_examen_views import *
from .views.precio_historico_tratamiento_views import *

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
    path('muestras/', MuestrasViews.as_view() , name='muestra_list'),
    path('muestras/busqueda/<str:criterio>/<str:campo>', MuestrasViews.as_view() , name='muestra_process'),
    path('muestras/id/<int:id>', MuestrasViews.as_view() , name='muestra_process_id'), 
    path('tmuestra/', Tipo_muestraViews.as_view() , name='tmuestra_list'),
    path('tmuestra/busqueda/<str:criterio>/<str:campo>', Tipo_muestraViews.as_view() , name='tmuestra_process'),
    path('tmuestra/id/<int:id>', Tipo_muestraViews.as_view() , name='tmuestra_process_id'), 
    path('subtipo/', subtipoView.as_view() , name='subtipo_list'),
    path('subtipo/busqueda/<str:criterio>/<str:campo>', subtipoView.as_view() , name='subtipo_process'),
    path('subtipo/id/<int:id>', subtipoView.as_view() , name='subtipo_process_id'), 
    path('tipo/', TiposView.as_view() , name='tipo_list'),
    path('tipo/busqueda/<str:criterio>/<str:campo>', TiposView.as_view() , name='tipo_process'),
    path('tipo/id/<int:id>', TiposView.as_view() , name='tipo_process_id'), 
    path('impuestoHistorico/', ImpuestoHistorico.as_view() , name='impuesto_historico_list'),
    path('impuestoHistorico/busqueda/<str:criterio>/<str:campo>', ImpuestoHistorico.as_view() , name='impuesto_historico_process'),
    path('impuestoHistorico/id/<int:id>', ImpuestoHistorico.as_view() , name='impuesto_historico_process_id'), 
    path('citas/', CitasViews.as_view() , name='citas_list'),
    path('citas/busqueda/<str:criterio>/<str:campo>', CitasViews.as_view() , name='citas_process'),
    path('citas/id/<int:id>', CitasViews.as_view() , name='citas_process_id'), 

    path('proveedores/', ProveedorView.as_view() , name='proveedores_list'),
    path('proveedores/busqueda/<str:criterio>/<str:campo>', ProveedorView.as_view() , name='proveedore_process'),
    path('proveedores/id/<int:id>', ProveedorView.as_view() , name='proveedore_process_id'), 

    path('medicamentos/', MedicamentosViews.as_view() , name='medicamentos_list'),
    path('medicamentos/busqueda/<str:criterio>/<str:campo>', MedicamentosViews.as_view() , name='medicamentos_process'),
    path('medicamentos/id/<int:id>', MedicamentosViews.as_view() , name='medicamentos_process_id'), 

    path('costoHistoricoMedicamento/', CostoHistoricoMedicamentosViews.as_view() , name='costo_historico_medicamento_list'),
    path('costoHistoricoMedicamento/busqueda/<str:criterio>/<str:campo>', CostoHistoricoMedicamentosViews.as_view() , name='costo_historico_medicamento_process'),
    path('costoHistoricoMedicamento/id/<int:id>', CostoHistoricoMedicamentosViews.as_view() , name='costo_historico_medicamento_process_id'), 

    path('precioHistoricoMedicamento/', PrecioHistoricoMedicamentosViews.as_view() , name='precio_historico_medicamento_list'),
    path('precioHistoricoMedicamento/busqueda/<str:criterio>/<str:campo>', PrecioHistoricoMedicamentosViews.as_view() , name='precio_historico_medicamento_process'),
    path('precioHistoricoMedicamento/id/<int:id>', PrecioHistoricoMedicamentosViews.as_view() , name='precio_historico_medicamento_process_id'), 
    
    path('laboratorios/', LaboratorioView.as_view() , name='laboratorios_list'),
    path('laboratorios/busqueda/<str:criterio>/<str:campo>', LaboratorioView.as_view() , name='laboratorios_process'),
    path('laboratorios/id/<int:id>', LaboratorioView.as_view() , name='laboratorios_process_id'), 
    
    path('sintomas/', SintomasView.as_view() , name='sintomas_list'),
    path('sintomas/busqueda/<str:criterio>/<str:campo>', SintomasView.as_view() , name='sintomas_process'),
    path('sintomas/id/<int:id>', SintomasView.as_view() , name='sintomas_process_id'), 

    path('enfermedades/', EnfermedadView.as_view() , name='enfermedades_list'),
    path('enfermedades/busqueda/<str:criterio>/<str:campo>', EnfermedadView.as_view() , name='enfermedades_process'),
    path('enfermedades/id/<int:id>', EnfermedadView.as_view() , name='enfermedades_process_id'),

    path('enfermedadDetalle/', EnfermedadDetalleView.as_view() , name='enfermedades_detalles_list'),
    path('enfermedadDetalle/busqueda/<str:criterio>/<str:campo>', EnfermedadDetalleView.as_view() , name='enfermedades_detalles_process'),
    path('enfermedadDetalle/id/<int:id>', EnfermedadDetalleView.as_view() , name='enfermedades_detalles_process_id'), 

    path('metodop/', metodoPagoViews.as_view() , name='metodop'),
    path('metodop/busqueda/<str:criterio>/<str:campo>', metodoPagoViews.as_view() , name='metodop'),
    path('metodop/id/<int:id>', metodoPagoViews.as_view() , name='metodop'), 

    path('diagnostico/', DiagnosticoView.as_view() , name='diagnostico_list'),
    path('diagnostico/busqueda/<str:criterio>/<str:campo>', DiagnosticoView.as_view() , name='diagnostico_process'),
    path('diagnostico/id/<int:id>', DiagnosticoView.as_view() , name='diagnostico_process_id'), 

    path('parametrosgenerales/', Parametros_GeneralesViews.as_view() , name='parametrosgenerales_list'),
    path('parametrosgenerales/busqueda/<str:criterio>/<str:campo>', Parametros_GeneralesViews.as_view() , name='parametrosgenerales_process'),
    path('parametrosgenerales/id/<int:id>', Parametros_GeneralesViews.as_view() , name='parametrosgenerales_process_id'), 

    path('diagnosticoDetalle/', DiagnosticoDetalleView.as_view() , name='diagnosticoDetalle_list'),
    path('diagnosticoDetalle/busqueda/<str:criterio>/<str:campo>', DiagnosticoDetalleView.as_view() , name='diagnosticoDetalle_process'),
    path('diagnosticoDetalle/id/<int:id>', DiagnosticoDetalleView.as_view() , name='diagnosticoDetalle_process_id'), 

    path('tratamientos/', tratamientosViews.as_view() , name='tratamientos_list'),
    path('tratamientos/busqueda/<str:criterio>/<str:campo>', tratamientosViews.as_view() , name='tratamientos_process'),
    path('tratamientos/id/<int:id>', tratamientosViews.as_view() , name='tratamientos_process_id'), 
    
    path('resultados/', resultadosViews.as_view() , name='resultados_list'),
    path('resultados/busqueda/<str:criterio>/<str:campo>', resultadosViews.as_view() , name='resultados_process'),
    path('resultados/id/<int:id>', resultadosViews.as_view() , name='resultados_process_id'), 
    
    path('precioHistoricoExamen/', PrecioHistoricoExamenesViews.as_view() , name='precio_historico_examen_list'),
    path('precioHistoricoExamen/busqueda/<str:criterio>/<str:campo>', PrecioHistoricoExamenesViews.as_view() , name='precio_historico_examen_process'),
    path('precioHistoricoExamen/id/<int:id>', PrecioHistoricoExamenesViews.as_view() , name='precio_historico_examen_process_id'), 
    
    path('precioHistoricoTratamiento/', PrecioHistoricoTratamientosViews.as_view() , name='precio_historico_tratamiento_list'),
    path('precioHistoricoTratamiento/busqueda/<str:criterio>/<str:campo>', PrecioHistoricoTratamientosViews.as_view() , name='precio_historico_tratamiento_process'),
    path('precioHistoricoTratamiento/id/<int:id>', PrecioHistoricoTratamientosViews.as_view() , name='precio_historico_tratamiento_process_id'), 
    
]