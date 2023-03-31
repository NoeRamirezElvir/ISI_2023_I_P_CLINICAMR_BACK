from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class EnfermedadView(View):
    #Este metodo permite realizar las conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        try:
            if (len(campo)> 0 and len(criterio)> 0):
                if criterio == "id":
                    enfermedades = Enfermedad.objects.filter(id=campo).values()
                    if enfermedades is not None:
                        enfermedades_values = []
                        for enfermedad in enfermedades:
                            enfermedad_dict = {
                                'id': enfermedad['id'],
                                'nombre': enfermedad['nombre'],
                                'idSintomas':{}
                            }
                            sintomas = EnfermedadDetalle.objects.filter(idEnfermedad = enfermedad['id']).select_related('idSintoma')
                            for sintoma in sintomas:
                                sintoma_dict = {
                                    'id': sintoma.idSintoma.id,
                                    'nombre': sintoma.idSintoma.nombre
                                }
                                enfermedad_dict['idSintomas'][sintoma.idSintoma.id] = sintoma_dict
                            enfermedades_values.append(enfermedad_dict)
                            context = {
                                'message': "Consulta exitosa",
                                'enfermedades': enfermedades_values
                            }
                            return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': enfermedades_values
                        }
                        return JsonResponse(context)
                elif criterio == "nombre":
                    consulta = Consulta.objects.filter(nombre=campo).values()
                    if consulta is not None:
                        consulta_values = []
                        for consultas in consulta:
                            consultas_dict = {
                                'id': consultas['id'],
                                'nombre': consultas['nombre'],
                                'idCita':{}
                            }
                          ##33  citas = EnfermedadDetalle.objects.filter(idEnfermedad = enfermedad['id']).select_related('idSintoma')
                            for sintoma in sintomas:
                                sintoma_dict = {
                                    'id': sintoma.idSintoma.id,
                                    'nombre': sintoma.idSintoma.nombre
                                }
                                enfermedad_dict['idSintomas'][sintoma.idSintoma.id] = sintoma_dict
                            enfermedades_values.append(enfermedad_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'enfermedades': enfermedades_values
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            'message': "No se encontraron los datos",
                            'enfermedades': enfermedades_values
                        }
                        return JsonResponse(context)
            else:
                enfermedades = Enfermedad.objects.values()
                if enfermedades is not None:
                    enfermedades_values = []
                    for enfermedad in enfermedades:
                        enfermedad_dict = {
                            'id': enfermedad['id'],
                            'nombre': enfermedad['nombre'],
                            'idSintomas':{}
                        }
                        sintomas = EnfermedadDetalle.objects.filter(idEnfermedad = enfermedad['id']).select_related('idSintoma')
                        for sintoma in sintomas:
                            sintoma_dict = {
                                'id': sintoma.idSintoma.id,
                                'nombre': sintoma.idSintoma.nombre
                            }
                            enfermedad_dict['idSintomas'][sintoma.idSintoma.id] = sintoma_dict
                        enfermedades_values.append(enfermedad_dict)
                        context = {
                            'message': "Consulta exitosa",
                            'enfermedades': enfermedades_values
                        }
                    return JsonResponse(context)
                else:
                    context = {
                        'message': "No se encontraron los datos",
                        'enfermedades': enfermedades_values
                    }
                    return JsonResponse(context)
            return JsonResponse(enfermedades)
        except TypeError as e:
            context = {
                'message': f"El registro no existe. Excepcion: {e}",
            }
            return JsonResponse(context)
        except Exception as a:
            context = {
                'message': f"Error. Excepcion: {a}",
            }
            return JsonResponse(context)
#Agregar un registro de tipo
    def post(self, request):
        jd=json.loads(request.body)
        rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
        if validar_id_empleado(jd['idEmpleado']):    
            consulta = {'message': "El paciente no existe"}
        if validar_id_cita(jd['idTipoMuestra']):    
            consulta = {'message': "El paciente no existe"}
        elif (rsp_fecha) is None:
            consulta = {'message': "La fecha esta vacía"}
        elif isinstance(rsp_fecha, str):
            consulta = {'message': "La fecha esta vacía"}
        elif (rsp_fecha.year) < 2000:
            consulta = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        elif (rsp_fecha.year) > 2030:
            consulta = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
        else:
            consulta = {'message': "Registro Exitoso."}
            Consulta.objects.create(idPaciente=instanciar_empleado(jd['idPaciente']), idCita=instanciar_cita(jd['idCita']),fecha=jd['fecha'])
            consulta = {'message':"Registro Exitoso."}
        return JsonResponse(consulta)

#Actualizar un registro de tipo
    def put(self, request,id):
        jd=json.loads(request.body)
        consultas = list(Consulta.objects.filter(id=id).values())
        if len(consulta) > 0:
            rsp_fecha = datetime.datetime.fromisoformat(jd['fecha'])
            consulta=Consulta.objects.get(id=id)
            if validar_id_empleado(jd['idPaciente']):    
                consulta = {'message': "El paciente no existe"}
            if validar_id_cita(jd['idTipoMuestra']):    
                consulta = {'message': "El paciente no existe"}
            elif (rsp_fecha) is None:
                consulta = {'message': "La fecha esta vacía"}
            elif isinstance(rsp_fecha, str):
                consulta = {'message': "La fecha esta vacía"}
            elif (rsp_fecha.year) < 2000:
                consulta = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            elif (rsp_fecha.year) > 2030:
                consulta = {'message': "La fecha debe estar en el rango de año de 2000 a 2030"}
            else:
                consultas.idEmpleado = instanciar_empleado(jd['idEmpleado'])
                consultas.idCita = instanciar_cita(jd['idCita'])
                consultas.fecha = jd['fecha']
                consultas.save()
                consulta = {'message': "La actualización fue exitosa."}
        return JsonResponse(consulta)
        
        
#Eliminar un registro de tipo
    def delete(self, request,id):
        muestra = list(Consulta.objects.filter(id=id).values())
        if len(muestra) > 0:
            Consulta.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'muestra': []}
        return JsonResponse(datos)
    
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

def instanciar_cita(id):
    if (id>0):
        empleado = Cita.objects.get(id=id)
        if empleado:
            return empleado   

def validar_id_cita(id):
    if (id>0):
        registro = Cita.objects.filter(id=id)
        if registro:
            return False
        else:
            return True  



def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))

