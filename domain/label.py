# domain/label.py
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base

class Label(Base):
    __tablename__ = 'labels'
    
    label_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50))
    created_at = Column(DATETIME, server_default=func.now())
    
    # Зв'язок 1:M (Один лейбл -> Багато альбомів)
    # "Album" - це назва класу
    # "label" - це назва поля 'relationship' у класі Album
    albums = relationship("Album", back_populates="label")

    def to_dict(self):
        """ Перетворює об'єкт Label на словник для JSON. """
        return {
            'label_id': self.label_id,
            'name': self.name,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None
            # 'albums' не додаємо, щоб уникнути циклу
        }