# calc_my_coins

*calc_my_coins* is a simple Python script that can calculate your coins instead of you.

*calc_my_coins* will parse a file that stores your coins info (coin denomination, amount, etc...) and display the final result, which is nothing but the sum of your coins.

To understand the syntax of the file that will be parsed, and what you're going to write inside it, take a look at the included demo file "coins". It has some comments inside which make the information required clear.

*calc_my_coins* might be simple but it has **strong** error handling, feel free to feed any kind of corner cases or such!

## Usage:
`calc_my_coins.py file token`,

`calc_my_coins.py file`,

`calc_my_coins.py token` or

`calc_my_coins.py`

`file` is the filename you want to be processed. If not specified, default to "coins" (the demo file)

`token` is a **single-character** string. If not specified, default to ':'

Notice that, the last command will actually run the script on the demo file with the default token.
