from datetime import datetime

import allure
import pytest
import yaml
from appium import webdriver as appium_web_driver
from appium.options.android import UiAutomator2Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from core.constants import APPIUM_SERVER_URL
from global_vars.paths import BASE_ROOT_PATH
from utilities.custom_parser import AllureEnvironmentParser

TEST_CONFIG = BASE_ROOT_PATH / 'test_config.yaml'


def pytest_configure():
    pytest.driver = pytest.browser = pytest.base_url = None


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="browser that the automation will run in",
                     choices=("chrome", "firefox", "chrome_headless"))
    parser.addoption("--env", action="store", default="test",
                     help="test environment name",
                     choices=("prod", "staging", "test"))
    parser.addoption("--mobile", action="store_true", help="use mobile user-agent")


@pytest.fixture(autouse=True)
# fetch browser kind and base url then writes a dictionary of key-value pair into allure's environment.properties file
def write_allure_environment(request):
    yield
    allure_report_dir = request.config.option.allure_report_dir
    if allure_report_dir:
        caps = request.cls.driver.caps
        driver_info = list(caps[caps['browserName']].items())[0]
        AllureEnvironmentParser(allure_report_dir).update_allure_env(
            {"Browser": caps['browserName'], "Browser-Version": caps['browserVersion'],
             "Driver-Version": driver_info[1],
             "Environment": request.config.option.env,
             "Platform": caps['platformName']}
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object

    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="class")
def driver(request):
    browser = request.config.option.browser
    env = request.config.option.env
    is_mobile = request.config.option.mobile
    with open(TEST_CONFIG, 'r') as fd:
        test_config = yaml.load(fd, Loader=yaml.loader.SafeLoader)
    if browser == "firefox":
        selenium_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser == "chrome_headless":
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        if is_mobile:
            # iphoneX emulation
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "
                             "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
            }
            opts.add_experimental_option("mobileEmulation", mobile_emulation)
        selenium_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                           options=opts)
    else:
        opts = webdriver.ChromeOptions()
        if is_mobile:
            # iphoneX emulation
            mobile_emulation = {
                "deviceMetrics": {"width": 375, "height": 812, "pixelRatio": 3.0},
                "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) "
                             "AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
            }
            opts.add_experimental_option("mobileEmulation", mobile_emulation)
        selenium_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opts)
    selenium_driver.implicitly_wait(5)
    selenium_driver.maximize_window()
    selenium_driver.get(test_config[env]["test_url"])
    # Get performance Timing
    nav_start_time = selenium_driver.execute_script("return window.performance.timing.navigationStart")
    resp_time = selenium_driver.execute_script("return window.performance.timing.responseStart")
    dom_complete_time = selenium_driver.execute_script("return window.performance.timing.domComplete")
    # calculate performance
    backend_perf = resp_time - nav_start_time
    frontend_perf = dom_complete_time - resp_time
    print(f"Front-end performance: {frontend_perf} ms")
    print(f"Back-end performance: {backend_perf} ms")
    request.cls.driver = selenium_driver


@pytest.fixture(scope="class")
def appium_driver(request):
    # caps created for Android Pixel 8 - with sample app package name
    capabilities = dict(
        platformName='Android',
        automationName='uiautomator2',
        deviceName='Pixel_8_API_35 [emulator-5554]',
        appPackage='com.sample.helloworld',  # app package name
        appActivity='.MainActivity',
        language='en',
        locale='US'
    )
    appium_webdriver = appium_web_driver.Remote(APPIUM_SERVER_URL,
                                                options=UiAutomator2Options().load_capabilities(capabilities))
    request.cls.driver = appium_webdriver


@pytest.fixture(scope="function", autouse=True)
def check_if_failed(request):
    yield
    # request.node is an "item" because we use the default
    # "function" scope
    if request.node.rep_setup.failed:
        print("setting up a test failed!", request.node.nodeid)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            file_name = f'{request.node.nodeid}_{datetime.today().strftime("%Y-%m-%d_%H:%M")}.png'
            file_name = file_name.replace("/", "_").replace("::", "__")
            allure.attach(request.cls.driver.get_screenshot_as_png(),
                          name=file_name,
                          attachment_type=allure.attachment_type.PNG)
            print("executing test failed", request.node.nodeid)
