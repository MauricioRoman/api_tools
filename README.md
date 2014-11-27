Apdex Tool
==========

Reads a performance metric from your Loggly account via the API, and calculates the Apdex metric with a given threshold T,
and then sends the metric back into Loggly for visualization.

##How to use:

For ease, a bash script is included that just needs 3 parameters:

$ ./apdex.sh <pivot_field> <T> <time interval>

##In a cron job:

*/15 *  *  *  *  $api_tool/my_apdex.sh json.ResponseTime_ms 1000 15m >> $log_dir"apdex.log" 2>&1


##As a python script

If you want to run the Python file directly:

```
$ python apdex.py -h
usage: apdex.py [-h] -t T -f PIVOT_FIELD -l TOKEN -u USERNAME -p PASSWORD -s
                SUBDOMAIN -i INTERVAL [--test]
```

Create Apdex metric from Loggly data via API

```
optional arguments:
  -h, --help      show this help message and exit
  -t T            T threshold
  -f PIVOT_FIELD  Pivot Field
  -l TOKEN        Loggly token
  -u USERNAME     Username
  -p PASSWORD     Password
  -s SUBDOMAIN    Subdomain
  -i INTERVAL     Search time interval (ex. 15m, 1h)
  --test          Test -- does not send data to Loggly
```

Example:

To fetch data, without sending data back into Loggly, use the --test flag:

python apdex.py -t 1000 -f json.ResponseTime_ms -l 63ddb0cf-b5e1-47ab-a581-2027bb8414ac -u john_doe -p 12345 -s acme -i 15m --test


