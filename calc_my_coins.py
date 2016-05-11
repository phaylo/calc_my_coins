### Calculate TL coins ###
### Python 2.6         ###


import os.path  # os.path.isfile
import sys      # sys.argv


# Token and initial file name constants
TOKEN = ':'
FILE = "coins"

# Type and comment constants
WHOLE = 'w'
FRACTIONS = 'f'
COMMENT = '#'


# Reserved character that can not be used as token
RESERVED = [
            WHOLE, FRACTIONS, COMMENT,
            0, 1, 2, 3, 4,
            5, 6, 7, 8, 9
           ]


## Exceptions ##

class FileNotFoundError(IOError):
	""" Thrown when the required is not found """
	pass


class ParseError(RuntimeError):
	""" Thrown when we can not parse the file correctly"""
	pass


class ReservedTokenError(RuntimeError):
	""" Thrown when a reserved has been used """
	pass


class InvalidTypeError(RuntimeError):
	""" Thrown when the parser detects invalid type """
	pass


class InvalidAmountError(RuntimeError):
	""" Thrown when the parser detects invalid amount """
	pass


class InvalidDenominationError(RuntimeError):
	""" Thrown when the parser detects invalid denomination """
	pass


class NaNError(RuntimeError):
	""" Thrown when a number (supposed to be) required to calculate the result is NaN """
	pass


def check_token(token):
	""" Check if the token is reserved """

	if token in RESERVED:
		raise ReservedTokenError("Error: Use of reserved tokens: " + str(RESERVED))


def calc_coins(coin_file = FILE, token = TOKEN):
	"""
	Calculate TL coins, info must be stored in a file

	:param coin_file: filename to be processed
	:param token: token used to split each line
	:type coin_file: string
	:type toke: single-character string
	:return: total money from the processed TL coins info
	:rtype: float
	"""

	# Checking coin_file type
	if not isinstance(coin_file, str):
		raise TypeError("coin_file must be a string")

	# Checking token type
	if not isinstance(token, str):
		raise TypeError("token must be a string")


	# Check if token is really a single-character string
	if len(token) != 1:
		raise ValueError("Token must be a single-character string")

	# Check if coin_file exist
	if not os.path.isfile(coin_file):
		raise FileNotFoundError(coin_file + " does not exist")


	# Open the file
	with open(coin_file) as money:

		# Final result
		result = 0.0

		# Line number
		line_num = 1

		# Read each line
		for line in money:

			# Remove all white spaces
			temp = line.strip()
			temp = temp.translate(None, ' ')

			# Ignore inline comments:
			comment_index = temp.find(COMMENT)
			temp = temp if comment_index == -1 else temp[:comment_index]

			# Skip  blank lines
			if len(temp) == 0:
				line_num += 1
				continue

			# Parse the file and get the info
			tl_info = temp.split(token)

			# Wrong structure?
			if len(tl_info) != 3:
				line_num += 1  
				raise ParseError("Invalid syntax --> [" + str(line_num - 1) + "] " + line)

			# Get the denomination, amount and type of a coin
			tl_denomination = tl_info[0]
			tl_amount = tl_info[1]
			tl_type = tl_info[2]


			## Check for any error concerns denomination, amount or type ##


			# Unknown coin type?
			if (tl_type != WHOLE and tl_type != FRACTIONS):
				line_num += 1  
				raise InvalidTypeError("Unknown coin type --> [" + str(line_num - 1) + "] " + line)

			# Amount is a float, negative or not a number?
			if not tl_amount.isdigit() or tl_amount == 0:  # isdigit can also detect signs
				line_num += 1  
				raise InvalidAmountError("Invalid amount --> [" + str(line_num - 1) + "] " + line)

			# Denomination is a float, negative or not a number?
			if not tl_denomination.isdigit() or tl_denomination == 0:  # isdigit can also detect signs
				line_num += 1  
				raise InvalidDenominationError("Invalid denomination --> [" + str(line_num - 1) + "] " + line)


			## Calculate the result ##


			# Whole
			if (tl_type == WHOLE):

				for i in xrange(int(tl_amount)):
					result += float(tl_denomination)

			# Fractions
			elif (tl_type == FRACTIONS):
				for i in xrange(int(tl_amount)):
					result += float(tl_denomination) / 100.0


			# Protect from a nasty "nan" exploit... (one could write 'nan' as denomination)
			if result == float('nan'):
				raise NaNError("One or more denomination IS a nan literally...")

			# Increment line_num
			line_num += 1

		# Return the result
		return result


if __name__ == "__main__":

	# Get the length of command line arguments
	argc = len(sys.argv)

	try:

		# Help!
		if argc == 2 and sys.argv[1] == "--help":
			print "  Usage: 'calc_my_coins.py file token'                     OR"
			print "         'calc_my_coins.py file' (default token is ':')    OR"
			print "         'calc_my_coins.py token' (default file is 'coins' OR"
			print "         'calc_my_coins.py' (default file is 'coins'and token is ':')"

		# No arguments
		elif argc == 1:
			print calc_coins()

		# One single-character string argument
		elif argc == 2 and len(sys.argv[1]) == 1:
			check_token(sys.argv[1])
			print calc_coins(token=sys.argv[1])

		# One non single-character string argument
		elif argc == 2:
			print calc_coins(sys.argv[1])

		# Two arguments
		elif argc == 3:
			check_token(sys.argv[2])
			print calc_coins(sys.argv[1], sys.argv[2])

		# else, display usage... they are doing it wrong
		else:
			print "  Usage: 'calc_my_coins.py file token'                     OR"
			print "         'calc_my_coins.py file' (default token is ':')    OR"
			print "         'calc_my_coins.py token' (default file is 'coins' OR"
			print "         'calc_my_coins.py' (default file is 'coins'and token is ':')"

	# Catch any known errors
	except (
			FileNotFoundError,
			ParseError,
			ReservedTokenError,
			InvalidTypeError,
			InvalidAmountError,
			InvalidDenominationError,
			NaNError) as err:
		print err.message,

	# Not a known error? let the default handler handle it
	except:
		print "\nUnhandled exception\n",
		raise
