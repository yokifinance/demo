from brownie import interface

from scripts.helpful_scripts import get_account
from scripts.price_convertor import get_amount_wei


def create_dca(token_to_sell: str, token_to_buy: str, dca_v3_factory_address: str):
    main_account = get_account(account_label='main')
    worker = get_account(account_label='worker')

    dca_v3_factory = interface.IDCAV3Factory(dca_v3_factory_address)

    position = (
        main_account.address, # Beneficiary address
        worker.address, # Executor address 
        get_amount_wei(1, 6), # Single spend amount 
        token_to_sell, 
        token_to_buy, 
        0
    )
    tx = dca_v3_factory.createDCA(main_account, position, {'from': main_account, 'gas_limit': 1400000, 'allow_revert': True})
    tx.wait(1)
    return tx

def open_position(token_to_sell: str, token_to_buy: str, dca_strategy_address: str):
    main_account = get_account(account_label='main')
    worker = get_account(account_label='worker')

    dca_v3 = interface.IDCA(dca_strategy_address)

    position = (
        main_account.address, # Beneficiary address
        worker.address, # Executor address 
        get_amount_wei(1, 6), # Single spend amount 
        token_to_sell, 
        token_to_buy, 
        0
    )
    tx = dca_v3.openPosition(position, {'from': main_account})
    tx.wait(1)
    return tx


def main():
    token_to_sell: str  = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F' # USDT
    token_to_buy: str = '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619' # WETH
    dca_v3_factory_address: str = '0x3158953dbC9292BC8D92ba5B0Dcb13bED039A514'
    # dca_v3_strategy_address: str = ''

    create_dca(token_to_sell, token_to_buy, dca_v3_factory_address)
    # open_position(
    #     '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', 
    #     '0xb0897686c545045aFc77CF20eC7A532E3120E0F1',
    #     dca_v3_factory_address)