import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

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


@pytest.fixture(autouse=True)
# fetch browser kind and base url then writes a dictionary of key-value pair into allure's environment.properties file
def write_allure_environment(request):
    yield
    allure_report_dir = request.config.option.allure_report_dir
    if allure_report_dir:
        caps = pytest.driver.caps
        driver_info = list(caps[caps['browserName']].items())[0]
        AllureEnvironmentParser(allure_report_dir).update_allure_env(
            {"Browser": caps['browserName'], "Browser-Version": caps['browserVersion'],
             "Driver-Version": driver_info[1],
             "Environment": request.config.option.env,
             "Platform": caps['platformName']}
        )


# https://stackoverflow.com/a/61433141/4515129
# @pytest.fixture
# # Instantiates Page Objects
# def pages():
#     sign_page = GoogleSearch(driver)
#     return locals()

def pytest_sessionstart(session):
    browser = session.config.option.browser
    env = session.config.option.env
    with open(TEST_CONFIG, 'r') as fd:
        config = yaml.load(fd, Loader=yaml.loader.SafeLoader)
    base_url = config[env]["test_url"]
    pytest.browser = browser
    pytest.base_url = base_url
    if browser == "firefox":
        pytest.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    # elif browser == "remote":
    #     capabilities = {
    #         'browserName': 'firefox',
    #         'javascriptEnabled': True
    #     }
    #     driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub",
    #                               options=capabilities)
    elif browser == "chrome_headless":
        opts = webdriver.ChromeOptions()
        opts.add_argument("--headless")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--no-sandbox")
        pytest.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                         options=opts)
    else:
        pytest.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    pytest.driver.implicitly_wait(5)
    pytest.driver.maximize_window()
    pytest.driver.get(base_url)
    # yield
    # if request.node.rep_call.failed:
    #     screenshot_name = 'screenshot on failure: %s' % datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    #     allure.attach(driver.get_screenshot_as_png(), name=screenshot_name,
    #                   attachment_type=allure.attachment_type.PNG)


def pytest_sessionfinish():
    pytest.driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object

    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)
