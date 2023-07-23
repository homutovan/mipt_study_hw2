import asyncio
from typing import Dict, Generator

import httpx
from tqdm import tqdm

from settings import API_URL, RETRY, SESSION_HEADERS, TIMEOUT, VERBOSE
from validators import ResponseModel, VacancyModel


async def extract_vacancy(_id: str, client: httpx.Client) -> Dict[str, str]:
    retry = RETRY
    result = None
    while retry:
        response = await client.get(API_URL + _id)

        if response.is_error:
            await asyncio.sleep(TIMEOUT)
            retry -= 1
            continue

        else:
            result = response.json()
            break

    return result


async def async_api_extractor(
        query: str,
        ) -> Generator[Dict[str, str], None, None]:

    async with httpx.AsyncClient(headers=SESSION_HEADERS) as client:
        with tqdm(colour='red', unit='page', disable=not VERBOSE) as pbar:
            page = 0

            while True:
                resp = await client.get(API_URL, params={
                    'text': query,
                    'page': page,
                    })

                rm = ResponseModel(**resp.json())
                pbar.total = rm.pages

                if not rm.items:
                    break

                for i in rm.items:

                    result = await extract_vacancy(i.id, client)

                    if result:
                        yield VacancyModel(**result).model_dump()

                page += 1
                pbar.update(1)
