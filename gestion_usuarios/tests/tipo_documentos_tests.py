from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import TipoDocumentos
import json

class TipoDocumentosTests(TestCase):
    def setUp(self):
        self.url = reverse('documento_list')

    def test_get_tipo_documentos(self):
        TipoDocumentos.objects.create(nombre='DNI', longitud=13)
        TipoDocumentos.objects.create(nombre='Pasaporte', longitud=9)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        tipo_documentos = response.json()
        self.assertEqual(len(tipo_documentos), 2) 

    def test_post_tipo_documento_valid_data(self):
        data = {
            'nombre': 'Carnet de Identidad',
            'longitud': 10
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')


        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(TipoDocumentos.objects.filter(nombre=data['nombre']).exists())

    def test_post_tipo_documento_invalid_data(self):
        data = {
            'nombre': 'Docuuumento',
            'longitud': 15
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertFalse(TipoDocumentos.objects.filter(nombre=data['nombre']).exists())

    def test_put_tipo_documento(self):
        tipo_documento = TipoDocumentos.objects.create(nombre='DNI', longitud=13)

        data = {
            'nombre': 'DNI actualizado',
            'longitud': 15
        }

        put_url = reverse('documento_process_id', args=[tipo_documento.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        tipo_documento.refresh_from_db()
        self.assertEqual(tipo_documento.nombre, 'DNI actualizado')
        self.assertEqual(tipo_documento.longitud, 15)

    def test_delete_tipo_documento(self):
        tipo_documento = TipoDocumentos.objects.create(nombre='Tipo de documento a eliminar', longitud=10)

        delete_url = reverse('documento_process_id', args=[tipo_documento.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(TipoDocumentos.DoesNotExist):
            tipo_documento.refresh_from_db()

    def test_delete_tipo_documento_invalid(self):
        tipo_documento = TipoDocumentos.objects.create(nombre='Tipo de documento a eliminar', longitud=10)

        delete_url = reverse('documento_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.json(), {'message': 'El tipo de documento no existe.'})
        tipo_documento.refresh_from_db()  # El tipo de documento no debe ser eliminado
        self.assertEqual(tipo_documento.nombre, 'Tipo de documento a eliminar')
        self.assertEqual(tipo_documento.longitud, 10)
