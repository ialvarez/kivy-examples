from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine


Base = declarative_base()


class TimeClockEntries(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    time_stamp_in = Column(Date)
    time_stamp_out = Column(Date)


class TimeClockTable(Base):
    __tablename__ = 'time_clock'

    id = Column(Integer, primary_key=True)
    time_stamp = Column(String(128), nullable=False)
    action = Column(String(3), nullable=False)


engine = create_engine('sqlite:///time_clock.db')
Base.metadata.create_all(engine)
