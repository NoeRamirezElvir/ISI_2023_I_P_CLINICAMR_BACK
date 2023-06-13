from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Laboratorios
import json

class LaboratoriosTests(TestCase):
    def setUp(self):
        self.url = reverse('laboratorios_list')  # Ajusta esto según la URL de tu vista

    def test_get_laboratorios(self):
        laboratorio1 = Laboratorios.objects.create(nombre='Laboratorio 1', direccion='Dirección 1', telefono='99887755', disponibilidad=1)
        laboratorio2 = Laboratorios.objects.create(nombre='Laboratorio 2', direccion='Dirección 2', telefono='88990044', disponibilidad=0)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        laboratorios = response.json()
        self.assertEqual(len(laboratorios), 2) 

    def test_post_laboratorio_valid_data(self):
        data = {
            'nombre': 'Laboratorio de prueba',
            'direccion': 'Dirección de prueba',
            'telefono': '88990044',
            'disponibilidad': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Laboratorios.objects.filter(nombre=data['nombre']).exists())

    def test_post_laboratorio_invalid_data(self):
        data = {
            'nombre': 'Laboratorio con dirección demasiado larga, más de 50 caracteres',
            'direccion': 'Dirección de prueba',
            'telefono': '88990044',
            'disponibilidad': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')


        self.assertEqual(response.json(), {'message': 'Datos inválidos.'})
        self.assertFalse(Laboratorios.objects.filter(nombre=data['nombre']).exists())

    def test_put_laboratorio(self):
        laboratorio = Laboratorios.objects.create(nombre='Laboratorio 1', direccion='Dirección 1', telefono='99887755', disponibilidad=1)

        data = {
            'nombre': 'Laboratorio actualizado',
            'direccion': 'Dirección actualizada',
            'telefono': '88990044',
            'disponibilidad': 0
        }

        put_url = reverse('laboratorios_process_id', args=[laboratorio.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        laboratorio.refresh_from_db()
        self.assertEqual(laboratorio.nombre, 'Laboratorio actualizado')
        self.assertEqual(laboratorio.direccion, 'Dirección actualizada')
        self.assertEqual(laboratorio.telefono, '88990044')
        self.assertEqual(laboratorio.disponibilidad, 0)

    def test_delete_laboratorio(self):
        laboratorio = Laboratorios.objects.create(nombre='Laboratorio a eliminar', direccion='Dirección', telefono='99887755', disponibilidad=1)

        delete_url = reverse('laboratorios_process_id', args=[laboratorio.pk]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Laboratorios.DoesNotExist):
            laboratorio.refresh_from_db()

    def test_delete_laboratorio_invalid(self):
        laboratorio = Laboratorios.objects.create(nombre='Laboratorio a eliminar', direccion='Dirección', telefono='99887755', disponibilidad=1)

        delete_url = reverse('laboratorios_process_id', args=[100]) 
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Laboratorios.DoesNotExist):
            laboratorio.refresh_from_db()
