from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Proveedor
import json

class ProveedorTests(TestCase):
    def setUp(self):
        self.url = reverse('proveedores_list')  # Ajusta esto según la URL de tu vista

    def test_get_proveedores(self):
        Proveedor.objects.create(nombre='Proveedor 1', telefono='97899900', correo='proveedor1@example.com', direccion='123 col miraflores')
        Proveedor.objects.create(nombre='Proveedor 2', telefono='97899901', correo='proveedor2@example.com', direccion='123 col miraflores')

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        proveedores = response.json()
        self.assertEqual(len(proveedores), 2) 

    def test_post_proveedor_valid_data(self):
        data = {
            'nombre': 'Proveedor de prueba',
            'telefono': '97899900',
            'correo': 'proveedorprueba@example.com',
            'direccion': 'Dirección de prueba'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Proveedor.objects.filter(nombre=data['nombre']).exists())

    def test_post_proveedor_invalid_data(self):
        data = {
            'nombre': 'Proveedor con nombre demasiado largo, más de 50 caracteres',
            'telefono': '97899900',
            'correo': 'proveedorprueba@example.com',
            'direccion': 'Dirección de prueba'
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.json(), {'message': 'Datos inválidos.'})
        self.assertFalse(Proveedor.objects.filter(nombre=data['nombre']).exists())

    def test_put_proveedor(self):
        proveedor = Proveedor.objects.create(nombre='Proveedor 1', telefono='98990088', correo='proveedor1@example.com', direccion='123 col miraflores')

        data = {
            'nombre': 'Proveedor actualizado',
            'telefono': '98990088',
            'correo': 'proveedor1@example.com',
            'direccion': 'Dirección actualizada'
        }

        put_url = reverse('proveedore_process_id', args=[proveedor.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        proveedor.refresh_from_db()
        self.assertEqual(proveedor.nombre, 'Proveedor actualizado')
        self.assertEqual(proveedor.telefono, '98990088')
        self.assertEqual(proveedor.correo, 'proveedor1@example.com')
        self.assertEqual(proveedor.direccion, 'Dirección actualizada')

    def test_delete_proveedor(self):
        proveedor = Proveedor.objects.create(nombre='Proveedor a eliminar', telefono='97889907', correo='proveedor1@example.com', direccion='Dirección')

        delete_url = reverse('proveedore_process_id', args=[proveedor.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Proveedor.DoesNotExist):
            proveedor.refresh_from_db()

    def test_delete_proveedor_invalid(self):
        proveedor = Proveedor.objects.create(nombre='Proveedor a eliminar', telefono='97889907', correo='proveedor1@example.com', direccion='Dirección')

        delete_url = reverse('proveedore_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Proveedor.DoesNotExist):
            proveedor.refresh_from_db()