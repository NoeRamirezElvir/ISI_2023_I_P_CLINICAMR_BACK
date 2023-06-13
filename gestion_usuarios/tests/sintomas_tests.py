from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Sintoma
import json

class SintomaTests(TestCase):
    def setUp(self):
        self.url = reverse('sintomas_list')  # Ajusta esto según la URL de tu vista

    def test_get_sintomas(self):
        sintoma1 = Sintoma.objects.create(nombre='Sintoma 1', descripcion='Descripción 1')
        sintoma2 = Sintoma.objects.create(nombre='Sintoma 2', descripcion='Descripción 2')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        sintomas = response.json()
        self.assertEqual(len(sintomas), 2) 

    def test_post_sintoma_valid_data(self):
        data = {
            'nombre': 'Sintoma de prueba',
            'descripcion': 'Descripción de prueba'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Sintoma.objects.filter(nombre=data['nombre']).exists())

    def test_post_sintoma_invalid_data(self):
        data = {
            'nombre': 'Sintoma con descripción demasiado larga, más de 50 caracteres',
            'descripcion': 'Descripción de prueba'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {'message': 'Datos inválidos.'})
        self.assertFalse(Sintoma.objects.filter(nombre=data['nombre']).exists())

    def test_put_sintoma(self):
        sintoma = Sintoma.objects.create(nombre='Sintoma 1', descripcion='Descripción 1')

        data = {
            'nombre': 'Sintoma actualizado',
            'descripcion': 'Descripción actualizada'
        }

        put_url = reverse('sintomas_process_id', args=[sintoma.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        sintoma.refresh_from_db()
        self.assertEqual(sintoma.nombre, 'Sintoma actualizado')
        self.assertEqual(sintoma.descripcion, 'Descripción actualizada')

    def test_delete_sintoma(self):
        sintoma = Sintoma.objects.create(nombre='Sintoma a eliminar', descripcion='Descripción')

        delete_url = reverse('sintomas_process_id', args=[sintoma.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Sintoma.DoesNotExist):
            sintoma.refresh_from_db()

    def test_delete_sintoma_invalid(self):
        sintoma = Sintoma.objects.create(nombre='Sintoma a eliminar', descripcion='Descripción')

        delete_url = reverse('sintomas_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Sintoma.DoesNotExist):
            sintoma.refresh_from_db()
