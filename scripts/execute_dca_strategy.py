from datetime import timedelta

import numpy as np
from brownie import interface, web3
from eth_abi import encode

from scripts.helpful_scripts import get_account
from scripts.price_convertor import get_amount_wei


def _get_encode_address_list(address_list: list):
    encoded_path = encode(['(address,address)'], [address_list])
    return encoded_path


def _get_deadline_timestamp(minutes: int):
    current_timestamp = web3.eth.get_block("latest").timestamp
    deadline_timestamp = current_timestamp + timedelta(minutes=minutes).seconds
    return deadline_timestamp


def execute_strategy(strategy_address: str, path: list):
    worker = get_account(account_label='worker')
    main_account = get_account(account_label='main')
    
    encoded_path = _get_encode_address_list(path)

    multi_params_for_execute = (
        path,
        main_account,
        _get_deadline_timestamp(10), # 2 minutes Deadline
        get_amount_wei(1, 6), # amountIn 2$
        get_amount_wei(1, 18), # amountOutMinimum
    )

    single_params_for_execute = (
        path[0], #tokenToSpend
        path[1], #tokenToBuy
        encode(['uint24'], [3000]), # pool Fee 0.3%
        main_account,
        _get_deadline_timestamp(10), # 10 minutes Deadline
        get_amount_wei(1, 6), # amountIn 1$
        0, # amountOutMinimum
        0 # sqrtPriceLimitX96
    )
    
    position_index: int = 1
    startegy = interface.IDCA(strategy_address)


    # tx = startegy.executeMultihopPurchase(position_index, params_for_execute, {'from': worker, 'gas_limit': 700000, 'allow_revert': True})
    tx = startegy.executeSinglePurchase(position_index, single_params_for_execute, {'from': worker, 'gas_limit': 1400000, 'allow_revert': True})
    tx.wait(1)


def main():
    path: list = ('0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', '0xb0897686c545045aFc77CF20eC7A532E3120E0F1')
    deployed_strategy_address: str = '0xab7F9697D40E8245cC8ac3F38e2C6F3a0757dBBf' #0x3A6e8a6Bfe6AB42d9E356b22704eb1029c4b6DF9'
    execute_strategy(deployed_strategy_address, path)
