import datetime
from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class ExpedientesViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                expedientes = Expediente.objects.filter(id=campo).select_related('idPaciente')
                if expedientes is not None:
                    expedientes_values = []
                    for expediente in expedientes:
                        expediente_dict = {
                            'id': expediente.id,
                            'fecha': expediente.fecha,
                            'observacion': expediente.observacion,
                            'activo': expediente.activo,
                                'idPaciente': {
                                'id': expediente.idPaciente.id,
                                'nombre': expediente.idPaciente.nombre,
                                'documeto': expediente.idPaciente.documento
                                
                                },
                          
                            }
                        
                        expedientes_values.append(expediente_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'expedientes': expedientes_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'expedientes': []
                    }
                    return JsonResponse(context)
                
                
            elif criterio == "nombre":
                
                expedientes = Expediente.objects.filter(idPaciente__nombre=campo)
                if expedientes is not None:
                    expedientes_values = []
                    for expediente in expedientes:
                        expediente_dict = {
                            'id': expediente.id,
                            'fecha': expediente.fecha,
                            'observacion': expediente.observacion,
                            'activo': expediente.activo,
                            
                                'idPaciente': {
                                'id': expediente.idPaciente.id,
                                'nombre': expediente.idPaciente.nombre,
                                'documeto': expediente.idPaciente.documento
                                
                                

                            }
                        }
                        expedientes_values.append(expediente_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'expedientes': expedientes_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'expedientes': []
                    }
                    return JsonResponse(context)          
        else:                
            expedientes = Expediente.objects.select_related('idPaciente')
            if expedientes is not None:
                expedientes_values = []
                for expediente in expedientes:
                    expediente_dict = {
                        'id': expediente.id,
                        'fecha': expediente.fecha,
                        'observacion': expediente.observacion,
                        'activo': expediente.activo,
                        
                            'idPaciente': {
                            'id': expediente.idPaciente.id,
                            'nombre': expediente.idPaciente.nombre,
                            'documeto': expediente.idPaciente.documento
                           

                        }
                    }
                    expedientes_values.append(expediente_dict)
                context = {
                    'message': "Consulta exitosa",
                    'expedientes': expedientes_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'expedientes': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
        if validar_id_paciente(jd['idPaciente']):    
            expedientes = {'message': "El tratamiento no existe"}
        elif len(jd['observacion']) <= 0:
            expedientes = {'message': "La observación esta vacía."}
        elif len(jd['observacion']) < 5:
            expedientes = {'message': "La observación debe tener más de 5 caracteres."}
        elif len(jd['observacion']) > 50:
            expedientes = {'message': "La observación debe tener menos de 50 caracteres."}
        elif not validar_cadena_espacios(jd['observacion']):
            expedientes = {'message': "No se permiten mas de un espacio consecutivo.[direccion]"}
        elif validar_cadena_repeticion(jd['observacion']):
            expedientes = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[direccion]"} 
        elif (rsp_fecha) is None:
            expedientes = {'message': "La fecha esta vacía"}
        elif isinstance(rsp_fecha, str):
            expedientes = {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            expedientes = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            expedientes = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif jd['activo'] < 0:
            expedientes = {'message': "confirmacion debe ser positivo."}
        elif jd['activo'] > 1:
            expedientes = {'message': "confirmacion debe unicamente puede ser 0 o 1."}
        
        else:
            expedientes = {'message': "Registro Exitoso."}
            Expediente.objects.create(idPaciente=instanciar_paciente(jd['idPaciente']),fecha=jd['fecha'],observacion=jd['observacion'],activo=jd['activo'])
            expedientes = {'message':"Registro Exitoso."}
        return JsonResponse(expedientes)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        expedientes = list(Expediente.objects.filter(id=id).values())
        if len(expedientes) > 0:
            rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
            expediente=Expediente.objects.get(id=id)
            
            if validar_id_paciente(jd['idPaciente']):    
                expedientes = {'message': "El tratamiento no existe"}
            elif len(jd['observacion']) <= 0:
                expedientes = {'message': "La observación esta vacía."}
            elif len(jd['observacion']) < 5:
                expedientes = {'message': "La observación debe tener más de 5 caracteres."}
            elif len(jd['observacion']) > 50:
                expedientes = {'message': "La observación debe tener menos de 50 caracteres."}
            elif not validar_cadena_espacios(jd['observacion']):
                expedientes = {'message': "No se permiten mas de un espacio consecutivo.[direccion]"}
            elif validar_cadena_repeticion(jd['observacion']):
                expedientes = {'message': "No se permiten mas de dos caracteres consecutivos del mismo tipo.[direccion]"} 
            elif (rsp_fecha) is None:
                expedientes = {'message': "La fecha esta vacía"}
            elif isinstance(rsp_fecha, str):
                expedientes = {'message': "La fecha esta vacía"}
            elif (rsp_fecha.year) < 2000:
                expedientes = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            elif (rsp_fecha.year) > 2030:
                expedientes = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            elif jd['activo'] < 0:
                expedientes = {'message': "confirmacion debe ser positivo."}
            elif jd['activo'] > 1:
                expedientes = {'message': "confirmacion debe unicamente puede ser 0 o 1."}
            
            else:
                
                expediente.idPaciente = instanciar_paciente(jd['idPaciente'])
                expediente.fecha = jd['fecha']
                expediente.observacion = jd['observacion']
                expediente.activo = jd['activo']
                expediente.save()
                expedientes = {'message': "La actualización fue exitosa."}
        return JsonResponse(expedientes)
        
        

#Eliminar un registro de cargos
    def delete(self, request,id):
        expedientes = list(Expediente.objects.filter(id=id).values())
        if len(expedientes) > 0:
            Expediente.objects.filter(id=id).delete()
            expedientes = {'message':"Registro Eliminado"}
        else:
            expedientes = {'message':"No se encontró el registro", 'expedientes': []}
        return JsonResponse(expedientes)
    

def validar_id_paciente(id):
    if (id>0):
        registro = Paciente.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  

def instanciar_paciente(id):
    if (id>0):
        paciente = Paciente.objects.get(id=id)
        if paciente:
            return paciente   



def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

