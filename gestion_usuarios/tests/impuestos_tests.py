from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Impuesto
import json

class ImpuestoTests(TestCase):
    def setUp(self):
        self.url = reverse('Impuestos_list')
        self.impuesto_post = Impuesto.objects.create(nombre='Impuesto 1', valor=0.10)

    def test_get_impuestos(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        impuestos = response.json()
        self.assertEqual(len(impuestos), 2)

    def test_post_impuesto(self):
        data = {
            'nombre': 'Impuesto 2',
            'valor': 0.15
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Impuesto.objects.filter(nombre='Impuesto 2').exists())
        self.impuesto_post = Impuesto.objects.filter(nombre='Impuesto 2').first()

    def test_post_impuesto_invalid_name(self):
        data = {
            'nombre': 'Impuestooo',
            'valor': 0.15
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

    def test_post_impuesto_invalid_value(self):
        data = {
            'nombre': 'Impuesto',
            'valor': 2
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

    def test_put_impuesto(self):
        impuesto = self.impuesto_post
        data = {
            'nombre': 'Impuesto Actualizado',
            'valor': 0.20
        }

        put_url = reverse('Impuestos_process_id', args=[impuesto.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        impuesto.refresh_from_db()
        self.assertEqual(impuesto.nombre, 'Impuesto Actualizado')
        self.assertEqual(impuesto.valor, Decimal('0.20'))

    def test_delete_impuesto(self):
        impuesto = self.impuesto_post
        delete_url = reverse('Impuestos_process_id', args=[impuesto.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Impuesto.DoesNotExist):
            impuesto.refresh_from_db()

    def test_delete_impuesto_invalid(self):
        impuesto = self.impuesto_post
        delete_url = reverse('Impuestos_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Impuesto.DoesNotExist):
            impuesto.refresh_from_db()
