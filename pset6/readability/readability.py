from cs50 import get_string
import string
import re

text= get_string("Text: ")

charcheck=0

for char in text:
    if char.isalpha() == True:
        charcheck+= 1

#print(charcheck)

#https://stackoverflow.com/questions/17618149/divide-string-by-line-break-or-period-with-python-regular-expressions
scheck = re.split(r"(?!<^)\s*[?!.\n]+\s*(?!$)", text)

#print(scheck)
#print(f"sentences: {len(scheck)} ")

wordcheck = text.split(' ')

#print(len(wordcheck))


L = charcheck / ( len(wordcheck) / 100 )
S = len(scheck) / ( len(wordcheck) / 100 )
index = 0.0588 * L - 0.296 * S - 15.8

if index < 1 :
    index = 1
    print(f" Before Grade 1 ")
elif index > 16 :
    index = 16
    print(f" Grade 16+ ")
else:
    print(f" Grade : {round(index)} ")

