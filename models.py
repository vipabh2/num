from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# إعداد قاعدة بيانات PostgreSQL
DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/num"
engine = create_engine(DATABASE_URL)

BASE = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SESSION = SessionLocal()

class Whisper(BASE):
    __tablename__ = "whispers"
    whisper_id = Column(String(255), primary_key=True)
    sender_id = Column(String(255))
    username = Column(String(255))
    message = Column(String(255))

    def __init__(self, whisper_id, sender_id, username, message):
        self.whisper_id = whisper_id
        self.sender_id = sender_id
        self.username = username
        self.message = message

BASE.metadata.create_all(bind=engine)

def store_whisper(whisper_id, sender_id, username, message):
    whisper = Whisper(whisper_id=whisper_id, sender_id=sender_id, username=username, message=message)
    SESSION.add(whisper)
    SESSION.commit()

def get_whisper(whisper_id):
    whisper = SESSION.query(Whisper).filter(Whisper.whisper_id == whisper_id).first()
    return whisper
