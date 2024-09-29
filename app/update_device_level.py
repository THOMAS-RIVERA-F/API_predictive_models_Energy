from sqlalchemy.orm import Session
from models import ConsumptionDevice
import database

# Clasificación de electrodomésticos por nivel de consumo
appliances_consumption = {
    "Refrigerador": "bajo consumo",
    "Lavadora": "consumo moderado",
    "Secadora": "alto consumo",
    "Aire acondicionado": "alto consumo",
    "Calefactor eléctrico": "alto consumo",
    "Televisor": "bajo consumo",
    "Computadora": "bajo consumo",
    "Horno microondas": "consumo moderado"
}

def update_device_level(db: Session):
    """Actualiza el nivel de consumo (level_consumption) para los dispositivos en la tabla ConsumptionDevices."""
    # Obtener todas las entradas de dispositivos
    devices = db.query(ConsumptionDevice).all()

    for device in devices:
        # Obtener el nivel de consumo basado en el nombre del dispositivo
        level = appliances_consumption.get(device.name, "bajo consumo")
        device.level_consumption = level  # Asignar el nivel de consumo

    db.commit()  # Guardar los cambios en la base de datos

if __name__ == "__main__":
    db_session = next(database.get_db())  # Obtén la sesión de base de datos
    try:
        update_device_level(db_session)  # Actualiza los niveles de consumo
        print("Nivel de consumo actualizado para todos los dispositivos.")
    finally:
        db_session.close()  # Asegúrate de cerrar la sesión
