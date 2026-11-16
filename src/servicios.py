from abc import abstractmethod
from src.entidades import EntidadBase
from src.excepciones import DatosInvalidosError, CalculoInconsistenteError

class Servicio(EntidadBase):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if not nombre or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor a cero.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> None:
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas: int, descuento_pct: float = 0.0, aplicar_iva: bool = True) -> float:
        pass

    def _aplicar_ajustes_financieros(self, subtotal: float, descuento_pct: float, aplicar_iva: bool) -> float:
        if not (0 <= descuento_pct <= 50):
            raise CalculoInconsistenteError(f"Porcentaje de descuento no permitido: {descuento_pct}% (Máx 50%).")
        
        total = subtotal * (1 - descuento_pct / 100)
        if aplicar_iva:
            total *= 1.19
        
        if total <= 0:
            raise CalculoInconsistenteError("El costo total calculado no puede ser menor o igual a cero.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado: Alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a 0.")
        self.capacidad = capacidad

    def validar_parametros(self, duracion_horas: int) -> None:
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatosInvalidosError("Las salas solo se reservan entre 1 y 12 horas por día.")

    def calcular_costo(self, duracion_horas: int, descuento_pct: float = 0.0, aplicar_iva: bool = True) -> float:
        self.validar_parametros(duracion_horas)
        subtotal = self.tarifa_base * duracion_horas
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Sala [{self.id}] {self.nombre} (Cap: {self.capacidad} pers.) - ${self.tarifa_base}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado: Alquiler de hardware/equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, gama: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if gama.lower() not in ["estandar", "alta"]:
            raise DatosInvalidosError("La gama del equipo debe ser 'estandar' o 'alta'.")
        self.gama = gama.lower()

    def validar_parametros(self, duracion_horas: int) -> None:
        if duracion_horas < 2:
            raise DatosInvalidosError("El alquiler de equipos requiere un mínimo de 2 horas.")

    def calcular_costo(self, duracion_horas: int, descuento_pct: float = 0.0, aplicar_iva: bool = True) -> float:
        self.validar_parametros(duracion_horas)
        recargo_gama = 1.25 if self.gama == "alta" else 1.0
        subtotal = (self.tarifa_base * duracion_horas) * recargo_gama
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "En uso"
        return f"Equipo [{self.id}] {self.nombre} (Gama {self.gama}) - ${self.tarifa_base}/h [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado: Consultoría técnica o de desarrollo de software."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not especialidad or not especialidad.strip():
            raise DatosInvalidosError("Debe especificar el área de especialidad de la asesoría.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, duracion_horas: int) -> None:
        if duracion_horas <= 0 or duracion_horas > 8:
            raise DatosInvalidosError("Las sesiones de asesoría deben durar entre 1 y 8 horas.")

    def calcular_costo(self, duracion_horas: int, descuento_pct: float = 0.0, aplicar_iva: bool = True) -> float:
        self.validar_parametros(duracion_horas)
        cargo_preparacion = 20000.0
        subtotal = cargo_preparacion + (self.tarifa_base * duracion_horas)
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría [{self.id}] {self.nombre} ({self.especialidad}) - ${self.tarifa_base}/h [{estado}]"
