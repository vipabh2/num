from sqlalchemy import Column, Integer, String
from db import BASE, SESSION, engine
class AljokerLink(BASE):
    __tablename__ = "aljoker_links"
    key = Column(String(255), primary_key=True)
    url = Column(String(255))

    def __init__(self, key, url):
        self.key = str(key)
        self.url = str(url)

AljokerLink.__table__.create(bind=engine, checkfirst=True)

def get_link(key):
    link = SESSION.query(AljokerLink).get(str(key))
    return link.url if link else None
def add_link(key, url):
    existing_link = SESSION.query(AljokerLink).filter_by(key=key).first()
    if existing_link:
        existing_link.url = url 
        SESSION.commit()
    else:
        new_link = AljokerLink(key=key, url=url)
        SESSION.add(new_link)
        SESSION.commit()

def delete_link(key):
    link = SESSION.query(AljokerLink).get(str(key))
    if link:
        SESSION.delete(link)
        SESSION.commit()
