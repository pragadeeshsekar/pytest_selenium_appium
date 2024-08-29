import pytest
from appium.webdriver.common.appiumby import AppiumBy

from tests.test_base import AppiumBaseTest
from utilities import api_util
from utilities.api_util import post_item


class TestMobileAppView(AppiumBaseTest):

    @pytest.mark.tags("apk")
    def test_get_product(self):
        el = self.app_driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Get Products"]')
        el.click()
        products_list = self.app_driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')
        # create empty list variable for manipulating the products details information
        products = []
        total_products = len(products_list)
        # one product contains 3 items - name, description and price
        for index in range(0, total_products, 4):
            # list index contains one product info
            products.append(products_list[index: index+4])
        print(products)
        for product in products:
            # post data to api endpoint - remove "id" from response (as it is not required for comparison)
            response = post_item(name=product[0], description=product[1], price=int(product[2][1:]),
                                 item_type="item-1")
            actual_data = api_util.get_item(response)
            actual_data.pop("id")
            expected_data = {"name": product[0], "description": product[1],
                             "price": product[2][1:], "item_type": "item-1"}
            assert actual_data == expected_data
