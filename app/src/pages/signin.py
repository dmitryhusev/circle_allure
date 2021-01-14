from app.src.pages import base


class SigninPage(base.BasePage):

    EMAIL = '//*[@name="email"]'
    PASSWORD = '//*[@name="password"]'
    LOGIN = '//*[@type="submit"]'

    def enter_email(self, email):
        self.enter_text(self.EMAIL, email)

    def enter_password(self, password):
        self.enter_text(self.PASSWORD, password)

    def click_login(self):
        self.click(self.LOGIN)
