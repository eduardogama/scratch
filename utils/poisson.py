import sys
import math
import random


RAND_MAX = 0

def nextTime(rateParameter, RAND_MAX=0):
    return -math.log(1.0 - random.random()/(RAND_MAX + 1)) / rateParameter


def main():
    
    n = int(sys.argv[1])
    for i in range(n):
        val = nextTime(1/5.0, RAND_MAX)
        print(val)


if __name__ == '__main__':
    sys.exit(main())

