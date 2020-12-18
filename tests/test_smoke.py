import pytest
from selenium import webdriver
from screen import make_attachment


@pytest.fixture
def browser():
    url = 'http://165.22.87.231:4444/wd/hub'
    capabilities = {
        'browserName': 'firefox',
        'version': '80',
        'enableVNC': True
    }
    driver = webdriver.Remote(url, capabilities)
    driver.set_window_size(1920, 1080)
    yield driver
    driver.quit()


@pytest.mark.smoke
def test_smoke_1(browser):
    browser.get('https://pytest-html.readthedocs.io/en/latest/user_guide.html')
    make_attachment(browser)
    assert 1


@pytest.mark.smoke
def test_smoke_2(browser):
    browser.get('https://alib.com.ua')
    make_attachment(browser)
    assert 0
