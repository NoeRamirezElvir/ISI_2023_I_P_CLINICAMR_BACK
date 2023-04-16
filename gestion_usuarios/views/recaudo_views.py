from datetime import date
from decimal import Decimal
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class RecaudoView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        #try:
            if (len(campo)> 0 and len(criterio)> 0):
                if criterio == "id":
                    recaudos = Recaudo.objects.filter(id=campo).select_related('idCorrelativo','idEmpleado','idMetodoPago','idPaciente','idConsulta')
                    if recaudos is not None:
                        recaudos_values = []
                        for recaudo in recaudos:
                            recaudo_dict = {
                                'id': recaudo.id,
                                'noFactura': recaudo.noFactura,
                                'fechaFacturacion': recaudo.fechaFacturacion,
                                'efectivo': recaudo.efectivo,
                                'tarjeta': recaudo.tarjeta,
                                'fechaEntrega': recaudo.fechaEntrega,
                                'estado': recaudo.estado,
                                'activa': recaudo.activa,
                                'idCorrelativo':{
                                    'id': recaudo.idCorrelativo.id,
                                    'cai': recaudo.idCorrelativo.cai,
                                    'rangoInicial': recaudo.idCorrelativo.rangoInicial,
                                    'rangoFinal': recaudo.idCorrelativo.rangoFinal,
                                    'consecutivo': recaudo.idCorrelativo.consecutivo,
                                    'fechaLimiteEmision': recaudo.idCorrelativo.fechaLimiteEmision,
                                    'fechaInicio': recaudo.idCorrelativo.fechaInicio
                                },
                                'idConsulta':{
                                    'id':recaudo.idConsulta.id,
                                    'precio':recaudo.idConsulta.idTipo.precio,
                                    'impuesto':recaudo.idConsulta.idTipo.idImpuesto.valor,
                                    'tipo':recaudo.idConsulta.idTipo.nombre,
                                    'paciente':recaudo.idConsulta.idCita.idPaciente.documento,
                                },
                                'idPaciente':{},
                                'idEmpleado':{
                                    'id':recaudo.idEmpleado.id,
                                    'nombre':recaudo.idEmpleado.nombre,
                                    'documento':recaudo.idEmpleado.documento
                                },
                                'idMetodoPago':{
                                    'id':recaudo.idMetodoPago.id,
                                    'nombre':recaudo.idMetodoPago.nombre
                                },
                                'medicamentos':{},
                                'tratamientos':{},
                                'examenes':{}
                            }
                            if (recaudo.idPaciente):
                                recaudo_dict = buscar_paciente(recaudo_dict,recaudo.idPaciente.id)
                            else:
                                recaudo_dict = buscar_paciente(recaudo_dict,0)
                            medicamentos = RecaudoDetalleMedicamento.objects.filter(idRecaudo = recaudo.id).select_related('idMedicamento')
                            medicamento_dict = {}
                            for medicamento in medicamentos:
                                medicamento_dict = {
                                    'id': medicamento.idMedicamento.id,
                                    'nombre': medicamento.idMedicamento.nombre
                                }
                                recaudo_dict['medicamentos'][medicamento.idMedicamento.id] = medicamento_dict
                            tratamientos = RecaudoDetalleTratamiento.objects.filter(idRecaudo = recaudo.id).select_related('idTratamiento')
                            tratamientos_dict = {}
                            for tratamiento in tratamientos:
                                tratamientos_dict = {
                                    'id': tratamiento.idTratamiento.id,
                                    'nombre': tratamiento.idTratamiento.idTipo.nombre
                                }
                                recaudo_dict['tratamientos'][tratamiento.idTratamiento.id] = tratamientos_dict
                            examenes = RecaudoDetalleExamen.objects.filter(idRecaudo = recaudo.id).select_related('idExamen')
                            examenes_dict = {}
                            for examen in examenes:
                                examenes_dict = {
                                    'id': examen.idExamen.id,
                                    'nombre': examen.idExamen.idTipo.nombre
                                }
                                recaudo_dict['examenes'][examen.idExamen.id] = examenes_dict
                            recaudos_values.append(recaudo_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'recaudo': recaudos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': examenes_dict
                        }
                        return JsonResponse(context)
                elif criterio == "numeroFactura":
                    recaudos = Recaudo.objects.filter(noFactura=campo).select_related('idCorrelativo','idEmpleado','idMetodoPago','idPaciente','idConsulta')
                    if recaudos is not None:
                        recaudos_values = []
                        for recaudo in recaudos:
                            recaudo_dict = {
                                'id': recaudo.id,
                                'noFactura': recaudo.noFactura,
                                'fechaFacturacion': recaudo.fechaFacturacion,
                                'efectivo': recaudo.efectivo,
                                'tarjeta': recaudo.tarjeta,
                                'fechaEntrega': recaudo.fechaEntrega,
                                'estado': recaudo.estado,
                                'activa': recaudo.activa,
                                'idCorrelativo':{
                                    'id': recaudo.idCorrelativo.id,
                                    'cai': recaudo.idCorrelativo.cai,
                                    'rangoInicial': recaudo.idCorrelativo.rangoInicial,
                                    'rangoFinal': recaudo.idCorrelativo.rangoFinal,
                                    'consecutivo': recaudo.idCorrelativo.consecutivo,
                                    'fechaLimiteEmision': recaudo.idCorrelativo.fechaLimiteEmision,
                                    'fechaInicio': recaudo.idCorrelativo.fechaInicio
                                },
                                'idConsulta':{
                                    'id':recaudo.idConsulta.id,
                                    'precio':recaudo.idConsulta.idTipo.precio,
                                    'impuesto':recaudo.idConsulta.idTipo.idImpuesto.valor,
                                    'tipo':recaudo.idConsulta.idTipo.nombre,
                                    'paciente':recaudo.idConsulta.idCita.idPaciente.documento,
                                },
                                'idPaciente':{},
                                'idEmpleado':{
                                    'id':recaudo.idEmpleado.id,
                                    'nombre':recaudo.idEmpleado.nombre,
                                    'documento':recaudo.idEmpleado.documento
                                },
                                'idMetodoPago':{
                                    'id':recaudo.idMetodoPago.id,
                                    'nombre':recaudo.idMetodoPago.nombre
                                },
                                'medicamentos':{},
                                'tratamientos':{},
                                'examenes':{}
                            }
                            if (recaudo.idPaciente):
                                recaudo_dict = buscar_paciente(recaudo_dict,recaudo.idPaciente.id)
                            else:
                                recaudo_dict = buscar_paciente(recaudo_dict,0)
                            medicamentos = RecaudoDetalleMedicamento.objects.filter(idRecaudo = recaudo.id).select_related('idMedicamento')
                            medicamento_dict = {}
                            for medicamento in medicamentos:
                                medicamento_dict = {
                                    'id': medicamento.idMedicamento.id,
                                    'nombre': medicamento.idMedicamento.nombre
                                }
                                recaudo_dict['medicamentos'][medicamento.idMedicamento.id] = medicamento_dict
                            tratamientos = RecaudoDetalleTratamiento.objects.filter(idRecaudo = recaudo.id).select_related('idTratamiento')
                            tratamientos_dict = {}
                            for tratamiento in tratamientos:
                                tratamientos_dict = {
                                    'id': tratamiento.idTratamiento.id,
                                    'nombre': tratamiento.idTratamiento.idTipo.nombre
                                }
                                recaudo_dict['tratamientos'][tratamiento.idTratamiento.id] = tratamientos_dict
                            examenes = RecaudoDetalleExamen.objects.filter(idRecaudo = recaudo.id).select_related('idExamen')
                            examenes_dict = {}
                            for examen in examenes:
                                examenes_dict = {
                                    'id': examen.idExamen.id,
                                    'nombre': examen.idExamen.idTipo.nombre
                                }
                                recaudo_dict['examenes'][examen.idExamen.id] = examenes_dict
                            recaudos_values.append(recaudo_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'recaudo': recaudos_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': examenes_dict
                        }
                        return JsonResponse(context)
            else:
                recaudos = Recaudo.objects.select_related('idCorrelativo','idEmpleado','idMetodoPago','idPaciente','idConsulta')
                if recaudos is not None:
                    recaudos_values = []
                    for recaudo in recaudos:
                        recaudo_dict = {
                            'id': recaudo.id,
                            'noFactura': recaudo.noFactura,
                            'fechaFacturacion': recaudo.fechaFacturacion,
                            'efectivo': recaudo.efectivo,
                            'tarjeta': recaudo.tarjeta,
                            'fechaEntrega': recaudo.fechaEntrega,
                            'estado': recaudo.estado,
                            'activa': recaudo.activa,
                            'idCorrelativo':{
                                'id': recaudo.idCorrelativo.id,
                                'cai': recaudo.idCorrelativo.cai,
                                'rangoInicial': recaudo.idCorrelativo.rangoInicial,
                                'rangoFinal': recaudo.idCorrelativo.rangoFinal,
                                'consecutivo': recaudo.idCorrelativo.consecutivo,
                                'fechaLimiteEmision': recaudo.idCorrelativo.fechaLimiteEmision,
                                'fechaInicio': recaudo.idCorrelativo.fechaInicio
                            },
                            'idConsulta':{
                                'id':recaudo.idConsulta.id,
                                'precio':recaudo.idConsulta.idTipo.precio,
                                'impuesto':recaudo.idConsulta.idTipo.idImpuesto.valor,
                                'tipo':recaudo.idConsulta.idTipo.nombre,
                                'paciente':recaudo.idConsulta.idCita.idPaciente.documento,
                            },
                            'idPaciente':{},
                            'idEmpleado':{
                                'id':recaudo.idEmpleado.id,
                                'nombre':recaudo.idEmpleado.nombre,
                                'documento':recaudo.idEmpleado.documento
                            },
                            'idMetodoPago':{
                                'id':recaudo.idMetodoPago.id,
                                'nombre':recaudo.idMetodoPago.nombre
                            },
                            'medicamentos':{},
                            'tratamientos':{},
                            'examenes':{}
                        }
                        if (recaudo.idPaciente):
                            recaudo_dict = buscar_paciente(recaudo_dict,recaudo.idPaciente.id)
                        else:
                            recaudo_dict = buscar_paciente(recaudo_dict,0)
                        medicamentos = RecaudoDetalleMedicamento.objects.filter(idRecaudo = recaudo.id).select_related('idMedicamento')
                        medicamento_dict = {}
                        for medicamento in medicamentos:
                            medicamento_dict = {
                                'id': medicamento.idMedicamento.id,
                                'nombre': medicamento.idMedicamento.nombre
                            }
                            recaudo_dict['medicamentos'][medicamento.idMedicamento.id] = medicamento_dict
                        tratamientos = RecaudoDetalleTratamiento.objects.filter(idRecaudo = recaudo.id).select_related('idTratamiento')
                        tratamientos_dict = {}
                        for tratamiento in tratamientos:
                            tratamientos_dict = {
                                'id': tratamiento.idTratamiento.id,
                                'nombre': tratamiento.idTratamiento.idTipo.nombre
                            }
                            recaudo_dict['tratamientos'][tratamiento.idTratamiento.id] = tratamientos_dict
                        examenes = RecaudoDetalleExamen.objects.filter(idRecaudo = recaudo.id).select_related('idExamen')
                        examenes_dict = {}
                        for examen in examenes:
                            examenes_dict = {
                                'id': examen.idExamen.id,
                                'nombre': examen.idExamen.idTipo.nombre
                            }
                            recaudo_dict['examenes'][examen.idExamen.id] = examenes_dict
                        recaudos_values.append(recaudo_dict)

                    context = {
                        'message': "Consulta exitosa",
                        'recaudo': recaudos_values
                    }
                    return JsonResponse(context)
                else:
                    recaudo_values = []
                    context = {
                        'message': "No se encontraron los datos",
                        'recaudo': recaudo_values
                    }
                    return JsonResponse(context)
            return JsonResponse(context)


