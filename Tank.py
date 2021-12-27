import csv

class Tank():
    ''' Tank object. The water tank will be represented
        with this object '''

    capacity = 0
    currentPerc = 0
    currentVol = 0
    empty_light = False

    # constructor
    def __init__(self, capacity, currentPerc):
        ''' class constructor
            capacity : full capacity in gallons
            currentPerc : current percentage of full tank '''

        self.capacity = capacity
        self.currentPerc = currentPerc
        self.currentVol = capacity

        # intialize the empty tank LED
        
        return 

    def getCurrentPerc(self):
        return self.currentPerc

    def reset(self):
        ''' resets the current capacity to full '''
        
        self.currentVol = self.capacity

        self.empty_light = False

        return 

    def setCurrentVol(self, newVol):
        ''' set new current volume '''

        self.currentVol = newVol
        self.currentPerc = (newVol / self.capacity) * 100

        return

    def subtractVol(self, ammount):
        ''' subtract an ammount of water from current volume '''

        newVol = self.currentVol - ammount

        # test if negative
        if newVol <= 0:
            newVol = 0
            self.empty_light = True

        # set new vol for the object
        self.setCurrentVol(newVol)

        return

    def saveToFile(self):
        ''' save status of tank to status.csv '''
        with open("status.csv", "w", newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([self.getCurrentPerc(), self.empty_light])

            csvfile.close()


    def tostring(self):
        ''' toString method '''

        print("Full capacity: " + str(self.capacity))
        print("Current percentage: " + str(self.currentPerc))
        print("Tank is empty: " + str(self.empty_light))

        return 