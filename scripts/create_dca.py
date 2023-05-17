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
        get_amount_wei(2, 6), # Single spend amount 
        token_to_sell, 
        token_to_buy, 
        0
    )
    tx = dca_v3_factory.createDCA(main_account, position, {'from': main_account})
    tx.wait(1)

def main():
    token_to_sell: str  = '0xc2132D05D31c914a87C6611C10748AEb04B58e8F' # USDT
    token_to_buy: str = '0xb33EaAd8d922B1083446DC23f610c2567fB5180f' # UNI
    dca_v3_factory_address: str = '0x62936416CE41f9fA51ffb202dc91559B7E461448'

    create_dca(token_to_sell, token_to_buy, dca_v3_factory_address)