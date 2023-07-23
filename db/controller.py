from typing import Dict, List

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from db.models import Base, Company, Skill, Vacancy
from settings import THRESHOLD
from utils import get_logger


class Driver:
    """
    """

    def __init__(self, uri: str, verbose: bool) -> None:
        self.engine = create_engine(uri, echo=verbose)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=True)
        self._data_list = []
        self.logger = get_logger(__name__)

    def create_db(self) -> None:
        Base.metadata.create_all(self.engine)

    def destroy_db(self) -> None:
        Base.metadata.drop_all(self.engine)

    def add_data(self, data: List[Base], commit=True) -> bool:
        if commit:
            return self._add_record(data)
        else:
            self._data_list.append(*data)
            if len(self._data_list) >= THRESHOLD:
                return self.commit()

            return True

    def _add_record(self, data: List[Base]) -> bool:
        try:
            with self.session_factory() as session:
                session.add_all(data)
                session.commit()

            return True
        except SQLAlchemyError as e:
            self.logger.error(e)
            return False

    def commit(self) -> bool:
        data = [*self._data_list]
        self._data_list = []
        return self._add_record(data)


class Controller(Driver):
    """
    """

    def add_company(
            self,
            data: List[Dict[str, str]],
            commit=True,
            ) -> bool:
        return self.add_data(list(map(
            lambda x: Company(**x), data)), commit=commit,
            )

    def add_vacancy(
            self,
            data: List[Dict[str, str]],
            commit=True,
            ) -> bool:
        return self.add_data([
            Vacancy(
                company_name=item['company_name'],
                position=item['position'],
                job_description=item['job_description'],
                key_skills=[
                    Skill(
                        name=skill_item['name'],
                    ) for skill_item in item['key_skills']
                ],
            ) for item in data
        ], commit=commit,
            )

    def add_skill(
            self,
            data: List[Dict[str, str]],
            commit=True,
            ) -> bool:
        return self.add_data(list(map(
            lambda x: Skill(**x), data)), commit=commit,
            )
