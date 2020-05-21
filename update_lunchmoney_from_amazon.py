import requests
import csv
import pandas
from datetime import datetime
from datetime import timedelta

headers = {'Authorization': 'Bearer YOUR_LUNCH_MONEY_API_KEY_HERE'}
payload = {'start_date': '2016-01-01', 'end_date': '2020-05-20'}

r = requests.get('https://dev.lunchmoney.app/v1/transactions', params = payload, headers = headers)
transactions = r.json()
amazon_transactions = [x for x in transactions['transactions'] if x['payee'] == 'Amazon']

amazon_purchases = pandas.read_csv('amazon.csv', header = 0, encoding='utf8')
amazon_purchases['Item Total'] = amazon_purchases['Item Total'].str.replace(',', '').str.replace('$', '').astype(float)
amazon_purchases['Title'] = amazon_purchases['Title'].astype(str)
amazon_purchases['Total Price'] = amazon_purchases.groupby(['Order ID'])['Item Total'].transform('sum')
amazon_purchases['Title Cat'] = amazon_purchases.groupby(['Order ID'])['Title'].transform(lambda x: '; '.join(x))
amazon_purchases = amazon_purchases.drop_duplicates(['Order ID'])
amazon_purchases.to_csv('amazon_nodupe.csv', encoding='utf-8', index=False)

amazon_purchases_nodupe = csv.DictReader(open('amazon_nodupe.csv', encoding='utf-8'))

transaction_id = []
transaction_note = []

for row in amazon_purchases_nodupe:
	for x in amazon_transactions:
		if float(x['amount']) == float(row['Total Price'].replace('$', '')):
			if timedelta(minutes=-2880) <= datetime.strptime(x['date'], '%Y-%m-%d') - datetime.strptime(row['Order Date'], '%m/%d/%y') <= timedelta(minutes=2880):
				transaction_id.append(x['id'])
				transaction_note.append(row['Title Cat'])

for x in range(len(transaction_id)):
	payload = {'transaction': {'notes': transaction_note[x]}}
	r = requests.put("https://dev.lunchmoney.app/v1/transactions/{}".format(transaction_id[x]), json = payload, headers=headers)
	print('Updating transaction ' + str(x+1) + '/' + str(len(transaction_id)))
