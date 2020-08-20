from cs50 import SQL
import sys
import csv
from sys import argv

db = SQL("sqlite:///students.db")

#command line check
if len(sys.argv) != 2:
    sys.exit("Check Command Line")



db.execute("DROP TABLE hp")
db.execute("CREATE TABLE hp (first_name TEXT, middle_name TEXT, last_name TEXT, house TEXT, birth INT)")
with open (argv[1],'r') as csv_file:
    datafile = csv.reader(csv_file)
    for row in datafile:
        namesplit = row[0].split(' ')


        #for 2 aka no middle name
        if len(namesplit) == 2:
            namesplit.insert( 1 , None )


        namesplit.extend([row[1], row[2]])


        SQL1 = "INSERT INTO hp (first_name, middle_name, last_name, house, birth) VALUES (?,?,?,?,?)"
        db.execute(SQL1, namesplit)

