from cs50 import SQL
import sys
import csv
from sys import argv

db = SQL("sqlite:///students.db")

#command line check
if len(sys.argv) != 2:
    sys.exit("Check Command Line")

house = argv[1]

output = db.execute("SELECT first_name, middle_name, last_name, birth FROM hp WHERE house = (?) ORDER BY last_name, first_name" , (house))



for i in range(len(output)):
    print(  output[i].get('first_name'), end=" ")

    if output[i].get('middle_name') != None:
        print(  output[i].get('middle_name'), end=" ")

    print(  output[i].get('last_name'), end=", ")

    print('born',output[i].get('birth') )