import allure
import pytest

from core.pages.main_page import MainPage


class BaseTest:
    driver = None

    @classmethod
    def setup_class(cls):
        cls.main_page = MainPage(cls.driver)

    def attach_screenshot(self, function_name):
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=function_name,
                      attachment_type=allure.attachment_type.PNG)
