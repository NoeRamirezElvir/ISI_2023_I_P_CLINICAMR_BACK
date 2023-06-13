from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import MetodoDePago
import json

class MetodoDePagoTests(TestCase):
    def setUp(self):
        self.url = reverse('metodop_list')
        self.metodo_pago_post = MetodoDePago.objects.create(nombre='Metodo 1', descripcion='Descripción 1')

    def test_get_metodos_pago(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        metodos_pago = response.json()
        self.assertEqual(len(metodos_pago), 2)

    def test_post_metodo_pago(self):
        data = {
            'nombre': 'Metodo 2',
            'descripcion': 'Descripción 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(MetodoDePago.objects.filter(nombre='Metodo 2').exists())
        self.metodo_pago_post = MetodoDePago.objects.filter(nombre='Metodo 2').first()

    def test_post_metodo_pago_invalid_name(self):
        data = {
            'nombre': 'Metodooo',
            'descripcion': 'Descripción 2'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(MetodoDePago.objects.filter(nombre='Metodo 2').exists())
        self.metodo_pago_post = MetodoDePago.objects.filter(nombre='Metodo 2').first()

    def test_post_metodo_pago_invalid_description(self):
        data = {
            'nombre': 'Metodo',
            'descripcion': 'abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(MetodoDePago.objects.filter(nombre='Metodo 2').exists())
        self.metodo_pago_post = MetodoDePago.objects.filter(nombre='Metodo 2').first()

    def test_put_metodo_pago(self):
        metodo_pago = self.metodo_pago_post
        data = {
            'nombre': 'Metodo Actualizado',
            'descripcion': 'Descripción Actualizada'
        }

        put_url = reverse('metodop_process_id', args=[metodo_pago.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        metodo_pago.refresh_from_db()
        self.assertEqual(metodo_pago.nombre, 'Metodo Actualizado')
        self.assertEqual(metodo_pago.descripcion, 'Descripción Actualizada')

    def test_delete_metodo_pago(self):
        metodo_pago = self.metodo_pago_post
        delete_url = reverse('metodop_process_id', args=[metodo_pago.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(MetodoDePago.DoesNotExist):
            metodo_pago.refresh_from_db()

    def test_delete_metodo_pago_invalid(self):
        metodo_pago = self.metodo_pago_post
        delete_url = reverse('metodop_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(MetodoDePago.DoesNotExist):
            metodo_pago.refresh_from_db()
