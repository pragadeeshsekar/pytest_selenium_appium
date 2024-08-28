import logging
import time
from abc import ABC

import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, NoSuchElementException, \
    TimeoutException

from core.constants import LARGE_TIMEOUT


# modified from page object python library.
class LocatorType:
    class_name = 'class_name'
    css = 'css'
    id_ = 'id'
    link_text = 'link_text'
    name = 'name'
    partial_link_text = 'partial_link_text'
    tag_name = 'tag_name'
    xpath = 'xpath'


class ElementCondition:
    clickable = 'clickable'
    frame_available = 'frame_available'
    invisible = 'invisible'
    no_presence = 'nopresence'
    presence = 'presence'
    selected = 'selected'
    visible = 'visible'


# Map PageElement constructor arguments to webdriver locator enums
_LOCATOR_MAP = {
    LocatorType.css: By.CSS_SELECTOR,
    LocatorType.id_: By.ID,
    LocatorType.name: By.NAME,
    LocatorType.xpath: By.XPATH,
    LocatorType.link_text: By.LINK_TEXT,
    LocatorType.partial_link_text: By.PARTIAL_LINK_TEXT,
    LocatorType.tag_name: By.TAG_NAME,
    LocatorType.class_name: By.CLASS_NAME,
}

# Map PageElement constructor arguments to webdriver locator enums
_EXPECTED_COND_ELEMENT = {
    ElementCondition.presence: expected_conditions.presence_of_element_located,
    ElementCondition.visible: expected_conditions.visibility_of_element_located,
    ElementCondition.frame_available: expected_conditions.frame_to_be_available_and_switch_to_it,
    ElementCondition.invisible: expected_conditions.invisibility_of_element_located,
    ElementCondition.no_presence: expected_conditions.invisibility_of_element,
    ElementCondition.clickable: expected_conditions.element_to_be_clickable,
    ElementCondition.selected: expected_conditions.element_to_be_clickable
}

_EXPECTED_COND_ELEMENTS = {
    ElementCondition.presence: expected_conditions.presence_of_all_elements_located,
    ElementCondition.visible: expected_conditions.visibility_of_any_elements_located,
}


class PageObject(ABC):
    """Page Object pattern."""

    def __init__(self, webdriver):
        """
        :param webdriver: selenium webdriver instance.
        :return: returns the page object
        """
        self.webdriver = webdriver
        self.logger = logging.getLogger("page_object_logger")

    @property
    def title(self):
        return self.webdriver.title


