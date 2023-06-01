from brownie import Wei


def get_amount_wei(amount: int, decimals: int):
    amount_with_decimals = amount * 10 ** decimals
    return Wei(amount_with_decimals)