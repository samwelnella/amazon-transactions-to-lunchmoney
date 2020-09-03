# amazon-transactions-to-lunchmoney

A tool for populating [Lunch Money](https://lunchmoney.app) Amazon transaction items with the name of item(s) bought.

Use the [Amazon Order History Reporter](https://chrome.google.com/webstore/detail/amazon-order-history-repo/mgkilgclilajckgnedgjgnfdokkgnibi?hl=en) Chrome extension to export your Amazon order history to a CSV file. Name the CSV file 'amazon.csv' and store it in the same folder as this plugin.

When the script is run for the first time it will prompt you enter your Lunch Money API key for safe storage in your operating system's keyring. It will then try to match each Amazon transaction in Lunch Money to a transaction in your Amazon transaction history file. If a match is found, the "notes" field of the Lunch Money transaction will be set to title of the transaction item in the Amazon transaction history file.
