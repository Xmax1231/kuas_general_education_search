# coding:utf-8

import requests
import json
import time
import getpass
from requests.auth import HTTPBasicAuth

URL = "https://kuas.grd.idv.tw:14769/v2/"   # API URL


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
        r = session.get(URL+'token')
        tmp = json.loads(r.text)

        return tmp['auth_token']
    except Exception as e:
        return


def querys(session, user):

    tmp_data = []
    try:
        for index_year in range(user['start_year'], user['end_year']+1):

            # Set Query Semester Range
            m = 2 if(index_year != user['end_year'])else user['semester']
            for index_semester in range(1, m+1):
                r = session.get(URL + "ap/users/scores/%d/%d"
                                % (index_year, index_semester))

                data = json.loads(r.text)
                for d in data['scores']['scores']:
                    if(u"通識" in d['title'] and
                       float(d['final_score']) >= 60.0):
                        tmp_data.append(d['title'])

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
        session.auth = (user['username'], user['password'])

        if login(session, user) is not None:
            break
        print("The username or password was wrong, try it again.")
    else:
        print("You has enter 3 times wrong password. Bye!")

    for i in querys(session, user):
        print(i)
