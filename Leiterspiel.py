import os
import time


MinPip = 1  #Minimale Anzahl der Würfelaugen
MaxPip = 6  #Maximal Anzahl der Würfelaugen
MaxSingleLadderUse = 3  #wie oft man ein und dieselbe Leiter benutzer darf, bevor man von einer Endlosschleife ausgehen kann
MaxNumberOfLastTriesToGoal = 5  #wie wie oft man den letzten Wurf um 100 zu kommen machen kann, bevor man von einer Endlossschleife ausgehen kann
NumberOfGoal = 100  #das Ziel des Spiels
Ladders = [(6,27),(14,19),(21,53),(31,42),(33,38),(46,62),(51,59),(70,76),(68,80),(65,85),(57,96),(92,98)]  #die Leitern im Spiel
ToMuchLadderUsageConditionText = "ToMuchLadders"    #Text der als Grund gesetzt wird, wenn von einer Endlosschleife durch Leitern ausgeangen wird
ToMuchTriesForGoalConditionText = "ToMuchTriesToGetGoal" #Text der als Grund gesetzt wird, wenn von einer Endlosschleife durch zu viele Letzte Versuch ausgegangen wird
Cancel = False  #Variable die zu Beendigung des Programms benutzt wird


#Funktion prüft ob eine Wert eine Zahl ist. Wenn es keine Zahl ist, wird ein Fehler ausgegeben
#Übergabewert zu prüfende Variable
#Der Rückgabewert sagt aus, ob es eine Zahl war oder nicht
def CheckIfInputIsnumeric(InputPip):
    if not InputPip.isdigit():
        print("Eingabe war keine Zahl!")
    return InputPip.isdigit()

#Funktion prüft, ob die eingebene Zahl innerhalb der zugelassenen Werte für Würfelaugenzahlen liegt. Wenn nicht, wird eine Meldung ausgegeben
#Übergabewert zu prüfende Variable
#der Rückgabewert sagt aus, ob die eingegebene Zahl innerhalb der zugelassenen Werte liegt
def CheckIfInputIsInRange(InputPip):
    InputPipInt = int(InputPip)
    if not MinPip <= InputPipInt <= MaxPip :
        print(f"Zahl ist nicht zwischen {MinPip} und {MaxPip}")
    return MinPip <= InputPipInt <= MaxPip


#prueft ob die übergebene Position ein Leiterfeld
#1. Rückgabewert sagt es aus, ob es ein Leiterfeld ist und welchen Index die Leiter in der Leitervariable hat
def IsLadder(Position):
    i = 0 
    for Ladder in Ladders: #durch Leiterliste loopen
        LowerRung, UpperRung = Ladder #Werte lesen
        if Position == LowerRung or Position == UpperRung: # prüfen ob die Position einem Feld der Leiter enspricht
            ReturnValue = True
        else:
            ReturnValue = False
        if ReturnValue:
            break    
        i = i + 1   #Zähler für den Index, damit nachgelagerte Funktion direkt auf diesen Index zugreifen können, ohne Schleife
    return ReturnValue, i

#gibt die neue Position durch die Leiter zurück übergeben wird aktuelle Position und der Index der Leiter in der Liste
#Rückgabewert ist die neue Position durch die Leiter
def GetNewPosition(CurrentPosition, LadderIndex):
    LowerRung, UpperRung = Ladders[LadderIndex] #die Tuple aus der Liste anhand des Indexes lesen
    if CurrentPosition == LowerRung: #prüfen ob die aktuelle Position am unteren Ende der Leiter ist 
        ReturnValue = UpperRung #neue Position ist der obere Wert der Leiter
    elif CurrentPosition == UpperRung: #prüfen ob die aktuelle Position am oberen Ende der Leiter ist 
        ReturnValue = LowerRung #neue Position ist der untere Wert der Leiter
    return ReturnValue

#Funktion zählt wie oft eine Leiter benutzt wird. Das wird dazu genutzt um eine eventuelle Enschlosschleife zu ermitteln
#übergeben wird der Index der Leiter aus der Liste und die Liste wo die benutzten Leitern gespeichert werden
def CountLadder(LadderIndex,UsedLadders):
    i = 0
    Found = False
    for UsedLadder in UsedLadders: #durch die Liste der benutzten Leitern loopen
        Index, Counter = UsedLadder   #werte lesen
        if Index == LadderIndex: #wenn der übergebene Index einem Index in der Liste entspricht
            Counter = Counter + 1 #Zähler für Leiternutzung erhöhen
            Found = True #kennzeichen setzen, das der Leiterindex sich bereits in der Liste befindet
            NewTuple = (Index,Counter) #Tuple mit neuem Counterwert bilden
            UsedLadders[i] = NewTuple # alten wert überschreiben
        i = i + 1 # Zähler weitersetzen mit direkt auf den Index der benutzen Leitern zugegriffen werden kann
    if not Found: #wenn der übergebene Index nicht gefunden wurde, wurde die Leiter das erste mal benutzt und wird hingefügt
        NewTuple = [(LadderIndex,1)] #Tuple wird zusammengesetzt
        UsedLadders.extend(NewTuple) #Tuple wird an die Liste der benutzten Leitern angefügt

#Funktion prüft, ob eine Endlosschleife vorliegt. Dies kann entweder durch entstehen, wenn man immer wieder auf Leitern stößt
#oder der letzt Wurf nicht aufgeht.
#1. Rückgabewert sagt aus, ob eine Endlosschleife vorliegt, 2. Rückgabewert enthält den Grund der Endlosschleife
def CheckInfiniteLoopCondition(TriesToGetToGoal,UsedLadders):
    IsInfiniteLoop = False #initial davon ausgehen dass keine Endlosschleife vorliegt
    Reason = '' #Variable für den Grund der Endlosschleife setzen
    for UsedLadder in UsedLadders: #zuerst prüfen ob Leitern zu oft benutzt worden sind. Dafür durch die Liste der benutzten Leitern loopen
        Index, Counter = UsedLadder # Werte lesen
        if Counter > MaxSingleLadderUse: # wenn der Counter für einer benutzte Leiter den zugelassenen Höchstwert übersteigt
            IsInfiniteLoop = True #von einer Endlosschleife ausgehen
            Reason = ToMuchLadderUsageConditionText #den Grund für spätere Auswertung setzen
            break #Schleife abbrechen, weil mindestens eine Leiter schon zu oft benutzt wurde
    if not IsInfiniteLoop: # wenn keine Endlosschleife durch zu viele Leiternutzungen vorlieg
        if TriesToGetToGoal > MaxNumberOfLastTriesToGoal: #prüfen ob die maximal zugelassene anzahl von letzten Würfen überschritten ist
            IsInfiniteLoop = True # von einer Endlosschleife ausgehen
            Reason = ToMuchTriesForGoalConditionText #Grund für spätere Auswertung setzen
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
        





