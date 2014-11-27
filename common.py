#!/Users/mauricio/anaconda/bin/python2.7

import requests, urllib2, simplejson, datetime

# Constants
MAX_RETRIES = 15       #Max number of retries when requesting data
TIMEOUT_RETURN = 100   #Timeout in calling API to retrieve results
DELAY        = 0.5     #Delay per retry in seconds (increases * no_retries)
MAX_FIELDS = 300       #Max fields to retrieve from field request via API


def logQueryData(loggly_key, data, test_flag):

    """ Logs a JSON object to Loggly """
    log_data = "PLAINTEXT=" + urllib2.quote(simplejson.dumps(data))

    if test_flag:
        print data

    else:
        # Send log data to Loggly
        urllib2.urlopen("https://logs-01.loggly.com/inputs/" + loggly_key + "/tag/queryAPI/",
                        log_data)

def getAPI(search_url, username, password):
    """ Fetches data from Loggly via the API """
    
    retries = 0
    while retries < MAX_RETRIES:
 
        try:
            # We launch the search
            r = requests.get(search_url, auth=(username, password), timeout=TIMEOUT_RETURN)
            res = r.json()
            try:
                if res['total_events']  >= 0:
                    return r.status_code, res['total_events']
                else:
                    return r.status_code, 0
 
            except ValueError as error:
                print '%s Error: %s - response: %s\n' % ( datetime.datetime.utcnow(), error, r )
 
            break
 
        except ValueError:
            print '%s Error status code: %d\n' % ( datetime.datetime.utcnow(), r.status_code )
            retries = retries + 1
 
        time.sleep(DELAY * (retries+1) )
 
    return 0