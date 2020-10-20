
from common.base_controller import BaseController
from models.user import User


class UserController(BaseController):

    def __init__(self, ctx):
        super().__init__(ctx)
        self.model = User
        return
