Using Pytest framework with unitest test styling - this automation project handles both selenium & appium webdriver handling 

- `driver` fixture uses selenium webdriver initialization
- `appium_driver` fixture uses appium driver initialization

this implementation uses fixture at class scope - directly added above respective test class function (In case of session scope & auto_use=True, both driver gets initialized immidiately after session creation )

for Web Automation - page_object_wrapper HTMLElement class is used for better handling of action & interaction with webelement.

- allure plugin - is used for reporting
