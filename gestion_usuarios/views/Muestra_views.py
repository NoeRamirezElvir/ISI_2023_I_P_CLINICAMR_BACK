from django.http.response import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
import re
from ..models import *
from django.views.decorators.http import require_http_methods

@method_decorator(require_http_methods(['POST','PUT','GET','DELETE']), name='dispatch')
class MuestraViews(View):
    #Este metodo permite realizar Els conultas que necesitan autentificacion. POST PUT DELETE
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    #Busquedas personalizadas y por defecto
    #las personalizadas varian segun el criterio ingresado, y por defecto muestra todos los objetos
    def get(self, request, campo="",criterio=""):
        if (len(campo)> 0 and len(criterio)> 0):
            if(criterio=="id"):
                muestras = list(Muestra.objects.filter(id=campo).values())
                if len(muestras) > 0:
                    muestras = muestras
                    muestras = {'message': "Consulta exitosa", 'muestras': muestras}
                else:
                    muestras = {'message': "No se encontraron los datos", 'muestras': []} 
                    return JsonResponse(muestras)
            elif(criterio=="fecha"):
                muestras= list(Muestra.objects.filter(fecha=campo).values())
                if len(muestras) > 0:
                    muestras = {'message': "Consulta exitosa", 'muestras': muestras}
                else:
                    muestras = {'message': "No se encontraron los datos", 'muestras': []} 
                    return JsonResponse(muestras)        
        else:
            muestras = list(Muestra.objects.values())
            if len(muestras) > 0:
                muestras = {'message': "Consulta exitosa", 'muestras': muestras}
            else:
                muestras = {'message': "No se encontraron los datos", 'muestras': []} 
        return JsonResponse(muestras)
    

#Agregar un registro de muestra
    def post(self, request):
        jd=json.loads(request.body)    
        if len(jd['fecha']) <= 0:
            muestras= {'message': "La fecha esta vacía."}
        elif len(str(jd['fecha'])) > 10:
            muestras = {'message': "La fecha debe tener menos de 10 caracteres."}
        elif (jd['idPacientes']) <= 0:
            muestras = {'message': "El tipo de documento esta vacío."}
          
        elif (jd['idTipoMuestra']) <= 0:
            muestras = {'message': "El cargo esta vacío."}  

        else:
            muestras = {'message': "Registro Exitoso."}
            Muestra.objects.create(fecha=datetime.strptime(str(jd['fecha']), "%Y-%m-%d").strftime("%Y-%m-%d"),idTipoMuestra=(instanciar_Muestra(jd['idTipoMuestra'])),idPacientes=instanciar_Pacientes(jd['idPacientes']))
            muestras = {'message':"Registro Exitoso."}
        return JsonResponse(muestras) 
    
#Actualizar un registro de cargos
    def put(self, request,id):
        jd=json.loads(request.body)
        muestras = list(Muestra.objects.filter(id=id).values())
        if len(muestras) > 0:
            muestra=Muestra.objects.get(id=id)
            
            if len(str(jd['fecha'])) <= 0:
                muestras = {'message': "La fecha  esta vacía."}
            elif len(str(jd['fecha'])) > 10:
                muestras = {'message': "La fecha debe tener menos de 10 caracteres."}
            
            elif (jd['idTipoMuestra']) <= 0:
                muestras = {'message': "El tipo de Muestra esta vacío."}
            
            
            elif (jd['idPaciente']) <= 0:
                muestras = {'message': "El Paciente esta vacío."}
            
            else:
                muestras = {'message': "Registro Exitoso."}
                
                muestra.fecha = datetime.strptime(str(jd['fecha']), "%Y-%m-%d").strftime("%Y-%m-%d")
                muestra.idTipoMuestra = instanciar_Muestra(jd['idTipoMuestra'])
                
                if jd['idPacientes'] > 0:
                    muestra.idPacientes = instanciar_Pacientes(jd['idPacientes'])
                
                
                print(muestra)
                muestra.save()
                empleados = {'message': "El actualización fue exitosa."}
        return JsonResponse(empleados)
    
#Eliminar un registro de cargos
    def delete(self, request,id):
        muestras = list(Muestra.objects.filter(id=id).values())
        if len(muestras) > 0:
            Muestra.objects.filter(id=id).delete()
            datos = {'message':"Registro Eliminado"}
        else:
            datos = {'message':"No se encontraró el registro", 'muestras': []}
        return JsonResponse(datos)
    

def instanciar_Pacientes(id):
    if (id>0):
        Pacientes = Paciente.objects.get(id=id)
        if Pacientes:
            return Pacientes

def instanciar_Muestra(id):
    if (id>0):
        Muestras = Muestra.objects.get(id=id)
        if Muestras:
            return Muestras
        
def validar_cadena_repeticion(cadena):
    patron = r'([a-zA-Z])\1\1'
    return bool(re.search(patron, cadena))

def validar_cadena_espacios(cadena):
    patron = r'^[^ ]+(?: {0,1}[^ ]+)*$'
    return bool(re.match(patron,cadena))