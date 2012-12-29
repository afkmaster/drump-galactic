import sys
import math
from guest import *
from elevator import *
from simulator import*

DEFAULT_FILE = './elevator_traffic_0.txt'
DOOR_OPEN_TIME = 10
FLOORS_PER_SECOND = 1
INITIAL_FLOOR = 1
WAIT_TIME = 1
INFINITY = 9999
BUSY_FLOORS = {0:0, 1:1, 10:0, 100:0} #key is each floor, value specifies whether an elevator has been assigned to that floor or not

def parseData(inputFile):
	f = open(inputFile, 'r')
	inputData = []
	for line in f:
		inputData.append(line.strip().split(','))
	f.close()
	inputData = [map(int, x) for x in inputData]
	return inputData

if __name__ == "__main__":
	if len(sys.argv) > 1:
		inputFile = sys.argv[1]
	else:
		inputFile = DEFAULT_FILE
	inputData = parseData(inputFile)
	Simulator(inputData)