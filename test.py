import json
import logging
import time
import requests
from dataclasses import dataclass
from web3 import Web3
from pprint import pp, pprint
# from .Constants import ABI


@dataclass
class ComparisionResult:
    Response: dict
    Gas: int

logging.basicConfig(level=logging.DEBUG)

def requset_parser(test_req, url) -> dict:
    res_1 = requests.post(url, json=test_req)
    if res_1.status_code == 200:
        res = res_1.json()
        if res.get('status_code') == 200:
            return res.get("result")
    raise ValueError(f"Bad response {res_1.json()}  {test_req}")


def swap_request(test_req, url) -> dict:
    return requset_parser(test_req, url + "/api/swap")


def find_request(test_req, url) -> dict:
    return requset_parser(test_req, url + "/api/find")


def estimate_gas(w3: Web3, trx_data: dict) -> int:
    trx_data.update(gasPrice=w3.eth.gas_price)
    trx_data.update(chainId=w3.eth.chain_id)
    try:
        trx_data.update(value=int(trx_data.get('value')))
    except Exception as  e:
        logging.exception(e)

    print("Gas Price: ", trx_data.get('gasPrice'))
    r = w3.eth.estimate_gas(trx_data)
    return r


def v1_result(test_req):
    w3 = Web3(Web3.HTTPProvider(ftm_rpc))
    find_res = find_request(test_req, url_1)
    swap_res = swap_request(test_req, url_1).get('transactions')[0]
    try:
        swap_res.pop('gas')
    except Exception as  e:
        logging.exception(e)
    gas = estimate_gas(w3, swap_res)
    return find_res, swap_res, gas


def v2_result(test_req):
    w3 = Web3(Web3.HTTPProvider(ftm_rpc))
    find_res = find_request(test_req, url_2)
    swap_res = swap_request(test_req, url_2)

    try:
        swap_res.update(
            {
                "from": test_req.get('walletAddress'),
                "to": swap_res.pop("router_address")
            }
        )
        swap_res.pop('state')

    except Exception as  e:
        logging.exception(e)
    gas = estimate_gas(w3, swap_res)
    return find_res, swap_res, gas


ftm_rpc = "https://rpc.ftm.tools/"
to_token = "0xFbfAE0DD49882e503982f8eb4b8B1e464ecA0b91"
from_token = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
amount = 50

url_1 = "https://timechainswap.com"
url_2 = "https://dev.tcswap.finance"


def test_ftm_to_tokens(test_req: dict, tokens: list):
    errors = {}
    results = {}
    for token in tokens:
        test_req['toToken'] = token
        pprint(
            f"Checking Tokens { test_req['fromToken']} to { test_req['toToken']}")
        try:
            r1 = v1_result(test_req)
        except Exception as e:
            r1 = [None, None, None]
            errors[token+"v1"] = e
        try:

            r2 = v2_result(test_req)
        except Exception as e:
            r2 = [None, None, None]
            errors[token+"v2"] = e

        pprint({"r1": r1[2], "r2": r2[2]})
        results[token] = {"r1": r1, "r2": r2}
        time.sleep(0.5)
    return results, errors


