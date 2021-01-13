import os
import time
from pathlib import Path
from selenium.common.exceptions import (
    TimeoutException as Toe,
    WebDriverException as Wde,
    ElementClickInterceptedException as Ecie,
    ElementNotInteractableException as Enie,
    StaleElementReferenceException as Sere,
    UnexpectedAlertPresentException as Uape,)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from app.src.settings import BASE_URL
from app.src import exception as exp
from app.src.settings import TIMEOUT


def open_page(browser, url='', full=False):
    if full:
        browser.get(url)
    else:
        browser.get(BASE_URL + url)


def page_title(browser, *titles, timeout=15):
    wait = WebDriverWait(browser, timeout)
    for title in titles:
        try:
            wait.until(lambda x: title == x.title)
            return True
        except (Toe, Uape):
            continue
    message = f'{titles} is/are not in {browser.title}'
    raise Toe(message)


class BasePage:

    # WAIT = '//div[@class="Select-menu-outer"]'

    def __init__(self, browser):
        self.browser = browser

    def close_tab(self):
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def text_on_page(self, text, timeout=30):
        wait = WebDriverWait(self.browser, timeout)
        try:
            msg = f'Text "{text}" is not displayed on the page'
            loc = '//*[contains(text(), "%s")]' % text
            wait.until(lambda x: x.find_element_by_xpath(loc), msg)
            return True
        except Toe:
            raise

    def no_text_on_page(self, text, timeout=15):
        locator = '//*[contains(text(), "%s")]' % text
        return self.absence_element(locator, timeout)

    def get_text(self, locator, lower=False, timeout=TIMEOUT):
        for _ in range(3):
            try:
                text = self.element(locator, timeout=timeout).text
                return text.lower() if lower else text
            except Sere:
                time.sleep(3)

    def fetch_attribute(self, locator, attr, timeout=TIMEOUT):
        return self.element(locator, timeout=timeout).get_attribute(attr)

    def text_of_elements(self, locator, timeout=TIMEOUT):
        elems = self.elements(locator, timeout=timeout)
        return [el.text for el in elems]

    def text_in_attribute(self, locator, text, attribute):
        # checking if text (e.g. "helloworld") is present in attribute ("src")
        # e.g: <img src="helloworld.jpg">

        attribute_value = self.element(locator).get_attribute(attribute)
        if text in attribute_value:
            return True
        else:
            raise ValueError(f'{text} is not in {attribute_value}')

    def check_logo(self, locator, image):
        return self.text_in_attribute(locator, image[:-4], 'src')

    def clear_field(self, locator):
        counter = 0
        while counter < 10:
            value = self.fetch_attribute(locator, 'value')
            if len(value) > 0:
                self.enter_text(locator, Keys.CONTROL + 'a')
                self.enter_text(locator, Keys.DELETE)
                self.element(locator).clear()
                return self
            else:
                time.sleep(1)
                counter += 1
        raise ValueError(f'This element {locator} should have some value')

    def enter_text_via_js(self, locator, text):
        # TODO: seems not needed
        self.browser.execute_script(f'arguments[0].value="{text}"', self.element(locator))

    def attach_item(self, locator, path, name):
        # base functionality for attaching images, pdf, xls

        path = path if path.startswith('/') else '/' + path
        path_to_file = f'{os.getcwd()}{Path(path, name)}'
        self.enter_text(locator, path_to_file)

    def refresh_to_find(self, locator, timeout=10, times=3):
        counter = 0
        while counter < times:
            try:
                return self.element(locator, timeout=timeout)
            except Toe:
                counter += 1
                self.browser.refresh()
        raise Toe(msg=f'Element {locator} not found')

    def refresh_not_to_find(self, locator, timeout=10, times=3):
        counter = 0
        while counter < times:
            try:
                return self.absence_element(locator, timeout=timeout)
            except exp.ElementFoundException:
                counter += 1
                self.browser.refresh()
        raise exp.ElementFoundException(f'Unexpected element is present: {locator}')

    # def choose_item_from_list(self, locator, value, to_wait=WAIT):
    #     # example: city/country while creating demand
    #
    #     self.enter_text(locator, Keys.DELETE)
    #     self.enter_text(locator, value)
    #     self.text_in_element(to_wait, value)
    #     self.enter_text(locator, Keys.ENTER)

    def element(self, locator, timeout=TIMEOUT):
        """
            Function returns web element if it is in DOM, visible and
            displayed; otherwise TimeoutException will be thrown.
                -- locator: XPATH locator of element
                -- timeout: time to trying to wait element
        """

        message = f'Element not found: {locator}'
        wait = WebDriverWait(self.browser, timeout, ignored_exceptions=Sere)
        try:
            return wait.until(lambda x: x.find_element_by_xpath(locator),
                              message)
        except Toe:
            raise

    def elements(self, locator, timeout=TIMEOUT):
        message = f'Elements not found: {locator}'
        wait = WebDriverWait(self.browser, timeout, ignored_exceptions=Sere)
        try:
            return wait.until(lambda x: x.find_elements_by_xpath(locator),
                              message)
        except Toe:
            raise

    def text_in_element(self, locator, text, timeout=TIMEOUT):

        wait = WebDriverWait(self.browser, timeout, ignored_exceptions=Sere)
        try:
            wait.until(
                ec.text_to_be_present_in_element((By.XPATH, locator), text),
                f'Element {locator} does not have text {text}')
            return self.get_text(locator)
        except Toe:
            raise

    def absence_element(self, locator, timeout=15):
        # Returns true if element is not visible or not found

        wait = WebDriverWait(self.browser, timeout, ignored_exceptions=Sere)
        try:
            wait.until_not(lambda x: x.find_element_by_xpath(locator).is_displayed())
            return True
        except Toe:
            raise exp.ElementFoundException(f'Unexpected element is present: {locator}')

    def click(self, locator, locator_to_wait=None, timeout=10, duration=35):
        # tries to click on web element
        # if exception appears, wait 1 sec and try to click again
        # total waiting time = duration

        start_time = time.time()
        while True:
            try:
                if locator_to_wait:
                    self.element(locator, timeout).click()
                    self.element(locator_to_wait, timeout=timeout)
                else:
                    self.element(locator, timeout).click()
                break
            except (Wde, Ecie, Toe):
                if time.time() < start_time + duration:
                    time.sleep(1)
                else:
                    raise

    def enter_text(self, locator, keys, timeout=TIMEOUT):
        start_time = time.time()
        while True:
            try:
                return self.element(locator).send_keys(keys)
            except (Enie, Wde, Sere):
                if time.time() < start_time + timeout:
                    time.sleep(1)
                else:
                    raise

    def switch_to_iframe(self, web_element):
        self.browser.switch_to.frame(web_element)

    def current_url(self):
        return self.browser.current_url
