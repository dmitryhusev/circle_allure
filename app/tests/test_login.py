import pytest
from app.src.pages.base import open_page
from app.src.pages.signin import SigninPage
from app.src.settings import USER_EMAIL, USER_PASSWORD


@pytest.mark.smoke
def test_login(browser):
    open_page(browser)
    page = SigninPage(browser)
    page.enter_email(USER_EMAIL)
    page.enter_password(USER_PASSWORD)
    page.click_login()
    assert page.text_on_page(USER_EMAIL)
