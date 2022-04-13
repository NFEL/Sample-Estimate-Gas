from web3 import Web3

rpc = "https://rpc.ftm.tools/"
w3 = Web3(Web3.HTTPProvider(rpc))

private_key = "01aa1bde721c4f3f88ffaff51b148dd32a8110450af9021c1c1777f38b0c0ead"

sender_wallet_address = w3.eth.account.privateKeyToAccount(private_key).address
print(sender_wallet_address)
proxy_address = "0x49B29B0f5c6Ac68094A9957E2cDcF54CD7B16554"

# tx ={
#             "from": sender_wallet_address,
#             "to": proxy_address,
#             "nonce": (
#                 w3
#                 .eth
#                 .get_transaction_count(sender_wallet_address)
#             ),
#             "gasPrice" :w3.eth.gas_price,
#             "data": '0x432d165b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000011bca70000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000021be370d5312f44cb42ce377bc9b8a0cef1a4c8300000000000000000000000004068da6c83afcfa0e13ba15a6696662335d5b750000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001c00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000006253f0ca00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000de0b6b3a764000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000143cb347acf464a36f3d2d01c7bf72fc6be4b4e7826f200000000000000000000',
#             "value": 0,
#         }

print(w3.eth.get_balance(sender_wallet_address))
    
tx = {
    "from": "0x5638f545C240E52920F49C035BA6e85846d229D6",
    "to": "0x49B29B0f5c6Ac68094A9957E2cDcF54CD7B16554",
    "data": "0x432d165b0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000011d585dcd807567d00000000000000000000000000000000000000000000000086cf9a00b62ee800000000000000000000000000fbfae0dd49882e503982f8eb4b8b1e464eca0b9100000000000000000000000021be370d5312f44cb42ce377bc9b8a0cef1a4c830000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000016000000000000000000000000000000000000000000000000000000000000001c000000000000000000000000000000000000000000000000000000000000000110000000000000000000000000000000000000000000000000000000073f783a5000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000086cf9a00b62ee8000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000014a5a8bd8e3cdf572e00050771ba66d3ee94571c126f200000000000000000000",
    "nonce": (
        w3
        .eth
        .get_transaction_count(sender_wallet_address)
    ),
    "gasPrice": w3.eth.gas_price,
    "value": 10 ** 18,
}
print(w3.eth.estimate_gas(tx))

# TODO from ftm -> tcs issue 

# signed_tx = w3.eth.account.sign_transaction(
#     tx,
#     private_key
# )
# tx_hash2 = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
# trx_2 = w3.eth.waitForTransactionReceipt(tx_hash2)