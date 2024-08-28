import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Pixel_8_API_35 [emulator-5554]',
    appPackage='com.dharma.stepin',
    appActivity='.MainActivity',
    language='en',
    locale='US'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    # def test_find_product(self) -> None:
    #     el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Get Products"]')
    #     el.click()

    def test_get_product(self) -> None:
        value=None
        el = self.driver.find_element(by=AppiumBy.XPATH, value='//*[@text="Get Products"]')
        el.click()

        product_info = self.driver.find_elements(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')

        # actual_product=[]
        # for product in product_info:
        #     value.append(product.get_attribute('text'))
        # #     # print("product details ",value)

        i = 0
        actual_product = []
        temp_array = []
        for product in product_info:
            i += 1
            temp_array.append(product.get_attribute('text'))
            if i == 3:
                actual_product.append(temp_array)
                temp_array = []
                i = 0

        actual_list = []
        for product in actual_product:
            temp_dic = dict()
            temp_dic["name"] = product[0]
            temp_dic["description"] = product[1]
            temp_dic["price"] = product[2]
            actual_list.append(temp_dic)

        print(actual_list)


if __name__ == '__main__':
    unittest.main()