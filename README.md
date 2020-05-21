# amazon-transactions-to-lunchmoney

Download your Amazon transaction history as a CSV file from https://www.amazon.com/gp/b2b/reports and name it amazon.csv. Put the CSV file in the same folder as this python script. Change YOUR_LUNCH_MONEY_API_KEY_HERE and the start_date and end_date variables as appropriate.

When the script is run, it will try to match each Amazon transaction in Lunch Money to a transaction in your Amazon transaction history file. If a match is found, the "notes" field of the Lunch Money transaction will be set to title of the transaction item in the Amazon transaction history file.

The script attempts to match multi-item orders by combining all orders with the same order ID, adding the totals and concatenating the item titles.
