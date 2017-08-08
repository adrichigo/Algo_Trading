import datetime
import string


#####################################################
#
#
#
#####################################################
def time_formatting(date):
    return str(date).replace('-', '+', -1)

######################################################
#
#
#
######################################################
def construct_Quote_Request(quote,startTime):
    # endTime is today
    endTime = time_formatting(datetime.date.today())
    #formatting the startTime
    startTime = time_formatting(startTime)

    url = "http://www.google.com/finance/historical?q="
    url += quote
    url += "&histperiod=daily&startdate="
    url += startTime
    url += "&enddate="
    url += endTime
    url += "&output=csv"
    return url

######################################################
#
#
#
######################################################
