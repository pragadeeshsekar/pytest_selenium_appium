import time

import pytest
from utilities import api_util
from tests.test_base import BaseTest


@pytest.mark.tags("CHECK")
class TestAPI(BaseTest):

    def test_api_send(self):
        data_to_send = {'name': '456_item',
                        'description': 'description123',
                        'price': 12345.0,
                        'item_type': 'sample_team'}

        new_id = api_util.post_item(**data_to_send)
        response = api_util.get_item(new_id)
        response.pop("id")
        assert response == data_to_send

