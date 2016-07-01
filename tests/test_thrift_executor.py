import unittest

import mock

import data
from thriftcli import ThriftExecutor


class TestThriftExecutor(unittest.TestCase):
    @mock.patch('thriftcli.TTransport.TFramedTransport.open')
    @mock.patch('thriftcli.TSocket.TSocket')
    @mock.patch('thriftcli.ThriftExecutor._import_package')
    @mock.patch('subprocess.call')
    @mock.patch('thriftcli.ThriftParser._load_file')
    def test_init(self, mock_load_file, mock_call, mock_import_package, mock_tsocket, mock_transport_open):
        mock_load_file.return_value = data.TEST_THRIFT_CONTENT
        mock_call.return_value = 0
        ThriftExecutor(data.TEST_THRIFT_PATH, data.TEST_SERVER_ADDRESS, data.TEST_THRIFT_SERVICE_REFERENCE)
        command = 'thrift -r --gen py %s' % data.TEST_THRIFT_PATH
        mock_call.assert_called_with(command, shell=True)
        mock_import_package.assert_called_with(data.TEST_THRIFT_MODULE_NAME)
        mock_tsocket.assert_called_with(data.TEST_SERVER_HOSTNAME, data.TEST_SERVER_PORT)
        self.assertTrue(mock_transport_open.called)

    def test_parse_address_for_hostname_and_url(self):
        hostname, port = ThriftExecutor._parse_address_for_hostname_and_port(data.TEST_SERVER_ADDRESS)
        hostname2, port2 = ThriftExecutor._parse_address_for_hostname_and_port(data.TEST_SERVER_ADDRESS2)
        hostname3, port3 = ThriftExecutor._parse_address_for_hostname_and_port(data.TEST_SERVER_ADDRESS3)
        expected_hostname, expected_port = data.TEST_SERVER_HOSTNAME, data.TEST_SERVER_PORT
        expected_hostname2, expected_port2 = data.TEST_SERVER_HOSTNAME2, data.TEST_SERVER_PORT2
        expected_hostname3, expected_port3 = data.TEST_SERVER_HOSTNAME3, data.TEST_SERVER_PORT3
        self.assertEqual((hostname, port), (expected_hostname, expected_port))
        self.assertEqual((hostname2, port2), (expected_hostname2, expected_port2))
        self.assertEqual((hostname3, port3), (expected_hostname3, expected_port3))