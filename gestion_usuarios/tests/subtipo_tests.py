from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Subtipo
import json

class SubtipoTests(TestCase):
    def setUp(self):
        self.url = reverse('subtipo_list')

    def test_get_subtipos(self):
        Subtipo.objects.create(nombre='Subtipo 1', activo=1)
        Subtipo.objects.create(nombre='Subtipo 2', activo=1)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        subtipos = response.json()
        self.assertEqual(len(subtipos), 2) 

    def test_post_subtipo_valid_data(self):
        data = {
            'nombre': 'Subtipo de prueba',
            'activo': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')


        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Subtipo.objects.filter(nombre=data['nombre']).exists())

    def test_post_subtipo_invalid_data(self):
        data = {
            'nombre': 'Subtipo con nombre demasiado largo, más de 40 caracteres',
            'activo': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertFalse(Subtipo.objects.filter(nombre=data['nombre']).exists())

    def test_put_subtipo(self):
        subtipo = Subtipo.objects.create(nombre='Subtipo 1', activo=1)

        data = {
            'nombre': 'subtipo uno',
            'activo': 0
        }

        put_url = reverse('subtipo_process_id', args=[subtipo.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        subtipo.refresh_from_db()
        self.assertEqual(subtipo.nombre, 'subtipo uno')
        self.assertEqual(subtipo.activo, 0)

    def test_delete_subtipo(self):
        subtipo = Subtipo.objects.create(nombre='Subtipo a eliminar', activo=1)

        delete_url = reverse('subtipo_process_id', args=[subtipo.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Subtipo.DoesNotExist):
            subtipo.refresh_from_db()

    def test_delete_subtipo_invalid(self):
        subtipo = Subtipo.objects.create(nombre='Subtipo a eliminar', activo=1)

        delete_url = reverse('subtipo_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.json(), {'message': 'El subtipo no existe.'})
        subtipo.refresh_from_db()  
        self.assertEqual(subtipo.nombre, 'Subtipo a eliminar')
        self.assertEqual(subtipo.activo, 1)
