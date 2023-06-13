from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import AutorizacionPaciente
import json

class AutorizacionPacienteTests(TestCase):
    def setUp(self):
        self.url = reverse('autorizar_list')
        self.autorizacion_post = AutorizacionPaciente.objects.create(motivos='Motivo', confirmacion=1)

    def test_get_autorizaciones_paciente(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        autorizaciones = response.json()
        self.assertEqual(len(autorizaciones), 2)

    def test_post_autorizacion_paciente(self):
        data = {
            'motivos': 'Motivo',
            'confirmacion': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(AutorizacionPaciente.objects.filter(motivos='Motivo').exists())

    def test_post_autorizacion_paciente_invalid_motivo_inicio(self):
        data = {
            'motivos': 'Motivo  prueba',
            'confirmacion': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(AutorizacionPaciente.objects.filter(motivos='Motivo').exists())

    def test_post_autorizacion_paciente_invalid_motivo_letras(self):
        data = {
            'motivos': 'Motivooo 43',
            'confirmacion': 0
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(AutorizacionPaciente.objects.filter(motivos='Motivo 43').exists())

    def test_put_autorizacion_paciente(self):
        autorizacion = self.autorizacion_post
        data = {
            'motivos': 'Motivo Actualizado',
            'confirmacion': 1
        }

        put_url = reverse('autorizar_process_id', args=[autorizacion.pk])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        autorizacion.refresh_from_db()
        self.assertEqual(autorizacion.motivos, 'Motivo Actualizado')
        self.assertEqual(autorizacion.confirmacion, 1)

    def test_delete_autorizacion_paciente(self):
        autorizacion = self.autorizacion_post
        delete_url = reverse('autorizar_process_id', args=[autorizacion.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(AutorizacionPaciente.DoesNotExist):
            autorizacion.refresh_from_db()

    def test_delete_autorizacion_paciente_invalid(self):
        autorizacion = self.autorizacion_post
        delete_url = reverse('autorizar_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(AutorizacionPaciente.DoesNotExist):
            autorizacion.refresh_from_db()
