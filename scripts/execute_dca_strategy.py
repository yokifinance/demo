import pytest
from brownie import accounts, interface, web3

from scripts.helpful_scripts import get_account
from scripts.price_convertor import get_amount_wei

def _get_encode_address_list(address_list: list):
    encoded_path = web3.solidityKeccak(['address[]'], [address_list]).hex()
    return encoded_path

def execute_strategy(strategy_address: str, path: list):
    worker = get_account(account_label='worker')
    main_account = get_account(account_label='main')
    
    encoded_path = _get_encode_address_list(path)

    params_for_execute = (
        encoded_path,
        main_account,
        60 * 2, # 2 minutes Deadline
        get_amount_wei(2, 6), # amountIn 2$
        get_amount_wei(1, 18), # amountOutMinimum
    )
    
    position_index: int = 0
    startegy = interface.IDCA(strategy_address)
    tx = startegy.executeMultihopPurchase(position_index, params_for_execute, {'from': worker, 'gas_limit': 700000, 'allow_revert': True})
    tx.wait(1)

def main():
    path: list = ['0xc2132D05D31c914a87C6611C10748AEb04B58e8F', '0xb33EaAd8d922B1083446DC23f610c2567fB5180f']
    deployed_strategy_address: str = '0xFeB3fFdb4628A80607FFb2249D6A42987d9Fd554'
    execute_strategy(deployed_strategy_address, path)
