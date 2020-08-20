import csv
from sys import argv
import re
import sys


datasave=[]

if len(argv) is not 3: #stop usage if not correct input
    print('Usage: python dna.py data.csv sequence.txt')
    sys.exit()

#open CSV file and save
with open (argv[1],'r') as csv_file:
    datafile = csv.reader(csv_file)
    line_count = 0
    for row in datafile:
        datasave.insert(line_count, row)
        line_count += 1
        
rowlength= len(datasave[0])-1
seqfile= open(argv[2],'r') #read argv2
countvector=[]

def STR(x): #choose between large or small databse

    ABC = ["AGATC", "TTTTTTCT", "AATG", "TCTAG", "GATA", "TATC", "GAAA", "TCTG"]
    DEF =["AGATC", "AATG", "TATC"]
    A = ABC[x]
    
    if argv[1] == 'databases/large.csv':
        A= ABC[x]
    elif argv[1] == 'databases/small.csv':
        A= DEF[x]
    return A


seqfile2 = seqfile.read()

#reminder x in count is repeated x-1 in task description , 2 occurence = repeated 1 times


for i in range(rowlength):
    newcount= 0
    STR1= STR(i)

    while True:
        Bfound = re.findall(STR1*newcount,seqfile2)
        if re.findall(STR1*newcount, seqfile2) == [] :
            countvector.append(newcount-1)
            break
        else:
            newcount += 1
            

countvector= str(countvector)[1:-1] #some formatting lines, converting first integers to string
countvector1= countvector.replace(',','') #removing , 
search_list= countvector1.split(' ') #splitting into list cuz the database i saved as list

rowcount=0
rowplacement=0

for row in datasave:
    indexcount=0
    truecount=0
    for i in range(rowlength):
        if search_list[i] in datasave[rowcount]:
            truecount+=1 #testing if index matches lists
            if truecount == rowlength: #matching all in the row will start this IF line
                rowplacement=rowcount
                print(datasave[rowplacement][0])
                
                break #this break doesnt work???????
            
        indexcount+=1
    rowcount+=1
    
if truecount is not rowlength and rowplacement == 0 :
    print('No match')    

