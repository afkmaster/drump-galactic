import sys
import math
from guest import *

DOOR_OPEN_TIME = 10
FLOORS_PER_SECOND = 1
INITIAL_FLOOR = 1
WAIT_TIME = 1
INFINITY = 9999
BUSY_FLOORS = {0:0, 1:1, 10:0, 100:0} #key is each floor, value specifies whether an elevator has been assigned to that floor or not

class Elevator(object):
	def __init__(self, id):
		self.id = id
		self.guests = {}
		self.guestsQueue = {}
		self.currentFloor = INITIAL_FLOOR
		self.doorOpenTime = 0
		self.assignedBusyFloor = INITIAL_FLOOR
		self.isGoingUp = None
		self.isActive = False
		self.DoorIsOpen = False
		self.destinationFloors = []

	def goUpOrDown(self):
		if self.isGoingUp != None:
			if self.isGoingUp:
				self.currentFloor += FLOORS_PER_SECOND
				print 'Elevator', self.id, 'going up to floor', self.currentFloor
			else:
				self.currentFloor -= FLOORS_PER_SECOND
				print 'Elevator', self.id, 'going down to floor', self.currentFloor

	def addGuests(self):
		for id, guest in self.guestsQueue.items():
			self.guests[guest.id] = guest
			guest.addElevator(self)
			if guest.destinationFloor not in self.destinationFloors:
				self.destinationFloors.append(guest.destinationFloor)
			print 'Adding Guest', guest.id, 'to Elevator', self.id, 'destination floor', guest.destinationFloor
			del self.guestsQueue[id]

		self.isGoingUp = self.guests[self.guests.keys()[0]].isGoingUp()
		self.destinationFloors.sort(reverse = not self.isGoingUp)

	def addGuestToQueue(self, guest):
		self.isActive = True
		self.guestsQueue[guest.id] = guest
		if guest.startFloor not in self.destinationFloors:
			self.destinationFloors.append(guest.startFloor)
		self.isGoingUp = self.currentFloor < guest.startFloor
		self.destinationFloors.sort(reverse = not self.isGoingUp)

		#print 'Adding Guest', guest.id, 'to Elevator', self.id, 'guest queue'

	def openDoor(self):
		self.DoorIsOpen = True

	def closeDoor(self):
		self.DoorIsOpen = False

	def wait(self):
		if self.doorOpenTime < DOOR_OPEN_TIME:
			self.doorOpenTime += WAIT_TIME
		else:
			self.doorOpenTime = 0

	def findClosestBusyFloor(self):
		closestFloorDistance = INFINITY
		closestFloor = None
		for floor, value in BUSY_FLOORS.items():
			if value == 0:
				if self.currentFloor > floor:
					if closestFloorDistance > self.currentFloor - floor:
						closestFloorDistance = self.currentFloor - floor
						closestFloor = floor
				elif self.currentFloor < floor:
					if closestFloorDistance > floor - self.currentFloor:
						closestFloorDistance = floor - self.currentFloor
						closestFloor = floor
				elif self.currentFloor == floor:
						closestFloorDistance = 0
						closestFloor = floor
		return closestFloor

	def handleAction(self):
		if self.currentFloor in self.destinationFloors:
			if self.doorOpenTime == 0:
				#pass
				print 'Elevator', self.id, 'arrived on destination floor', self.currentFloor
			self.destinationFloors.remove(self.currentFloor)

		for id, guest in self.guestsQueue.items():
			if guest.startFloor == self.currentFloor:
				self.openDoor()
				self.addGuests()
				break

		if self.guests or self.guestsQueue:
			self.isActive = True
			BUSY_FLOORS[self.assignedBusyFloor] = 0
		else:
			self.isActive = False
			self.isGoingUp = None
			floor = self.findClosestBusyFloor()
			if floor != None:
				BUSY_FLOORS[floor] = 1
				self.assignedBusyFloor = floor

		if self.DoorIsOpen:
			self.wait()
			if self.doorOpenTime == 0:
				self.closeDoor()
		else:
			if self.isActive:
				self.goUpOrDown()
			else:
				if floor > self.currentFloor and floor != None:
					self.currentFloor += FLOORS_PER_SECOND
				elif floor < self.currentFloor and floor != None:
					self.currentFloor -= FLOORS_PER_SECOND
				if floor != None:
					print 'Elevator', self.id, 'is idle and moving to assigned busy floor', floor

		for id, guest in self.guests.items():
			if guest.destinationFloor == self.currentFloor:
				print 'Guest',guest ,'leaving elevator', self.id
				del self.guests[id]
			else:
				guest.wait()

		for guest in self.guestsQueue.values():
			guest.wait()

	def __str__(self):
		return "ID: " + str(self.id) + " Current Floor: " + str(self.currentFloor)