data = (
        test_ftm_to_tokens(
            {
                "fromToken": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
                "amount_in": 60,
                "chainId": 250,
                "slippage": 5,
                "walletAddress": "0x0cB225F3e02365E261CCB15d4fD63e38df7fbE81"
            },
            # Prod tokens list
            # Code is  [_.get('address') for _ in requests.get("https://timechainswap.com/api/tokens").json().get('result') ]
            ['0xFbfAE0DD49882e503982f8eb4b8B1e464ecA0b91', '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75', '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83', '0xf16e81dce15B08F326220742020379B855B87DF9', '0xD67de0e0a0Fd7b15dC8348Bb9BE742F3c5850454', '0x049d68029688eAbF473097a2fC38ef61633A3C7A', '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E', '0x5Cc61A78F164885776AA610fb0FE1257df78E59B', '0xE1C8f3d529BEa8E3fA1FAC5B416335a2f998EE1C', '0x82f0B8B456c1A451378467398982d4834b6829c1', '0xAd84341756Bf337f5a0164515b1f6F993D194E1f', '0xdDcb3fFD12750B45d32E084887fdf1aABAb34239', '0x74b23882a30290451A17c44f4F05243b6b58C76d', '0x09e145A1D53c0045F41aEEf25D8ff982ae74dD56', '0x321162Cd933E2Be498Cd2267a90534A804051b11', '0x6c021Ae822BEa943b2E66552bDe1D2696a53fbB7', '0x10b620b2dbAC4Faa7D7FFD71Da486f5D44cd86f9', '0xb3654dc3D10Ea7645f8319668E8F54d2574FBdC8', '0x8e4A2fA6e651DF75F7F4E9e9Ac81f8f9347a4aDD', '0x6a07A792ab2965C72a5B8088d3a069A7aC3a993B', '0xD0660cD418a64a1d44E9214ad8e459324D8157f1', '0x4cdF39285D7Ca8eB3f090fDA0C069ba5F4145B37', '0x657A1861c15A3deD9AF0B6799a195a249ebdCbc6',
                '0x85dec8c4B2680793661bCA91a8F129607571863d', '0xf61cCdE1D4bB76CeD1dAa9D4c429cCA83022B08B', '0xae75A438b2E0cB8Bb01Ec1E1e376De11D44477CC', '0xC5e2B037D30a390e62180970B3aa4E91868764cD', '0x1E4F97b9f9F913c46F1632781732927B9019C68b', '0xe0654C8e6fd4D733349ac7E09f6f23DA256bF475', '0x753fbc5800a8C8e3Fb6DC6415810d627A387Dfc9', '0x29b0Da86e484E1C0029B56e817912d778aC0EC69', '0xe64B9fd040D1F9D4715C645e0D567EF69958D3D9', '0xd6070ae98b8069de6B494332d1A1a81B6179D960', '0x9Ba3e4F84a34DF4e08C112e1a0FF148b81655615', '0x56ee926bD8c72B2d5fa1aF4d9E4Cbb515a1E3Adc', '0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE', '0xe2fb177009FF39F52C0134E8007FA0e4BaAcBd07', '0x91fa20244Fb509e8289CA630E5db3E9166233FDc', '0xF24Bcf4d1e507740041C9cFd2DddB29585aDCe1e', '0x627524d78B4fC840C887ffeC90563c7A42b671fD', '0x0789fF5bA37f72ABC4D561D00648acaDC897b32d', '0xFbc3c04845162F067A0B6F8934383E63899c3524', '0x0e121961DD741C9D49C9A04379da944A9D2FAc7a', '0x3b57f3FeAaF1e8254ec680275Ee6E7727C7413c7', '0xCD29c9F84924b96202eEB5Ad204bd0d0Fb47606c']
        ),
        test_ftm_to_tokens(
            {
                "fromToken": "0xFbfAE0DD49882e503982f8eb4b8B1e464ecA0b91",
                "amount_in": 60,
                "chainId": 250,
                "slippage": 5,
                "walletAddress": "0x1E1031581D0B7CC9c838d0cdCc5A6177Be8fE448"
            },
            # Prod tokens list
            # Code is  [_.get('address') for _ in requests.get("https://timechainswap.com/api/tokens").json().get('result') ]
            ['0xFbfAE0DD49882e503982f8eb4b8B1e464ecA0b91', '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75', '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83', '0xf16e81dce15B08F326220742020379B855B87DF9', '0xD67de0e0a0Fd7b15dC8348Bb9BE742F3c5850454', '0x049d68029688eAbF473097a2fC38ef61633A3C7A', '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E', '0x5Cc61A78F164885776AA610fb0FE1257df78E59B', '0xE1C8f3d529BEa8E3fA1FAC5B416335a2f998EE1C', '0x82f0B8B456c1A451378467398982d4834b6829c1', '0xAd84341756Bf337f5a0164515b1f6F993D194E1f', '0xdDcb3fFD12750B45d32E084887fdf1aABAb34239', '0x74b23882a30290451A17c44f4F05243b6b58C76d', '0x09e145A1D53c0045F41aEEf25D8ff982ae74dD56', '0x321162Cd933E2Be498Cd2267a90534A804051b11', '0x6c021Ae822BEa943b2E66552bDe1D2696a53fbB7', '0x10b620b2dbAC4Faa7D7FFD71Da486f5D44cd86f9', '0xb3654dc3D10Ea7645f8319668E8F54d2574FBdC8', '0x8e4A2fA6e651DF75F7F4E9e9Ac81f8f9347a4aDD', '0x6a07A792ab2965C72a5B8088d3a069A7aC3a993B', '0xD0660cD418a64a1d44E9214ad8e459324D8157f1', '0x4cdF39285D7Ca8eB3f090fDA0C069ba5F4145B37', '0x657A1861c15A3deD9AF0B6799a195a249ebdCbc6',
                '0x85dec8c4B2680793661bCA91a8F129607571863d', '0xf61cCdE1D4bB76CeD1dAa9D4c429cCA83022B08B', '0xae75A438b2E0cB8Bb01Ec1E1e376De11D44477CC', '0xC5e2B037D30a390e62180970B3aa4E91868764cD', '0x1E4F97b9f9F913c46F1632781732927B9019C68b', '0xe0654C8e6fd4D733349ac7E09f6f23DA256bF475', '0x753fbc5800a8C8e3Fb6DC6415810d627A387Dfc9', '0x29b0Da86e484E1C0029B56e817912d778aC0EC69', '0xe64B9fd040D1F9D4715C645e0D567EF69958D3D9', '0xd6070ae98b8069de6B494332d1A1a81B6179D960', '0x9Ba3e4F84a34DF4e08C112e1a0FF148b81655615', '0x56ee926bD8c72B2d5fa1aF4d9E4Cbb515a1E3Adc', '0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE', '0xe2fb177009FF39F52C0134E8007FA0e4BaAcBd07', '0x91fa20244Fb509e8289CA630E5db3E9166233FDc', '0xF24Bcf4d1e507740041C9cFd2DddB29585aDCe1e', '0x627524d78B4fC840C887ffeC90563c7A42b671fD', '0x0789fF5bA37f72ABC4D561D00648acaDC897b32d', '0xFbc3c04845162F067A0B6F8934383E63899c3524', '0x0e121961DD741C9D49C9A04379da944A9D2FAc7a', '0x3b57f3FeAaF1e8254ec680275Ee6E7727C7413c7', '0xCD29c9F84924b96202eEB5Ad204bd0d0Fb47606c']
        ),
        
        # FIND MOre Wallets
        test_ftm_to_tokens(
            {
                "fromToken": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
                "amount_in": 60,
                "chainId": 250,
                "slippage": 5,
                "walletAddress": "0x0cB225F3e02365E261CCB15d4fD63e38df7fbE81"
            },
            # Prod tokens list
            # Code is  [_.get('address') for _ in requests.get("https://timechainswap.com/api/tokens").json().get('result') ]
            ['0xFbfAE0DD49882e503982f8eb4b8B1e464ecA0b91', '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75', '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83', '0xf16e81dce15B08F326220742020379B855B87DF9', '0xD67de0e0a0Fd7b15dC8348Bb9BE742F3c5850454', '0x049d68029688eAbF473097a2fC38ef61633A3C7A', '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E', '0x5Cc61A78F164885776AA610fb0FE1257df78E59B', '0xE1C8f3d529BEa8E3fA1FAC5B416335a2f998EE1C', '0x82f0B8B456c1A451378467398982d4834b6829c1', '0xAd84341756Bf337f5a0164515b1f6F993D194E1f', '0xdDcb3fFD12750B45d32E084887fdf1aABAb34239', '0x74b23882a30290451A17c44f4F05243b6b58C76d', '0x09e145A1D53c0045F41aEEf25D8ff982ae74dD56', '0x321162Cd933E2Be498Cd2267a90534A804051b11', '0x6c021Ae822BEa943b2E66552bDe1D2696a53fbB7', '0x10b620b2dbAC4Faa7D7FFD71Da486f5D44cd86f9', '0xb3654dc3D10Ea7645f8319668E8F54d2574FBdC8', '0x8e4A2fA6e651DF75F7F4E9e9Ac81f8f9347a4aDD', '0x6a07A792ab2965C72a5B8088d3a069A7aC3a993B', '0xD0660cD418a64a1d44E9214ad8e459324D8157f1', '0x4cdF39285D7Ca8eB3f090fDA0C069ba5F4145B37', '0x657A1861c15A3deD9AF0B6799a195a249ebdCbc6',
             '0x85dec8c4B2680793661bCA91a8F129607571863d', '0xf61cCdE1D4bB76CeD1dAa9D4c429cCA83022B08B', '0xae75A438b2E0cB8Bb01Ec1E1e376De11D44477CC', '0xC5e2B037D30a390e62180970B3aa4E91868764cD', '0x1E4F97b9f9F913c46F1632781732927B9019C68b', '0xe0654C8e6fd4D733349ac7E09f6f23DA256bF475', '0x753fbc5800a8C8e3Fb6DC6415810d627A387Dfc9', '0x29b0Da86e484E1C0029B56e817912d778aC0EC69', '0xe64B9fd040D1F9D4715C645e0D567EF69958D3D9', '0xd6070ae98b8069de6B494332d1A1a81B6179D960', '0x9Ba3e4F84a34DF4e08C112e1a0FF148b81655615', '0x56ee926bD8c72B2d5fa1aF4d9E4Cbb515a1E3Adc', '0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE', '0xe2fb177009FF39F52C0134E8007FA0e4BaAcBd07', '0x91fa20244Fb509e8289CA630E5db3E9166233FDc', '0xF24Bcf4d1e507740041C9cFd2DddB29585aDCe1e', '0x627524d78B4fC840C887ffeC90563c7A42b671fD', '0x0789fF5bA37f72ABC4D561D00648acaDC897b32d', '0xFbc3c04845162F067A0B6F8934383E63899c3524', '0x0e121961DD741C9D49C9A04379da944A9D2FAc7a', '0x3b57f3FeAaF1e8254ec680275Ee6E7727C7413c7', '0xCD29c9F84924b96202eEB5Ad204bd0d0Fb47606c']
        ),
        test_ftm_to_tokens(
            {
                "fromToken": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
                "amount_in": 60,
                "chainId": 250,
                "slippage": 5,
                "walletAddress": "0x0cB225F3e02365E261CCB15d4fD63e38df7fbE81"
            },
            # Prod tokens list
            # Code is  [_.get('address') for _ in requests.get("https://timechainswap.com/api/tokens").json().get('result') ]
            ['0xFbfAE0DD49882e503982f8eb4b8B1e464ecA0b91', '0x04068DA6C83AFCFA0e13ba15A6696662335D5B75', '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83', '0xf16e81dce15B08F326220742020379B855B87DF9', '0xD67de0e0a0Fd7b15dC8348Bb9BE742F3c5850454', '0x049d68029688eAbF473097a2fC38ef61633A3C7A', '0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E', '0x5Cc61A78F164885776AA610fb0FE1257df78E59B', '0xE1C8f3d529BEa8E3fA1FAC5B416335a2f998EE1C', '0x82f0B8B456c1A451378467398982d4834b6829c1', '0xAd84341756Bf337f5a0164515b1f6F993D194E1f', '0xdDcb3fFD12750B45d32E084887fdf1aABAb34239', '0x74b23882a30290451A17c44f4F05243b6b58C76d', '0x09e145A1D53c0045F41aEEf25D8ff982ae74dD56', '0x321162Cd933E2Be498Cd2267a90534A804051b11', '0x6c021Ae822BEa943b2E66552bDe1D2696a53fbB7', '0x10b620b2dbAC4Faa7D7FFD71Da486f5D44cd86f9', '0xb3654dc3D10Ea7645f8319668E8F54d2574FBdC8', '0x8e4A2fA6e651DF75F7F4E9e9Ac81f8f9347a4aDD', '0x6a07A792ab2965C72a5B8088d3a069A7aC3a993B', '0xD0660cD418a64a1d44E9214ad8e459324D8157f1', '0x4cdF39285D7Ca8eB3f090fDA0C069ba5F4145B37', '0x657A1861c15A3deD9AF0B6799a195a249ebdCbc6',
             '0x85dec8c4B2680793661bCA91a8F129607571863d', '0xf61cCdE1D4bB76CeD1dAa9D4c429cCA83022B08B', '0xae75A438b2E0cB8Bb01Ec1E1e376De11D44477CC', '0xC5e2B037D30a390e62180970B3aa4E91868764cD', '0x1E4F97b9f9F913c46F1632781732927B9019C68b', '0xe0654C8e6fd4D733349ac7E09f6f23DA256bF475', '0x753fbc5800a8C8e3Fb6DC6415810d627A387Dfc9', '0x29b0Da86e484E1C0029B56e817912d778aC0EC69', '0xe64B9fd040D1F9D4715C645e0D567EF69958D3D9', '0xd6070ae98b8069de6B494332d1A1a81B6179D960', '0x9Ba3e4F84a34DF4e08C112e1a0FF148b81655615', '0x56ee926bD8c72B2d5fa1aF4d9E4Cbb515a1E3Adc', '0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE', '0xe2fb177009FF39F52C0134E8007FA0e4BaAcBd07', '0x91fa20244Fb509e8289CA630E5db3E9166233FDc', '0xF24Bcf4d1e507740041C9cFd2DddB29585aDCe1e', '0x627524d78B4fC840C887ffeC90563c7A42b671fD', '0x0789fF5bA37f72ABC4D561D00648acaDC897b32d', '0xFbc3c04845162F067A0B6F8934383E63899c3524', '0x0e121961DD741C9D49C9A04379da944A9D2FAc7a', '0x3b57f3FeAaF1e8254ec680275Ee6E7727C7413c7', '0xCD29c9F84924b96202eEB5Ad204bd0d0Fb47606c']
        ),
    )


with open('log.txt','w') as f:
    json.dump(data , f)
