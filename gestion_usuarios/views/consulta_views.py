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
class ConsultaViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                consultas = Consulta.objects.filter(id=campo).select_related('idCita','idEmpleado')
                if consultas is not None:
                    consultas_values = []
                    for consulta in consultas:
                        consulta_dict = {
                            'id': consulta.id,
                            'fecha': consulta.fecha,

                            'idCita':{
                            'fechaActual': consulta.idCita.fechaActual,
                            'fechaProgramada': consulta.idCita.fechaProgramada
                            },
                                'idPaciente': {
                                'id': consulta.idCita.idPaciente.id,
                                'nombre': consulta.idCita.idPaciente.nombre,
                                'documeto': consulta.idCita.idPaciente.documento,
                                'id': consulta.idCita.id,
                                'fechaActual': consulta.idCita.fechaActual,
                                'fechaProgramada': consulta.idCita.fechaProgramada
                            },
                                
                                'idEmpleado': {
                                'id': consulta.idEmpleado.id,
                                'nombre': consulta.idEmpleado.nombre,
                                'documeto': consulta.idEmpleado.documento
                                
                                }    
                            }
                        
                        
                        
                        consultas_values.append(consulta_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'consultas': consultas_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'consultas': []
                    }
                    return JsonResponse(context)
                
                
            elif criterio == "nombre":
                
                consultas = Consulta.objects.filter(idCita__idEmpleado__nombre=campo)
                if consultas is not None:
                    consultas_values = []
                    for consulta in consultas:
                        consulta_dict = {
                             'id': consulta.id,
                            'fecha': consulta.fecha,

                            'idCita':{
                            
                                'fechaActual': consulta.idCita.fechaActual,
                                'fechaProgramada': consulta.idCita.fechaProgramada
                            },
                                'idPaciente': {
                                'id': consulta.idCita.idPaciente.id,
                                'nombre': consulta.idCita.idPaciente.nombre,
                                'documeto': consulta.idCita.idPaciente.documento,
                                'id': consulta.idCita.id,


                                },
                                
                                'idEmpleado': {
                                'id': consulta.idEmpleado.id,
                                'nombre': consulta.idEmpleado.nombre,
                                'documeto': consulta.idEmpleado.documento
                                
                                }    
                            
                        }
                        
                        consultas_values.append(consulta_dict)
                    context = {
                        'message': "Consulta exitosa",
                        'consultas': consultas_values
                    }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'consultas': []
                    }
                    return JsonResponse(context)          
        else:                
            consultas = Consulta.objects.select_related('idCita','idEmpleado')
            if consultas is not None:
                consultas_values = []
                for consulta in consultas:
                    consulta_dict = {
                         'id': consulta.id,
                            'fecha': consulta.fecha,

                            'idCita':{
                                'fechaActual': consulta.idCita.fechaActual,
                                'fechaProgramada': consulta.idCita.fechaProgramada
                            },
                                'idPaciente': {
                                'id': consulta.idCita.idPaciente.id,
                                'nombre': consulta.idCita.idPaciente.nombre,
                                'documeto': consulta.idCita.idPaciente.documento,
                                'id': consulta.idCita.id,
                                'fechaActual': consulta.idCita.fechaActual,
                                'fechaProgramada': consulta.idCita.fechaProgramada
                            },
                                
                                'idEmpleado': {
                                'id': consulta.idEmpleado.id,
                                'nombre': consulta.idEmpleado.nombre,
                                'documeto': consulta.idEmpleado.documento
                                
                                }    
                            }
                        
                        
                    consultas_values.append(consulta_dict)
                context = {
                    'message': "Consulta exitosa",
                    'consultas': consultas_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'consultas': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
        if validar_id_empleado(jd['idEmpleado']):    
            consultas = {'message': "El tratamiento no existe"}
        elif validar_id_cita(jd['idCita']):    
            consultas = {'message': "El tratamiento no existe"}

        elif (rsp_fecha) is None:
            consultas = {'message': "La fecha esta vacía"}
        elif isinstance(rsp_fecha, str):
            consultas = {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            consultas = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            consultas = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        else:
            consultas = {'message': "Registro Exitoso."}
            Consulta.objects.create(idEmpleado=instanciar_empleado(jd['idEmpleado']),idCita=instanciar_cita(jd['idCita']),fecha=jd['fecha'])
            consultas = {'message':"Registro Exitoso."}
        return JsonResponse(consultas)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        consultas = list(Consulta.objects.filter(id=id).values())
        if len(consultas) > 0:
            rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
            consulta=Consulta.objects.get(id=id)           
        if validar_id_empleado(jd['idEmpleado']):    
            consultas = {'message': "El tratamiento no existe"}
        elif validar_id_cita(jd['idCita']):    
            consultas = {'message': "El tratamiento no existe"}
        elif (rsp_fecha) is None:
            consultas = {'message': "La fecha esta vacía"}
        elif isinstance(rsp_fecha, str):
            consultas = {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            consultas = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            consultas = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        else:
                
                consulta.idEmpleado = instanciar_empleado(jd['idEmpleado'])
                consulta.idCita = instanciar_cita(jd['idCita'])
                consulta.fecha = jd['fecha']
                consulta.save()
                consultas = {'message': "La actualización fue exitosa."}
        return JsonResponse(consultas)
        
        

#Eliminar un registro de cargos
    def delete(self, request,id):
        consultas = list(Consulta.objects.filter(id=id).values())
        if len(consultas) > 0:
            Consulta.objects.filter(id=id).delete()
            consultas = {'message':"Registro Eliminado"}
        else:
            consultas = {'message':"No se encontró el registro", 'consultas': []}
        return JsonResponse(consultas)

def instanciar_cita(id):
    if (id>0):
        cita = Cita.objects.get(id=id)
        if cita:
            return cita   

def validar_id_cita(id):
    if (id>0):
        registro = Cita.objects.filter(id=id)
        if registro:
            return False
        else:
            return True    
   

def instanciar_empleado(id):
    if (id>0):
        empleado = Empleado.objects.get(id=id)
        if empleado:
            return empleado   

def validar_id_empleado(id):
    if (id>0):
        registro = Empleado.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  

def validar_id_subtipo(id):
    if (id>0):
        subtipo = Subtipo.objects.filter(id=id)
        if subtipo:
            return False
        else:
            return True

def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

