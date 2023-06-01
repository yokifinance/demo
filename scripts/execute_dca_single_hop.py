import struct
from datetime import timedelta

from brownie import interface, web3

from scripts.helpful_scripts import get_account
from scripts.price_convertor import get_amount_wei


def _get_deadline_timestamp(minutes: int):
    current_timestamp = web3.eth.get_block("latest").timestamp
    deadline_timestamp = current_timestamp + timedelta(minutes=minutes).seconds
    return deadline_timestamp


def execute_strategy(strategy_address: str, path: list, position_index: int):
    worker = get_account(account_label='worker')
    main_account = get_account(account_label='main')
    
    single_params_for_execute = (
        path[0], #tokenToSpend
        path[1], #tokenToBuy
        3000, # pool Fee 0.3%
        main_account,
        _get_deadline_timestamp(10), # 10 minutes Deadline
        get_amount_wei(1, 6), # amountIn 1$
        0, # amountOutMinimum
        0 # sqrtPriceLimitX96
    )
    
    startegy = interface.IDCA(strategy_address)

    tx = startegy.single_params_for_execute(position_index, single_params_for_execute, {'from': worker, 'gas_limit': 1400000, 'allow_revert': True})
    tx.wait(1)
    return tx


def main():
    position_index = 0
    path: list = ('0xc2132D05D31c914a87C6611C10748AEb04B58e8F', '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619')
    deployed_strategy_address: str = '0xA8786b57389D02dB07c411fd11c4D64972f890bf' #0x3A6e8a6Bfe6AB42d9E356b22704eb1029c4b6DF9'
    execute_strategy(deployed_strategy_address, path, position_index)
