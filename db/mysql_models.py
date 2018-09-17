# coding: utf-8


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, Integer, Date, Float, BLOB

Base = declarative_base()


class CodeProxy(Base):

    __tablename__ = "proxy"

    id = Column(BigInteger, primary_key=True)
    photo = Column(BLOB)
    identify_code = Column(String(10))
    req_time = Column(Float)
    plat = Column(String(20))
    created = Column(BigInteger)


    def __init__(self, data):

        self.photo = data.get("photo")
        self.identify_code = data.get("identify_code", "")
        self.req_time = data.get("req_time", None)
        self.plat = data.get("plat", "")
        self.created = data.get("created")