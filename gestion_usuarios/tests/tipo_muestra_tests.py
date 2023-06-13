from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import TipoMuestra
import json

class TipoMuestraTests(TestCase):
    def setUp(self):
        self.url = reverse('tmuestra_list')
        self.tipo_muestra_post = TipoMuestra.objects.create(nombre='Tipo Muestra 1', metodoConservacion='Conservación 1')

    def test_get_tipos_muestra(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        tipos_muestra = response.json()
        self.assertEqual(len(tipos_muestra), 2)

    def test_post_tipo_muestra(self):
        data = {
            'nombre': 'Tipo Muestra 2',
            'metodoConservacion': 'Conservación 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(TipoMuestra.objects.filter(nombre='Tipo Muestra 2').exists())
        self.tipo_muestra_post = TipoMuestra.objects.filter(nombre='Tipo Muestra 2').first()

    def test_post_tipo_muestra_invalid_name(self):
        data = {
            'nombre': 'Tipooo Muestra 2',
            'metodoConservacion': 'Conservación 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(TipoMuestra.objects.filter(nombre='Tipo Muestra 2').exists())
        self.tipo_muestra_post = TipoMuestra.objects.filter(nombre='Tipo Muestra 2').first()

    def test_post_tipo_muestra_invalid_method(self):
        data = {
            'nombre': 'Tipo Muestra 2',
            'metodoConservacion': 'abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwabcdefghijklmnopqrst'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(TipoMuestra.objects.filter(nombre='Tipo Muestra 2').exists())
        self.tipo_muestra_post = TipoMuestra.objects.filter(nombre='Tipo Muestra 2').first()

    def test_put_tipo_muestra(self):
        tipo_muestra = self.tipo_muestra_post
        data = {
            'nombre': 'Tipo Muestra Actualizado',
            'metodoConservacion': 'Conservación Actualizada'
        }

        put_url = reverse('tmuestra_process_id', args=[tipo_muestra.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        tipo_muestra.refresh_from_db()
        self.assertEqual(tipo_muestra.nombre, 'Tipo Muestra Actualizado')
        self.assertEqual(tipo_muestra.metodoConservacion, 'Conservación Actualizada')

    def test_delete_tipo_muestra(self):
        tipo_muestra = self.tipo_muestra_post
        delete_url = reverse('tmuestra_process_id', args=[tipo_muestra.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(TipoMuestra.DoesNotExist):
            tipo_muestra.refresh_from_db()

    def test_delete_tipo_muestra_invalid(self):
        tipo_muestra = self.tipo_muestra_post
        delete_url = reverse('tmuestra_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(TipoMuestra.DoesNotExist):
            tipo_muestra.refresh_from_db()
