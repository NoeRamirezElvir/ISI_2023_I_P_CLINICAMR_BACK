from django.test import TestCase
from django.urls import reverse
from gestion_usuarios.models import *
import json

class TrasladoTests(TestCase):
    def setUp(self):
        self.url = reverse('traslados_list')
        self.autorizacion = AutorizacionPaciente.objects.create(motivos='Motivo', confirmacion=1)

        self.cargo = CargoEmpleado.objects.create(nombre='Cargo 1', descripcion='Descripción 1', activo=1)
        self.tipoDocumento = TipoDocumentos.objects.create(nombre='DNI',longitud=13)
        self.especialidad = EspecialidadMedico.objects.create(nombre='Medico general', descripcion='Descripción 1')
        self.empleado = Empleado.objects.create(nombre='empleado', apellidos='prueba',
                                                fechaNacimiento='2000-11-11',
                                                email='empleado@example.com',
                                                telefono='99887700',
                                                direccion='123 col prueba',
                                                idTipoDocumentos=self.tipoDocumento,
                                                documento='0801200200482',
                                                idEspecialidadMedico=self.especialidad,
                                                idCargoEmpleado=self.cargo,
                                                activo=1)
        
        self.paciente = Paciente.objects.create(nombre='paciente',
                                                apellido='prueba',
                                                fechaNacimiento='2000-11-11',
                                                correo='correo@tipo.com',
                                                telefono='99886677',
                                                direccion='123 col prueba',
                                                idTipoDocumento=self.tipoDocumento,
                                                documento='8901220004753')

    def test_get_traslados(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        traslados = response.json()
        self.assertEqual(len(traslados), 2)

    def test_post_traslados(self):
        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar traslado',
            'direccion':'123 lugar traslado',
            'telefono':22889956
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(TrasladoPaciente.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_post_traslados_invalid_name(self):
        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar  traslado',
            'direccion':'123 lugar traslado',
            'telefono':22889956
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(TrasladoPaciente.objects.filter(idPaciente__documento='8901220004753').exists())

    def test_post_traslados_invalid_descripcion(self):
        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar tttraslado',
            'direccion':'123 lugar traslado',
            'telefono':22889956
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Exitoso.'})
        self.assertTrue(TrasladoPaciente.objects.filter(idPaciente__documento='8901220004753').exists())



    def test_put_paciente(self):
        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar traslado',
            'direccion':'123 lugar traslado',
            'telefono':22889956
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        traslado = TrasladoPaciente.objects.get(idPaciente__documento='8901220004753')

        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar traslado actualizado',
            'direccion':'123 lugar traslado actualizado',
            'telefono':22889956
        }


        put_url = reverse('traslados_process_id', args=[traslado.pk])  
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})


        traslado.refresh_from_db()
        self.assertEqual(traslado.nombre, 'lugar traslado actualizado')
        self.assertEqual(traslado.direccion, '123 lugar traslado actualizado')

    def test_put_paciente_invalid_telefono(self):
        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar traslado',
            'direccion':'123 lugar traslado',
            'telefono':22889956
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        traslado = TrasladoPaciente.objects.get(idPaciente__documento='8901220004753')

        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar traslado actualizado',
            'direccion':'123 lugar traslado actualizado',
            'telefono':12889956
        }


        put_url = reverse('traslados_process_id', args=[traslado.pk])  
        response = self.client.put(put_url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'La actualización fue exitosa.'})


        traslado.refresh_from_db()
        self.assertEqual(traslado.telefono, 12889956)

    def test_delete_traslado(self):
        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar traslado',
            'direccion':'123 lugar traslado',
            'telefono':22889956
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        traslado = TrasladoPaciente.objects.get(idPaciente__documento='8901220004753')

        delete_url = reverse('traslados_process_id', args=[traslado.pk])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(traslado.DoesNotExist):
            traslado.refresh_from_db()

    def test_delete_traslado(self):
        data = {
            'idAutorizacionPaciente':self.autorizacion.pk,
            'idPaciente':self.paciente.pk,
            'idEmpleado':self.empleado.pk,
            'nombre':'lugar traslado',
            'direccion':'123 lugar traslado',
            'telefono':22889956
        }

        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        traslado = TrasladoPaciente.objects.get(idPaciente__documento='8901220004753')

        delete_url = reverse('traslados_process_id', args=[100])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Registro Eliminado'})
        with self.assertRaises(traslado.DoesNotExist):
            traslado.refresh_from_db()


    