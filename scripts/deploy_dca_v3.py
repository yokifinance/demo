from brownie import DCAV3, config, network

from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRENMENTS, get_account


def deploy_dca_v3():
    account = get_account()

    dca_v3 = DCAV3.deploy(

        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify')
    )

    print(f'Contract deployed to: {dca_v3.address}')
    return dca_v3

def main():
    deploy_dca_v3()