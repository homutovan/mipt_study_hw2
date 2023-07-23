# Share settings

VERBOSE = True
log_file = True
log_path = 'logs'

# DataBase settings

DB_URI = 'postgresql://postgres:postgres@localhost:15432/etl'
THRESHOLD = 20

# HH scraper settings

SOURCE_URL = 'https://novosibirsk.hh.ru/search/vacancy'

SESSION_HEADERS = {
    # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'user-agent': 'PostmanRuntime/7.31.1'
    }

ITEMS_COUNT = 20

POSITION_LINK_ATTR = {
    'name': 'a',
    'attrs': {'class': 'serp-item__title'},
}

COMPANY_LINK_ATTR = {
    'name': 'a',
    'attrs': {'class': 'bloko-link bloko-link_kind-tertiary'}, 
}

COMPANY_LINK_ATTR_ALT = {
    'name': 'div', 
    'attrs': {'class': 'vacancy-serp-item__meta-info-company'},
}

DESCR_LINK_ATTR = {
    'name': 'div',
    'attrs' :{'data-qa': 'vacancy-description'},
}

SKILLS_LINK_ATTR = {
    'name': 'div',
    'attrs': {'class': 'bloko-tag-list'},
}

VACANCY_COUNT_ATTR = {
    'name': 'h1', 
    'attrs': {'class': 'bloko-header-section-3'},
}

VACANCY_LIST_ATTR = {
    'name': 'div',
    'attrs': {'class': 'vacancy-serp-item-body__main-info'},
}


# HH api-client settings

API_URL = 'https://api.hh.ru/vacancies/'
RETRY = 5
TIMEOUT = 2

