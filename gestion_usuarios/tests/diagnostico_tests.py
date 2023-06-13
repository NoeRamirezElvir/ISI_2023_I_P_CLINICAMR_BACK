from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import Diagnostico, Sintoma, Enfermedad, EnfermedadDetalle, DiagnosticoDetalle
import json

class DiagnosticoTests(TestCase):
    def setUp(self):
        self.url = reverse('diagnostico_list')
        self.sintoma=Sintoma.objects.create(nombre='sintoma 1', descripcion='sintoma 1')
        self.enfermedad=Enfermedad.objects.create(nombre='enfermedad 1')
        EnfermedadDetalle.objects.create(idEnfermedad = self.enfermedad, idSintoma = self.sintoma)
        self.diagnostico = Diagnostico.objects.create(descripcion='diagnostico 1')
        DiagnosticoDetalle.objects.create(idDiagnostico = self.diagnostico, idEnfermedad = self.enfermedad)

    def test_get_diagnosticos(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        diagnosticos = response.json()
        self.assertEqual(len(diagnosticos), 2)

    def test_post_diagnostico(self):
        data = {
            'descripcion': 'Descripción del diagnóstico',
            'idEnfermedades':[{
                'id':self.enfermedad.pk
            }]
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro exitoso'})
        self.assertTrue(Diagnostico.objects.filter(descripcion='Descripción del diagnóstico').exists())

    def test_post_diagnostico_invalid(self):
        data = {
            'descripcion': 'Descripciooon incorrecta',
            'idEnfermedades':[{
                'id':self.enfermedad.pk
            }]
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro exitoso'})
        self.assertTrue(Diagnostico.objects.filter(descripcion='Descripción del diagnóstico').exists())

    def test_put_diagnostico(self):
        diagnostico = Diagnostico.objects.create(descripcion='Descripción inicial')
        data = {
            'descripcion': 'Descripción actualizada',
            'idEnfermedades':[{
                'id':self.enfermedad.pk
            }]
        }

        put_url = reverse('diagnostico_process_id', args=[diagnostico.id])
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})

        diagnostico.refresh_from_db()
        self.assertEqual(diagnostico.descripcion, 'Descripción actualizada')

    def test_delete_diagnostico(self):
        diagnostico = self.diagnostico
        delete_url = reverse('diagnostico_process_id', args=[diagnostico.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Diagnostico.DoesNotExist):
            diagnostico.refresh_from_db()

    def test_delete_diagnostico_invalid(self):
        diagnostico = self.diagnostico
        delete_url = reverse('diagnostico_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(Diagnostico.DoesNotExist):
            diagnostico.refresh_from_db()
