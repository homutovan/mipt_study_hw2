from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table, BigInteger, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, relationship
from typing import List

Base = declarative_base()


# association_table = Table(
#     'association_table',
#     Base.metadata,
#     Column('vacancy_id', ForeignKey('vacancy._id')),
#     Column('skill_id', ForeignKey('skill._id')),
# )

# class Vacancy(Base):
#     __tablename__ = 'vacancy'

#     _id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
#     company_name: Mapped[str] = mapped_column(ForeignKey('company.name'))
#     position: Mapped[str] = mapped_column(nullable=False)
#     job_description: Mapped[str] = mapped_column(nullable=False)
#     key_skills: Mapped[List[Skill]] = relationship(secondary=association_table)


# class Skill(Base):
#     __tablename__ = 'skill'

#     _id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=False, unique=True)
#     vacancies: Mapped[List[Vacancy]] = relationship(secondary=association_table)


# class Company(Base):
#     __tablename__ = 'company'

#     _id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=False, unique=True)
#     vacancies: Mapped[List[Vacancy]] = relationship(back_populates='company', cascade='all, delete-orphan')

vacancy_skills = Table(
    'vacancy_skills',
    Base.metadata,
    Column('_id',BigInteger, autoincrement=True, primary_key=True),
    Column('vacancy_id', ForeignKey('vacancy._id'), primary_key=True),
    Column('skill_id', ForeignKey('skill._id'), primary_key=True),
)

class Vacancy(Base):
    __tablename__ = 'vacancy'

    _id = Column(BigInteger, autoincrement=True, primary_key=True) #Serial??
    company_name = Column(String(255), ForeignKey('company.name'))
    position = Column(String(1024), nullable=False)
    job_description = Column(String)
    key_skills = relationship('Skill', secondary=vacancy_skills, back_populates='vacancies')


class Skill(Base):
    __tablename__ = 'skill'

    _id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String(1024), nullable=False,)
    vacancies = relationship('Vacancy', secondary=vacancy_skills, back_populates='key_skills')


class Company(Base):
    __tablename__ = 'company'

    _id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(String(1024), nullable=False, unique=True)
    vacancies = relationship('Vacancy')

