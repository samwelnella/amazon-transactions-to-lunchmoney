import requests
import csv
import pandas
import keyring
import re
from datetime import datetime
from datetime import timedelta
import calendar

service_id = 'AMAZON_TO_LM'

#On first run store the Lunch Money API key in the OS keyring. If this needs to be changed later you can change the API key with keyring.set_password(service_id, 'lmauth', 'YOUR_LUNCH_MONEY_API_KEY_HERE')
if not keyring.get_password(service_id, 'lmauth'):
	print('Lunch money API key not found.')
	apikey = str(input('Please enter your Lunch Money API key for secure storage in your operating system\'s keyring: '))
	keyring.set_password(service_id, 'lmauth', apikey)
	del apikey

today = datetime.today()

print('Time range for transaction import?')
print('\n1) This month')
print('2) Last month')
print('3) All time')
print('4) Custom range\n')

while True:
	try:
		selection = int(input('Please choose: '))
	except ValueError:
		print('Please pick a valid choice')
		continue
	if not 0 < selection < 5:
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
	start_date = str(datetime.fromisoformat('1994-07-05'))
	end_date = str(today.date().isoformat())
elif selection == 4:
	while True:
		try:
			start_date = str(input('\nPlease enter start date [YYYY-MM-DD]: '))
			datetime.fromisoformat(start_date)
		except ValueError:
			print('Please format the date correctly')
			continue
		else:
			break
	while True:
		try:
			end_date = str(input('Please enter end date [YYYY-MM-DD]: '))
			datetime.fromisoformat(end_date)
		except ValueError:
			print('Please format the date correctly')
			continue
		else:
			break

lmauth = keyring.get_password(service_id, 'lmauth')
headers = {'Authorization': 'Bearer {}'.format(lmauth)}
del lmauth

payload = {'start_date': start_date, 'end_date': end_date}

r = requests.get('https://dev.lunchmoney.app/v1/transactions', params = payload, headers = headers)
transactions = r.json()
amazon_transactions = [x for x in transactions['transactions'] if re.match('(?i)(Amazon|AMZN)(\s(Prime|Marketplace|MKTP)|\.\w+)?',x['payee'])]
print(str(len(amazon_transactions)) + ' Lunch Money Amazon transactions found.')

transaction_id = []
transaction_note = []

amazon_purchases_single = csv.DictReader(open('amazon.csv', encoding='utf-8'))

#Repeat without combining items to get items where Amazon did not combine items in the same order ID in one transaction
for row in amazon_purchases_single:
	for x in amazon_transactions:
		payment_parse = row['payments'].split(':')
		if len(payment_parse) == 3:
			if float(x['amount']) == float(re.sub('[^\d\.]+','',payment_parse[2])):
				if timedelta(minutes=-2880) <= datetime.strptime(x['date'], '%Y-%m-%d') - datetime.strptime(payment_parse[1].strip(), '%B %d, %Y') <= timedelta(minutes=2880):
					transaction_id.append(x['id'])
					transaction_note.append(row['items'])

for x in range(len(transaction_id)):
	payload = {'transaction': {'notes': transaction_note[x]}}
	r = requests.put("https://dev.lunchmoney.app/v1/transactions/{}".format(transaction_id[x]), json = payload, headers=headers)
	print('Updating transaction ' + str(x+1) + '/' + str(len(transaction_id)))

del headers
