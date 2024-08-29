import time
from datetime import datetime

import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from tests.test_base import SeleniumBaseTest


class TestMainPage(SeleniumBaseTest):

    @pytest.mark.tags("ui")
    def test_news_page(self):
        category = "business"
        self.main_page.business.is_present()
        time.sleep(2)
        self.main_page.business.click()
        carousel_data = {}
        if len(self.selenium_driver.window_handles) > 1:
            self.selenium_driver.switch_to.window(self.selenium_driver.window_handles[-1])
            time.sleep(2)
            assert category.title() in self.selenium_driver.title
            for index in [0, 1, 2]:
                elements = self.india_page.slick_dots.native_webelements
                ele = elements[index]
                action = ActionChains(self.selenium_driver)
                action.move_to_element(ele).perform()
                ele.click()
                element_id = ele.find_element(By.TAG_NAME, "button").get_attribute("id")
                link = self.selenium_driver.find_element(
                    By.CSS_SELECTOR, f"[aria-describedby='{element_id}'] a"
                ).get_attribute("href")
                self.main_page.active_carousel.click()
                updated_time = self.main_page.updated_time.get_text()
                date_object = datetime.strptime(updated_time, "Updated: %B %d, %Y %H:%M IST")
                updated_time = int(date_object.strftime("%d%m%Y"))
                headline_text = self.main_page.heading_title.get_text()
                self.selenium_driver.back()
                carousel_data.update({f"carousel_{index}": {"name": headline_text,
                                                            "description": link, "price": updated_time,
                                                            'item_type': 'item-1'}})
            print(carousel_data)
            self.selenium_driver.close()