#Agregar un registro de cargos
    def post(self, request):
        jd=json.loads(request.body)
        if 2 <= 0:
            mensaje_post = {'message': "El nombre esta vacío."}
        else:
            if jd['montoEfectivo']:
                efectivo = round(Decimal(jd['montoEfectivo']),2)
            else: 
                efectivo = None

            if jd['estado'] == 'Pendiente':
                activa = 1
                fecha = None
            elif jd['estado'] == 'Enviada' or jd['estado'] == 'Pagada' or jd['estado'] == 'Vencida':
                activa = 1
                fecha = date.today()
            elif jd['estado'] == 'Anulada':
                activa = 0
                fecha = None
            else:
                activa = 0
                fecha = None

            correlativo = instanciar_correlativo(int(jd['correlativo']))
            consecutivo = correlativo.consecutivo
            con = str(consecutivo + 1).zfill(4)
            numeroFactura = f'{correlativo.rangoFinal} { correlativo.fechaLimiteEmision } { con }'
            if instanciar_paciente(int(jd['idPaciente'])):
                correlativo.consecutivo += 1
                correlativo.save()
                recaudo = Recaudo.objects.create(
                    idCorrelativo = instanciar_correlativo(int(jd['correlativo'])),
                    noFactura = numeroFactura,
                    idPaciente = instanciar_paciente(int(jd['idPaciente'])),
                    fechaFacturacion = jd['fechaActual'],
                    fechaEntrega = fecha,
                    idEmpleado = instanciar_empleado(int(jd['idEmpleado'])),
                    idMetodoPago = instanciar_metodo(int(jd['idMetodo'])),
                    idConsulta = instanciar_consulta(int(jd['idConsulta'])),
                    efectivo = efectivo,
                    tarjeta = jd['numeroTarjeta'],
                    estado = jd['estado'],
                    activa = activa
                )
                if jd['medicamentos']:
                    for item in jd['medicamentos']:
                        registro = instanciar_medicamento(int(item['id']))
                        RecaudoDetalleMedicamento.objects.create(idRecaudo=recaudo, idMedicamento = registro, cantidad=int(item['cantidad']))
                if jd['tratamientos']:
                    for item in jd['tratamientos']:
                        registro = instanciar_tratamiento(int(item['id']))
                        RecaudoDetalleTratamiento.objects.create(idRecaudo=recaudo, idTratamiento = registro)
                if jd['examenes']:
                    for item in jd['examenes']:
                        registro = instanciar_examen(int(item['id']))
                        RecaudoDetalleExamen.objects.create(idRecaudo=recaudo, idExamen = registro)
            else:
                correlativo.consecutivo += 1
                correlativo.save()
                recaudo = Recaudo.objects.create(
                    idCorrelativo = instanciar_correlativo(int(jd['correlativo'])),
                    noFactura = numeroFactura,
                    fechaFacturacion = jd['fechaActual'],
                    fechaEntrega = fecha,
                    idEmpleado = instanciar_empleado(int(jd['idEmpleado'])),
                    idMetodoPago = instanciar_metodo(int(jd['idMetodo'])),
                    idConsulta = instanciar_consulta(int(jd['idConsulta'])),
                    efectivo = efectivo,
                    tarjeta = jd['numeroTarjeta'],
                    estado = jd['estado'],
                    activa = activa
                )
                if jd['medicamentos']:
                    for item in jd['medicamentos']:
                        registro = instanciar_medicamento(int(item['id']))
                        RecaudoDetalleMedicamento.objects.create(idRecaudo=recaudo, idMedicamento = registro, cantidad=int(item['cantidad']))
                if jd['tratamientos']:
                    for item in jd['tratamientos']:
                        registro = instanciar_tratamiento(int(item['id']))
                        RecaudoDetalleTratamiento.objects.create(idRecaudo=recaudo, idTratamiento = registro)
                if jd['examenes']:
                    for item in jd['examenes']:
                        registro = instanciar_examen(int(item['id']))
                        RecaudoDetalleExamen.objects.create(idRecaudo=recaudo, idExamen = registro)
            mensaje_post = {'message':"Registro Exitoso.", 'numeroFactura': numeroFactura }
        return JsonResponse(mensaje_post)

