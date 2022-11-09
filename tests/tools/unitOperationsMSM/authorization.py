from pullgerMultiSessionManager import apiMSM
from django.test import TestCase


def make_all_session_authorization(self: TestCase):
    result = apiMSM.make_all_session_authorization()
