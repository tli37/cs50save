import os
import csv
import math

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, render_template_string
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures import ImmutableMultiDict

import plotly.express as px
import datetime as dt

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloadeda
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

#from reactive trainingsystems the RPE csv sheet
with open('RpeTrainingCalc.csv') as csv_file:
    RPE = list(csv.reader(csv_file, delimiter = ";" ))
    # starts at 1 and 1

#wathen 1RM formula 1RM = 100 * weight / (48,8 + 53,8*e^-0,075*rep)
def oneRM(w , r):

    a = 100 * w
    b = 48.8 + 53.8 * math.exp(-0.075 * r)
    c= round ( a/b , 1)
    return c

def RPEcalc(x, r):
    #input RPE and rep
    # -2 RPE + 21  to determine index

    a = int(-2 * 7 + 21)
    b = round( float(RPE[a][r]) / 100 , 3)

    return b


@app.route("/")
def index():

    dbsearch = db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='diary'")
    if not dbsearch:
        #create table
        db.execute("CREATE TABLE diary (squatweight NUMERIC, squatrep INTEGER , benchweight NUMERIC , benchrep INTEGER , dlweight NUMERIC, dlrep INTEGER , RPE NUMERIC, date DATE NOT NULL)")
    dbsearch = db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='PRhistory'")
    if not dbsearch:
        #create table
        db.execute("CREATE TABLE PRhistory (squatweight NUMERIC, squatrep INTEGER , benchweight NUMERIC , benchrep INTEGER , dlweight NUMERIC, dlrep INTEGER , RPE NUMERIC, date DATE NOT NULL)")


    weightdata = db.execute("SELECT * FROM diary ORDER BY date")
    squatdata = db.execute("SELECT squatweight, squatrep, RPE, date FROM diary WHERE squatweight IS NOT NULL ORDER BY date")
    benchdata = db.execute("SELECT benchweight, benchrep, RPE, date FROM diary WHERE benchweight IS NOT NULL ORDER BY date")
    dldata = db.execute("SELECT dlweight, dlrep, RPE, date FROM diary WHERE dlweight IS NOT NULL ORDER BY date")

    squatweight = []
    squatrep = []
    benchweight = []
    benchrep = []
    dlweight = []
    dlrep = []

    squatdate = []
    volsdate = []
    benchdate = []
    volbdate = []
    dldate = []
    voldldate = []

    datecheck = []
    squatpoorest1rm = []
    benchpoorest1rm = []
    dlpoorest1rm = []
    spoordate = []
    bpoordate = []
    dlpoordate = []

    squatest1rm = []
    squatest1rmdate = []
    benchest1rm = []
    benchest1rmdate = []
    dlest1rm = []
    dlest1rmdate = []

    svol= []
    bvol=[]
    dlvol=[]

    #1RM check if same day, then do comparison if 1RM is higher, then change date (only for est 1RM and poor1RM)

    for i in range(len(squatdata)):
        squatweight.append(squatdata[i]['squatweight'] )
        squatrep.append(squatdata[i]['squatrep'] )
        squatdate.append(squatdata[i]['date'] )
        daily1rm = oneRM(squatdata[i]['squatweight'], squatdata[i]['squatrep'])
        dailyvol = squatdata[i]['squatrep'] * squatdata[i]['squatweight']
        est1rm = 0

        if squatdata[i]['RPE'] != None and isinstance(squatdata[i]['RPE'], int) == True :
            #RPE factor * 1RM calculation
            est1rm = round( oneRM(squatdata[i]['squatweight'], squatdata[i]['squatrep']) / RPEcalc(squatdata[i]['RPE'], squatdata[i]['squatrep'] )  , 1)
        if datecheck == squatdata[i]['date']:
            svol[len(svol)-1] = svol[len(svol)-1] + dailyvol   #add volume to same date indext
            if squatpoorest1rm[-1] < daily1rm: #if same date, check if new is bigger than old
                squatpoorest1rm[-1] = daily1rm
            if squatest1rm[-1] < est1rm:
                squatest1rm[-1] = est1rm
        else:
            svol.append(dailyvol)
            volsdate.append(squatdata[i]['date'])
            squatpoorest1rm.append(daily1rm)
            spoordate.append(squatdata[i]['date'])
            if est1rm > 0: #if it has done the "none check" otherwise est1rm will be 0
                squatest1rm.append(est1rm)
                squatest1rmdate.append(squatdata[i]['date'])
            #check next day
            datecheck = squatdata[i]['date']

    datecheck = []

    for i in range(len(benchdata)):
        benchweight.append(benchdata[i]['benchweight'] )
        benchrep.append(benchdata[i]['benchrep'] )
        benchdate.append(benchdata[i]['date'] )
        daily1rm = oneRM(benchdata[i]['benchweight'], benchdata[i]['benchrep'])
        dailyvol = benchdata[i]['benchrep'] * benchdata[i]['benchweight']
        est1rm = 0

        if benchdata[i]['RPE'] != None and isinstance(benchdata[i]['RPE'], int) == True :
            #RPE factor * 1RM calculation
                est1rm = round( oneRM(benchdata[i]['benchweight'], benchdata[i]['benchrep']) / RPEcalc(benchdata[i]['RPE'], benchdata[i]['benchrep'] ) , 1)
        if datecheck == benchdata[i]['date']:
            bvol[len(bvol)-1] = bvol[len(bvol)-1] + dailyvol
            if benchpoorest1rm[-1] < daily1rm: #if same date, check if new is bigger than old
                benchpoorest1rm[-1] = daily1rm
            if benchest1rm[-1] < est1rm:
                benchest1rm[-1] = est1rm
        else:
            bvol.append(dailyvol)
            volbdate.append(benchdata[i]['date'])
            benchpoorest1rm.append(daily1rm)
            bpoordate.append(benchdata[i]['date'])
            if est1rm > 0: #if it has done the "none check" otherwise est1rm will be 0
                benchest1rm.append(est1rm)
                benchest1rmdate.append(benchdata[i]['date'])
            #check next day
            datecheck = benchdata[i]['date']

    datecheck = []

    for i in range(len(dldata)):
        dlweight.append(dldata[i]['dlweight'] )
        dlrep.append(dldata[i]['dlrep'] )
        dldate.append(dldata[i]['date'] )
        daily1rm = oneRM(dldata[i]['dlweight'], dldata[i]['dlrep'])
        dailyvol = dldata[i]['dlrep'] * dldata[i]['dlweight']
        est1rm = 0

        if dldata[i]['RPE'] != None and isinstance(dldata[i]['RPE'], int) == True :
            #RPE factor * 1RM calculation
                est1rm = round( oneRM(dldata[i]['dlweight'], dldata[i]['dlrep']) / RPEcalc(dldata[i]['RPE'], dldata[i]['dlrep'] ), 1)
        if datecheck == dldata[i]['date']:
            dlvol[len(dlvol)-1] = dlvol[len(dlvol)-1] + dailyvol
            if dlpoorest1rm[-1] < daily1rm: #if same date, check if new is bigger than old
                dlpoorest1rm[-1] = daily1rm
            if dlest1rm[-1] < est1rm:
                dlest1rm[-1] = est1rm
        else:
            dlvol.append(dailyvol)
            voldldate.append(dldata[i]['date'])
            dlpoorest1rm.append(daily1rm)
            dlpoordate.append(dldata[i]['date'])
            if est1rm > 0: #if it has done the "none check" otherwise est1rm will be 0
                dlest1rm.append(est1rm)
                dlest1rmdate.append(dldata[i]['date'])
            #check next day
            datecheck = dldata[i]['date']


    prsquatweight=[]
    prsquatrep=[]
    prsquatdate=[]
    prsquat1rm=[]

    prbenchweight=[]
    prbenchrep=[]
    prbenchdate=[]
    prbench1rm=[]

    prdlweight=[]
    prdlrep=[]
    prdldate=[]
    prdl1rm=[]

    squatprdata = db.execute("SELECT squatweight, squatrep, date FROM PRhistory WHERE squatweight IS NOT NULL ORDER BY squatrep")
    benchprdata = db.execute("SELECT benchweight, benchrep, date FROM PRhistory WHERE benchweight IS NOT NULL ORDER BY benchrep")
    dlprdata = db.execute("SELECT dlweight, dlrep, date FROM PRhistory WHERE dlweight IS NOT NULL ORDER BY dlrep")

    #create PR arrays

    for i in range(len(squatprdata)):
        prsquatweight.append(squatprdata[i]['squatweight'])
        prsquatrep.append(squatprdata[i]['squatrep'])
        prsquat1rm.append(oneRM(squatprdata[i]['squatweight'], squatprdata[i]['squatrep']))
        prsquatdate.append(squatprdata[i]['date'])

    for i in range(len(benchprdata)):
        prbenchweight.append(benchprdata[i]['benchweight'])
        prbenchrep.append(benchprdata[i]['benchrep'])
        prbench1rm.append(oneRM(benchprdata[i]['benchweight'], benchprdata[i]['benchrep']))
        prbenchdate.append(benchprdata[i]['date'])

    for i in range(len(dlprdata)):
        prdlweight.append(dlprdata[i]['dlweight'])
        prdlrep.append(dlprdata[i]['dlrep'])
        prdl1rm.append(oneRM(dlprdata[i]['dlweight'], dlprdata[i]['dlrep']))
        prdldate.append(dlprdata[i]['date'])

    return render_template("index.html", len1 = len(prsquatweight), len2 = len(prbenchweight), len3 = len(prdlweight),
    squatest1rm = squatest1rm, squatest1rmdate = squatest1rmdate, benchest1rm = benchest1rm , benchest1rmdate =  benchest1rmdate, dlest1rm = dlest1rm, dlest1rmdate = dlest1rmdate ,
    squatpoorest1rm = squatpoorest1rm,  spoordate = spoordate, benchpoorest1rm = benchpoorest1rm, bpoordate = bpoordate, dlpoorest1rm = dlpoorest1rm,  dlpoordate = dlpoordate,
    squatrep = squatrep, squatweight = squatweight, benchrep = benchrep, benchweight = benchweight, dlrep = dlrep, dlweight = dlweight,
    squatdate = squatdate,  benchdate = benchdate , dldate = dldate,
    svol = svol, volsdate = volsdate, bvol = bvol, volbdate = volbdate, dlvol = dlvol, voldldate = voldldate,
    prsquatweight = prsquatweight, prsquatrep = prsquatrep, prsquatdate = prsquatdate, prsquat1rm = prsquat1rm,
    prbenchweight = prbenchweight, prbenchrep = prbenchrep, prbenchdate = prbenchdate, prbench1rm = prbench1rm,
    prdlweight = prdlweight, prdlrep = prdlrep, prdldate = prdldate, prdl1rm = prdl1rm)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:

        inputs = request.form
        Dicttrans = inputs.to_dict(flat=False)
        length = len(request.form)

        #find keys and append in list
        keylist=[]
        keys = Dicttrans.keys()
        for key in keys:
            keylist.append(key)

        #search for table
        dbsearch = db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='diary'")
        if not dbsearch:
            #create table
            db.execute("CREATE TABLE diary (squatweight NUMERIC, squatrep INTEGER , benchweight NUMERIC , benchrep INTEGER , dlweight NUMERIC, dlrep INTEGER , RPE NUMERIC, date DATE NOT NULL)")
        dbsearch = db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='PRhistory'")
        if not dbsearch:
            #create table
            db.execute("CREATE TABLE PRhistory (squatweight NUMERIC, squatrep INTEGER , benchweight NUMERIC , benchrep INTEGER , dlweight NUMERIC, dlrep INTEGER , RPE NUMERIC, date DATE NOT NULL)")

        #if for each name find the placement of each exeriise in dictonary#####

        if 'squatweight' in Dicttrans:
            keylen1 = len(Dicttrans['squatweight'])
            #insert squats
            for i in range(keylen1):
                db.execute("INSERT INTO diary (squatweight, squatrep, RPE, date) VALUES ( :sw , :sr , :RPE, :date)",
                sw = Dicttrans['squatweight'][i] , sr = Dicttrans['squatrep'][i], RPE = Dicttrans['RPE'][i], date = Dicttrans['date'][0])
                #check for PR
                pr = db.execute("SELECT squatweight FROM PRhistory WHERE squatrep = :squatrep" , squatrep = Dicttrans['squatrep'][i] )
                #if empty- just insert
                if not pr:
                    db.execute("INSERT INTO PRhistory (squatweight, squatrep, RPE, date) VALUES ( :sw , :sr , :RPE, :date)",
                    sw = Dicttrans['squatweight'][i] , sr = Dicttrans['squatrep'][i], RPE = Dicttrans['RPE'][i], date = Dicttrans['date'][0])
                else: #uncoventional elseif, pr[0] will bug if checked at empty list- delete and then insert
                    if int(Dicttrans['squatweight'][i]) > int(pr[0]['squatweight']) :
                        db.execute("DELETE FROM PRhistory WHERE squatrep = :squatrep", squatrep = Dicttrans['squatrep'][i] )
                        db.execute("INSERT INTO PRhistory (squatweight, squatrep, RPE, date) VALUES ( :sw , :sr , :RPE, :date)",
                        sw = Dicttrans['squatweight'][i] , sr = Dicttrans['squatrep'][i], RPE = Dicttrans['RPE'][i], date = Dicttrans['date'][0])
        if 'benchweight' in Dicttrans:
            keylen2 = len(Dicttrans['benchweight'])
            #insert bench
            for i in range(keylen2):
                db.execute("INSERT INTO diary (benchweight, benchrep, RPE, date) VALUES ( :bw , :br , :RPE, :date)",
                bw = Dicttrans['benchweight'][i] , br = Dicttrans['benchrep'][i], RPE = Dicttrans['RPE'][i], date = Dicttrans['date'][0])
                #check for PR
                pr = db.execute("SELECT benchweight FROM PRhistory WHERE benchrep = :benchrep", benchrep = Dicttrans['benchrep'][i])
                #if empty insert
                if not pr:
                    db.execute("INSERT INTO PRhistory (benchweight, benchrep, RPE, date) VALUES ( :bw , :br , :RPE, :date)",
                    bw = Dicttrans['benchweight'][i] , br = Dicttrans['benchrep'][i], RPE = Dicttrans['RPE'][i] , date = Dicttrans['date'][0])
                else : #uncoventional elseif, pr[0] will bug if checked at empty list- delete and then insert
                    if int(Dicttrans['benchweight'][i]) > int(pr[0]['benchweight']):
                        db.execute("DELETE FROM PRhistory WHERE benchrep = :benchrep" , benchrep = Dicttrans['benchrep'][i] )
                        db.execute("INSERT INTO PRhistory (benchweight, benchrep, RPE, date) VALUES ( :bw , :br , :RPE, :date)",
                        bw = Dicttrans['benchweight'][i] , br = Dicttrans['benchrep'][i], RPE= Dicttrans['RPE'][i], date = Dicttrans['date'][0])
        if 'dlweight' in Dicttrans:
            keylen3 = len(Dicttrans['dlweight'])
            #insert DL
            for i in range(keylen3):
                db.execute("INSERT INTO diary (dlweight, dlrep, RPE, date) VALUES ( :dlw , :dlr , :RPE, :date)",
                dlw = Dicttrans['dlweight'][i] , dlr = Dicttrans['dlrep'][i], RPE = Dicttrans['RPE'][i], date = Dicttrans['date'][0])
                #check for PR
                pr = db.execute("SELECT dlweight FROM PRhistory WHERE dlrep = :dlrep", dlrep = Dicttrans['dlrep'][i])
                #if empty insert
                if not pr:
                    db.execute("INSERT INTO PRhistory (dlweight, dlrep, RPE, date) VALUES ( :dlw , :dlr , :RPE, :date)",
                    dlw = Dicttrans['dlweight'][i] , dlr = Dicttrans['dlrep'][i], RPE = Dicttrans['RPE'][i] , date = Dicttrans['date'][0])
                else : #uncoventional elseif, pr[0] will bug if checked at empty list- delete and then insert
                    if int(Dicttrans['dlweight'][i]) > int(pr[0]['dlweight']):
                        db.execute("DELETE FROM PRhistory WHERE dlrep = :dlrep" , dlrep = Dicttrans['dlrep'][i] )
                        db.execute("INSERT INTO PRhistory (dlweight, dlrep, RPE, date) VALUES ( :dlw , :dlr , :RPE, :date)",
                        dlw = Dicttrans['dlweight'][i] , dlr = Dicttrans['dlrep'][i], RPE= Dicttrans['RPE'][i], date = Dicttrans['date'][0])

        return redirect("/")

