from brownie import interface

from scripts.helpful_scripts import get_account
from scripts.price_convertor import get_amount_wei

def get_all_possition(contract_addres: str):
    dca_v3 = interface.IDCA(contract_addres)
    all_possition_lenght = dca_v3.allPositionsLength()
    return all_possition_lenght

def get_possition_by_index(positin_index: int, contract_addres: str):
    dca_v3 = interface.IDCA(contract_addres)
    position = dca_v3.getPosition(positin_index)
    return position

def open_position(contract_addres: str):
    dca_v3 = interface.IDCA(contract_addres)

    account = get_account(account_label='main')
    worker = get_account(account_label='worker')

    position = (
        account.address, # Beneficiary address
        worker.address, # Executor address 
        get_amount_wei(1, 6), # Single spend amount 
        '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174', 
        '0xb0897686c545045aFc77CF20eC7A532E3120E0F1',
        0
    )

    tx = dca_v3.openPosition(position, {'from': account})
    tx.wait(1)
    return tx

def main():
    dca_v3_address: str = '0xab7F9697D40E8245cC8ac3F38e2C6F3a0757dBBf'
    print(get_all_possition(dca_v3_address))

    print(get_possition_by_index(0, dca_v3_address))

    print(get_possition_by_index(1, dca_v3_address))

    # print(open_position(dca_v3_address))


