import random
from datetime import timedelta
from sqlalchemy.orm import Session
from models import ConsumptionEntry, ConsumptionDevice
import database


def get_consumption_rate(device_name: str) -> tuple:
    """Devuelve una tasa de consumo en kWh según el tipo de dispositivo."""
    # Definir tasas de consumo por tipo de dispositivo
    CONSUMPTION_RATES = {
        "bajo_consumo": (0.5, 1.5),    # kWh por hora
        "consumo_moderado": (1.5, 3),  # kWh por hora
        "alto_consumo": (3, 5)         # kWh por hora
    }
    
    # Asignar la tasa de consumo basada en el nombre del dispositivo
    if ("Refrigerador" or "Televisor" or "Computadora") in device_name:
        return CONSUMPTION_RATES["bajo_consumo"]
    elif ("Horno microondas" or "Lavadora") in device_name:
        return CONSUMPTION_RATES["consumo_moderado"]
    elif ("Secadora" or "Aire acondicionado" or "Calefactor eléctrico") in device_name:
        return CONSUMPTION_RATES["alto_consumo"]
    
    # Valor por defecto si no se encuentra el tipo de dispositivo
    return (1.0, 2.0)


def update_consumption_value(db: Session):
    """Actualiza el valor de consumo (consumption_value) basado en el tipo de dispositivo y tiempo de uso."""
    # Obtener todas las entradas de consumo
    entries = db.query(ConsumptionEntry).all()
    
    for entry in entries:
        # Obtener el dispositivo relacionado
        device = db.query(ConsumptionDevice).filter(ConsumptionDevice.id == entry.device_id).first()
        if device:
            # Obtener la tasa de consumo del dispositivo
            consumption_rate = get_consumption_rate(device.name)
            
            # Calcular el tiempo de uso en horas
            time_use = (entry.end_time - entry.start_time).total_seconds() / 3600  # Convertir a horas
            
            # Calcular el nuevo valor de consumo
            consumption_value = random.uniform(*consumption_rate) * time_use
            
            # Actualizar el campo consumption_value
            entry.consumption_value = round(consumption_value, 2)

    db.commit()  # Guardar los cambios en la base de datos


if __name__ == "__main__":
    db_session = next(database.get_db())  # Obtén la sesión de base de datos
    try:
        update_consumption_value(db_session)  # Actualiza los valores de consumo
        print("Valores de consumo actualizados para todas las entradas de consumo.")
    finally:
        db_session.close()  # Asegúrate de cerrar la sesión
