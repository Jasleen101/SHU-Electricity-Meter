import unittest
from unittest.mock import MagicMock, patch
from web3 import Web3

#run test with = python -m unittest tests/test_solidity_contract.py
#all tests = python -m unittest discover -s tests

#mock abi to simulate contracts methods and i/o
mock_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "uid", "type": "string"},
            {"internalType": "uint256", "name": "mtr_reading", "type": "uint256"}
        ],
        "name": "storeMeterReading",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getMeterBill",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "constant": True,
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "constant": True,
        "type": "function"
    }
]

class TestSolidityContract(unittest.TestCase):
    """
    unit tests for smart contract
    includes positive and negative scenarios
    """

    def setUp(self):
        """
        method sets up reuseable attributes
        """
        # Initialize the mock Web3 and contract objects
        self.web3_mock = MagicMock()
        self.contract_mock = MagicMock()
        self.web3_mock.eth.contract.return_value = self.contract_mock

        self.uid = "uid"
        self.meter_reading = 20
        self.expected_bill = self.meter_reading * 2

    #positive Test
    #storing and retrieving bill
    #mocking storage of data
    @patch('web3.Web3')
    def test_store_and_get_bill(self, web3_mock):
        """
        test storing meter reading and returning bill from contract
        mocks borth storage and retireving using mock data
        """
        web3_mock.eth.default_account = "Account_Mock"

        self.contract_mock.functions.storeMeterReading.return_value.transact.return_value = \
            "mock_tx_hash"
        self.contract_mock.functions.getMeterBill.return_value.call.return_value = 40

        #storing
        tx_hash = self.contract_mock.functions.storeMeterReading(
            self.uid,
            self.meter_reading
        ).transact()
        self.assertEqual(tx_hash, "mock_tx_hash", "transaction hash mismatch")

        #retrieving
        actual_bill = self.contract_mock.functions.getMeterBill().call()
        self.assertEqual(actual_bill, self.expected_bill, "bill calculation error")

        print(f"expected bill: {self.expected_bill}, actual bill: {actual_bill}")

    #positive test
    #retrieving contract owner adddress
    @patch('web3.Web3')
    def test_get_owner(self, web3_mock):
        """
        test retrieving owner addresses of the contract
        mocks contract owner
        """
        with patch('web3.Web3', return_value=web3_mock), \
            patch.object(web3_mock.eth, 'contract', return_value=self.contract_mock):

            mock_owner_address = "Owner_Mock"
            self.contract_mock.functions.owner.return_value.call.return_value = mock_owner_address

            owner_address = self.contract_mock.functions.owner().call()

            self.assertEqual(owner_address, mock_owner_address, "owner address mismatch")
            print(f"mocked owner address: {owner_address}")

    #negative test
    #test invalid input handeling
    @patch('web3.Web3')
    def test_store_meter_reading_invalid(self, web3_mock):
        """
        test handling of wrong meter reading
        """
        with patch('web3.Web3',
                   return_value=web3_mock
                ), patch.object(
                    web3_mock.eth,
                    'contract',
                    return_value=self.contract_mock
                ):
            self.contract_mock.functions.storeMeterReading.return_value.transact.side_effect = \
                Exception("transaction reverted")

            meter_reading = -10 #invalid input

            with self.assertRaises(Exception) as context:
                self.contract_mock.functions.storeMeterReading(self.uid, meter_reading).transact()

            # Assertions
            self.assertIn("transaction reverted", str(context.exception),
                          "expected transaction revert msg not found")
            print(f"caught expected exception: {context.exception}")

    #negative test
    #retrieving bill with no reading        
    @patch('web3.Web3')
    def test_get_empty_bill(self, web3_mock):
        """
        test retrieving empty bill when nothing has been stored
        """
        with patch('web3.Web3', return_value=web3_mock), \
            patch.object(web3_mock.eth, 'contract', return_value=self.contract_mock):

            self.contract_mock.functions.getMeterBill.return_value.call.return_value = 0

            actual_bill = self.contract_mock.functions.getMeterBill().call()

            self.assertEqual(actual_bill, 0, "expected bill to be 0")
            print(f"bill with no readings: {actual_bill}")

if __name__ == '__main__':
    unittest.main()