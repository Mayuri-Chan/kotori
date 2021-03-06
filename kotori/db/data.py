import threading

from kotori import BASE, SESSION
from sqlalchemy import Column, BigInteger, Integer, String, UnicodeText

class GDData(BASE):
	__tablename__ = "gd_data"
	_id = Column(Integer, primary_key=True, autoincrement=True)
	user_id = Column(BigInteger)
	file_id = Column(UnicodeText)
	file_name = Column(UnicodeText)
	time = Column(BigInteger)

	def __init__(self,user_id,file_id,file_name,time):
		self.user_id = user_id
		self.file_id = file_id
		self.file_name = file_name
		self.time = time

	def __repr__(self):
		return "<GDData '%s'>" % (self.user_id)

GDData.__table__.create(checkfirst=True)

GDDATA_INSERTION_LOCK = threading.RLock()

def add_to_gddata(user_id,file_id,file_name,time):
	with GDDATA_INSERTION_LOCK:
		gddata_filt = GDData(user_id,file_id,file_name,time)
		SESSION.merge(gddata_filt)
		SESSION.commit()

def get_data(user_id,lim,offs):
	return SESSION.query(GDData).filter(GDData.user_id==user_id).order_by(GDData._id.desc()).offset(offs).limit(lim).all()

def count_data(user_id):
	return len(SESSION.query(GDData).filter(GDData.user_id==user_id).all())

def get_file(file_id):
	try:
		return SESSION.query(GDData).filter(GDData.file_id == file_id).all()
	finally:
		SESSION.close()

def delete_from_gddata(file_id):
	data = get_file(file_id)
	if data:
		for x in data:
			SESSION.delete(x)
			SESSION.commit()
		return True
	return False

def get_all():
        try:
                return SESSION.query(GDData).all()
        finally:
                SESSION.close()

def check_file(file_name):
	try:
		return SESSION.query(GDData).filter(GDData.file_name == file_name).all()
	finally:
		SESSION.close()
