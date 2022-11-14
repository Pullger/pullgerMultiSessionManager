from django.test import TestCase
from pullgerMultiSessionManager import apiMSM
from pullgerMultiSessionManager.tests.tools import unitOperationsMSM
import time


class Unit001OperationExecution(TestCase):
    # def test_001_00_00_screenshot(self):
    #     uuid_session = UnitOperations.add_new_session_selenium_headless(self)
    #     api.operation_get_page(uuid_session=uuid_session, url="https://linkedin.com")

    def test_001_00_00_get_page(self):

        for i in range(1):
            if i == 0:
                uuid_session = unitOperationsMSM.add_new_session_selenium_stand_alone(self)
            # elif i == 1:
            #     uuid_session = UnitOperations.add_new_session_selenium_headless(self)
            # elif i == 2:
            #     uuid_session = UnitOperations.add_new_session_selenium_headless(self)

            error_description = None
            try:
                api.operation_get_page(uuid_session=uuid_session, url="https://google.com")
            except BaseException as e:
                error_description = str(e)

            self.assertEqual(error_description, None, f"Error on get page on iteration. Description: {error_description}")

            html = api.operation_get_html(uuid_session)
            self.assertNotEquals(html.find("<html"), -1, 'Incorrect html.')

            time.sleep(10)

            unitOperationsMSM.kill_session(self, uuid_session=uuid_session)