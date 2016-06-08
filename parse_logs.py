#! /usr/bin/env python3

import re
import sys
import json
import csv
import codecs
from datetime import datetime
from fileIO import FileIO

##
## CONSTANTS and REGEX
##

LOG_ENCODING = "utf-8"
DELIMITER = "\t"

##
## FUNCTIONS
##

def main():
  import argparse
  
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--in", metavar="FILE", dest="in_file", default=None,
                    help="Specify the input FILE.", required=True)
  parser.add_argument("-o", "--out", metavar="FILE", dest="out_file", default=None,
                    help="Specify the output FILE.", required=True)
  args = parser.parse_args()
  in_file = args.in_file
  out_file = args.out_file
  
  log = Logs(in_file=in_file, out_file=out_file)
  log.read(verbose=True)
  log.parse(verbose=True)
  log.data = log.data_list
  log.write()
  

##
## CLASSES
##

class Logs(FileIO):
  '''
  Class that extracts log data
  '''
  def __init__(self, *args, **kwargs):
    FileIO.__init__(self, *args, **kwargs)
    self.data_list = []
    
  def parse(self, verbose=False):
    # want to use csv's Dict reader to produce series of dicts from the logs 
    # need to pull from the dicts the following fields:
    # date, time => single datetime object
    # cs-host, cs-url-stem, cs-url-query => full url? and from here also just notice ID
    # c-ip
    # cs(User-Agent)
    # cs(Cookie)
    # cs(Referer)
    # cs-host
    if self.data is not None:
      for event in self.data:
        try:
          cookie = event["cs(Cookie)"]
          referer = event["cs(Referer)"]
          date = event['date'] + " " + event['time']
          # format: '2016-01-01 00:22:58'
          date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
          d = {"date": date.isoformat(),
              "url": "http://" + event["cs-host"] + event["cs-uri-stem"] + "?" + event["cs-uri-query"],
              "notice_id": int(event["cs-uri-query"].split("=")[1]),
              "ip": event["c-ip"],
              "cookie": cookie if cookie is not "-" else None,
              "referer": referer if referer is not "-" else None,
              "user_agent": event["cs(User-Agent)"]
              }
        except ValueError:
          if verbose:
            print(json.dumps(event, sort_keys=True, indent=2), file=sys.stderr)
        self.data_list.append(d)
##
## MAIN 
##

if __name__ == '__main__':
  main()
