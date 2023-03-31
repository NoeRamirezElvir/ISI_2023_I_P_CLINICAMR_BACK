from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
#Las llaves foraneas deben ser NULL y agregar on_delete=models.PROTECT
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
        fechaCreacion = models.DateTimeField()
        fechaModificacion = models.DateTimeField(auto_now=True)
        intentos = models.PositiveSmallIntegerField(null=True, blank=True,default=0)
#Paciente
class Paciente(models.Model):
        nombre = models.CharField(max_length=40)
        apellido = models.CharField(max_length=40)
        fechaNacimiento = models.DateField()
        idTipoDocumento = models.ForeignKey(TipoDocumentos, on_delete=models.PROTECT)
        telefono = models.CharField(max_length=15)
        documento = models.CharField(max_length=50)
        correo = models.CharField(max_length=40)
        direccion = models.CharField(max_length=40)
#Tipo Muestra
class TipoMuestra(models.Model):
        nombre = models.CharField(max_length=40)
        metodoConservacion = models.CharField(max_length=50)
#Muestra
class Muestra(models.Model):
        idTipoMuestra = models.ForeignKey(TipoMuestra, on_delete=models.PROTECT)
        idPaciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
        fecha = models.DateField()
#Impuesto
class Impuesto(models.Model):
        nombre = models.CharField(max_length=20)
        valor = models.DecimalField(max_digits=4, decimal_places=2)
#Impuesto Historico
class ImpuestoHitorico(models.Model):
        idImpuesto = models.ForeignKey(Impuesto, on_delete=models.PROTECT)
        fechaInicio = models.DateTimeField()
        fechaFinal = models.DateTimeField(null=True, blank=True)
        valor = models.DecimalField(max_digits=4, decimal_places=2)
#Cita
class Cita(models.Model):
        idPaciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
        fechaActual = models.DateTimeField()
        fechaProgramada = models.DateTimeField()
        fechaMaxima = models.DateTimeField()
        activa = models.PositiveSmallIntegerField()
#Subtipo
class Subtipo(models.Model):
        nombre = models.CharField(max_length=40)
        activo = models.PositiveSmallIntegerField()
#Tipo
class Tipo(models.Model):
        idsubtipo = models.ForeignKey(Subtipo,  on_delete=models.PROTECT)
        nombre = models.CharField(max_length=40)
        descripcion = models.CharField(max_length=40)
        precio = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
#Falta
class Proveedor(models.Model):
        nombre = models.CharField(max_length=50)
        telefono = models.CharField(max_length=15)
        correo = models.CharField(max_length=30)
        direccion = models.CharField(max_length=50)

#Medicamento Falta
class Medicamento(models.Model):
        nombre = models.CharField(max_length=50)
        idTipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
        fechaRegistro = models.DateField()
        activo = models.PositiveSmallIntegerField()
        stockActual = models.PositiveIntegerField()
        stockMinimo = models.PositiveIntegerField()
        stockMaximo = models.PositiveIntegerField()
        idProveedor = models.ForeignKey(Proveedor,on_delete=models.PROTECT)
        idImpuesto  = models.ForeignKey(Impuesto, on_delete=models.PROTECT)
        costoCompra = models.DecimalField(max_digits=8, decimal_places=2)
        precioVenta = models.DecimalField(max_digits=8, decimal_places=2)
#Falta
class CostoHistoricoMedicamento(models.Model):
        idmedicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
        fechaInicio = models.DateTimeField()
        fechaFinal = models.DateTimeField(null=True, blank=True)
        activo  = models.PositiveSmallIntegerField()
        costo = models.DecimalField(max_digits=8, decimal_places=2)
#Falta
class PrecioHistoricoMedicamento(models.Model):
        idmedicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
        fechaInicio = models.DateTimeField()
        fechaFinal = models.DateTimeField(null=True, blank=True)
        activo  = models.PositiveSmallIntegerField()
        precio = models.DecimalField(max_digits=8, decimal_places=2)

class Laboratorios(models.Model):
        nombre = models.CharField(max_length=50)
        direccion = models.CharField(max_length=50)
        telefono = models.CharField(max_length=15)
        disponibilidad = models.PositiveSmallIntegerField()

class Enfermedad(models.Model):
        nombre = models.CharField(max_length=50)

class Sintoma(models.Model):
        nombre = models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)

class EnfermedadDetalle(models.Model):
        idEnfermedad = models.ForeignKey(Enfermedad, on_delete=models.PROTECT)
        idSintoma = models.ForeignKey(Sintoma, on_delete=models.PROTECT)

class MetodoDePago(models.Model):
        nombre = models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)

class Diagnostico(models.Model):
        descripcion = models.CharField(max_length=100)

class Consulta(models.Model):
        idCita = models.ForeignKey(TipoMuestra, on_delete=models.PROTECT)
        idEmpleado = models.ForeignKey(Paciente, on_delete=models.PROTECT)
        fecha = models.DateField()

class ParametrosGenerales(models.Model):
        nombre =models.CharField(max_length=50)
        descripcion = models.CharField(max_length=50)
        valor = models.CharField(max_length=100)

class ConsultaDetalle(models.Model):
        idEnfermedad = models.ForeignKey(Enfermedad, on_delete=models.PROTECT)
        idSintoma = models.ForeignKey(Sintoma, on_delete=models.PROTECT)
        idMedicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)

class DiagnosticoDetalle(models.Model):
        idEnfermedad = models.ForeignKey(Enfermedad, on_delete=models.PROTECT)
        idDiagnostico = models.ForeignKey(Diagnostico, on_delete=models.PROTECT)

class Tratamiento(models.Model):
        idTipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
        idPaciente = models.ForeignKey(Paciente, on_delete=models.PROTECT)
        fecha = models.DateField()
        diasTratamiento = models.PositiveIntegerField()
        estado = models.CharField(max_length=50)

class Resultados(models.Model):
        idTratamiento = models.ForeignKey(Tratamiento, on_delete=models.PROTECT)        
        fecha = models.DateField()
        observacion = models.CharField(max_length=100)

class Examen(models.Model):
        idMuestra = models.ForeignKey(Muestra, on_delete=models.PROTECT)
        idTipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
        fecha = models.DateTimeField(auto_now_add=True)
        fechaProgramada = models.DateTimeField()
        observacion = models.CharField(max_length=100)
        idLaboratorio = models.ForeignKey(Laboratorios, on_delete=models.PROTECT)

class PrecioHistoricoExamen(models.Model):
        idTipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
        fechaInicio = models.DateTimeField()
        fechaFinal = models.DateTimeField(null=True, blank=True)
        activo  = models.PositiveSmallIntegerField()
        precio = models.DecimalField(max_digits=8, decimal_places=2)

class PrecioHistoricoTratamiento(models.Model):
        idTipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
        fechaInicio = models.DateTimeField()
        fechaFinal = models.DateTimeField(null=True, blank=True)
        activo  = models.PositiveSmallIntegerField()
        precio = models.DecimalField(max_digits=8, decimal_places=2)