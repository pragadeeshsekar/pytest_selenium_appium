from . import PageObject, HTMLElement, HTMLElementList


class MainPage(PageObject):
    pop_up_close = HTMLElement(id="popup-widget238491-close-icon")
    name = HTMLElement(xpath='//*[@id="bs-8"]//div[@data-aid="CONTACT_FORM_NAME"]//input')
    email = HTMLElement(xpath='//*[@id="bs-8"]//div[@data-aid="CONTACT_FORM_EMAIL"]//input')
    send_button = HTMLElement(xpath='//*[@id="bs-8"]//button')
    submit_success = HTMLElement(xpath='//*[@id="bs-8"]//div[@data-aid="CONTACT_FORM_SUBMIT_SUCCESS_MESSAGE"]')

    contact_forms = HTMLElementList(xpath='//button')
    county_iframe = HTMLElement(tag_name="iframe")
    county_list = HTMLElementList(xpath='//option')
    county_dropdown = HTMLElement(id="tCounty")
