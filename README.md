##  ROUTER - AGGregator TEST
Here are some test cases for router and aggregator :
#### TEST Senarios *V1*
This is production api [ **https://timechainswap.com/swagger** ]
- *AggregatorV1* 
  - Find relation from all token [ **/find** ]
    - fetch token list [ **/tokens** ]
    - check if for all source tokens, api can find amountOut for destination token
  - comapring amountOut for following price ranges
    - 1 $
    - 10 $
    - 100 $
    - 10_000 $
  - success rate of api
    - status_code in api respose beeing 200 
    - how many times api gave unrelated results and why
    - Which Reponses take more than 5s [ **API TIME OUT**] 
  - SWAP data generatrion
    - For each find request, check if raw data can be generated [ **/swap** ] 
    - Error log [ **graylog** ]
- *RouterV1* 
  - This router is in production and raw data is feeded using api 
  - Calculate Gas Fee 
    - Must use estimate_gas of rpc 
      - to compare how much gas this transaction is going to consume 
      - [*ATTENTION*] gas_price in generated must be the same as in other trasnaction
        - Gas_price is a rpc method gas_price() that shows the ideal gas price next block should have
        - trasnaction gas price is calculated as in gas_price * gas_used[**Op codes ran in transaction**] 
  - Compare
#### TEST Senarios *V2*
This is production api [ **http://qa.tcswap.finance/api/docs** ]
- *AggregatorV2* 
  - Find relation from all token [ **/find** ]
    - fetch token list [ **/tokens** ]
    - check if for all source tokens, api can find amountOut for destination token
  - comapring amountOut for following price ranges
    - 1 $
    - 10 $
    - 100 $
    - 10_000 $
  - success rate of api
    - status_code in api respose beeing 200 
    - how many times api gave unrelated results and why
    - Which Reponses take more than 5s [ **API TIME OUT**] 
  - SWAP data generatrion
    - For each find request, check if raw data can be generated [ **/swap** ] 
    - Error log [ **graylog** ]
    - [**V2 special**] in each created transaction a bitmap is created
      - check if bitmap is within correct range
        - Visit [Contract info](https://github.com/Timechainapp/timechainswap-contracts/blob/main/readme.md) 
- *RouterV2* 
  - This router is in qa stage and raw data is feeded from api 
  - Calculate Gas Fee 
    - Must use estimate_gas of rpc 
      - to compare how much gas this transaction is going to consume 
      - [*ATTENTION*] gas_price in generated must be the same as in other trasnaction
        - Gas_price is a rpc method gas_price() that shows the ideal gas price next block should have
        - trasnaction gas price is calculated as in gas_price * gas_used[**Op codes ran in transaction**] 
      - While estimating gas Contract log contract logic errors
        - most common issue is trasnfer_from fail 
          - Not giving approve to spender contract raises this issue
        - Worst is execution reverted which unknown errors 
          - must be loged to further check router contract
        - Other is 96-bit issue on tokens with 96-bit uint 
          - Under debugging or now  
##### Comapre Trasanction gas
In this test we should estimate gas on successful transactions and compare results from both routerV1 and routerV2 for identical request
