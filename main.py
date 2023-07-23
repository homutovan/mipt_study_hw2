import asyncio
from tqdm.contrib.logging import logging_redirect_tqdm
from typing import Generator, Callable

from db.controller import Controller
from settings import DB_URI, VERBOSE
from scraper import scrap_on_query
from api_extractor import api_extractor
from async_api_extractor import async_api_extractor
from validators import Vacancy, Company
from utils import get_logger


def init() -> Controller:
    controller = Controller(DB_URI, VERBOSE)
    controller.destroy_db()
    controller.create_db()
    return controller


def task(generator: Generator) -> Callable:
    def task_by_gen(query: str, controller: Controller):
        for item in generator(query):
            controller.add_company([Company(**item).model_dump()])
            controller.add_vacancy([Vacancy(**item).model_dump()])

    return task_by_gen

async def async_task_2(query: str, controller: Controller):
    async for item in async_api_extractor(query):
        controller.add_company([Company(**item).model_dump()])
        controller.add_vacancy([Vacancy(**item).model_dump()])


task_1 = task(scrap_on_query)
task_2 = task(api_extractor)

if __name__ == '__main__':

    logger = get_logger(__name__)

    query = 'middle python developer'

    with logging_redirect_tqdm():
        logger.info('execution started')
        try:

            controller = init()
            task_1(query, controller)
            task_2(query, controller)
            asyncio.run(async_task_2(query, controller))

        except KeyboardInterrupt:
            logger.info('execution interrupted by user')

        finally:
            logger.info('execution stopped')

