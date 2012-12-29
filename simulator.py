import sys
import math
from guest import *
from elevator import *

DOOR_OPEN_TIME = 10
FLOORS_PER_SECOND = 1
INITIAL_FLOOR = 1
WAIT_TIME = 1
INFINITY = 9999
BUSY_FLOORS = {0:0, 1:1, 10:0, 100:0} #key is each floor, value specifies whether an elevator has been assigned to that floor or not

class Simulator(object):
	def __init__(self, inputData):
		self.inputData = inputData
		self.elevators = []
		self.guests = []
		self.activeGuests = {}
		self.elevators = [Elevator(i) for i in range(4)]

		guestId = 0
		for guest in inputData:
			startTime = guest[0]
			startFloor = guest[1]
			destinationFloor = guest[2]
			newGuest = Guest(guestId, startTime, startFloor, destinationFloor)
			self.guests.append(newGuest)
			guestId += 1

		self.run()

	def allElevatorsEmpty(self):
		for elevator in self.elevators:
			if elevator.guests or elevator.guestsQueue:
				return True
		return False

	def findBestElevator(self, guest):
		bestElevator = None
		shortestWait = INFINITY
		for elevator in self.elevators:
			if elevator.isActive:
				if (len(elevator.guestsQueue) > 0 and guest.isGoingUp() != elevator.guestsQueue[elevator.guestsQueue.keys()[0]].isGoingUp()):
					continue
				if guest.isGoingUp() and elevator.isGoingUp and elevator.currentFloor <= guest.startFloor:
					if elevator.DoorIsOpen:
						if (guest.startFloor - elevator.currentFloor + DOOR_OPEN_TIME - elevator.doorOpenTime) < shortestWait:
							shortestWait = guest.startFloor - elevator.currentFloor + DOOR_OPEN_TIME - elevator.doorOpenTime
							bestElevator = elevator
					else:
						if (guest.startFloor - elevator.currentFloor) < shortestWait:
							shortestWait = guest.startFloor - elevator.currentFloor
							bestElevator = elevator
				elif (not guest.isGoingUp()) and (not elevator.isGoingUp) and elevator.currentFloor >= guest.startFloor:
					if elevator.DoorIsOpen:
						if (elevator.currentFloor - guest.startFloor + DOOR_OPEN_TIME - elevator.doorOpenTime) < shortestWait:
							shortestWait = elevator.currentFloor - guest.startFloor + DOOR_OPEN_TIME - elevator.doorOpenTime
							bestElevator = elevator
					else:
						if (elevator.currentFloor - guest.startFloor) < shortestWait:
							shortestWait = elevator.currentFloor - guest.startFloor
							bestElevator = elevator
			else:
				if (guest.startFloor - elevator.currentFloor) > 0:
					if (guest.startFloor - elevator.currentFloor) < shortestWait:
						shortestWait = guest.startFloor - elevator.currentFloor
						bestElevator = elevator
				else:
					if (elevator.currentFloor - guest.startFloor) < shortestWait:
						shortestWait = elevator.currentFloor - guest.startFloor
						bestElevator = elevator
		return bestElevator

	def run(self):
		counter = 0
		while counter < len(self.guests) or self.allElevatorsEmpty():
			#for guests that have called the elevator
			for guest in self.guests:
				if guest.startTime == counter:
					self.activeGuests[guest.id] = guest

			#handle guests and add them into an elevator
			for id, guest in self.activeGuests.items():
				elevator = self.findBestElevator(guest)
				if elevator:
					elevator.addGuestToQueue(guest)
					del self.activeGuests[id]
				else:
					guest.wait()

			#move each elevator
			for elevator in self.elevators:
				elevator.handleAction()

			counter += 1

		waitTime = self.getAverageWaitTime()
		standardDeviation = self.getStandardDeviation()
		print 'Average wait time for each guest is', waitTime, 'seconds'
		print 'Standard deviation', standardDeviation

	def getAverageWaitTime(self):
		total = 0
		for guest in self.guests:
			total += guest.waitTime
		return total/len(self.guests)

	def getStandardDeviation(self):
		total = 0
		average = self.getAverageWaitTime()
		waitTime = [guest.waitTime for guest in self.guests]
		for time in waitTime:
			total += (time - average)*(time - average)
		return math.sqrt(total/len(self.guests))