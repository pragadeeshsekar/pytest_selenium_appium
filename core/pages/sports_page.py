from . import PageObject, HTMLElement, HTMLElementList


class SportsPage(PageObject):
    slick_dots = HTMLElementList(css='.sports .slick-dots')
