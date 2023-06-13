
from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Descuento
import json
from decimal import Decimal

class DescuentoTests(TestCase):
    def setUp(self):
        self.url = reverse('Descuentos_list')  # Ajusta esto según la URL de tu vista

    def test_post_valid_data(self):
        data = {
            'nombre': 'Descuento de prueba',
            'valor': 0.10
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Descuento.objects.filter(nombre=data['nombre']).exists())

    def test_post_invalid_nombre_data(self):
        data = {
            'nombre': '',
            'valor': 0.10
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertFalse(Descuento.objects.filter(valor=data['valor']).exists())

    def test_post_invalid_valor_data(self):
        data = {
            'nombre': 'Descuento de prueba',
            'valor': 0.30
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertFalse(Descuento.objects.filter(nombre=data['nombre']).exists())

    def test_get_descuentos(self):
        Descuento.objects.create(nombre='Descuento 1', valor=0.10)
        Descuento.objects.create(nombre='Descuento 2', valor=0.20)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        descuentos = response.json()
        self.assertEqual(len(descuentos), 2) 

    def test_put_descuento(self):
        descuento = Descuento.objects.create(nombre='Descuento 1', valor=0.10)

        data = {
            'nombre': 'Descuento ac',
            'valor': 0.15
        }

        put_url = reverse('Descuentos_process_id', args=[descuento.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        descuento.refresh_from_db()
        self.assertEqual(descuento.nombre, 'Descuento ac')
        self.assertEqual(descuento.valor, Decimal('0.15'))

    def test_delete_descuento(self):
        descuento = Descuento.objects.create(nombre='Descuento a eliminar', valor=0.10)

        delete_url = reverse('Descuentos_process_id', args=[descuento.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Descuento.DoesNotExist):
            descuento.refresh_from_db()

    def test_delete_descuento_invalid(self):
        descuento = Descuento.objects.create(nombre='Descuento a eliminar', valor=0.10)

        delete_url = reverse('Descuentos_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        descuento.refresh_from_db()