from django.test import TestCase
from pullgerMultiSessionManager import apiMSM
from pullgerMultiSessionManager.tests.tools import UnitOperations


class Unit001OperationElements(TestCase):
    def test_001_00_00_get_page(self):

        for i in range(2):
            if i == 0:
                uuid_session = UnitOperations.add_new_session_selenium_standard(self)
            elif i == 1:
                uuid_session = UnitOperations.add_new_session_selenium_headless(self)

            api.operation_get_page(uuid_session=uuid_session, url="https://google.com")

            el_count = api.operation_elements_scan(uuid_session=uuid_session)
            el_list = api.operation_elements_list(uuid_session=uuid_session)

            # Input search field
            el = el_list[1]

            api.operation_element_send_string(
                uuid_session=uuid_session,
                uuid_auto_element=el['uuid_auto_element'],
                string='test'
            )

            api.operation_element_send_enter(
                uuid_session=uuid_session,
                uuid_auto_element=el['uuid_auto_element'],
            )

            current_url = api.operation_get_current_url(uuid_session=uuid_session)

            find_mark = current_url.find("google.com/search?")
            self.assertNotEqual(find_mark, -1, "Incorrect search operation.")

            UnitOperations.kill_session(self, uuid_session=uuid_session)
