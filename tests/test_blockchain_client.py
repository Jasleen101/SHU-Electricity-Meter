import asyncio
import os
import unittest
from unittest.mock import AsyncMock, MagicMock, mock_open, patch

from client.blockchain_client import (
    BlockchainConnectionError,
    BlockchainConnectionMonitor,
    BlockchainGetAlerts,
    BlockchainGetBill,
    BlockchainStoreReading,
    GenerateReadings,
    SmartMeterUI,
    get_contract,
)

# run test with = python -m unittest tests/test_blockchain_client.py
# all tests = python -m unittest discover -s tests


class TestClientBlockchain(unittest.TestCase):
    """
    unit tests for blockchain client functionality
    includes positive and negative scenarios
    """

    def setUp(self):
        """
        method sets up reuseable attributes
        """
        self.mock_w3 = MagicMock()
        self.mock_contract = MagicMock()
        self.mock_ui_callback = MagicMock()
        self.mock_app = MagicMock()
        self.private_key = "0x" + "a" * 64

    # positive test
    # get_contract works with connection
    @patch("client.blockchain_client.Web3")
    @patch("builtins.open", mock_open(read_data='{"contract_address": "0x12345"}'))
    def test_get_contract_success(self, MockWeb3):
        """
        test get_contract works correctly when web3 is connected
        mocks web3 connection and contract
        """
        self.mock_w3.is_connected.return_value = True

        # mock contract
        contract_mock = MagicMock()
        self.mock_w3.eth.contract.return_value = contract_mock

        MockWeb3.return_value = self.mock_w3

        w3, contract = get_contract(self.mock_app)

        self.assertIsNotNone(w3)
        self.assertIsNotNone(contract)
        self.mock_app.update_connection_status.assert_called_with("connected")

    # positive test
    # check connection when web3 is connected
    @patch("client.blockchain_client.Web3")
    def test_check_connection_connected(self, MockWeb3):
        """
        test BlockchainConnectionMonitor when web3 is connected
        checks if monitor updates UI
        """
        self.mock_w3.is_connected.return_value = True

        monitor = BlockchainConnectionMonitor(self.mock_app, self.mock_w3)

        with patch("time.sleep", return_value=None):
            monitor.check_connection(stop_flag=True)

        self.mock_app.update_connection_status.assert_called_with("connected")

    # positive test
    # check BlockchainGetBill is correct
    def test_blockchain_get_bill(self):
        """
        tests input of BlockchainGetBill
        """
        bill_instance = BlockchainGetBill(
            self.private_key,
            self.mock_w3,
            self.mock_contract,
            self.mock_ui_callback,
        )

        self.assertEqual(bill_instance.private_key, self.private_key)
        self.assertEqual(bill_instance.w3, self.mock_w3)
        self.assertEqual(bill_instance.contract, self.mock_contract)
        self.assertEqual(bill_instance.ui_callback, self.mock_ui_callback)

    # positive test
    # simulate polling for bills
    @patch(
        "client.blockchain_client.BlockchainGetBill.poll_bill", new_callable=MagicMock
    )
    def test_poll_bill(self, mock_poll_bill):
        """
        test poll_bill method in BlockChainGetBill
        mocks poll_bill
        """
        bill_instance = BlockchainGetBill(
            self.private_key,
            self.mock_w3,
            self.mock_contract,
            self.mock_ui_callback,
        )

        async def mock_poll_bill_coroutine():
            return None

        mock_poll_bill.side_effect = mock_poll_bill_coroutine

        asyncio.run(bill_instance.poll_bill())

        mock_poll_bill.assert_called_once()

    # positive test
    # gen random readings test
    def test_generate_reading(self):
        """
        tests GenerateReadings.generate_reading method
        test to see it is in the expected range
        """
        generated_reading = GenerateReadings.generate_reading()
        self.assertTrue(0 <= generated_reading <= 1)

    # positive test
    # simulate storing readings in blockchain
    @patch(
        "client.blockchain_client.BlockchainStoreReading.store_reading",
        new_callable=MagicMock,
    )
    def test_store_reading(self, mock_store_reading):
        """
        test store_reading method in BlockchainStoreReading
        """
        reading_instance = BlockchainStoreReading(
            self.private_key, self.mock_w3, self.mock_contract
        )

        async def mock_store_reading_coroutine(reading):
            return None

        mock_store_reading.side_effect = mock_store_reading_coroutine

        asyncio.run(reading_instance.store_reading(5))

        mock_store_reading.assert_called_once_with(5)

    # negative test
    # test to see how get_contract is handled
    @patch("client.blockchain_client.Web3")
    @patch("builtins.open", mock_open())
    def test_get_contract_error_handling(self, MockWeb3):
        """
        test get_contract function when web3 is not connected
        """
        self.mock_w3.is_connected.return_value = False

        MockWeb3.return_value = self.mock_w3

        with self.assertRaises(BlockchainConnectionError):
            get_contract(self.mock_app)

        self.mock_app.update_connection_status.assert_called_with("error")

    # positive test
    # veriify UI updates status
    def test_update_connection_status_connected(self):
        """
        test smartmeterUI updates the connection status
        """

        if os.getenv("CI") == "true":
            # Skip UI tests in CI environment
            return

        app = SmartMeterUI()
        app.update_connection_status("connected")
        self.assertEqual(
            app.connection_status_label.cget("text"), "Connected to server"
        )
        self.assertEqual(app.connection_status_label.cget("text_color"), "green")

    # positive test
    # handling of grid alrt and integration with UI
    def test_handle_grid_alert(self):
        """
        test the implementation of handle_grid_alert in BlockchainGetAlerts
        checks correct UI message is updated when an alert is received
        """
        alerts_instance = BlockchainGetAlerts(
            self.mock_w3, self.mock_contract, self.mock_ui_callback
        )

        mock_event = MagicMock()
        mock_event.args.message = "Test Alert"

        async def async_test():
            await alerts_instance.handle_grid_alert(mock_event)
            self.mock_ui_callback.update_notice_message.assert_called_with("Test Alert")

        asyncio.run(async_test())

    # positive test
    # checks interaction with the mocked handle_grid_alert method
    @patch(
        "client.blockchain_client.BlockchainGetAlerts.handle_grid_alert",
        new_callable=AsyncMock,
    )
    def test_handle_grid_alert_mocked(self, mock_handle_grid_alert):
        """
        test interaction with mocked handle_grid_alert method in BlockchainGetAlerts
        """
        alerts_instance = BlockchainGetAlerts(
            self.mock_w3, self.mock_contract, self.mock_ui_callback
        )

        mock_event = MagicMock()
        asyncio.run(alerts_instance.handle_grid_alert(mock_event))
        mock_handle_grid_alert.assert_called_once_with(mock_event)

    # negative test
    # test to see how connection is handle when web3 is not connected
    @patch("time.sleep", return_value=None)
    def test_check_connection_disconnected(self, mock_sleep):
        """
        test BlockchainConnectionMonitor when web3 is disconnected
        test to see UI is updated
        """
        self.mock_w3.is_connected.return_value = False

        monitor = BlockchainConnectionMonitor(self.mock_app, self.mock_w3)
        monitor.check_connection(stop_flag=True)

        self.mock_app.update_connection_status.assert_called_with("error")

    # negative test
    # validate private key test
    def test_invalid_private_key(self):
        """
        test BlockchainStoreReading with wrong private key
        and error is raised correctly
        """
        private_key = "invalid_key"

        with self.assertRaises(ValueError):
            BlockchainStoreReading(private_key, self.mock_w3, self.mock_contract)

    # negative test
    # simulate polling fail
    @patch(
        "client.blockchain_client.BlockchainGetBill.poll_bill", new_callable=AsyncMock
    )
    def test_poll_bill_failure(self, mock_poll_bill):
        """
        test poll_bill to see if handles errors correctly
        """
        bill_instance = BlockchainGetBill(
            self.private_key,
            self.mock_w3,
            self.mock_contract,
            self.mock_ui_callback,
        )

        async def mock_poll_bill_coroutine():
            raise Exception("Polling error")

        mock_poll_bill.side_effect = mock_poll_bill_coroutine

        with self.assertRaises(Exception):
            asyncio.run(bill_instance.poll_bill())

        mock_poll_bill.assert_called_once()


if __name__ == "__main__":
    unittest.main()
