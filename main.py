from db.controller import Controller
from settings import DB_URI, VERBOSE
import httpx
from bs4 import BeautifulSoup

from pprint import pprint


def init() -> Controller:
    controller = Controller(DB_URI, VERBOSE)
    controller.destroy_db()
    controller.create_db()
    return controller


if __name__ == '__main__':

    # logger = get_logger(__name__)

    # controller = init()

    resp = httpx.get('https://novosibirsk.hh.ru/vacancies/middle-python-developer')

    if resp.is_success:
        # pprint(dir(resp))
        # pprint(resp.content.decode())
        soup = BeautifulSoup(resp.content.decode(), 'lxml')
        # print(soup.prettify())
        # print(dir(soup))
        res = soup.find('div', attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_standard'})
        print(res.prettify())
