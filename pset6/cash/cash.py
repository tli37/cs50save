from cs50 import get_float

Q=25
D=10
N=5
P=1

money=0
while money <= 0: 
    money = get_float("Change owed: ")
    
money2= 100 * money


QT= money2 % Q #modulus
QC= (money2 - QT) / Q # quarter count

DT= QT % D
DC= (QT - DT) / D

NT = DT % N
NC = (DT - NT) / N

PT = NT % P
PC = (NT - PT) / P


print(int(QC+DC+NC+PC))