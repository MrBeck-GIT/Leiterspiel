MaxWürfe = 30
aktuelle_position = 0
AnzahlWürfe = 0
IsWinable = True
def IsLadder(aktuelle_position):
    for leiter in [(6,27),(14,19),(21,53),(31,42),(33,38),(46,62),(51,59),(70,76),(68,80),(65,85),(57,96),(92,98)]:
        if aktuelle_position == leiter[0] or aktuelle_position == leiter[1]:
                if aktuelle_position == leiter[0]:
                    aktuelle_position = leiter[1]
                else:
                    aktuelle_position = leiter[0]
                break
    return(aktuelle_position)

Augenzahl = input("Geben Sie eine Augenzahl ein: ")
Augenzahl = int(Augenzahl)

while aktuelle_position != 100:
     aktuelle_position = aktuelle_position + Augenzahl
     aktuelle_position = IsLadder(aktuelle_position)
     AnzahlWürfe = AnzahlWürfe + 1
     if AnzahlWürfe == MaxWürfe:
        IsWinable = False
        break
     


if IsWinable:
    print(f"Gewinnbar mit {AnzahlWürfe} Würfen")
else:
    print("Nicht gewinnbar")


