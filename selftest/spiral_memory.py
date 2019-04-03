
"""
自测题一
"""
import math
import sys
import getopt
def getLocationOfSpiral(number):
    # 1. find nearest squar of odd
    s = math.floor(math.sqrt(number))
    s = s if s%2==1 else s-1
    return abs((s+1)/2-number+s*s+math.floor((number-s*s)/(s+1))*(s+1))+(s+1)/2



if __name__=='__main__':
    argv = sys.argv[1:]
    number = 1
    try:
       opts, args = getopt.getopt(argv,"hn:",["number="])
    except getopt.GetoptError:
       print('spiral_memory.py -n <number>')
       sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('spiral_memory.py -n <number>')
            sys.exit()
        elif opt in ("-n", "--number"):
            number = int(arg)
        else:
            print('You shall specify the number. ')
            sys.exit(2)
    print(getLocationOfSpiral(number))