from . import PageObject, HTMLElement, HTMLElementList


class IndiaPage(PageObject):
    slick_dots = HTMLElementList(css='.india .slick-dots')
