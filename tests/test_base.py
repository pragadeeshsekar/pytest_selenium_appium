import unittest

import allure
import pytest

from core.pages.india_page import IndiaPage
from core.pages.main_page import MainPage
from core.pages.sports_page import SportsPage


@pytest.mark.usefixtures("driver")
class SeleniumBaseTest(unittest.TestCase):
    driver = None

    @classmethod
    def setUp(cls):
        cls.selenium_driver = cls.driver
        cls.main_page = MainPage(cls.driver)
        cls.sports_page = SportsPage(cls.driver)
        cls.india_page = IndiaPage(cls.driver)

    @classmethod
    def tearDown(cls):
        cls.selenium_driver.quit()

    def attach_screenshot(self, function_name):
        allure.attach(self.selenium_driver.get_screenshot_as_png(),
                      name=function_name,
                      attachment_type=allure.attachment_type.PNG)


@pytest.mark.usefixtures("appium_driver")
class AppiumBaseTest:
    driver = None

    @classmethod
    def setup(cls):
        cls.app_driver = cls.driver

    def attach_screenshot(self, function_name):
        allure.attach(self.app_driver.get_screenshot_as_png(),
                      name=function_name,
                      attachment_type=allure.attachment_type.PNG)