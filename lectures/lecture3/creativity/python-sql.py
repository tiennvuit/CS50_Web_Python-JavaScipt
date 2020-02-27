import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# DATABASE_URL = "tien://tiennv:tien250500@localhost:5432/lecture3"
engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))

lecturers = db.execute("SELECT * FROM giangvien").fetchall()
for lecturer in lecturers:
    print(f"{lecture.TenGV}")
