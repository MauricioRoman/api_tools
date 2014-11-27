#!/usr/bin/python

import time, sys, argparse, datetime
from common import logQueryData, getAPI, MAX_FIELDS

def process_arguments(args):

    parser = argparse.ArgumentParser(description=
                        "Create Apdex metric from Loggly data via API")

    # Let's add our arguments
    parser.add_argument('-t',
                        dest='T',
                        type=float,
                        required=True,
                        help='T threshold'
                        )

    parser.add_argument('-f',
                        dest='pivot_field',
                        type=str,
                        required=True,
                        help='Pivot Field'
                        )

    parser.add_argument('-l',
                        dest='token',
                        type=str,
                        required=True,
                        help='Loggly token'
                        )

    parser.add_argument('-u',
                        dest='username',
                        type=str,
                        required=True,
                        help='Username'
                        )

    parser.add_argument('-p',
                        dest='password',
                        type=str,
                        required=True,
                        help='Password'
                        )

    parser.add_argument('-s',
                        dest='subdomain',
                        type=str,
                        required=True,
                        help='Subdomain'
                        )

    parser.add_argument('-i',
                        dest='interval',
                        type=str,
                        required=True,
                        help='Search time interval (ex. 15m, 1h)'
                        )

    parser.add_argument('--test', action='store_true',
                        help='Test -- does not send data to Loggly')

    options = parser.parse_args(args)

    return options


def getApdex(id, query, pivot_field, percentages, searchFrom, searchTo, timestamp,
              subdomain, deployment, username, password, output_key, test_flag):
    """ Calculates Apdex score and stores result back into Loggly
        id: a label for the log, for instance, indicating how often the data is fetched
        query: dict with queries to generate numerator, denominator, etc. for calculation
        percentages: dict with definitions of how metrics are calculated
        -- all other terms are self explanatory --
    """

    results = {}

    #Iterate over queries and get results
    for key in query.iterkeys():

        search_url = "http://%s.%s/apiv2/fields/%s?q=%s&from=%s&until=%s&facet_size=%d" % (
                      subdomain, deployment,pivot_field, query[key],searchFrom,searchTo, MAX_FIELDS)

        status, results[key] =  getAPI(search_url, username, password)

    # Get last term in pivot field to use as key in log event
    pivot = pivot_field.split('.')[-1] + '_perf'

    Rs = getApdexPercent(results, percentages, 'Rs')
    Rt = getApdexPercent(results, percentages, 'Rt') - Rs

    apdex = Rs + Rt / 2.0

    metrics_dict = dict( zip( [ 'Rs','Rt','apdex'],
                              [ round(Rs,1), round(Rt,1), round(apdex,1)] ))

    #Send data to your data store 
    # (Put your own code here)
   
    #Log to stdout
    now = datetime.datetime.now()
    print now, pivot, metrics_dict

    #Send values back to Loggly
    logQueryData(output_key,dict([('timestamp',str(timestamp.isoformat()) ), ('action','analytics'),
                                    ('bin',id), (pivot,metrics_dict) ] ), test_flag)

    return 0

def getApdexPercent(results, percentages, key):
        percentage = 0.
        numerator = results[percentages[key]['numerator']]
        denominator = results[percentages[key]['denominator']]

        if denominator > 0:
            percentage = round( float(numerator) / float(denominator) * 100., 2)

        return percentage

def main():

    options = process_arguments(sys.argv[1:])

    query_terms = {
                   'A': '%s:*' % options.pivot_field,
                   'B': '%s:<%d' % (options.pivot_field, options.T),
                   'C': '%s:<%d' % (options.pivot_field, 4*options.T)
                  }

    percentages = {'Rs':{
                       'numerator':'B',
                       'denominator':'A'
                      },
                   'Rt':{
                       'numerator':'C',
                       'denominator':'A'
                      }
                  }
    now = datetime.datetime.utcnow()

    getApdex(options.interval, query_terms, options.pivot_field, percentages, '-'+options.interval,
            'now', now, options.subdomain, 'loggly.com', options.username, options.password,
            options.token, options.test)

if __name__ == '__main__':
    sys.exit(main())
