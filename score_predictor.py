
##
## IMPORTS
##

from __future__ import print_function
import re
import numpy as np
# import statistics # py3 only?
from scipy import stats 
from nltk.corpus import stopwords

##
## CONSTANTS
##

# set stopwords
stops = stopwords.words("english")

# file io
in_file = "./hits+titles.tsv"

# read input file
# exptected format: {score[int]}\t{text[string]}
ingest_list = []
with open(in_file, "rU") as f:
  for line in f.readlines():
    ingest_list.append(line)
 
# dl1 = []
# for item in ingest_list:
#   a = item.partition("\t")
#   b = {"score": int(a[0]), "string": a[2]}
#   dl1.append(b)


# convert ingest_list into list of dictionaries:
dl1 = []
for item in ingest_list:
  a = item.partition("\t")
  b = {"score": int(a[0]), "string": a[2]}
  c = {"score": b["score"],
       "parsed_str": [w for w in re.split("\W", b["string"].strip().lower()) 
       if w not in stops and w != ""]}
  dl1.append(c)

# using parsed strings, create master dictionary that logs all scores for each string
# do we need to remove rare words that might not be reliably predictive? As in d2 block, below
d1 = {}
for item in dl1:
  for word in item["parsed_str"]:
    if word != "" and word not in d1:
      d1[word] = [item["score"]]
    elif word != "" and word in d1:
      d1[word].append(item["score"])

# to_del = []
# for item in d1:
#   if len(d1[item]) < 3:
#     to_del.append(item)

# for jtem in to_del:
#   del d1[jtem]

# d2 = []
# for item in d1:
#   if len(d1[item]) >= 3:
#     mean = np.mean(d1[item])
#     std_dev = np.std(d1[item])
#     d2.append((std_dev, mean, item))

# # sort by variance 
# d2.sort()

d_filtered = {}
for item in d1:
  if len(d1[item]) >= 3:
    d_filtered[item] = d1[item]

# create vector dictionary and lists (mean and std_dev)
# this is - effectively - the model for prediction
vector_dict = {} # format {"string": index[int], ...}
vector_mean = []
vector_std = []

i = 0
for term in d_filtered:
  vector_dict[term] = i 
  vector_mean.append(np.mean(d_filtered[term]))
  vector_std.append(np.std(d_filtered[term]))
  i += 1

length = len(vector_dict)
n_slices = 20
slc_size = length / float(n_slices)

std_sorted = vector_std[:]
std_sorted.sort()

std_co_vals = []
for i in range(n_slices):
  std_co_vals.append(std_sorted[int((i+1) * f_slice - 1)]) 

## evaluating model
def eval_model(std_co, d_test=dl1):
  predicted_v_actual = []
  for doc in d_test:
    actual = doc["score"]
    s = doc["parsed_str"]
    scalar_list = []
    for word in s:
      if word in vector_dict and vector_std[vector_dict[word]] >= std_co: #short circuit eval
        idx = vector_dict[word]
        vec = vector_mean[idx]
        scalar_list.append(vec)
    sqr_list = []
    for score in scalar_list:
      sqr_list.append(score ** 2)
    predicted_score = np.sqrt(sum(sqr_list))
    predicted_v_actual.append((predicted_score, actual))
  slope, intercept, r_value, p_value, std_err = stats.linregress(predicted_v_actual)
  return slope, intercept, r_value, predicted_v_actual


for co in std_co_vals:
  slope, intercept, r_value, xy = eval_model(co)
  print("%s  :  %s  :  %s  :  %s" % (co, r_value, slope, intercept))


determined_co = 251.937823017
slope, intercept, r_value, xy = eval_model(determined_co)


out_file = "dn_prediction_vec3.csv"

with open(out_file, "w") as f:
  for line in xy:
    w = "\t".join([ str(x) for x in line ]) + "\n"
    f.write(w)


##
## OLD
##


scalar_list = []
for word in s:
  if word in vector_dict:
    idx = vector_dict[word]
    vec = vector_mean[idx]
    scalar_list.append(vec)

# now have scalar values of non-zero vectors
# can use to determine magnitude of vector
sqr_list = []
for score in scalar_list:
  sqr_list.append(score ** 2)

predicted_score = np.sqrt(sum(sqr_list))

test_str = "IMPORTANT REMINDERS: Guidance On Inclement Weather, Government Closures And Delayed Arrivals"

s = [w for w in re.split("\W", test_str.strip().lower()) if w not in stops and w != ""]

# mean of all feature scores
def rankMeans(strng, score_dict):
  s = [w for w in re.split("\W", strng.strip().lower()) if w not in stops and w != ""]
  scores = []
  words = []
  for word in s:
    if word in score_dict:
      scores.append(score_dict[word]["mean"])
      words.append(word)
  expected_score = np.mean(scores)
  # scores_std_dev = np.std(scores)
  derevations = zip(words, scores)
  return expected_score, derevations

# sum of each feature/std_dev
# nope! basically flattens the scores
def rankSumVar(strng, score_dict):
  s = [w for w in re.split("\W", strng.strip().lower()) if w not in stops and w != ""]
  scores = []
  words = []
  for word in s:
    if word in score_dict:
      scores.append(score_dict[word]["mean"] / np.sqrt(score_dict[word]["std_dev"]))
      words.append(word)
  expected_score = sum(scores)
  # scores_std_dev = np.std(scores)
  derevations = zip(words, scores)
  return expected_score, derevations

predicted_v_actual = []

for item in dl1:
  score_actual = item["score"]
  try:
    predict = rankSumVar(item["string"], score_dict)
  except ZeroDivisionError:
    print("Cannot predict: " + item["string"])
    pass
  score_predicted = predict[0]
  predicted_v_actual.append((score_predicted, score_actual))
