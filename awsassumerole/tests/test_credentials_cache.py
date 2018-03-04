import os
import unittest

from fixture.response import assume_role_response

from credentials_cache import CredentialsCache
from data_models import AssumeRoleArgs


class TestCredentialsCache(unittest.TestCase):

    def setUp(self):
        self.credentials_cache = CredentialsCache()

        self.assume_role_args = AssumeRoleArgs(role_arn='arn:aws:iam::123456789012:role/rolename', role_session_name='sessionname')

    def test_cache_directory_name(self):
        self.assertEqual(self.credentials_cache.cache_directory,
                         '{}/.awsassume/cache'.format(os.path.expanduser('~')))

    def test_cache_directory_exist(self):
        self.assertTrue(os.path.exists(self.credentials_cache.cache_directory))

    def test_get_cache_name(self):
        self.assertEqual(self.credentials_cache.get_cache_name(self.assume_role_args),
                         'sessionname__123456789012_rolename')

    def test_get_cache_full_path(self):
        self.assertEqual(self.credentials_cache.get_cache_full_path(self.assume_role_args),
                         '{}/{}'.format(self.credentials_cache.cache_directory, 'sessionname__123456789012_rolename'))

    def test_set_get_delete_aws_credentials(self):
        self.credentials_cache.set_aws_credentials_to_cache(self.assume_role_args, assume_role_response)
        self.assertTrue(os.path.isfile('{}/{}'.format(self.credentials_cache.cache_directory, 'sessionname__123456789012_rolename')))

        cached_assume_role_response = self.credentials_cache.get_aws_credentials_from_cache(self.assume_role_args)
        self.assertEqual(cached_assume_role_response, assume_role_response)

        self.credentials_cache.delete_cache_file(self.assume_role_args)
        self.assertFalse(os.path.isfile('{}/{}'.format(self.credentials_cache.cache_directory, 'sessionname__123456789012_rolename')))


if __name__ == '__main__':
    unittest.main()