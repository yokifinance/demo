from brownie import accounts, config, network

FORKED_LOCAL_ENVIRENMENTS = ['mainnet-fork', 'mainnet-fork-dev', 'mumbai-fork-dev', 'polygon-fork-dev']
LOCAL_BLOCKCHAIN_ENVIRENMENTS = ['development', 'ganache-local']


def get_account(account_label='main'):
    if(
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRENMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRENMENTS
    ):
        account = accounts[0] if account_label == 'main' else accounts[1]
        return account
    return accounts.add(config['wallets'][account_label]['from_key'])
