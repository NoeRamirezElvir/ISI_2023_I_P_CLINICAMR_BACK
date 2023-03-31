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
class tratamientosViews(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto tratamiento todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if criterio == "id":
                tratamientos = Tratamiento.objects.filter(id=campo).select_related('idPaciente')
                if tratamientos is not None:
                    tratamientos_values = []
                    for tratamiento in tratamientos:
                        paciente = tratamiento.idPaciente
                        tratamiento_dict = {
                            'id': tratamiento.id,
                            'idTipo': tratamiento.idTipo.id,
                            'fecha': tratamiento.fecha,
                            'idPaciente': {
                                'id': paciente.id,
                                'nombre': paciente.nombre
                            }
                        }
                        tratamientos_values.append(tratamiento_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'tratamientos': tratamientos_values
                        }
                        return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'tratamientos': []
                    }
                    return JsonResponse(context)
            elif criterio == "nombre":
                idPaciente = Paciente.objects.filter(nombre=campo)
                if idPaciente is not None:
                    for paciente in idPaciente:
                        reg = Tratamiento.objects.filter(idPaciente=paciente.id).select_related('idPaciente')
                        if reg is not None:
                            tratamientos_values = []
                            for tratamiento in reg:
                                paciente = tratamiento.idPaciente
                                tratamiento_dict = {
                                    'id': tratamiento.id,
                                    'idTipo': tratamiento.idTipo.id,
                                    'fecha': tratamiento.fecha,
                                    'idPaciente': {
                                        'id': paciente.id,
                                        'nombre': paciente.nombre
                                    }
                                }
                                tratamientos_values.append(tratamiento_dict)
                            context = {
                                'message': "Consulta exitosa",
                                'tratamientos': tratamientos_values
                            }
                            return JsonResponse(context)
                        else:
                            context = {
                                'message': "No se encontraron los datos",
                                'tratamientos': []
                            }
                            return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'tratamientos': []
                    }
                    return JsonResponse(context)
            context = {
                    'message': "No se encontraron los datos",
                    'tratamientos': []
                }
            return JsonResponse(context)
        else:
            reg = Tratamiento.objects.select_related('idPaciente')
            if reg is not None:
                tratamientos_values = []
                for tratamiento in reg:
                    paciente = tratamiento.idPaciente
                    tratamiento_dict = {
                        'id': tratamiento.id,
                        'idTipo': tratamiento.idTipo.id,
                        'fecha': tratamiento.fecha,
                        'idPaciente': {
                            'id': paciente.id,
                            'nombre': paciente.nombre
                        }
                    }
                    tratamientos_values.append(tratamiento_dict)
                context = {
                    'message': "Consulta exitosa",
                    'tratamientos': tratamientos_values
                }
                return JsonResponse(context)
            else:
                context = {
                    'message': "No se encontraron los datos",
                    'tratamientos': []
                }
                return JsonResponse(context)

#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
        if validar_id_paciente(jd['idPaciente']):    
            tratamientos = {'message': "El paciente no existe"}
        if validar_id_tipo(jd['idTipo']):    
            tratamientos = {'message': "El paciente no existe"}
        elif (rsp_fecha) is None:
            tratamientos = {'message': "La fecha esta vacía"}
        elif isinstance(rsp_fecha, str):
            tratamientos = {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            tratamientos = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            tratamientos = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        else:
            tratamientos = {'message': "Registro Exitoso."}
            Tratamiento.objects.create(idPaciente=instanciar_paciente(jd['idPaciente']), idTipo=instanciar_tipo(jd['idTipo']),fecha=jd['fecha'])
            tratamientos = {'message':"Registro Exitoso."}
        return JsonResponse(tratamientos)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        tratamientos = list(Tratamiento.objects.filter(id=id).values())
        if len(tratamientos) > 0:
            rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
            tratamiento=Tratamiento.objects.get(id=id)
            if validar_id_paciente(jd['idPaciente']):    
                tratamientos = {'message': "El paciente no existe"}
            if validar_id_tipo(jd['idTipo']):    
                tratamientos = {'message': "El paciente no existe"}
            elif (rsp_fecha) is None:
                tratamientos = {'message': "La fecha esta vacía"}
            elif isinstance(rsp_fecha, str):
                tratamientos = {'message': "La fecha esta vacía"}
            elif (rsp_fecha.year) < 2000:
                tratamientos = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            elif (rsp_fecha.year) > 2030:
                tratamientos = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            else:
                tratamiento.idPaciente = instanciar_paciente(jd['idPaciente'])
                tratamiento.idTipo = instanciar_tipo(jd['idTipo'])
                tratamiento.fecha = jd['fecha']
                tratamiento.save()
                tratamientos = {'message': "La actualización fue exitosa."}
        return JsonResponse(tratamientos)
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        tratamiento = list(Tratamiento.objects.filter(id=id).values())
        if len(tratamiento) > 0:
            Tratamiento.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'tratamiento': []}
        return JsonResponse(datos)
    
def instanciar_paciente(id):
    if (id>0):
        paciente = Paciente.objects.get(id=id)
        if paciente:
            return paciente   

def validar_id_paciente(id):
    if (id>0):
        registro = Paciente.objects.filter(id=id)
        if registro:
            return False
        else:
            return True    

def instanciar_tipo(id):
    if (id>0):
        paciente = Tipo.objects.get(id=id)
        if paciente:
            return paciente   

def validar_id_tipo(id):
    if (id>0):
        registro = Tipo.objects.filter(id=id)
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

