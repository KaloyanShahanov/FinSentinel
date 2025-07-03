def check_alerts(transactions, client_profiles):
    alerts = []
    for txn in transactions:
        client = client_profiles.get(txn['client_id'], {})
        if txn['amount'] > 10000 and client.get('country') == 'X':
            alerts.append({
                "client_id": txn['client_id'],
                "amount": txn['amount'],
                "reason": "High value transaction from Country X"
            })
    return alerts