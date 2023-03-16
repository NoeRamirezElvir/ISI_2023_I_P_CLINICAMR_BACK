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
    

