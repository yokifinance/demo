import struct
from datetime import timedelta

from brownie import interface, web3
from eth_utils import to_bytes

from scripts.helpful_scripts import get_account
from scripts.price_convertor import get_amount_wei


def _get_encode_path(address_list: list, pool_fee: int):
    first_address_bytes = to_bytes(hexstr=address_list[0])
    second_address_bytes = to_bytes(hexstr=address_list[1])
    pool_fee_bytes = struct.pack('>I', pool_fee)[1:]
    encoded_path = first_address_bytes + second_address_bytes + pool_fee_bytes
    return encoded_path


def _get_deadline_timestamp(minutes: int):
    current_timestamp = web3.eth.get_block("latest").timestamp
    deadline_timestamp = current_timestamp + timedelta(minutes=minutes).seconds
    return deadline_timestamp


def execute_strategy(strategy_address: str, path: list, position_index: int):
    worker = get_account(account_label='worker')
    main_account = get_account(account_label='main')
    
    params_for_execute = (
        _get_encode_path(path),
        main_account,
        _get_deadline_timestamp(10), # 10 minutes Deadline
        get_amount_wei(1, 6), # amountIn 1$
        0, # amountOutMinimum
    )

    startegy = interface.IDCA(strategy_address)

    tx = startegy.executeMultihopPurchase(position_index, params_for_execute, {'from': worker, 'gas_limit': 1400000, 'allow_revert': True})
    tx.wait(1)
    return tx


def main():
    position_index: int = 0
    path: list = ('0xc2132D05D31c914a87C6611C10748AEb04B58e8F', '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619')
    deployed_strategy_address: str = '0xA8786b57389D02dB07c411fd11c4D64972f890bf'
    execute_strategy(deployed_strategy_address, path, position_index)
