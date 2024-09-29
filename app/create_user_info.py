import random
import uuid
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, UserInfo
from database import get_db  # Asegúrate de que este import sea correcto

# Conexión a la base de datos
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)

# Crear la tabla UserInfo
Base.metadata.create_all(engine)

def generate_random_user_info():
    energy_behaviors = ["Conservador", "Eficiente", "Moderado", "Intensivo"]
    housing_types = [
        "Apartamento", 
        "Casa Unifamiliar (1 piso)", 
        "Casa Unifamiliar (2 pisos)", 
        "Casa Unifamiliar (3 pisos o más)", 
        "Duplex", 
        "Casa Rural", 
        "Finca"
    ]
    
    return UserInfo(
        user_id=str(uuid.uuid4()),  # Genera un UUID4 para el user_id
        energy_behavior=random.choice(energy_behaviors),
        number_occupant_living=random.randint(1, 4),
        housing_type=random.choice(housing_types)
    )

def fill_user_info_table(db_session, num_records=100):
    """Llena la tabla UserInfo con datos aleatorios."""
    for _ in range(num_records):
        random_user_info = generate_random_user_info()
        db_session.add(random_user_info)
    
    db_session.commit()

if __name__ == "__main__":
    db_session = next(get_db())  # Obtener la sesión de la base de datos
    try:
        fill_user_info_table(db_session, num_records=50)  # Llena la tabla con 50 registros
        print("Datos aleatorios insertados con éxito.")
    finally:
        db_session.close()
