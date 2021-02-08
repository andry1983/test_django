import os
from django.test import TestCase
from backend.security.services import (
    create_security_file_credentials,
    SECURE_FILE_PATH_FOR_TEST,
    read_security_file
)


class HelpersTestCase(TestCase):

    def setUp(self) -> None:
        self.keys_data = ['TEST_SECRET_KEY']
        self._dell_test_security_file()

    def test_create_security_file_without_args(self):
        with self.assertRaises(ValueError):
            create_security_file_credentials([])

    def test_create_security_file(self):
        self.assertFalse(os.path.exists(SECURE_FILE_PATH_FOR_TEST))
        create_security_file_credentials(self.keys_data)
        self.assertTrue(os.path.exists(SECURE_FILE_PATH_FOR_TEST))
        file_data = read_security_file()
        self.assertListEqual(self.keys_data, list(file_data.keys()))

    def test_read_security_file(self):
        create_security_file_credentials(self.keys_data)
        file_data = read_security_file()
        self.assertListEqual(self.keys_data, list(file_data.keys()))

    def test_read_bad_security_file(self):
        create_security_file_credentials(self.keys_data)
        if os.path.exists(SECURE_FILE_PATH_FOR_TEST):
            with open(SECURE_FILE_PATH_FOR_TEST, 'w') as file:
                file.write('')
        with self.assertRaises(ValueError):
            read_security_file()

    @classmethod
    def _dell_test_security_file(cls):
        if os.path.exists(SECURE_FILE_PATH_FOR_TEST):
            os.remove(SECURE_FILE_PATH_FOR_TEST)

    @classmethod
    def setUpClass(cls) -> None:
        cls._dell_test_security_file()

    @classmethod
    def tearDownClass(cls) -> None:
        cls._dell_test_security_file()
