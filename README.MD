Create an API request that will take as parameter the date range, the currency and the merchantId  and will give back the volume of transactions and the value of the amount for all transactions (sum of all amounts) for the given date range. The data for the calculation will be fetched from a Redis database

```
GET @ /transactions/all:
-startDate and endDate (optional) if not there then we should get the results for all time.
Sample request payload
{
"merchantId": “1234567890”,
"currency": "GBP”,
"startDate": "2021-08-20T00:00:00Z"
"endDate": "2021-08-21T00:00:00Z"
}
RESPONSE:
{
"valueTransactions" : { "amount" : "1000",
"currency": "GBP"}
"volumeTransactions": 33
}

To connect to Redis use the following:
URI: redis://:p48c33a294b3863689cc537475c27ec398a544c022216bb4122b3c6dd8c6ecc29@ec2-52-54-111-142.compute-1.amazonaws.com:7090
```