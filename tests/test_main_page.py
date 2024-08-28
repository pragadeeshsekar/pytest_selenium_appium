import time

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tests.test_base import BaseTest


class TestMainPage(BaseTest):
    driver = None

    @pytest.mark.tags("ui", "done")
    @pytest.mark.parametrize("category", ["india", "sports", "business"])
    def test_headlines_present(self, category):
        match category:
            case "india":
                self.main_page.india.is_present()
                self.main_page.india.click()
            case "sports":
                self.main_page.sports.is_present()
                self.main_page.sports.click()
            case "business":
                self.main_page.business.is_present()
                self.main_page.business.click()
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            assert category.title() in self.driver.title
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    @pytest.mark.tags("ui", "test")
    @pytest.mark.parametrize("category", ["india"])
    def test_headlines_present(self, category):
        match category:
            case "sports":
                self.main_page.sports.is_present()
                self.main_page.sports.click()
            case "india":
                self.main_page.india.is_present()
                self.main_page.india.click()
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            assert category.title() in self.driver.title
            for element in self.sports_page.slick_dots.native_webelements:
                action = ActionChains(self.driver)
                action.move_to_element(element).perform()
                element.click()
                print(element.find_element(By.TAG_NAME, "button").get_attribute("href"))
                self.main_page.active_carousel.click()
                print(self.main_page.updated_time.text)
                time.sleep(5)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
