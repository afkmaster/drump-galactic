import sys
import math

DEFAULT_FILE = './elevator_traffic_0.txt'
DOOR_OPEN_TIME = 10
FLOORS_PER_SECOND = 1
INITIAL_FLOOR = 1
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

	def addGuest(self, guest):
		self.guests[guest.id] = guest
		guest.addElevator(self)
		if guest.destinationFloor not in self.destinationFloors:
			self.destinationFloors.append(guest.destinationFloor)
		print 'Adding Guest', guest.id, 'to Elevator', self.id, 'destination floor', guest.destinationFloor

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

	def addFloorToDestinations(self, floor):
		self.isActive = True
		if floor not in self.destinationFloors:
			self.destinationFloors.append(floor)
		self.isGoingUp = self.currentFloor < floor
		self.destinationFloors.sort(reverse = not self.isGoingUp)

	def openDoor(self):
		self.DoorIsOpen = True

	def closeDoor(self):
		self.DoorIsOpen = False

	def wait(self):
		if self.doorOpenTime < DOOR_OPEN_TIME:
			self.doorOpenTime += FLOORS_PER_SECOND
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

	def handleAction(self, guestQueue):
		if self.currentFloor in self.destinationFloors:
			if self.doorOpenTime == 0:
				print 'Elevator', self.id, 'arrived on destination floor', self.currentFloor
			self.destinationFloors.remove(self.currentFloor)

		for id, guest in guestQueue.items():
			if guest.startFloor == self.currentFloor:
					self.openDoor()
					self.addGuest(guest)
					del guestQueue[id]
				if self.isActive:
					if self.isGoingUp and guest.isGoingUp():
				else:
					self.isGoingUp = guest.isGoingUp()


		for id, guest in self.guests.items():
			if guest.destinationFloor == self.currentFloor:
				print 'Guest',guest ,'leaving elevator', self.id
				del self.guests[id]
			else:
				guest.wait()

		if self.guests or self.destinationFloors:
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

		if not self.DoorIsOpen:
			if self.isActive:
				self.goUpOrDown()
			else:
				if floor > self.currentFloor and floor != None:
					self.currentFloor += FLOORS_PER_SECOND
					print 'Elevator', self.id, 'is idle and moving to assigned busy floor', floor
				elif floor < self.currentFloor and floor != None:
					self.currentFloor -= FLOORS_PER_SECOND
					print 'Elevator', self.id, 'is idle and moving to assigned busy floor', floor



	def __str__(self):
		return "ID: " + str(self.id) + " Current Floor: " + str(self.currentFloor)

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
		self.waitTime += FLOORS_PER_SECOND
		if self.onElevator:
			pass
			#print 'Guest', self.id, 'going to floor', self.destinationFloor, 'waiting for', self.waitTime, 'seconds, on elevator', self.onElevator
		else:
			pass
			#print 'Guest', self.id, 'starting on floor', self.startFloor, 'going to floor', self.destinationFloor, 'waiting for', self.waitTime, 'seconds, not on elevator yet'

	def addElevator(self, elevator):
		self.onElevator = elevator

	def __str__(self):
		return "ID: " + str(self.id) + " Start Time: " + str(self.startTime) + " Start Floor: " + str(self.startFloor) + " Destination Floor: " + str(self.destinationFloor) + " Waiting Time: " + str(self.waitTime)


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
			if elevator.guests or self.activeGuests:
				return True
		return False

	def findBestElevator(self, guest):
		shortestWait = INFINITY
		bestElevator = None
		for elevator in self.elevators:
			if elevator.isActive:
				if (len(elevator.destinationFloors) > 0 and guest.isGoingUp() != elevator.isGoingUp):
					continue
				if guest.isGoingUp() and elevator.isGoingUp and elevator.currentFloor <= guest.startFloor:
					if (guest.startFloor - elevator.currentFloor) < shortestWait:
						shortestWait = guest.startFloor - elevator.currentFloor
						bestElevator = elevator
				elif (not guest.isGoingUp()) and (not elevator.isGoingUp) and elevator.currentFloor >= guest.startFloor:
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
		while counter < 40:
		#len(self.guests) or self.allElevatorsEmpty():
			#for guests that have called the elevator
			for guest in self.guests:
				if guest.startTime == counter:
					self.activeGuests[guest.id] = guest

			for id, guest in self.activeGuests.items():
				elevator = self.findBestElevator(guest)
				if elevator:
					print guest.startFloor
					elevator.addFloorToDestinations(guest.startFloor)
				else:
					guest.wait()

			for elevator in self.elevators:
				print 'ELEVATOR', elevator.id, elevator.destinationFloors
				elevator.handleAction(self.activeGuests)

			for guest in self.activeGuests.values():
				guest.wait()

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