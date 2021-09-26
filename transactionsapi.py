import redis
import datetime
import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config['DEBUG'] = True

@app.route('/transactions/all', methods=['GET'])
def get_transactions():
    start_datetime = request.args.get('startDate')
    end_datetime = request.args.get('endDate')

    if start_datetime != None and end_datetime != None:
        start_date = datetime.datetime.timestamp(datetime.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%SZ"))
        end_date = datetime.datetime.timestamp(datetime.datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%SZ"))
    else:
        start_date = 0
        end_date = datetime.datetime.timestamp(datetime.datetime.now())
    payee_id = request.args.get('merchantId')
    currency = request.args.get('currency')
    valueTransactions = { 
        'amount' : 0,
        'currency' : currency
    }
    result = {
        'valueTransactions' : valueTransactions,
        'volumeTransactions' : 0
    }
    total_amount = 0
    try:
        r = redis.StrictRedis(decode_responses=True, host='ec2-52-54-111-142.compute-1.amazonaws.com', password="p48c33a294b3863689cc537475c27ec398a544c022216bb4122b3c6dd8c6ecc29", port=7090, ssl=True, ssl_cert_reqs=None)
        for key in r.scan_iter("*payment*",_type="HASH"):
            vals = r.hgetall(key)
            if 'payee_id' in vals and vals['payee_id'] == payee_id and 'currency' in vals and vals['currency'] == currency and 'created_at' in vals and float(vals['created_at']) > start_date and float(vals['created_at']) < end_date:
                if 'amount' in vals:
                    result['volumeTransactions'] += 1
                    valueTransactions['amount'] = valueTransactions['amount'] + float(vals['amount'])
                else:
                    continue
    except Exception as e:
        print(e)
    return(jsonify(result))
    

if __name__ == '__main__':
    app.run()