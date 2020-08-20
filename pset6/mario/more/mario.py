from cs50 import get_int

Height=0
while Height < 1 or Height >8:
    Height = get_int("Height: ")

for i in range(Height):
    
    A=Height-i-1
    B=Height-A
    
    for j in range(A): # left side sapces
        print(" ", end="")
    
    for k in range(B): #left side squares
        print("#", end="")
        
    print(" ",end="") #middle
    
    for l in range(B): #right side squares
        print("#", end="")
    for m in range(A): #righht side spaces
        print(" ", end="")

    print()
    