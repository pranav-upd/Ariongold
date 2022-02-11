import os
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, PaymentTxn


def initialize_client():
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = os.getenv('PS_API')
    headers = {
        "X-API-Key": algod_token,
    }
    algod_client = algod.AlgodClient(algod_token, algod_address, headers)
    return algod_client


def create_asset(client, asset_name, circulation_no):
    params = client.suggested_params()
    creator_sk, creator_pk = mnemonic_to_pskey(os.getenv('ip_mnc'))
    asset_config = AssetConfigTxn(
        sender=creator_pk,
        sp=params,
        total=circulation_no,
        default_frozen=False,
        unit_name=asset_name.upper(),
        asset_name=asset_name.lower(),
        manager=creator_pk,
        reserve=creator_pk,
        freeze=creator_pk,
        clawback=creator_pk,
        decimals=0)
    asset_txn_sign = asset_config.sign(creator_sk)
    txn_id = client.send_transaction(asset_txn_sign)
    try:
        account_info = client.account_info(creator_pk)
    except Exception as e:
        print(e)
    return txn_id, account_info['assets']


def mnemonic_to_pskey(mnemonic_text):
    algo_sk = mnemonic.to_private_key(mnemonic_text)
    algo_pk = account.address_from_private_key(algo_sk)
    return algo_sk, algo_pk


def send_transaction(self_address, rcv_address, amount, algo_sk, asset_id):
    client = initialize_client()
    params = client.suggested_params()
    txn = AssetTransferTxn(
        sender=self_address,
        sp=params,
        receiver=rcv_address,
        amt=int(amount),
        index=int(asset_id)
    )

    stxn = txn.sign(algo_sk)
    txn_id = client.send_transaction(stxn)
    print(f"Transaction of {amount} to {rcv_address} from {self_address} is successful with id:{txn_id}")
    return txn_id


def get_balance(address, asset_id):
    j = 0
    balance = None
    client = initialize_client()
    account_info = client.account_info(address)
    for i in account_info['assets']:
        if i["asset-id"] == asset_id:
            balance = i["amount"]
            break
        else:
            pass
    if balance == None:
        return 0
    else:
        return balance


def generate_acc():
    address_sk, address = account.generate_account()
    mnemonic_data = mnemonic.from_private_key(address_sk)
    return address_sk, address, mnemonic_data


def acc_send1mil(address, acc_pk, acc_sk):
    client = initialize_client()
    params = client.suggested_params()
    txn = PaymentTxn(acc_pk, params, address, 1000000, None)
    stxn = txn.sign(acc_sk)
    client.send_transaction(stxn)
    print("successfully sent 1 million microAlgos")
    return 0


def auth_accasset(address, address_sk, asset_id):
    # This account must have atleast a minimum of 10000 microAlgos
    send_transaction(address, address, 0, address_sk, asset_id)
    return 0

