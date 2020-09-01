import requests
import csv
import pandas
import keyring
from datetime import datetime
from datetime import timedelta
import calendar

service_id = 'AMAZON_TO_LM'

today = datetime.today()

print('Time range for transaction import?')
print('\n1) This month')
print('2) Last month')
print('3) Custom range\n')

while True:
	try:
		selection = int(input('Please choose: '))
	except ValueError:
		print('Please pick a valid choice')
		continue
	if not 0 < selection < 4:
		print('Please pick a valid choice')
		continue
	else:
		break

if selection == 1:
	start_date = str(today.date().replace(day=1).isoformat())
	end_date = str(today.date().isoformat())
elif selection == 2:
	start_date = today.date().replace(day=1)- timedelta(days=1)
	start_date = str(start_date.replace(day=1).isoformat())
	end_date = today.date().replace(day=1)- timedelta(days=1)
	end_date = str(end_date.isoformat())
elif selection == 3:
	while True:
		try:
			start_date = str(input('\nPlease enter start date [YYYY-MM-DD]:'))
			datetime.fromisoformat(start_date)
		except ValueError:
			print('Please format the date correctly')
			continue
		else:
			break
	while True:
		try:
			end_date = str(input('Please enter end date [YYYY-MM-DD]:'))
			datetime.fromisoformat(end_date)
		except ValueError:
			print('Please format the date correctly')
			continue
		else:
			break

print(start_date)
print(end_date)

#Set your lmauth variable with keyring.set_password(service_id, 'lmauth', 'YOUR_LUNCH_MONEY_API_KEY_HERE')
lmauth = keyring.get_password(service_id, 'lmauth')
headers = {'Authorization': 'Bearer {}'.format(lmauth)}
del lmauth

payload = {'start_date': start_date, 'end_date': end_date}

r = requests.get('https://dev.lunchmoney.app/v1/transactions', params = payload, headers = headers)
transactions = r.json()
amazon_transactions = [x for x in transactions['transactions'] if x['payee'] == 'Amazon' or x['payee'] == 'Amazon Prime' or x['payee'] == 'Amazon Marketplace' or x['payee'] == 'AMAZON.COM']
print(str(len(amazon_transactions)) + ' Lunch Money Amazon transactions found.')

transaction_id = []
transaction_note = []

amazon_purchases_single = csv.DictReader(open('amazon.csv', encoding='utf-8'))

#Repeat without combining items to get items where Amazon did not combine items in the same order ID in one transaction
for row in amazon_purchases_single:
	for x in amazon_transactions:
		payment_parse = row['payments'].split(':')
		if len(payment_parse) == 3:
			if float(x['amount']) == float(payment_parse[2].replace('$', '').replace(';', '').strip()):
				if timedelta(minutes=-2880) <= datetime.strptime(x['date'], '%Y-%m-%d') - datetime.strptime(payment_parse[1].strip(), '%B %d, %Y') <= timedelta(minutes=2880):
					transaction_id.append(x['id'])
					transaction_note.append(row['items'])

print(transaction_id)
print(transaction_note)
	
for x in range(len(transaction_id)):
	payload = {'transaction': {'notes': transaction_note[x]}}
	r = requests.put("https://dev.lunchmoney.app/v1/transactions/{}".format(transaction_id[x]), json = payload, headers=headers)
	print('Updating transaction ' + str(x+1) + '/' + str(len(transaction_id)))

del headers
