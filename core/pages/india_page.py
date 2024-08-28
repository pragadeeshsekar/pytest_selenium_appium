from . import PageObject, HTMLElement, HTMLElementList


class IndiaPage(PageObject):
    slick_dots = HTMLElementList(css='.sports .slick-dots li')
