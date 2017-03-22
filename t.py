#coding=utf-8

from flask import Flask
import requests
import json
import sys
import time
import getpass

USERNAME = "" 
PASSWORD = ""

s = "" # session

URL = "http://kuas.grd.idv.tw:14768/" #API URL

def setData():
    global USERNAME,PASSWORD
    USERNAME = raw_input("Enter Your Account:")
    PASSWORD = getpass.getpass("Enter Your Password:")

    k = list()
    ltime = time.localtime(time.time())
    k.append(int(USERNAME[1:4])) # Set First Year
    k.append(ltime.tm_year-1912) # Set Last Year so far
    
    if (ltime.tm_mon <= 7 ): # Set Semester Every Year
        k.append(1)
    else:
        k.append(2)
    
    return k


def login():
    global s
    s = requests.session()
    
    try:
        r = s.get(URL)
    except Exception as e:
        return 

    try:
        r = s.post(URL + "ap/login", data={"username": USERNAME,"password": PASSWORD})
        if(not r.text.startswith("true")):
            if(USERNAME != ""):print('Username or Password was wrong')
            return 0
        else:
            return 1

    except Exception as e:
        return


def querys( tmp ):
    global s
    k = list()
    try:
        for i in range(tmp[0],tmp[1]+1):
            m = 2 if(i != tmp[1]) else tmp[2] # Set Query Semester Range
            
            for j in range(1,m+1):
                r = s.post(URL + "ap/query", data = {"arg01": str(i) ,"arg02": str(j) ,"arg03": USERNAME,"fncid":"ag008"})
        
                data = json.loads(r.text)
                for d in data[0]:
                    if( (u'通識' in d['course_name']) and (float(d['final_score']) >= 60.0)):
                        k.append(d['course_name'])
  
        return k    
    except Exception as e:
        print(' Query Error !')
        print(e)
        return


if __name__ == "__main__":

    year = list() # Store Year And Semester

    while(login() != 1):
        year = setData()
    
    for i in querys(year):
        print(i)
