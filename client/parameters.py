import json 
import os
from pathlib import Path

COMPILED_CONTRACT_FILE_NAME = 'ElectricityMeterReading.json'
COTNRACT_ADDRESS_FILE_NAME = 'deployment_config.json'
CONTRACT_TRUFFLE_COMPILE_DIR = 'blockchain/build/contracts'
GANACHE_DATA_DIR_PATH = 'docker-config/ganache-data/'
GANACHE_ACCOUNTS_FILE = 'ganache-accounts.json'
BLOCKCHAIN_BASE_DIR = 'blockchain'
BLOCKCHAIN_URL = 'http://127.0.0.1:8545'
PARENT_DIR = str(Path(__file__).parents[1])
CONTRACT_COMPILE_FILE_PATH = os.path.join(PARENT_DIR, CONTRACT_TRUFFLE_COMPILE_DIR, COMPILED_CONTRACT_FILE_NAME)
CONTRACT_ADDRESS_FILE_PATH = os.path.join(PARENT_DIR, BLOCKCHAIN_BASE_DIR, COTNRACT_ADDRESS_FILE_NAME)
GANACHE_ACCOUNTS_FILE_PATH = os.path.join(PARENT_DIR, GANACHE_DATA_DIR_PATH, GANACHE_ACCOUNTS_FILE)

def load_json_file(file_path): 
    try: 
        with open(file_path) as f: 
            data = json.load(f)
            return data 
    except Exception as e: 
        raise e 

CONTRACT_ABI = load_json_file(CONTRACT_COMPILE_FILE_PATH)['abi']
CONTRACT_ADDRESS = load_json_file(CONTRACT_ADDRESS_FILE_PATH)['address']
ACCOUNTS_DATA = load_json_file(GANACHE_ACCOUNTS_FILE_PATH)
first_address = list(ACCOUNTS_DATA['private_keys'].keys())[0]
first_private_key = ACCOUNTS_DATA['private_keys'][first_address]

def get_account_pairs():
    return list(ACCOUNTS_DATA['private_keys'].items())

all_account_pairs = get_account_pairs()
