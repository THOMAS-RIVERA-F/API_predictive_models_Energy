import random
from sqlalchemy.orm import Session
from models import ConsumptionEntry, UserInfo
import database


def update_consumption_entries_with_new_user_ids(db: Session):
    """Actualiza las entradas de consumo con nuevos user_id de UserInfo."""
    # Obtener todos los nuevos user_id de UserInfo
    new_user_ids = db.query(UserInfo.user_id).all()
    new_user_ids = [user_id[0] for user_id in new_user_ids]  # Extraer el ID de la tupla

    # Obtener todas las entradas de consumo
    entries = db.query(ConsumptionEntry).all()
    for entry in entries:
        # Seleccionar un nuevo user_id aleatorio
        entry.user_id = random.choice(new_user_ids)

    db.commit()  # Guardar los cambios en la base de datos


if __name__ == "__main__":
    db_session = next(database.get_db())  # Obtén la sesión de base de datos
    try:
        update_consumption_entries_with_new_user_ids(db_session)  # Actualiza las entradas de consumo
        print("Entradas de consumo actualizadas con nuevos user_id.")
    finally:
        db_session.close()  # Asegúrate de cerrar la sesión
