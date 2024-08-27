import time

import pytest

from tests.test_base import BaseTest


class TestMainPage(BaseTest):

    @pytest.mark.tags("ui", "prod", "staging", "test")
    def test_form_send(self):
        self.main_page.pop_up_close.click()
        self.main_page.pop_up_close.is_not_present()
        self.main_page.name.send_keys("Fury of Gods")
        self.main_page.email.send_keys("joker@gmail.com")
        time.sleep(5)
        self.main_page.send_button.click()
        assert self.main_page.submit_success.is_present(timeout=20)
        self.attach_screenshot(self.test_form_send.__name__)

    @pytest.mark.tags("ui", "test")
    def test_county_list(self):
        self.main_page.county_iframe.scroll_to_view()
        time.sleep(10)
        self.main_page.county_iframe.switch_to_frame()
        self.main_page.county_dropdown.click()
        time.sleep(10)
        assert self.main_page.county_list.get_array_len == 50
        self.main_page.county_iframe.switch_to_default_content()