class Element(ABC):
    """Element descriptor."""
    _wait_timeout = LARGE_TIMEOUT

    def __init__(self, **kwargs):
        self.logger = logging.getLogger("page_object_logger")
        if not kwargs:
            raise ValueError("atleast locator needs to be passed")
        len_kwargs = len(kwargs)
        for key, value in kwargs.items():
            if key in _LOCATOR_MAP:
                self._locator = (_LOCATOR_MAP[key], value)

    def __get__(self, instance, owner):
        self.pg_name = None
        if isinstance(instance, PageObject):
            self.driver = instance.webdriver
            self.pg_name = instance.__class__.__name__
        elif isinstance(instance, Element):
            self.driver = instance.driver
        return self

    def get_element(self, timeout: int = None):
        self._wait_timeout = LARGE_TIMEOUT if timeout is None else timeout
        retry = 3
        while retry >= 0:
            try:
                return WebDriverWait(self.driver, self._wait_timeout).until(
                    _EXPECTED_COND_ELEMENT[ElementCondition.visible](self._locator)
                )
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException) as ex:
                self.logger.error(f"Exception {ex} raised on {self._locator} with condition {ElementCondition.visible}")
                retry -= 1
        return False

    def is_present(self, timeout=None):
        with allure.step(f"check Locator={self._locator} presence on Page: {self.pg_name}"):
            element = self.get_element(timeout)
            return True if element else element  # if element not found

    def is_not_present(self, timeout=None):
        self._wait_timeout = LARGE_TIMEOUT if timeout is None else timeout
        with allure.step(f"check Locator={self._locator} Absence on Page: {self.pg_name}"):
            return WebDriverWait(self.driver, self._wait_timeout).until(
                _EXPECTED_COND_ELEMENT[ElementCondition.no_presence](self._locator)
            )

    def clear(self):
        with allure.step(f"Clear action on Locator={self._locator} in Page: {self.pg_name}"):
            element = self.get_element()
            element.clear()

    def click(self):
        with allure.step(f"Click action on Locator={self._locator} in Page: {self.pg_name}"):
            element = self.get_element()
            action = ActionChains(self.driver)
            action.move_to_element(element)
            action.click().perform()

    def send_keys(self, value):
        with allure.step(f"Send Keys {value} on Locator={self._locator} in Page: {self.pg_name}"):
            element = self.get_element()
            action = ActionChains(self.driver)
            action.move_to_element(element)
            action.click().send_keys(value).perform()

    def submit(self):
        with allure.step(f"Submit action on Locator={self._locator} in Page: {self.pg_name}"):
            element = self.get_element()
            element.submit()

    def scroll_to_view(self):
        action = ActionChains(self.driver)
        action.move_to_element(self.get_element()).perform()

    def switch_to_frame(self):
        element = self.get_element()
        self.driver.switch_to.frame(element)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def get_text(self):
        element = self.get_element()
        return element.text



    ("'accessible_name', "
     "'aria_role', "
     "'clear', "
     "'click', "
     "'find_element', "
     "'find_elements', "
     "'get_attribute', "
     "'get_dom_attribute',"
     " 'get_property',"
     " 'id',"
     " 'is_displayed',"
     " 'is_enabled', "
     "'is_selected', "
     "'location', "
     "'location_once_scrolled_into_view', "
     "'parent', "
     "'rect', "
     "'screenshot', "
     "'screenshot_as_base64', "
     "'screenshot_as_png', "
     "'send_keys', "
     "'shadow_root', "
     "'size', "
     "'submit', "
     "'tag_name', "
     "'text', "
     "'value_of_css_property']")






    # _expected_condition = ElementCondition.visible  # default value
    # _expected_cond_map = _EXPECTED_COND_ELEMENT
    # _locator = None
    # _wait_timeout = LARGE_TIMEOUT
    # _find_retries = 3
    # parent_ele = None
    #
    # def __init__(self, **kwargs):
    #     self.logger = logging.getLogger("page_object_logger")
    #     if not kwargs:
    #         raise ValueError("Please specify a locator")
    #     len_kwargs = len(kwargs)
    #     if len_kwargs < 1:
    #         raise ValueError("Element only takes atleast 1 arguments , but %d given" % len_kwargs)
    #     for key, value in kwargs.items():
    #         if key in _LOCATOR_MAP:
    #             self._locator = (_LOCATOR_MAP[key], value)
    #         elif key == "expected_condition":
    #             self._expected_condition = value
    #             if value not in self._expected_cond_map:
    #                 raise ValueError("INVALID expected condition %s", value)
    #         elif key == "wait_timeout":
    #             if isinstance(value, int) and value > 0:
    #                 self._wait_timeout = value
    #             else:
    #                 raise ValueError("invalid wait_timeout")
    #         else:
    #             raise ValueError("INVALID input: %s", key)
    #     if self._locator is None:
    #         raise ValueError("Please specify a locator")
    #
    # def find(self, condition=None):
    #     self.logger.debug('Find %s by %s: <%s>', self.__class__.__name__, *self._locator)
    #     tries = 3
    #     while True:
    #         try:
    #             condition = self._expected_condition if condition is None else condition
    #             return WebDriverWait(self.parent_ele, self._wait_timeout).until(
    #                 self._expected_cond_map[self._expected_condition](self._locator),
    #                 "Didn't find element by %s: <%s>" % self._locator)
    #         except StaleElementReferenceException as e:
    #             self.logger.debug("StaleElementReferenceException found on parent. Retry find parent: %s"
    #                               % self.parent_pageelement.__class__.__name__)
    #             self.parent_ele = self.parent_pageelement._refind_element()
    #             time.sleep(1)
    #             tries -= 1
    #             if tries == 0:
    #                 self.logger.error("failed to find the element after %d retries" % tries)
    #                 raise NoSuchElementException
    #         except TimeoutException as e:
    #             return self
    #
    # def __get__(self, instance, owner):
    #     self.expected_condition = None
    #     if isinstance(instance, PageObject):
    #         self.logger.debug("Finding %s under %s ", self.__class__.__name__, instance.__class__.__name__)
    #         self.parent_ele = instance.webdriver
    #     elif isinstance(instance, Element):
    #         self.logger.debug("Finding child element of %s", instance.__class__.__name__)
    #         # print instance.element.get_attribute('class')
    #         self.parent_ele = instance.element
    #         self.expected_condition = instance.element.get_attribute('expected_condition')
    #     else:
    #         raise ValueError(
    #             "PageElement of ParentPageElement can only be instantiated on PageObject or ParentPageElement ")
    #     self.parent_pageelement = instance
    #     self.element = self.find(condition=self.expected_condition)
    #     return self
    #
    # def __set__(self, instance, value):
    #     if value is not None:
    #         self.element = self.__get__(instance, instance.__class__)
    #         value = str(value)
    #         if len(value) > 0:
    #             self.logger.debug("Type text '%s' into the element")
    #             self.element.send_keys(value)
    #             return 1
    #
    # def _refind_element(self):
    #     self.logger.debug("Refind element")
    #     return self.find()
    #
    # @property
    # def native_webelement(self):
    #     return self.element
    #
    # def __click(self):
    #     return self.element.click()
    #
    # def __send_keys(self, value):
    #     return self.element.send_keys(value)
    #
    # def __swtich_case_for_webelement_actions(self, actions_str, value=None):
    #     switcher = {
    #         'click': self.__click(),
    #         'send_keys:': self.__send_keys(value)
    #     }
    #     return switcher.get(actions_str, "None")
    #
    # def _wrapper_webelement_actions(self, action, value=None):
    #     with allure.step(f"Perform {action=} on locator: {self._locator} with condition: {self._expected_condition}"):
    #         if action == "click":
    #             ret = self.element.click()
    #         elif action == "send_keys":
    #             ret = self.element.send_keys(value)
    #         elif action == "clear":
    #             ret = self.element.clear()
    #         elif action == "text":
    #             ret = self.element.text
    #         elif action == "get_attribute":
    #             ret = self.element.get_attribute(value)
    #         elif action == "is_displayed":
    #             ret = self.element.is_displayed()
    #         elif action == "submit":
    #             ret = self.element.submit()
    #         elif action == "is_enabled":
    #             ret = self.element.is_enabled()
    #         elif action == "is_selected":
    #             ret = self.element.is_selected()
    #         elif action == "is_not_present":
    #             ret = self.element.is_not_present()
    #         else:
    #             raise "Action Not defined. Library Script Issue"
    #
    # def click(self):
    #     self._wrapper_webelement_actions('click')
    #
    # def clear(self):
    #     return self._wrapper_webelement_actions('clear')
    #
    # def send_keys(self, value):
    #     return self._wrapper_webelement_actions('send_keys', value)
    #
    # @property
    # def text(self):
    #     return self._wrapper_webelement_actions('text')
    #
    # def get_attribute(self, value):
    #     return self._wrapper_webelement_actions('get_attribute', value)
    #
    # def is_displayed(self):
    #     return self._wrapper_webelement_actions('is_displayed')
    #
    # def submit(self):
    #     return self._wrapper_webelement_actions('submit')
    #
    # def is_enabled(self):
    #     return self._wrapper_webelement_actions('is_enabled')
    #
    # def is_selected(self):
    #     return self._wrapper_webelement_actions('is_selected')
    #
    # def parent(self):
    #     return self.parent
    #
    # def is_not_present(self):
    #     try:
    #         self.find()
    #         return False
    #     except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
    #         # In the case of NoSuchElement, returns true because the element is
    #         # not present in DOM. The try block checks if the element is present
    #         # but is invisible.
    #         # In the case of StaleElementReference, returns true because stale
    #         # element reference implies that element is no longer visible.
    #         return True


