from typing import Dict, Generator

from bs4 import BeautifulSoup as Soup, Tag
import httpx

from settings import (
    COMPANY_LINK_ATTR, COMPANY_LINK_ATTR_ALT, DESCR_LINK_ATTR,
    POSITION_LINK_ATTR, SKILLS_LINK_ATTR, VACANCY_COUNT_ATTR,
    VACANCY_LIST_ATTR,
)


class Vacancy:
    """
    """

    def __init__(self, tag: Tag, client: httpx.Client):
        self.tag = tag
        self.client = client
        self.description = ''
        self.key_skills = []

    def _fill(self):
        position_link = self.tag.find(**POSITION_LINK_ATTR)
        url = position_link['href']
        self.position = position_link.getText()
        self.company_name = (self.tag.find(**COMPANY_LINK_ATTR)
                             or self.tag.find(**COMPANY_LINK_ATTR_ALT)).text
        resp = self.client.get(url)

        if resp.status_code != 200:
            return

        soup = Soup(resp.content.decode(), 'lxml')
        description_tag = soup.find(**DESCR_LINK_ATTR)
        skills_tag = soup.find(**SKILLS_LINK_ATTR)

        if description_tag:
            self.description = ''.join(list(map(
                lambda x: x.text if x else '', description_tag.contents,
                )))

        if skills_tag:
            self.key_skills = list(map(
                lambda x: {'name': x.text}, skills_tag.contents,
                ))

    def to_dict(self) -> Dict[str, str]:
        self._fill()
        return {
            'position': self.position,
            'company_name': self.company_name,
            'job_description': self.description,
            'key_skills': self.key_skills,
        }


class VacancySearchPage:
    """
    """

    def __init__(self, page: str, client: httpx.Client):
        self.page = page
        self.client = client
        self._fill()

    def _fill(self):
        self.soup = Soup(self.page, 'lxml')
        self.count = int(self.soup.find(**VACANCY_COUNT_ATTR).contents[0])

    def to_list(self) -> Generator[Dict[str, str], None, None]:
        for vacancy_tag in self.soup.find_all(**VACANCY_LIST_ATTR):
            yield Vacancy(vacancy_tag, self.client).to_dict()
