import allure
import pytest

from core.pages.india_page import IndiaPage
from core.pages.main_page import MainPage
from core.pages.sports_page import SportsPage


class BaseTest:
    driver = None

    @classmethod
    def setup_class(cls):
        cls.main_page = MainPage(cls.driver)
        cls.sports_page = SportsPage(cls.driver)
        cls.india_page = IndiaPage(cls.driver)

    def attach_screenshot(self, function_name):
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=function_name,
                      attachment_type=allure.attachment_type.PNG)