class ListElements(Element):
    _expected_cond_map = _EXPECTED_COND_ELEMENTS

    def __get__(self, instance, owner):
        super(ListElements, self).__get__(instance, owner)
        self.elements = self.driver.find_elements(*self._locator)
        return self

    def __getitem__(self, item):
        self.index_item = item
        # since this is list elements, need to replace the self.element to the item we need.
        self.element = self.elements[item]
        return self

    def _refind_element(self):
        self.logger.debug("Refind element with index %s" % self.index_item)
        return self.get_element()[self.index_item]

    # access only by parent class or guardedelements
    @property
    def get_array_len(self):
        # indicates the array of elements
        if self._expected_cond_map == _EXPECTED_COND_ELEMENTS:
            return len(self.elements)
        else:
            raise SyntaxError("get_array_len can only be called on a element list object, "
                              "PageElements or ParentElements")

    @property
    def native_webelements(self):
        return self.elements


class HTMLElement(Element):
    """
    Possible arguments list: \n
        \t LocatorType=value \n
        \t expected_conditions=ElementCondition \n
    defined LocatorType : attributes defined in LocatorType class \n
    \t 'class_name', 'css', 'id_', 'link_text', 'name', 'partial_link_text', 'tag_name', 'xpath' \n
    ElementCondition: attributes defined in ElementCondition class : \t
    \t 'clickable', 'frame_available', 'invisible', 'no_presence', 'presence', 'selected', 'visible' \n
    \n \n
    example : HTMLElement(css='#name', expected_conditions='no_presence')
    """
    pass


class HTMLElementList(ListElements):
    pass
