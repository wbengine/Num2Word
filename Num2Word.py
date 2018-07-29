#!/usr/bin/env python

"""
Numbers to Words by Christopher Scott
http://www.scottdchris.com/

Program takes an integer as an input and returns the word representation of the integer.
Works up to 999,999,999
Program begins by parsing number to array of digits with numToArray mehtod
"""

units = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',]
teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
thous = ['hundred', 'thousand', 'million', 'billion']

places = ['zeroth', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth']
teenPlaces = ['tenth', 'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth']
tensPlaces = ['', 'tenth', 'twentieth', 'thirtieth', 'fortieth', 'fifthieth', 'sixthieth', 'seventieth', 'eightieth', 'ninetieth']
thouPlaces = ['hundredth', 'thousandth', 'millionth', 'billionth']

def numToArray(num):
	numArray = []
	while num > 0:
		numArray.append(num % 10)
		num = int(num / 10)

	if not numArray:
		return [0]
	return numArray

def hasTrailingZeros(numArray):
	if (numArray[6]!=0):
		return numArray[7]==0 and numArray[8]==0
	elif (numArray[3]!=0 or numArray[4]!=0 or numArray[5]!=0):
		return numArray[6]==0 and numArray[7]==0 and numArray[8]==0
	elif (numArray[0]!=0 or numArray[1]!=0 or numArray[2]!=0):
		return numArray[3]==0 and numArray[4]==0 and numArray[5]==0 and numArray[6]==0 and numArray[7]==0 and numArray[8]==0

def arrayToWords(numArray, units=units, teens=teens, tens=tens, thous=thous):
	if not numArray:
		return []

	words = []
	if len(numArray) == 1:
		words = [ units[numArray[0]] ]

	elif len(numArray) == 2:
		if numArray[1] == 1:
			words = [ teens[numArray[0]] ]
		else:
			words.append(tens[numArray[1]])
			if numArray[0] != 0:
				words.append(units[numArray[0]])

	elif len(numArray) == 3:
		if numArray[2] > 0:
			words.append(units[numArray[2]])
			words.append(thous[0])
		words += arrayToWords(numArray[0:2], units, teens, tens, thous)

	else:
		for i in range(0, len(numArray), 3):
			a = arrayToWords(numArray[i: i+3], units, teens, tens, thous)
			if i > 0 and a:
				a.append(thous[int(i/3)])
			words = a + words

	return [s for s in words if s != '']


def numToWords(num):
	if isinstance(num, str):
		num = int(num)
	return ' '.join(arrayToWords(numToArray(num), units, teens, tens, thous))

def numToPlace(num):
	if isinstance(num, str):
		num = int(num)
	a = arrayToWords(numToArray(num), units, teens, tens, thous)
	wlist = units + teens + tens + thous
	plist = places + teenPlaces + tensPlaces + thouPlaces
	a[-1] = plist[wlist.index(a[-1])]
	return ' '.join(a)

def yearToWords(num):
	if isinstance(num, str):
		num = int(num)
	numArray = numToArray(num)
	if len(numArray) == 4:
		return ' '.join(arrayToWords(numArray[2:]) + arrayToWords(numArray[0: 2]))
	elif len(numArray) == 2:
		return ' '.join(arrayToWords(numArray))
	else:
		raise TypeError('this is not a legal Year: %d' % num)

def floatToWords(s):
	if not isinstance(s, str):
		s = str(s)

	if s.find('.') == -1:
		return numToWords(s)

	n, d = s.split('.')
	n = numToWords(n)
	d = ' '.join([units[int(c)] for c in d])
	return n + ' point ' + d

def main(number):
	print('Word:\t%s' % numToWords(number))
	print('Place:\t%s' % numToPlace(number))

if __name__ == '__main__':
	print(yearToWords(str(1959)))

