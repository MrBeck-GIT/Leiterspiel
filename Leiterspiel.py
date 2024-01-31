import os

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
    RollResults = [] #Variable für Ergebnis initialisieren
    UsedLadders = [] #Variable für benutzte Leitern initialisieren
    RollCounter = 0 #Zähler für Würfelvorgänge
    CurrentPosition = 0 #aktuelle Position auf dem Spielfeld
    TriesToGetToGoal = 0 #Zähler für den letzten Würfel versuch
    while CurrentPosition < NumberOfGoal: #Schleife für das Spiel, also solange wie man nicht das Ziel erreicht hat
        RollCounter = RollCounter + 1 #Würfelvorgänge zählen
        CurrentPosition = CurrentPosition + Pip #Position um die Würfelaugen versetz
        if CurrentPosition > NumberOfGoal: #prüfen ob wir mit Würfel und unserer Position über das Ziel kommen
            CurrentPosition = NumberOfGoal - (CurrentPosition - NumberOfGoal) #Zielfeld laut den Spielregeln ermitteln, auf das wir müssen, weil wir über das Ziel hinaus sind
            TriesToGetToGoal = TriesToGetToGoal + 1 #Versuche das Ziel mit dem letzten Wurf zu erreichen, zählen um eine eventuelle Endlosschleife zu ermitteln
        IsLadderResult = IsLadder(CurrentPosition) #prüfen ob wir uns gerade auf einem Leiterfeld befinden
        UseLadder, LaddersIndex = IsLadderResult #Werte für Leiterfeldprüfung lesen
        if UseLadder: #wenn wir eine Leiter benutzen müssen, also wenn es ein Leiterfeld ist
            LadderResults = GetNewPosition(CurrentPosition, LaddersIndex) #das Zielfeld ermitteln lassen
            CurrentPosition = LadderResults #unsere Position auf das Zielfeld setzen
            CountLadder(LaddersIndex,UsedLadders) #die Benutzung der Leiter zählen um eine eventuelle Endlosschleife zu ermitteln
        CheckForInfiniteLoopResults = CheckInfiniteLoopCondition(TriesToGetToGoal,UsedLadders) #prüfen ob eine Konditon für eine Endlosschleife vorliegt
        IsInfiniteLoop, InfiniteLoopReason = CheckForInfiniteLoopResults #Werte für Endlosschleifenprüfung lesen
        if IsInfiniteLoop:   # wenn es eine Endlosschleife ist
            RollCounter = InfiniteLoopReason #wird die Anzahl der Würfelversuche mit dem Grund der Enlosschleife für spätere Auswertung überschrieben
            break #Schleife für das Spiel verlassen, weil das Spiel Aufgrund einer Endlosschleife nicht erfüllt werden kann
    NewResult = [(Pip,RollCounter)] #Resulat Tuple erzeugen
    RollResults.extend(NewResult) #Resultat in Liste speichern
    return RollResults #Resultate zurückgeben
    

#Funkion analysiert die Ergebnisse uns gibt sie aus
#Übergabe wert ist die Resultat Liste
def AnalyseResults(RollResults):
        Pip, Result = RollResults[0] #da es wegen eines Wurfs nur ein Resultat geben kann, das erste Item der Liste lesen
        ResultString = str(Result) #um später zu prüfen ob das Resultat eine Zahl ist, wird es in einen String umgewandelt um isdigit nutzen zu können
        if ResultString == ToMuchLadderUsageConditionText: #wenn der Grund unser vordefinierter Text für zu viele Leiterbenutzungen ist
            print(f"Mit Augenzahl {Pip} ist kein Sieg möglich, da eine Endloschleife bei Leitern eintritt.")
        elif ResultString == ToMuchTriesForGoalConditionText: #wenn der Grund unser vordefinierter Text für zu viele letzte Würfelversuche um auf's Ziel zu kommen, ist
            print(f"Mit Augenzahl {Pip} ist kein Sieg möglich, da das Ziel nicht mit einem genauen Wurf beendet werden kann.")
        elif ResultString.isdigit(): #wenn es eine Zahl ist, ist das Spiel erfolgreich beendet und wir haben eine Anzahl Würfelvorgänge
            print(f"Mit Augenzahl {Pip} ist ein Sieg mit {ResultString} Würfen möglich.")
        


#das eigentliche Programm
while not Cancel:   #solange niemand abbrechen möchte
    os.system('cls') #bildschirm löschen
    InputPip = input("Geben Sie eine Augenzahl ein (a für abbrechen): ") #Usereingabe lesen
    if not InputPip == "a":# wenn kein a für abbrechen eingegeben wurde
        if CheckIfInputIsnumeric(InputPip): #prüfen ob eine zahl eingeben wurde
            if CheckIfInputIsInRange(InputPip): #prüfen ob sich die Zahl in der vorgebenen Spanne befindet
                RollResults = RollTheDice(int(InputPip)) #die Würfel rollen lassen und das Resultat empfangen
                AnalyseResults(RollResults) #Resultat analysieren
        print()#eine leerZeile wegen der Übersichtlichkeit
        InputDoNext = input("(w)eiter (a)bbrechen   ") #fragen wie wir weitermachen wollen
        if InputDoNext == "a": #wenn ein a eingeben wurde die Ausstiegsbedingung für die Programmschleife setzten
            Cancel = True
    else:
        Cancel = True #wenn ein a eingeben wurde die Ausstiegsbedingung für die Programmschleife setzten
        





