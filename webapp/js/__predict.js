
var stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again",
             "against", "all", "almost", "alone", "along", "already", "also","although",
             "always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another",
             "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",
             "at", "back","be","became", "because","become","becomes", "becoming", "been",
             "before", "beforehand", "behind", "being", "below", "beside", "besides",
             "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can",
             "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe",
             "detail", "do", "done", "down", "due", "during", "each", "eg", "eight",
             "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even",
             "ever", "every", "everyone", "everything", "everywhere", "except", "few",
             "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former",
             "formerly", "forty", "found", "four", "from", "front", "full", "further",
             "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her",
             "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself",
             "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc",
             "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last",
             "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me",
             "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
             "move", "much", "must", "my", "myself", "name", "namely", "neither", "never",
             "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not",
             "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only",
             "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out",
             "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same",
             "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she",
             "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
             "somehow", "someone", "something", "sometime", "sometimes", "somewhere",
             "still", "such", "system", "take", "ten", "than", "that", "the", "their",
             "them", "themselves", "then", "thence", "there", "thereafter", "thereby",
             "therefore", "therein", "thereupon", "these", "they", "thickv", "thin",
             "third", "this", "those", "though", "three", "through", "throughout", "thru",
             "thus", "to", "together", "too", "top", "toward", "towards", "twelve",
             "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via",
             "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever",
             "where", "whereafter", "whereas", "whereby", "wherein", "whereupon",
             "wherever", "whether", "which", "while", "whither", "who", "whoever",
             "whole", "whom", "whose", "why", "will", "with", "within", "without",
             "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"];

function add(a, b) {
    return a + b;
}

function isInt(val) {
    return Number(parseFloat(val))==val;
}

function explain(score_map) {
  // for each word used in the prediction, specifies to which category it is
  // most clearly associated, but index value
  var word_to_cat = {};
  var idx;
  for (var word in score_map) {
    var best_score = 0;
    for (var i = 0; i < score_map[word].length; i++) {
      if ( (0 < score_map[word][i]) && (score_map[word][i] > best_score)) {
        best_score = score_map[word][i];
        idx = i;
      }
    }
    word_to_cat[word] = idx;
  }
  return word_to_cat;
}
/*
  def explain(self):
    '''for each word used in the prediction, specifies to which
    category it is most associated, by index value'''
    self.word_to_cat = {}
    for word in self.score_map:
      best_score = 0
      for i in range(len(self.score_map[word])):
        if 0 < self.score_map[word][i] > best_score:
          best_score = self.score_map[word][i]
          idx = i
      self.word_to_cat[word] = idx
    return self.word_to_cat
*/

function cleanString(w){

  if (!(w.toLowerCase() in stopwords) && w != " " && isInt(w)) {
    return stemmer(w);
  }
  else {
    return null;
  }
}

function predictScore(in_text, ranges, model, stopwords){
  var text_split = in_text.split(/\W+/g);
  var text_map = {};
  var predict_dict = {};

  for (var w in text_split) {
    var key = w;
    var val = cleanString(w);
    if ( !(val === null) ) {
      text_map[key] = val;
    }
  }

  if ( Object.keys(text_map).length === 0 ) {
    var predict = {};
    predict["category"] = null;
    predict["explain"] = "All words removed by initial filter";
  }
  else {
    var score_map = {};
    for (var k in text_map) {
      if ( text_map[k] in Object.keys(model) ) {
        score_map[k] = model[text_map[k]];
      }
    }

    var score_list = function (score_map) {
      // initialize new array of 0s for each of the ranges
      var s_list = new Array(ranges.length).fill(0);

      function zip2d(e, i) {
        return [ s_list[i], score_map[item[i]] ];
      }

      // for each listing in score_map, zip toegther with s_list and then add each
      // value in s_list to provide totals for each 'bin'
      for (var item in score_map) {
        var _2d_list = s_list.map(zip2d(e, i));
        for (var i = 0; i < s_list.length; i++) {
          s_list[i] = _2d_list[i].reduce(add,0);
        }
      }
    };
    var denominator = score_list.reduce(add,0);
    if (denominator === 0) {
      predict_dict["category"] = null;
      predict_dict["explain"] = "Insufficient data to estimate score";
    }
    else {
      var normalized_score_list = [];

      for (var i = 0; i < score_list.length; i++) {
        normalized_score_list[i] = score_list[i] / denominator; // should not have divide by 0 errors
      }

      var range_score_list = [];
      var r;
      var prob;

      // name the strings for the different range categories
      for (i = 0; i < ranges.length; i++) {
        if (i === 0) {
          r = ranges[i].toString() + "+";
          prob = normalized_score_list[i].toString();
        }

        else {
          r = ranges[i].toString() + " - " + ranges[i-1].toString();
          prob = normalized_score_list[i].toString();
        }

        range_score_list[i] = [r, prob];
      }

      predict_dict["score_distribution"] = range_score_list;
      predict_dict["score"] = Math.max(...normalized_score_list);
      predict_dict["explain"] = explain(score_map);
    }
  }

  return predict_dict;
}


/*

        predict_dict["score_distribution"] = self.range_score_list
        predict_dict["score"] = max(self.normalized_score_list)
        predict_dict["category"] = sorted([ (item[1],item[0]) for item in self.range_score_list ], reverse=True)[0][1]

        if explain:
          predict_dict["explain"] = self.explain()

    if to_print:
      print(json.dumps(predict_dict, sort_keys=True, indent=2))
    else:
      return predict_dict
  */