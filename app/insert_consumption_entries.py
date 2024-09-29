import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import ConsumptionEntry, UserInfo
import database
import uuid

def insert_consumption_entries(db: Session):
    """Inserta 70 registros en ConsumptionEntry según las condiciones en UserInfo."""
    
    # Filtrar los usuarios que cumplen las condiciones
    eligible_users = db.query(UserInfo).filter(
        (UserInfo.number_occupant_living >= 3) |
        (UserInfo.energy_behavior == "Intensivo")
    ).all()

    if not eligible_users:
        print("No se encontraron usuarios elegibles.")
        return

    # Insertar 10 registros
    for _ in range(10):
        user = random.choice(eligible_users)  # Selecciona un usuario elegible
        start_time = datetime.now() - timedelta(days=random.randint(0, 30))
        end_time = start_time + timedelta(hours=random.randint(1, 23))
        
        new_entry = ConsumptionEntry(
            id=str(uuid.uuid4()),
            user_id=user.user_id,
            consumption_value=round(random.uniform(1.0, 100.0), 2),
            start_time=start_time,
            end_time=end_time,
            device_id=str(uuid.uuid4())  # Puedes ajustar el device_id
        )
        db.add(new_entry)

    db.commit()
    print("70 registros insertados en ConsumptionEntry.")

if __name__ == "__main__":
    db_session = next(database.get_db())
    try:
        insert_consumption_entries(db_session)
    finally:
        db_session.close()


'''
if device:
        if ("Refrigerador" or "Televisor" or "Computadora") in device.name:
            return CONSUMPTION_RATES["bajo_consumo"]
        elif ("Horno microondas" or "Lavadora") in device.name:
            return CONSUMPTION_RATES["consumo_moderado"]
        elif ("Secadora" or "Aire acondicionado" or "Calefactor eléctrico") in device.name:
            return CONSUMPTION_RATES["alto_consumo"]
    return (1.0, 2.0)  # Valor por defecto si no se encuentra el dispositivo
'''