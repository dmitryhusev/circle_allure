import pytest
from screen import make_attachment


@pytest.mark.smoke
def test_smoke_1(browser):
    browser.get('https://pytest-html.readthedocs.io/en/latest/user_guide.html')
    make_attachment(browser)
    assert 1


@pytest.mark.smoke
def test_smoke_2(browser):
    browser.get('https://alib.com.ua')
    make_attachment(browser)
    assert 1
