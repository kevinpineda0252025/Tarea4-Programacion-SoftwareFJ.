from src.entidades import EntidadBase, Cliente
from src.servicios import Servicio
from src.excepciones import (
    ErrorSistemaFJ,
    ServicioNoDisponibleError,
    OperacionReservaError,
    DatosInvalidosError
)

class Reserva(EntidadBase):
    """Integra Cliente, Servicio y duración, gestionando su ciclo de vida."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        super().__init__(id_reserva)
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("Se requiere una instancia válida de Servicio.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def procesar_reserva(self, logger, descuento_pct: float = 0.0, aplicar_iva: bool = True) -> None:
        """Procesa y confirma la reserva demostrando try/except/else/finally y encadenamiento."""
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre}' no está disponible actualmente."
                )
            self.costo_total = self.servicio.calcular_costo(
                self.duracion_horas,
                descuento_pct=descuento_pct,
                aplicar_iva=aplicar_iva
            )
        except ErrorSistemaFJ as e:
            self.estado = "RECHAZADA"
            logger.error(f"Fallo al procesar Reserva {self.id}: {e}")
            raise OperacionReservaError(f"No se pudo completar la reserva {self.id}.") from e
        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False
            logger.info(
                f"Reserva {self.id} CONFIRMADA | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Total: ${self.costo_total:,.2f}"
            )
        finally:
            logger.info(f"Auditoría finalizada para intento de reserva [{self.id}] (Estado: {self.estado}).")

    def cancelar_reserva(self, logger) -> None:
        """Cancela una reserva activa y libera el servicio."""
        try:
            if self.estado != "CONFIRMADA":
                raise OperacionReservaError(
                    f"Solo se pueden cancelar reservas CONFIRMADAS (Estado actual: {self.estado})."
                )
        except OperacionReservaError as e:
            logger.warning(f"Intento inválido de cancelación en {self.id}: {e}")
            raise
        else:
            self.estado = "CANCELADA"
            self.servicio.disponible = True
            logger.info(f"Reserva {self.id} CANCELADA. Servicio '{self.servicio.nombre}' liberado.")

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Estado: {self.estado} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} ({self.duracion_horas}h) | Total: ${self.costo_total:,.2f}"
        )
