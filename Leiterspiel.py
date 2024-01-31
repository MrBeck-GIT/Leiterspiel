import os
import time


MinPip = 1
MaxPip = 6
MaxSingleLadderUse = 3
MaxNumberOfLastTriesToGoal = 5
NumberOfGoal = 100
Ladders = [(6,27),(14,19),(21,53),(31,42),(33,38),(46,62),(51,59),(70,76),(68,80),(65,85),(57,96),(92,98)]
ToMuchLadderUsageConditionText = "ToMuchLadders"
ToMuchTriesForGoalConditionText = "ToMuchTriesToGetGoal"
Cancel = False


def CheckIfInputIsnumeric(InputPip):
    if not InputPip.isdigit():
        print("Eingabe war keine Zahl!")
    return InputPip.isdigit()

def CheckIfInputIsInRange(InputPip):
    InputPipInt = int(InputPip)
    if not MinPip <= InputPipInt <= MaxPip :
        print("Zahl ist nicht zwischen 1 und 6")
    return MinPip <= InputPipInt <= MaxPip

#prueft ob die aktuelle Position eine Leiter ist
def IsLadder(Position):
    i = 0
    for Ladder in Ladders:
        LowerRung, UpperRung = Ladder
        if Position == LowerRung or Position == UpperRung:
            ReturnValue = True
        else:
            ReturnValue = False
        if ReturnValue:
            break    
        i = i + 1
    return ReturnValue, i

#gibt die neue Position durch die Leiter zurück übergeben wird aktuelle Position und der Index der Leiter für Ladders
def GetNewPosition(CurrentPosition, LadderIndex):
    LowerRung, UpperRung = Ladders[LadderIndex]
    if CurrentPosition == LowerRung:
        ReturnValue = UpperRung
    elif CurrentPosition == UpperRung:
        ReturnValue = LowerRung
    return ReturnValue

def CountLadder(LadderIndex,UsedLadders):
    i = 0
    Found = False
    for UsedLadder in UsedLadders:
        Index, Counter = UsedLadder   
        if Index == LadderIndex:
            Counter = Counter + 1
            Found = True
            NewTuple = (Index,Counter)
            UsedLadders[i] = NewTuple
        i = i + 1
    if not Found:
        NewTuple = [(LadderIndex,1)]
        UsedLadders.extend(NewTuple)

def CheckInfiniteLoopCondition(TriesToGetToGoal,UsedLadders):
    IsInfiniteLoop = False
    Reason = ''
    for UsedLadder in UsedLadders:
        Index, Counter = UsedLadder
        if Counter > MaxSingleLadderUse:
            IsInfiniteLoop = True
            Reason = ToMuchLadderUsageConditionText
            break
    if not IsInfiniteLoop:
        if TriesToGetToGoal > MaxNumberOfLastTriesToGoal:
            IsInfiniteLoop = True
            Reason = ToMuchTriesForGoalConditionText
    return IsInfiniteLoop, Reason

def RollTheDice(Pip):
    RollResults = []
    UsedLadders = []
    RollCounter = 0
    CurrentPosition = 0
    UsedLadders = []
    TriesToGetToGoal = 0
    while CurrentPosition < NumberOfGoal:
        RollCounter = RollCounter + 1
        CurrentPosition = CurrentPosition + Pip
        if CurrentPosition > NumberOfGoal:
            CurrentPosition = NumberOfGoal - (CurrentPosition - NumberOfGoal)
            TriesToGetToGoal = TriesToGetToGoal + 1
        IsLadderResult = IsLadder(CurrentPosition)
        UseLadder, LaddersIndex = IsLadderResult
        if UseLadder:
            LadderResults = GetNewPosition(CurrentPosition, LaddersIndex)
            CurrentPosition = LadderResults 
            CountLadder(LaddersIndex,UsedLadders)
        CheckForInfiniteLoopResults = CheckInfiniteLoopCondition(TriesToGetToGoal,UsedLadders)
        IsInfiniteLoop, InfiniteLoopReason = CheckForInfiniteLoopResults  
        if IsInfiniteLoop:   
            RollCounter = InfiniteLoopReason
            break
    NewResult = [(Pip,RollCounter)]
    RollResults.extend(NewResult)
    return RollResults
    

def AnalyseResults(RollResults):
        Pip, Result = RollResults[0]
        ResultString = str(Result)
        if ResultString == ToMuchLadderUsageConditionText:
            print(f"Mit Augenzahl {Pip} ist kein Sieg möglich, da eine Endloschleife bei Leitern eintritt.")
        elif ResultString == ToMuchTriesForGoalConditionText:
            print(f"Mit Augenzahl {Pip} ist kein Sieg möglich, da das Ziel nicht mit einem genauen Wurf beendet werden kann.")
        elif ResultString.isdigit():
            print(f"Mit Augenzahl {Pip} ist ein Sieg mit {ResultString} Würfen möglich.")
        


while not Cancel:   
    os.system('cls')
    InputPip = input("Geben Sie eine Augenzahl ein (a für abbrechen): ")
    if not InputPip == "a":
        if CheckIfInputIsnumeric(InputPip):
            if CheckIfInputIsInRange(InputPip):
                RollResults = RollTheDice(int(InputPip))
                AnalyseResults(RollResults)
        print()
        InputDoNext = input("(w)eiter (a)bbrechen   ")
        if InputDoNext == "a":
            Cancel = True
    else:
        Cancel = True
        





