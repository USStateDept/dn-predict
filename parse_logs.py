#! /usr/bin/env python3

import re
import sys
import json
import csv
import codecs
from datetime import datetime

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

class FileIO(object):
  '''
  General read/write of files
  '''
  def __init__(self, in_file=None, out_file=None, data=None):
    self.file = in_file
    self.out = out_file
    # self.fields = []
    self.data = data

  def write(self):
    if self.out is not None:
      with codecs.open(self.out, "w", encoding="utf-8") as f:
        fieldnames = list(self.data_list[0].keys()) 
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=DELIMITER)                 
        writer.writeheader()                                             
        for event in self.data_list:                                      
          writer.writerow(event) 
    else:
      print("Output file is not specified - cannot write", file=sys.stderr)
  
  def read(self, verbose=False):
    if self.file is not None:
      with codecs.open(self.file, "r", encoding=LOG_ENCODING) as f:
        i = 0
        li = []
        reader = csv.DictReader(f, delimiter=" ")
        for row in reader:
          if verbose:
            i += 1 
            if i % 25 == 0:
              print("processed %s events" % i)
          li.append(row)
        self.data = li
    else:
      print("Input file is not specified - cannot read", file=sys.stderr)


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
