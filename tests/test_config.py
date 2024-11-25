import unittest
from unittest.mock import patch, mock_open
import os
import json
import config
import argparse

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Reset the _config variable before each test
        config._config = None

    @patch.dict(os.environ, {'TEST_PARAM': 'env_value'}, clear=True)
    def test_get_parameter_from_env(self):
        param = config.get_parameter('TEST_PARAM')
        self.assertEqual(param, 'env_value')

    def test_get_parameter_from_config(self):
        config._config = {'TEST_PARAM': 'config_value'}
        param = config.get_parameter('TEST_PARAM')
        self.assertEqual(param, 'config_value')

    def test_get_parameter_default(self):
        param = config.get_parameter('NON_EXISTENT_PARAM', default='default_value')
        self.assertEqual(param, 'default_value')

    @patch.dict(os.environ, {}, clear=True)
    def test_set_parameter(self):
        config.set_parameter('NEW_PARAM', 'new_value')
        self.assertEqual(os.environ['NEW_PARAM'], 'new_value')

    def test_convert_to_typed_value(self):
        self.assertEqual(config.convert_to_typed_value('{"key": "value"}'), {'key': 'value'})
        self.assertEqual(config.convert_to_typed_value('true'), True)
        self.assertEqual(config.convert_to_typed_value('null'), None)
        self.assertEqual(config.convert_to_typed_value('123'), 123)
        self.assertEqual(config.convert_to_typed_value('string'), 'string')

    @patch('config._get_default_path')
    @patch('builtins.open', new_callable=mock_open, read_data='{"param1": "value1"}')
    def test_init_config_with_file(self, mock_file, mock_get_default_path):
        mock_get_default_path.return_value = 'config.json'
        config._init_config()
        self.assertEqual(config._config, {'param1': 'value1'})

    @patch('config._get_default_path')
    def test_init_config_no_file(self, mock_get_default_path):
        mock_get_default_path.return_value = None
        with patch('logging.Logger.info') as mock_logger_info:
            config._init_config()
            self.assertEqual(config._config, {})
            mock_logger_info.assert_called_with('Initializing empty config')

    @patch.dict(os.environ, {}, clear=True)
    def test_overwrite_from_args(self):
        args = argparse.Namespace(param1='value1', param2=None)
        with patch('config.set_parameter') as mock_set_parameter:
            config.overwrite_from_args(args)
            mock_set_parameter.assert_any_call('param1', 'value1')

    def test_overwrite_from_args_with_iteritems(self):
        args = argparse.Namespace(param1='value1', param2=None)

        class ArgsWithIteritems(dict):
            def iteritems(self):
                return self.items()

        args_with_iteritems = ArgsWithIteritems(vars(args))

        with patch('config.vars', return_value=args_with_iteritems):
            with patch('config.set_parameter') as mock_set_parameter:
                config.overwrite_from_args(args)
                mock_set_parameter.assert_any_call('param1', 'value1')

    @patch('config.os.getcwd')
    @patch('config.os.path.isfile')
    @patch('config.os.path.abspath')
    @patch('config.os.path.join')
    def test_get_default_path_file_exists(self, mock_join, mock_abspath, mock_isfile, mock_getcwd):
        mock_getcwd.return_value = '/path/to/project'
        mock_join.side_effect = lambda a, b: f'{a}/{b}'
        mock_abspath.side_effect = lambda x: x

        def isfile_side_effect(path):
            return path == '/path/to/project/config.json'
        mock_isfile.side_effect = isfile_side_effect

        path = config._get_default_path()
        self.assertEqual(path, '/path/to/project/config.json')

    def test_get_parameter_complex_type(self):
        config._config = {'COMPLEX_PARAM': {'nested_key': 'nested_value'}}
        param = config.get_parameter('COMPLEX_PARAM')
        self.assertEqual(param, {'nested_key': 'nested_value'})

if __name__ == '__main__':
    unittest.main()
