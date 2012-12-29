import sys
import math
from elevator import *

DOOR_OPEN_TIME = 10
FLOORS_PER_SECOND = 1
INITIAL_FLOOR = 1
WAIT_TIME = 1
INFINITY = 9999
BUSY_FLOORS = {0:0, 1:1, 10:0, 100:0} #key is each floor, value specifies whether an elevator has been assigned to that floor or not

class Guest(object):
	def __init__(self, id, startTime, startFloor, destinationFloor):
		self.id = id
		self.startTime = startTime
		self.startFloor = startFloor
		self.destinationFloor = destinationFloor
		self.waitTime = 0
		self.calledElevator = False
		self.onElevator = False

	def isGoingUp(self):
		return self.destinationFloor > self.startFloor

	def wait(self):
		self.waitTime += WAIT_TIME
		if self.onElevator:
			#pass
			print 'Guest', self.id, 'going to floor', self.destinationFloor, 'waiting for', self.waitTime, 'seconds, on elevator', self.onElevator
		else:
			#pass
			print 'Guest', self.id, 'starting on floor', self.startFloor, 'going to floor', self.destinationFloor, 'waiting for', self.waitTime, 'seconds, not on elevator yet'

	def addElevator(self, elevator):
		self.onElevator = elevator

	def __str__(self):
		return "ID: " + str(self.id) + " Start Time: " + str(self.startTime) + " Start Floor: " + str(self.startFloor) + " Destination Floor: " + str(self.destinationFloor) + " Waiting Time: " + str(self.waitTime)