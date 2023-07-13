from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Vacancy(Base):
    __tablename__ = 'vacancy'

    _id = Column(BigInteger, autoincrement=True, primary_key=True) #Serial??
    company_name = Column(String(255), ForeignKey('company.name'))
    position = Column(String(1024), nullable=False)
    job_description = Column(String)
    key_skills = Column(String(255), ForeignKey('skill.name'))


class Skill(Base):
    __tablename__ = 'skill'

    _id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String(1024), nullable=False, unique=True)
    vacancies = relationship('Vacancy')


class Company(Base):
    __tablename__ = 'company'

    _id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String(1024), nullable=False, unique=True)
    vacancies = relationship('Vacancy')
