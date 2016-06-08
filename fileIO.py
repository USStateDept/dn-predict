
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