# coding=utf-8
import requests
import getpass
from bs4 import BeautifulSoup

def login( sson ):
    loginUrl = 'http://140.127.113.131/kuas/perchk.jsp'
    loginCheck = 'http://140.127.113.131/kuas/f_head.jsp'
    user = input( "user:" )

    pwd = getpass.getpass()
    data = { 'uid': user, 'pwd': pwd }
    sson.post( loginUrl, data = data )
    chk = sson.get( loginCheck ).text
    return u'修改密碼' in chk

def getCourse( soup ):
    courses = soup.select("table")
    if( len( courses ) >= 2 ):
        courses = courses[1].select("tr")
        courseNum = len( courses )
        for i, cour in zip( range( courseNum ), courses ):
            if( i == 0 ):
                continue
            cName = cour.select( '[name=subcount{0}]'.format( i ) )[0].text
            if( u'通識' in cName ):
                print( cName )

if( __name__ == '__main__' ):
    sson = requests.session()
    if( login( sson ) ):
        searchCourseUrl = 'http://140.127.113.131/kuas/ag_pro/ag103.jsp'
        data = { 'yms':'105,1','spath':'ag_pro/ag103.jsp?','arg01':'105','arg02':'1' }
        startYear = int( input( "start year:" ) )
        endYear = int( input( "end year:" ) )
        if( endYear < startYear ):
            print( "null" )
        else:
            for year in range( startYear, endYear + 1 ):
                data['arg01'] = year
                for semester in range( 1, 3 ):
                    data['yms'] = '{0},{1}'.format( year, semester )
                    data['arg02'] = semester
                    soup = BeautifulSoup( sson.post( searchCourseUrl, data = data ).text, 'lxml' )
                    getCourse( soup )
