from pathlib import Path

from global_vars.paths import BASE_ROOT_PATH


class AllureEnvironmentParser:
    def __init__(self, report_dir):
        self.file_path = BASE_ROOT_PATH / f"{report_dir}/environment.properties"

    def update_allure_env(self, dict_value):
        # w+ mode creates file if not present
        with open(self.file_path, 'w+') as fd:
            for key, value in dict_value.items():
                fd.write(f"{key}={value}\n")
