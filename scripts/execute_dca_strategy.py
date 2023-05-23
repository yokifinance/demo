from brownie import interface
from eth_abi import encode

from scripts.helpful_scripts import get_account
from scripts.price_convertor import get_amount_wei


def _get_encode_address_list(address_list: list):
    encoded_path = encode(['(address,address)'], [address_list])
    return encoded_path


def execute_strategy(strategy_address: str, path: list):
    worker = get_account(account_label='worker')
    main_account = get_account(account_label='main')
    
    encoded_path = _get_encode_address_list(path)

    multi_params_for_execute = (
        path,
        main_account,
        60 * 2, # 2 minutes Deadline
        get_amount_wei(1, 6), # amountIn 2$
        get_amount_wei(1, 18), # amountOutMinimum
    )

    single_params_for_execute = (
        path[0],
        path[1],
        3000, # pool Fee 0.3%
        main_account,
        60 * 2, # 2 minutes Deadline
        1000000, # get_amount_wei(1, 6), # amountIn 1$
        0, # amountOutMinimum
        0 # sqrtPriceLimitX96
    )
    
    position_index: int = 0
    startegy = interface.IDCA(strategy_address)


    # tx = startegy.executeMultihopPurchase(position_index, params_for_execute, {'from': worker, 'gas_limit': 700000, 'allow_revert': True})
    tx = startegy.executeSinglePurchase(position_index, single_params_for_execute, {'from': worker, 'gas_limit': 700000, 'allow_revert': True})
    tx.wait(1)


def main():
    path: list = ('0xc2132D05D31c914a87C6611C10748AEb04B58e8F', '0x9c2C5fd7b07E95EE044DDeba0E97a665F142394f')
    deployed_strategy_address: str = '0xE108c1F9b0546dF81D6Ea598d0404BD48791EED6' #0x3A6e8a6Bfe6AB42d9E356b22704eb1029c4b6DF9'
    execute_strategy(deployed_strategy_address, path)
