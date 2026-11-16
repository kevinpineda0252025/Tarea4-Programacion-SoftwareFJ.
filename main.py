from src.logger import configurar_logger
from src.entidades import Cliente
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.reservas import Reserva
from src.excepciones import ErrorSistemaFJ

def ejecutar_simulacion():
    logger = configurar_logger()
    logger.info("=== INICIO DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ ===")

    clientes = []
    servicios = []
    reservas = []

    print("\n--- 1. GESTIÓN DE CLIENTES ---")
    try:
        c1 = Cliente("CLI-01", "Laura Gómez", "laura.gomez@email.com", "3104567890")
        clientes.append(c1)
        logger.info(f"Registrado: {c1.obtener_resumen()}")
        print(f"[OK] {c1.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.error(f"Error registrando cliente: {e}")

    try:
        c2 = Cliente("CLI-02", "Carlos Mendoza", "cmendoza@empresa.co", "3209876543")
        clientes.append(c2)
        logger.info(f"Registrado: {c2.obtener_resumen()}")
        print(f"[OK] {c2.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.error(f"Error registrando cliente: {e}")

    try:
        c_invalido1 = Cliente("CLI-03", "Andrés Ruiz", "andres_sin_arroba.com", "3001112233")
        clientes.append(c_invalido1)
    except ErrorSistemaFJ as e:
        logger.error(f"Error controlado (Cliente inválido): {e}")
        print(f"[ERROR CONTROLADO] No se creó cliente: {e}")

    try:
        c_invalido2 = Cliente("CLI-04", "Marta Díaz", "marta@correo.com", "300ABC45")
        clientes.append(c_invalido2)
    except ErrorSistemaFJ as e:
        logger.error(f"Error controlado (Cliente inválido): {e}")
        print(f"[ERROR CONTROLADO] No se creó cliente: {e}")

    print("\n--- 2. GESTIÓN DE SERVICIOS ---")
    try:
        s1 = ReservaSala("SRV-01", "Sala Innovación A", 80000, capacidad=15)
        servicios.append(s1)
        logger.info(f"Servicio creado: {s1.obtener_resumen()}")
        print(f"[OK] {s1.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.error(f"Error creando servicio: {e}")

    try:
        s2 = AlquilerEquipo("SRV-02", "Workstation Dell Precision", 35000, gama="alta")
        servicios.append(s2)
        logger.info(f"Servicio creado: {s2.obtener_resumen()}")
        print(f"[OK] {s2.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.error(f"Error creando servicio: {e}")

    try:
        s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud", 120000, especialidad="AWS / DevOps")
        servicios.append(s3)
        logger.info(f"Servicio creado: {s3.obtener_resumen()}")
        print(f"[OK] {s3.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        logger.error(f"Error creando servicio: {e}")

    try:
        s_invalido = ReservaSala("SRV-04", "Sala Fantasma", -50000, capacidad=10)
        servicios.append(s_invalido)
    except ErrorSistemaFJ as e:
        logger.error(f"Error controlado (Servicio inválido): {e}")
        print(f"[ERROR CONTROLADO] No se creó servicio: {e}")

    print("\n--- 3. GESTIÓN DE RESERVAS ---")
    try:
        r1 = Reserva("RES-01", clientes[0], servicios[0], duracion_horas=4)
        r1.procesar_reserva(logger, descuento_pct=10.0, aplicar_iva=True)
        reservas.append(r1)
        print(f"[OK] {r1.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        print(f"[ERROR CONTROLADO] {e} | Causa: {e.__cause__}")

    try:
        r2 = Reserva("RES-02", clientes[1], servicios[0], duracion_horas=2)
        r2.procesar_reserva(logger)
        reservas.append(r2)
    except ErrorSistemaFJ as e:
        print(f"[ERROR CONTROLADO] {e} | Causa: {e.__cause__}")

    try:
        r3 = Reserva("RES-03", clientes[1], servicios[1], duracion_horas=1)
        r3.procesar_reserva(logger)
        reservas.append(r3)
    except ErrorSistemaFJ as e:
        print(f"[ERROR CONTROLADO] {e} | Causa: {e.__cause__}")

    try:
        r4 = Reserva("RES-04", clientes[1], servicios[2], duracion_horas=3)
        r4.procesar_reserva(logger, descuento_pct=0.0, aplicar_iva=False)
        reservas.append(r4)
        print(f"[OK] {r4.obtener_resumen()}")

        r4.cancelar_reserva(logger)
        print(f"[OK] {r4.obtener_resumen()}")
    except ErrorSistemaFJ as e:
        print(f"[ERROR CONTROLADO] {e}")

    logger.info("=== FIN DE SIMULACIÓN DEL SISTEMA SOFTWARE FJ ===")
    print("\nSimulación finalizada sin interrupciones. Revisa 'logs/sistema.log' para ver la auditoría completa.")

if __name__ == "__main__":
    ejecutar_simulacion()
