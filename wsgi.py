from app import app
from app.utils import commands, config, login, logger
from app.domain import schemas, models, service
from app.data import repos
from app.data import CRUD
from app.resources import route
from app import exceptions

if __name__ == "__main__":
    app.run()

