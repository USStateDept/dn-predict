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

START = re.compile("^From:	eDepartment Notices")
SENT = re.compile("^Sent:")
NOTICE = re.compile("^\*") # not uniform; some notices have line breaks, 
                           # so this will not catch all. I've manually edited source
                           # based on the AssertionError below
URL = re.compile("http[a-zA-Z-0-9=\.:/_\?]*")
MESSAGE_NO = re.compile("	Message #[0-9].*")

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
  
  # to do - add cla for write tsv
  write_tsv = True
  
  notices = Notices(in_file=in_file, out_file=out_file, write_tsv=write_tsv)
  notices.read()
  notices.parse()
  if write_tsv:
    notices.flatten()
  notices.fmt()
  notices.write()

##
## CLASSES
##

class FileIO(object):
  '''
  General read/write of files
  '''
  def __init__(self, in_file=None, out_file=None, data=None, write_tsv=False):
    self.intake = in_file
    self.out = out_file
    self.write_tsv = write_tsv
    # self.fields = []
    self.data_in = data
    self.data_temp = []
    self.data_out = None

  def fmt(self):
    if not self.write_tsv:
      self.data_out = json.dumps(self.data_temp, sort_keys=True, indent=2)
    else:
      self.data_out = self.data_temp

  def write(self):
    if self.out is not None and self.data_out is not None:
      if self.write_tsv is True:
        files = list(self.data_out.keys())
        for file in files:
          filename = file + "_" + self.out
          with codecs.open(filename, "w", encoding="utf-8") as f:
            # need to write two files, not one
            fieldnames = list(self.data_out[file][0].keys()) 
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=DELIMITER)                 
            writer.writeheader()                                             
            for event in self.data_out[file]:                                      
              writer.writerow(event) 
      else:
        with codecs.open(self.out, "w", "utf-8") as f:
          for line in self.data_out:
            # f.write(line + u"\n")
            f.write(line)
    else:
      print("Output file is not specified - cannot write", file=sys.stderr)
  
  def read(self, debug=False):
    if self.intake is not None:
      with codecs.open(self.intake, "r", "utf-8") as f:
        li = []
        i = 0
        for line in f.readlines():
          if debug:
            i += 1 
            print(str(i))
          li.append(line)
        self.data_in = li
    else:
      print("Input file is not specified - cannot read", file=sys.stderr)


class Notices(FileIO):
  '''
  Class that catalogs notices data from email source
  '''
  def __init__(self, *args, **kwargs):
    FileIO.__init__(self, *args, **kwargs)
    self.is_flat = False
    
  def parse(self):
    switch = False
    line_no = 0
    # False = not inside a record, True = inside
    for line in self.data_in:
      line_no += 1
      if switch == False:
        d = {"sent_date": None,
             "weekday": None,
             "notices": [],
             "urls": [],
             "message_no": None}
        if START.match(line):
          # we have now entered a record, need new data_dict
          switch = True
      else:
        if SENT.match(line):
          date = line.split("\t")[1].strip()
          date = datetime.strptime(date, "%A, %B %d, %Y %I:%M %p")
          d["sent_date"] = date.isoformat()
          d["weekday"] = date.isoweekday()
        elif NOTICE.match(line):
          l = line.strip("^*\t").strip().strip(">").split("<")
          try:
            assert len(l) == 2
            d["notices"].append(l[0])
            d["urls"].append(l[1])
          except AssertionError:
            print(str(line_no) + " ** notice / url error: " + line, file=sys.stderr)
        elif MESSAGE_NO.match(line):
          try:
            d["message_no"] = int(line.strip().split(" #")[1])
          except ValueError:
            print(str(line_no) + " ** message number error: " + line, file=sys.stderr)
      if d["message_no"] is not None:
        # message number is the last content line of the email, therefore close it out
        self.data_temp.append(d)
        switch = False
  
  def flatten(self):
    '''Converts relational-like output of self.parse() into a flat, csv-like list of dicts'''
    if self.data_temp != []:
      messages = []
      notices = []
      for document in self.data_temp:
        message = {"message_no": document["message_no"],
                   "sent_date": document["sent_date"],
                   "count": len(document["notices"]),
                   "weekday": document["weekday"]}
        
        messages.append(message)
        
        for i in range(len(document["notices"])):
          notice = {"index": i + 1,
                    "title": document["notices"][i],
                    "url": document["urls"][i],
                    "message_no": document["message_no"],
                    "notice_id": int(document["urls"][i].split("=")[1])}
          notices.append(notice)
        
      self.is_flat = True
      self.data_temp = {"messages": messages, "notices": notices}
    else:
      print("processed dataset is empty; run parse() before flatten()", file=sys.stderr)
    
    
##
## MAIN 
##

if __name__ == '__main__':
  main()