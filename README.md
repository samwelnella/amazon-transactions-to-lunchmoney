# amazon-transactions-to-lunchmoney

Use the [Amazon Order History Reporter](https://chrome.google.com/webstore/detail/amazon-order-history-repo/mgkilgclilajckgnedgjgnfdokkgnibi?hl=en) Chrome extension to export your Amazon order history to a CSV file. Name the CSV file 'amazon.csv' and store it in the same folder as this plugin.

Run the following python command where YOUR_LUNCH_MONEY_API_KEY_HERE is replaced with your Lunch Money API key:
```python 
keyring.set_password(service_id, 'lmauth', 'YOUR_LUNCH_MONEY_API_KEY_HERE')
```

When the script is run, it will try to match each Amazon transaction in Lunch Money to a transaction in your Amazon transaction history file. If a match is found, the "notes" field of the Lunch Money transaction will be set to title of the transaction item in the Amazon transaction history file.
