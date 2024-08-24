import pytest

from core.pages.main_page import MainPage


class BaseTest:

    @classmethod
    def setup_class(cls):
        cls.main_page = MainPage(pytest.driver)
