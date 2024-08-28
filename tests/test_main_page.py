import json
import time
from datetime import datetime

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from global_vars.paths import BASE_ROOT_PATH
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
                time.sleep(2)
                self.main_page.india.click()
        carousel_data = {}
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            assert category.title() in self.driver.title
            for index in [0, 1, 2]:
                elements = self.india_page.slick_dots.native_webelements
                ele = elements[index]
                action = ActionChains(self.driver)
                action.move_to_element(ele).perform()
                ele.click()
                element_id = ele.find_element(By.TAG_NAME, "button").get_attribute("id")
                link = self.driver.find_element(
                    By.CSS_SELECTOR, f"[aria-describedby='{element_id}'] a"
                ).get_attribute("href")
                self.main_page.active_carousel.click()
                updated_time = self.main_page.updated_time.get_text()
                date_object = datetime.strptime(updated_time, "Updated: %B %d, %Y %H:%M IST")
                updated_time = int(date_object.strftime("%d%m%Y"))
                headline_text = self.main_page.heading_title.get_text()
                self.driver.back()
                carousel_data.update({f"carousel_{index}": {"headline": headline_text,
                                                            "news_link": link, "updated_time": updated_time}})
            print(carousel_data)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            if carousel_data:
                with open(BASE_ROOT_PATH / f"temp_data/{category}.json", "w") as fp:
                    json.dump(carousel_data, fp)
