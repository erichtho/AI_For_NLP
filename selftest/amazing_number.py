"""
自测题二
"""

import sys
import getopt
def isAmazing(number):
    factor = []
    while number!=1:
        if number%2==0:
            number = number/2
            factor.append(2)
        elif number%3==0:
            number = number/3
            factor.append(3)
        elif number%5==0:
            number = number/5
            factor.append(5)
        else:
            return None
    return factor


if __name__=='__main__':
    argv = sys.argv[1:]
    number = 1
    try:
       opts, args = getopt.getopt(argv,"hn:",["number="])
    except getopt.GetoptError:
       print('amazing_number.py -n <number>')
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('amazing_number.py -n <number>')
            sys.exit()
        elif opt in ("-n", "--number"):
            number = int(arg)
        else:
            print('You shall specify the number. ')
            sys.exit(2)
    print(isAmazing(number))