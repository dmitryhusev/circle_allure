import pytest


@pytest.mark.smoke
def test_smoke_1(browser):
    browser.get('https://pytest-html.readthedocs.io/en/latest/user_guide.html')
    assert 1


@pytest.mark.smoke
def test_smoke_2(browser):
    browser.get('https://alib.com.ua')
    assert 1