#Actualizar un registro de cargos

        
#Eliminar un registro de cargos
    def delete(self, request,id):
        enfermedades = list(Enfermedad.objects.filter(id=id).values())
        if len(enfermedades) > 0:
            Enfermedad.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraron registros", 'enfermedades': []}
        return JsonResponse(datos)
    

def buscar_paciente(diccionario, id):
    registros = Paciente.objects.filter(id=id)
    if registros:
        for registro in registros:
            diagnostico_dict = {
                'id': registro.id,
                'nombre': registro.nombre + " " + registro.apellido,
                'documento': registro.documento
            }
            diccionario['idPaciente'][0] = diagnostico_dict
        return diccionario
    else:
        diagnostico_dict = {
            'id': 0,
            'nombre': 'Consumidor Final'
        }
        diccionario['idPaciente'][0] = diagnostico_dict
        return diccionario
    
def instanciar_correlativo(id):
    if (id > 0):
        item = CorrelativoSar.objects.filter(id=id).last()
    if item:
        return item
    
def instanciar_paciente(id):
    if (id > 0):
        item = Paciente.objects.filter(id=id).last()
        if item:
            return item
        else:
            return None

def instanciar_empleado(id):
    if (id > 0):
        item = Empleado.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def instanciar_metodo(id):
    if (id > 0):
        item = MetodoDePago.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def instanciar_consulta(id):
    if (id > 0):
        item = Consulta.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None
    
def instanciar_medicamento(id):
    if (id > 0):
        item = Medicamento.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None
    
def instanciar_tratamiento(id):
    if (id > 0):
        item = Tratamiento.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def instanciar_examen(id):
    if (id > 0):
        item = Examen.objects.filter(id=id).last()
    if item:
        return item
    else:
        return None

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))
