import json
import time
from datetime import datetime

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from global_vars.paths import BASE_ROOT_PATH
from tests.test_base import BaseTest
from utilities import api_util


class TestMainPage(BaseTest):
    driver = None

    @pytest.mark.tags("ui")
    @pytest.mark.parametrize("category", ["business"])
    def test_news_page(self, category):
        self.main_page.business.is_present()
        time.sleep(2)
        self.main_page.business.click()
        carousel_data = {}
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(2)
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
                carousel_data.update({f"carousel_{index}": {"name": headline_text,
                                                            "description": link, "price": updated_time,
                                                            'item_type': 'Logitech-1'}})
            print(carousel_data)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            if carousel_data:
                with open(BASE_ROOT_PATH / f"temp_data/{category}.json", "w") as fp:
                    json.dump(carousel_data, fp)
            created_ids = []
            for page_data in carousel_data.values():
                created_id = api_util.post_item(**page_data)
                created_ids.append(created_id)
                response = api_util.get_item(created_id)
                response.pop("id")
                assert response == page_data

