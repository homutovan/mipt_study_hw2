from typing import Dict, Generator

import httpx
from tqdm import tqdm

from parsers import VacancySearchPage
from settings import (
    ITEMS_COUNT, SESSION_HEADERS, SOURCE_URL, VERBOSE,
)
from utils import get_logger


logger = get_logger(__name__)


def scrap_on_query(query: str) -> Generator[Dict[str, str], None, None]:

    transport = httpx.HTTPTransport(retries=5)

    with httpx.Client(headers=SESSION_HEADERS, transport=transport) as client:
        with tqdm(colour='red', unit='vacancy', disable=not VERBOSE) as pbar:

            page = 0

            while True:

                params = {
                    'text': query,
                    'page': page,
                    'items_on_page': ITEMS_COUNT,
                }
                try:
                    resp = client.get(SOURCE_URL, params=params)

                except httpx.ReadTimeout as e:
                    logger.error(e)
                    continue

                if resp.is_error:
                    break

                vacancy_page = VacancySearchPage(resp.content.decode(), client)
                pbar.total = vacancy_page.count

                for vacancy in vacancy_page.to_list():
                    pbar.update(1)
                    yield vacancy

                page += 1

    logger.info('data reading completed')
