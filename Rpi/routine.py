from enum import Enum


class RoutineStates(Enum):
    CHECKGARBAGE = 0
    GARBAGEFULL = 1
    FILTERSTATE = 2
    SAMPLESTATE = 3


class LilypodRoutine():

    def __init__(self):
        self.lengthOfRoutine = 4
        self.currentRoutineStep = []
        self.routineLookUp = [None]*self.lengthOfRoutine
        self.timingLookUp = {}
        self.initializeRoutineTiming()
        self.initializeRoutineLookUp()

    def initializeRoutineTiming(self):
        # in seconds
        self.timingLookUp = {'CHECKGARBAGE': 5, 'GARBAGEFULL': float("inf"), 'FILTERSTATE': 5, 'SAMPLESTATE': 10}

    def initializeRoutineLookUp(self):
        # FORMAT OF PACKAGE:
        # [pumpState, bulbState, garageState, garageDir, trapState, trapDir, phState, condState, ussState, ledStrip]
        # 0.0 means off/close/CW
        # 1.0 means on/open/CCW/outwards
        # Speed is in terms of percentage
        # Check garbage state
        self.routineLookUp[RoutineStates.CHECKGARBAGE.value] = [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        # Garbage full state
        self.routineLookUp[RoutineStates.GARBAGEFULL.value] = [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 3.0]
        # Filtering state
        self.routineLookUp[RoutineStates.FILTERSTATE.value] = [1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        # Sampling state
        self.routineLookUp[RoutineStates.SAMPLESTATE.value] = [1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 2.0]

    def updateState(self, state):
        self.currentRoutineStep = self.routineLookUp[RoutineStates[state].value]
