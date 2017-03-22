# coding:utf-8

from flask import Flask
import requests
import json
import sys
import time
import getpass

URL = "http://kuas.grd.idv.tw:14768/"   # API URL


def setData(user):

    user['username'] = raw_input("Enter Your Account:")
    user['password'] = getpass.getpass("Enter Your Password:")

    local_time = time.localtime(time.time())

    user['start_year'] = int(user['username'][1:4])  # Set First Year
    user['end_year'] = local_time.tm_year-1912       # Set Last Year so far

    if (local_time.tm_mon <= 7):                    # Set Semester Every Year
        user['semester'] = 1
    else:
        user['semester'] = 2


def login(session, user):

    try:
        r = session.get(URL)
    except Exception as e:
        return

    try:
        r = session.post(
                URL + "ap/login",
                data={"username": user['username'],
                      "password": user['password']})
        return r.text
    except Exception as e:
        return


def querys(session, user):

    tmp_data = []
    try:
        for index_year in range(user['start_year'], user['end_year']+1):

            # Set Query Semester Range
            m = 2 if(index_year != user['end_year'])else user['semester']
            for index_semester in range(1, m+1):
                r = session.post(
                        URL + "ap/query",
                        data={"arg01": str(index_year),
                              "arg02": str(index_semester),
                              "arg03": user['username'],
                              "fncid": "ag008"})

                data = json.loads(r.text)
                for d in data[0]:
                    if(u"通識" in d['course_name'] and
                       float(d['final_score']) >= 60.0):
                        tmp_data.append(d['course_name'])

        return tmp_data
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":

    user = {'username': None, 'password': None,
            'start_year': None, 'end_year': None, 'semester': None}
    session = requests.session()

    for x in range(0, 3):
        setData(user)
        if login(session, user).startswith("true"):
            break
        print("The username or password was wrong, try it again.")
    else:
        print("You has enter 3 times wrong password. Bye!")

    for i in querys(session, user):
        print(i)
