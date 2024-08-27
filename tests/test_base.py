import pytest

from core.pages.main_page import MainPage


class BaseTest:
    driver = None

    @classmethod
    def setup_class(cls):
        cls.main_page = MainPage(cls.driver)
