from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
#Las llaves foraneas deben ser NULL y agregar on_delete=models.CASCADE
#Cargos de Empleados
class CargoEmpleado(models.Model):
        nombre = models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)
        activo = models.PositiveSmallIntegerField()
     
#Tipo de Documentos
class TipoDocumentos(models.Model):
        nombre = models.CharField(max_length=50)
        longitud = models.PositiveSmallIntegerField()

#Especialidades de Medicos
class EspecialidadMedico(models.Model):
        nombre = models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)

#Empleados
class Empleado(models.Model):
        nombre = models.CharField(max_length=40)
        apellidos = models.CharField(max_length=40)
        email = models.EmailField(max_length=40)
        fechaNacimiento = models.DateField()
        telefono = models.CharField(max_length=15)
        direccion = models.CharField(max_length=50)
        idTipoDocumentos = models.ForeignKey(TipoDocumentos, on_delete=models.PROTECT, null=True,blank=True)
        documento = models.CharField(max_length=20)
        idEspecialidadMedico = models.ForeignKey(EspecialidadMedico, on_delete=models.PROTECT, null=True,blank=True)
        idCargoEmpleado = models.ForeignKey(CargoEmpleado, on_delete=models.PROTECT, null=True,blank=True)
        activo = models.PositiveSmallIntegerField()

#Usuarios
class Usuario(models.Model):
        idEmpleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, null=True,blank=True)
        nombreUsuario = models.CharField(max_length=40)
        password = models.CharField(max_length=100)
        activo = models.PositiveSmallIntegerField()
        bloqueado = models.PositiveSmallIntegerField()
        fechaCreacion = models.DateTimeField(auto_now_add=True)
        fechaModificacion = models.DateTimeField(auto_now=True)


class Paciente(models.Model):
        nombre = models.CharField(max_length=40)
        apellido = models.CharField(max_length=40)
        fechaNacimiento = models.DateTimeField()
        idTipoDocumento = models.ForeignKey(TipoDocumentos, on_delete=models.PROTECT)
        documento = models.CharField(max_length=50)
        telefono = models.CharField(max_length=15)
        correo = models.CharField(max_length=40)
        direccion = models.CharField(max_length=40)

class TipoMuestra(models.Model):
        nombre = models.CharField(max_length=40)
        metodoConservacion = models.CharField(max_length=50)

class Muestra(models.Model):
        idTipoMuestra = models.ForeignKey(TipoMuestra, on_delete=models.PROTECT)
        idPaciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
        fecha = models.DateField(auto_now_add=True)

class Impuesto(models.Model):
        nombre = models.CharField(max_length=20)

class Cita(models.Model):
        idPaciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
        fechaActual = models.DateTimeField(auto_now_add=True)
        fechaProgramada = models.DateTimeField()
        fechaMaxima = models.DateTimeField()
        activa = models.PositiveSmallIntegerField()

class Subtipo(models.Model):
        nombre = models.CharField(max_length=40)
        activo = models.PositiveSmallIntegerField()

class Tipo(models.Model):
        idSubtipo = models.ForeignKey(Subtipo,  on_delete=models.PROTECT)
        nombre = models.CharField(max_length=40)
        descripcion = models.CharField(max_length=40)

class Proveedor(models.Model):
        nombre = models.CharField(max_length=50)
        idTipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
        telefono = models.CharField(max_length=15)
        correo = models.CharField(max_length=30)
        direccion = models.CharField(max_length=50)



        