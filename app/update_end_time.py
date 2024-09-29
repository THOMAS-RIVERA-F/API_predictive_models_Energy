import random
from datetime import timedelta
from sqlalchemy.orm import Session
from models import ConsumptionEntry
import database


def update_end_time(db: Session):
    """Actualiza el end_time para que sea mayor que start_time por entre 1h y 23h."""
    # Obtener todas las entradas de consumo
    entries = db.query(ConsumptionEntry).all()
    
    for entry in entries:
        # Calcular un tiempo aleatorio entre 1 y 23 horas
        random_hours = random.randint(1, 23)
        # Establecer end_time como start_time más el tiempo aleatorio
        entry.end_time = entry.start_time + timedelta(hours=random_hours)

    db.commit()  # Guardar los cambios en la base de datos


if __name__ == "__main__":
    db_session = next(database.get_db())  # Obtén la sesión de base de datos
    try:
        update_end_time(db_session)  # Actualiza el end_time
        print("end_time actualizado para todas las entradas de consumo.")
    finally:
        db_session.close()  # Asegúrate de cerrar la sesión
