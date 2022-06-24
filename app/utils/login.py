"""Flask_login setup"""

from flask_login import LoginManager
from app import app
from app.data.repos import user_repo
from app.domain.schemas import GetFromIdSchema


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return user_repo.get_with_id(GetFromIdSchema(id=user_id))
