from abc import ABC, abstractmethod
import re
from src.excepciones import DatosInvalidosError

class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad del sistema."""

    def __init__(self, id_entidad: str):
        if not id_entidad or not id_entidad.strip():
            raise DatosInvalidosError("El ID de la entidad no puede estar vacío.")
        self._id = id_entidad.strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto obligatorio para describir la entidad."""
        pass


class Cliente(EntidadBase):
    """Representa a un cliente de Software FJ con encapsulación y validaciones."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise DatosInvalidosError(f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not re.match(patron, valor.strip()):
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise DatosInvalidosError(f"Teléfono inválido: '{valor}'. Debe contener solo números (mínimo 7).")
        self._telefono = valor

    def obtener_resumen(self) -> str:
        return f"Cliente [{self.id}]: {self.nombre} | Tel: {self.telefono} | Email: {self.correo}"
