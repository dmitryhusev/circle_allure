import allure
from allure_commons.types import AttachmentType


def make_attachment(browser, output=None, name='custom output'):
    allure.attach(
        browser.get_screenshot_as_png(),
        'screenshot',
        AttachmentType.PNG
    )
    allure.attach(
        f'url: {browser.current_url}\ntitle: {browser.title}',
        'page url/title',
        AttachmentType.TEXT
    )
    if output:
        allure.attach(
            output,
            name,
            AttachmentType.TEXT
        )
