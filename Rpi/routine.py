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
        self.initializeRoutineLookUp()

    def initializeRoutineLookUp(self):
        # FORMAT OF PACKAGE:
        # [pumpState, pumpSpeed, garageState, garageDir, trapState, trapDir, phState, condState, ussState, ledStrip]
        # 0.0 means off/close/CW
        # 1.0 means on/open/CCW/outwards
        # Speed is in terms of percentage
        # Check garbage state
        self.routineLookUp[RoutineStates.CHECKGARBAGE.value] = [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0]
        # Garbage full state
        self.routineLookUp[RoutineStates.GARBAGEFULL.value] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0]
        # Filtering state
        self.routineLookUp[RoutineStates.FILTERSTATE.value] = [1.0, 75.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0]
        # Sampling state
        self.routineLookUp[RoutineStates.SAMPLESTATE.value] = [1.0, 75.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 2.0]

    def updateState(self, state):
        self.currentRoutineStep = self.routineLookUp[RoutineStates[state].value]
