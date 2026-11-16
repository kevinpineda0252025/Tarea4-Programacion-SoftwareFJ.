class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    pass

class DatosInvalidosError(ErrorSistemaFJ):
    """Se lanza cuando los datos ingresados no cumplen con el formato o reglas."""
    pass

class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin cupo."""
    pass

class OperacionReservaError(ErrorSistemaFJ):
    """Se lanza ante cambios de estado no permitidos en una reserva."""
    pass

class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo de tarifa o descuento da un valor inválido."""
    pass
