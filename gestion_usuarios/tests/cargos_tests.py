from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import CargoEmpleado
from gestion_usuarios.views.cargo_views import CargosView
import json

class CargoTests(TestCase):
    def setUp(self):
        self.url = reverse('cargo_list')  # Ajusta esto según la URL de tu vista

    def test__cargo_post_valid_data(self):
        url = reverse('cargo_list')
        data = {
            'nombre': 'Cargo de prueba',
            'descripcion': 'Descripción de prueba',
            'activo': 1
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(CargoEmpleado.objects.filter(nombre=data['nombre']).exists())

    def test_post_cargo_invalid_nombre_letras_data(self):
        url = reverse('cargo_list')

        data = {
            'nombre': 'Cargooo de prueba',
            'descripcion': 'Descripción de prueba',
            'activo': 1
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

        self.assertTrue(CargoEmpleado.objects.filter(nombre=data['nombre']).exists())

    def test_cargo_post_invalid_nombre_espacios_data(self):
        url = reverse('cargo_list')

        data = {
            'nombre': 'Cargo  de prueba',
            'descripcion': 'Descripción de prueba',
            'activo': 1
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})

        self.assertTrue(CargoEmpleado.objects.filter(nombre=data['nombre']).exists())


    def test_get_cargos(self):
        CargoEmpleado.objects.create(nombre='Cargo 1', descripcion='Descripción 1', activo=1)
        CargoEmpleado.objects.create(nombre='Cargo 2', descripcion='Descripción 2', activo=1)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        cargos = response.json()
        self.assertEqual(len(cargos), 2) 

    def test_put_cargo(self):

        cargo = CargoEmpleado.objects.create(nombre='Cargo 1', descripcion='Descripción 1', activo=1)

        data = {
            'nombre': 'Cargo actualizado',
            'descripcion': 'Descripción actualizada',
            'activo': 0
        }

        put_url = reverse('cargos_process_id', args=[cargo.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        cargo.refresh_from_db()
        self.assertEqual(cargo.nombre, 'Cargo actualizado 1')
        self.assertEqual(cargo.descripcion, 'Descripción actualizada 1')
        self.assertEqual(cargo.activo, 0)

    def test_delete_cargo(self):
        cargo = CargoEmpleado.objects.create(nombre='Cargo a eliminar', descripcion='Descripción', activo=1)

        delete_url = reverse('cargos_process_id', args=[cargo.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(CargoEmpleado.DoesNotExist):
            cargo.refresh_from_db()

    def test_delete_cargo_invalid(self):
        cargo = CargoEmpleado.objects.create(nombre='Cargo a eliminar', descripcion='Descripción', activo=1)

        delete_url = reverse('cargos_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(CargoEmpleado.DoesNotExist):
            cargo.refresh_from_db()