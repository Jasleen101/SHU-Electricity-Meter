import time
from uuid import uuid4
import random 
from parameters import ACCOUNTS_DATA, BLOCKCHAIN_URL, CONTRACT_ABI, CONTRACT_ADDRESS
from web3 import Web3

grid_alerts = [
    "High power use detected. Reduce consumption.",
    "Maintenance scheduled: Power outage 2-4 PM.",
    "Voltage fluctuation detected.",
    "Conserve energy during peak hours (4-8 PM).",
    "Grid overload: Reduce usage immediately.",
    "Power outage reported. Restoration underway.",
    "Energy use exceeds your set limit.",
    "Critical grid event: Load-shedding may occur.",
    "Renewable surplus detected. Shift usage now.",
    "Potential hazard detected. Contact support.",
    "" # Empty string to simulate no alert
]


def select_random_alert():
    index = random.randint(0, len(grid_alerts)-1)
    return grid_alerts[index]


def send_alert(contract):
    try:
        select_random_alert_text = select_random_alert()
        print(f"Alert: {select_random_alert_text}")
        contract.functions.sendGridAlert(
            select_random_alert_text
        ).transact({"from": example_address})
    except Exception as e: 
        pass 


if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
    example_address = Web3.to_checksum_address(list(ACCOUNTS_DATA["addresses"])[1])
    contract_instance = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    while True:
        random_sleep_interval = random.randint(15,60)
        send_alert(contract_instance)
        time.sleep(random_sleep_interval)
