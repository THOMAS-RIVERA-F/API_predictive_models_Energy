import uuid  # Colocamos este import primero como es un estándar
from sqlalchemy import Column, DECIMAL, TIMESTAMP, Integer, String
from sqlalchemy.dialects.mysql import CHAR
from database import Base

class ConsumptionEntry(Base):
    """Modelo que representa una entrada de consumo."""
    __tablename__ = "ConsumptionEntries"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID como CHAR(36)
    user_id = Column(CHAR(36), nullable=False)
    consumption_value = Column(DECIMAL(10, 2), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    device_id = Column(CHAR(36), nullable=False)
    
    def __str__(self):
        return f"{self.user_id} - {self.consumption_value} - {self.start_time} - {self.end_time} - {self.device_id}"

class ConsumptionDevice(Base):
    """Modelo que representa un dispositivo de consumo."""
    __tablename__ = "ConsumptionDevices"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(CHAR(200), nullable=False)
    level_consumption = Column(String(50), nullable=True)  # Nueva columna para el nivel de consumo

class UserInfo(Base):
    """Modelo que representa información del usuario."""
    __tablename__ = 'UserInfo'

    user_id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID como CHAR(36)
    energy_behavior = Column(String(50), nullable=False)
    number_occupant_living = Column(Integer, nullable=False)
    housing_type = Column(String(100), nullable=False)