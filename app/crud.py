import pandas as pd
from sqlalchemy.orm import Session
from models import ConsumptionEntry
import database


def get_all_consumption_data(db: Session):
    """Obtiene todos los registros de consumo de la base de datos."""
    return db.query(ConsumptionEntry).all()


if __name__ == "__main__":
    db_session = next(database.get_db())  # Obtén la sesión de base de datos
    try:
        # Obtener todos los registros de consumo
        consumptions = get_all_consumption_data(db_session)
        
        # Crear un DataFrame con las columnas device_id, user_id y valor_consumo
        data = {
            'device_id': [consumption.device_id for consumption in consumptions],
            'user_id': [consumption.user_id for consumption in consumptions],
            'valor_consumo': [consumption.consumption_value for consumption in consumptions],
        }
        
        df = pd.DataFrame(data)
        print(df)
    
    finally:
        db_session.close()  # Asegúrate de cerrar la sesión
