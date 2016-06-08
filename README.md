# DN Predict
Data-informed internal communications

## Overview
DN (Department Notices) are the Department's "mass-market" internal communications that are delivered to almost all domestic staff. DN Predict was created to help Notice authors determine if their internal marketing strategy is likely to be successful, and if not, how they might go about iterating in order to enhance the appeal. 

**How?**

By ingesting several months worth of data related to Notices web traffic, I created a simple model that connects Notice title diction to numbers of views. Using that model, I created a client-side web application that allows authors to enter a proposed title. If there are data to support it, the app will return:

+ The predicted number of views
+ A word heatmap to highlight correlations between views and words
+ A histogram that highlights the likelihood of the accuracy of the prediction

This is not a complex tool, and was produced as a  quick demonstrator for how data can be used to enhance internal communication within the Department. Note that it is intentionally 'undesigned' to ape the current look and feel of the DN :)

---

## Usage

Data from DN server logs and emails were parsed using `parse_logs.py` and `parse_emails.py`. There were, unfortunately, some manual cleanup steps of the logs that I failed to capture - removal of errors, server restart warnings, etc. Once stripped down to only those requests that were for DN pages, the data were dumped into a pair of SQL tables (`schema.sql`) and then analyzed (`analysis.sql`). For this app, the analysis is simply an ordered list of DN titles, ranked from most traffic ('events') to least. This output was then passed to `dn_predict.py` to output the ranges and model. Both of these values are then converted into JavaScript (`ranges.js` and `model.js`) for use in the webapp.

N.B.: `dn_predict.py` and `predict.js` are implementations of the same algorithm (in order to accurately compare the model to novel inputs, they must be handled identically), and must therefore be altered in lockstep.

---

## Dependencies

### Python
Written in Python 3.5.1; Not 2.x compatible.

#### Packages

NLTK - http://www.nltk.org/

### JavaScript/CSS

Porter Stemmer - http://tartarus.org/martin/PorterStemmer/

Foundation for sites (v6.x) - http://foundation.zurb.com/sites.html

---

## To Do List

The original `dn_predict.py` was lost to an unfortunate hardware failure, and is currently being reverse engineered from `predict.js`... hang tight!
