from django.contrib.auth.models import User
from django.db import models


class Activation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)


# ===========================
#      UBICACIÓN
# ===========================

class Estado(models.Model):
    nombre_estado = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_estado


class Ciudad(models.Model):
    nombre_ciudad = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_ciudad


# ===========================
#        USUARIOS
# ===========================

class TipoUsuario(models.Model):
    tipousuario = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.tipousuario


class Usuario(models.Model):
    # Relación con Django User (si quieres usarlo)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    correo = models.EmailField(unique=True)
    contrasena_hash = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.correo


# ===========================
#       TRABAJADORES
# ===========================

class Trabajador(models.Model):
    id_trabajador = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    titulo_profesional = models.CharField(max_length=150, blank=True, null=True)
    acerca_de_mi = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    disponibilidad = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno or ''}".strip()


# ===========================
#    TIPO TRABAJO / HABILIDADES
# ===========================

class TipoTrabajo(models.Model):
    nombre_tipo = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_tipo


class Habilidad(models.Model):
    nombre_habilidad = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre_habilidad


class TrabajadorHabilidad(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    habilidad = models.ForeignKey(Habilidad, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('trabajador', 'habilidad')


# ===========================
#      HISTORIAL LABORAL
# ===========================

class HistorialLaboral(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    empresa = models.CharField(max_length=150)
    puesto = models.CharField(max_length=150)
    fecha_inicio = models.CharField(max_length=20)
    fecha_fin = models.CharField(max_length=20, null=True, blank=True)


# ===========================
#        POSTULACIONES
# ===========================

class Postulacion(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    usuario_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_trabajo = models.ForeignKey(TipoTrabajo, on_delete=models.SET_NULL, null=True)
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estado_solicitud = models.CharField(max_length=100, null=True, blank=True)


# ===========================
#      PAGOS Y RECIBOS
# ===========================

class MetodoPago(models.Model):
    metododepago = models.CharField(max_length=100)

    def __str__(self):
        return self.metododepago


class Pago(models.Model):
    postulacion = models.OneToOneField(Postulacion, on_delete=models.CASCADE)
    metododepago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    monto = models.FloatField()
    fecha_pago = models.DateTimeField(auto_now_add=True)


class Recibo(models.Model):
    pago = models.OneToOneField(Pago, on_delete=models.CASCADE)
    ruta_archivo_recibo = models.CharField(max_length=255, blank=True, null=True)


# ===========================
#          BANEOS
# ===========================

class Baneo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.CharField(max_length=20)
    fecha_fin = models.CharField(max_length=20, null=True, blank=True)
    motivo = models.TextField(null=True, blank=True)


# ===========================
#          REPORTES
# ===========================

class Reporte(models.Model):
    usuario_reporta = models.ForeignKey(Usuario, related_name='reporta', on_delete=models.CASCADE)
    usuario_reportado = models.ForeignKey(Usuario, related_name='reportado', on_delete=models.SET_NULL, null=True)
    entidad_reportada = models.IntegerField(null=True, blank=True)
    tipo_entidad = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(auto_now_add=True)


# ===========================
#          TICKETS
# ===========================

class Tickets(models.Model):
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    asunto = models.CharField(max_length=255)
    estado_solicitud = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
