#!/usr/bin/env python

from Num2Word import numToWords, numToPlace, yearToWords, floatToWords

import os, argparse
import re


def trans_year(s):
	if s[-1] == 's':
		return yearToWords(s[0:-1]) + 's'
	return yearToWords(s)


def trans_money(s):
	return floatToWords(s[1:]) + ' dollar'


def trans_fraction(s):
	a1, a2 = s.split('/')
	n1 = int(a1)
	n2 = int(a2)
	if n1 < n2:
		return numToWords(n1) + ' ' + numToPlace(n2)
	else:
		return numToWords(n1) + ' ' + numToWords(n2)


def trans_time(s):
	a1, a2 = s.split(':')
	s1 = numToWords(a1)
	s2 = numToWords(a2)
	if s2 != 'zero':
		s1 += ' ' + s2
	return s1


def trans_int(s):
	return numToWords(''.join(s.split(',')))


def trans_place(s):
	return numToPlace(''.join(s[0:-2].split(',')))


def trans_digits(s):
	p = re.compile('\d')
	res = ''
	for c in list(s):
		if p.match(c):
			res += numToWords(c)
		else:
			res += c
	return res


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--text', help='the input text', type=str)
	parser.add_argument('--output', help='write the text', type=str)
	parser.add_argument('--log', help='the log information', type=str, default='process_text.log')
	args = parser.parse_args()

	assert os.path.exists(args.text), 'no file: %s' % args.text

	pattern_list = [
		('year', re.compile('^((15|16|17|18|19|20|21)\d{2}s?|\d{2}s)$'), trans_year),  # year
		('int', re.compile('^[,\d]+$'), trans_int),		 # integer, e.g. 10, 23
		('float', re.compile('^\d+\.\d+$'), floatToWords),		 # float, e.g. 10.2, 3.4
		('place', re.compile('^\d+(st|nd|rd|th)$'), trans_place),   # e.g. 10th, 21st, 22nd, 32rd
		('time', re.compile('^\d{1,2}:\d{1,2}$'), trans_time),   # time, 7:00, 12:30
		('money', re.compile('^\$(\d+|\d+\.\d+)$'), trans_money),   # $1, $10, $9.5
		('faction', re.compile('^\d+/\d+$'), trans_fraction),  # 24/7
		('unknown', re.compile('^\D*\d+\D*'), trans_digits),   # others u2, 4g ...
		]
	with open(args.text) as f, open(args.output, 'wt') as fout, open(args.log, 'wt') as flog:
		for line in f:

			# no digits
			if not re.findall('\d+', line):
				fout.write(line)
				continue

			res_w = []
			for w in line.split():
				if not re.findall('\d+', w):
					res_w.append(w)
				else:
					new_w = w
					is_trans = False
					trans_name = None
					for name, p, fun in pattern_list:
						if p.match(w):
							new_w = fun(w)
							is_trans = True
							trans_name = name
							break

					if not is_trans:
						raise TypeError('unknown %s in %s\n' % (w, line[0:-1]))
					else:
						flog.write('[%s] replace %s -> %s in %s\n' % (trans_name, w, new_w, line[0:-1]))
					flog.flush()
					res_w.append(new_w)

			fout.write(' '.join(res_w) + '\n')
			fout.flush()


if __name__ == '__main__':
	main()
