from . import PageObject, HTMLElement, HTMLElementList


class MainPage(PageObject):
    india = HTMLElement(css='[href="https://indianexpress.com/section/india/"]')
    business = HTMLElement(css='[href="https://indianexpress.com/section/business/"]')
    sports = HTMLElement(css='[href="https://indianexpress.com/section/sports/"]')

    active_carousel = HTMLElement(css='.mainslider li.slick-active')
    updated_time = HTMLElement(css='.story-details [itemprop="dateModified"]')

