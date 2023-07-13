from db.controller import Controller
from settings import DB_URI, VERBOSE


def init() -> Controller:
    controller = Controller(DB_URI, VERBOSE)
    controller.destroy_db()
    controller.create_db()
    return controller


if __name__ == '__main__':

    # logger = get_logger(__name__)

    controller = init()