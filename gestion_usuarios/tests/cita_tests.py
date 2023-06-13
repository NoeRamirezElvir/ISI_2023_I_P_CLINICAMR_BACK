from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Cita, Paciente, TipoDocumentos
from datetime import datetime
import json

class CitaTests(TestCase):
    def setUp(self):
        self.url = reverse('citas_list')
        self.documento = TipoDocumentos.objects.create(nombre='DNI',longitud='13')
        self.paciente = Paciente.objects.create(
                                                nombre='paciente',
                                                apellido='prueba',
                                                fechaNacimiento='2001-11-15',
                                                correo='paciente.prueba@correo.com',
                                                telefono=88990077,
                                                direccion='123 col prueba',
                                                idTipoDocumento=self.documento,
                                                documento='0801200200577'
                                            )
        self.cita_post = Cita.objects.create(
                                                idPaciente=self.paciente,
                                                fechaActual=datetime(2023, 6, 12, 10, 0),
                                                fechaProgramada=datetime(2023, 6, 13, 10, 0),
                                                fechaMaxima=datetime(2023, 6, 15, 9, 0),
                                                activa=1
                                            )


    def test_get_citas(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        citas = response.json()
        self.assertEqual(len(citas), 2)

    def test_post_cita(self):
        data = {
            'idPaciente': self.paciente.pk,
            'fechaActual': '2023-06-12T15:30:00',
            'fechaProgramada': '2023-06-13T15:30:00',
            'fechaMaxima': '2023-06-20T15:30:00',
            'activa': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Cita.objects.filter(idPaciente=self.paciente).exists())

    def test_post_cita_invalid_date_actual(self):
        data = {
            'idPaciente': self.paciente.pk,
            'fechaActual': '2023-06-14T15:30:00',
            'fechaProgramada': '2023-06-13T15:30:00',
            'fechaMaxima': '2023-06-20T15:30:00',
            'activa': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Cita.objects.filter(idPaciente=self.paciente).exists())

    def test_post_cita_invalid_date_programada(self):
        data = {
            'idPaciente': self.paciente.pk,
            'fechaActual': '2023-06-12T15:30:00',
            'fechaProgramada': '2023-06-21T15:30:00',
            'fechaMaxima': '2023-06-20T15:30:00',
            'activa': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Cita.objects.filter(idPaciente=self.paciente).exists())

    def test_post_cita_invalid_date_maxima(self):
        data = {
            'idPaciente': self.paciente.pk,
            'fechaActual': '2023-06-12T15:30:00',
            'fechaProgramada': '2023-06-15T15:30:00',
            'fechaMaxima': '2023-06-20T23:30:00',
            'activa': 1
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(Cita.objects.filter(idPaciente=self.paciente).exists())


    def test_put_cita(self):
        cita = self.cita_post
        data = {
            'idPaciente': self.paciente.pk,
            'fechaActual': '2023-06-12T15:30:00',
            'fechaProgramada': '2023-06-25T11:00:00',
            'fechaMaxima': '2023-06-25T10:30:00',
            'activa': 1
        }

        put_url = reverse('citas_process_id', args=[cita.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        cita.refresh_from_db()
        self.assertEqual(cita.idPaciente, self.paciente)
        self.assertEqual(cita.activa, 1)

    def test_delete_cita(self):
        cita = self.cita_post
        delete_url = reverse('citas_process_id', args=[cita.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Cita.DoesNotExist):
            cita.refresh_from_db()

    def test_delete_cita_invalid(self):
        cita = self.cita_post
        delete_url = reverse('citas_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Cita.DoesNotExist):
            cita.refresh_from_db()
