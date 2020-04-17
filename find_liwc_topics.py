import sys, re, collections
from string import punctuation

class LIWCParser:
  def __init__(self, languageFiles):
    #Initialize with the right languages
    if type(languageFiles) == str:
      self.languages = [languageFiles]
    elif type(languageFiles) == list:
      self.languages = languageFiles

    self.ws = re.compile("\s+")

    categoryDict = {}
    wordToCategories = collections.OrderedDict()

    for lang in self.languages:
      liwcfile = open("langs/" + lang)
      #toss the first line
      liwcfile.readline()
      mode = "readingCats"
      for line in liwcfile:
        line = line.strip()
        if line == "%":
          mode = "readingWords"
        elif mode == "readingCats":
          parts = line.split("\t")
          categoryDict[int(parts[0])] = parts[1]
        elif mode == "readingWords":
          parts = line.split("\t")
          try:
            wordToCategories[parts[0]] = map(int, parts[1:])
          except ValueError as ve:
            sys.stderr.write("%s\n" % (ve,))

    self.categoryDict = categoryDict
    self.wordToCategories = wordToCategories

  def _cleanWord(self, w):
    # return w
    w = "".join([x for x in w if x not in punctuation])
    return w.lower()

  def _stringMatch(self, w1, dictWord):
    if dictWord[-1] == '*':
      dictWord = dictWord[0:-1]
      w1 = w1[0:len(dictWord)]

    return dictWord == w1
    
  def parseDoc(self, words):

    docLabels = []
    for cleanedWord in words:
      wordLabel = []
      hypotheses = [cleanedWord]
      hypotheses += [cleanedWord[0:i] + '*' for i in range(len(cleanedWord))]

      for word in hypotheses:
        tops = self.wordToCategories.get(word, [])
        for topic in tops:
          wordLabel.append(self.categoryDict[topic])
      docLabels.append(wordLabel)
      
    return docLabels

  def getCategoryNames(self):
    return self.categoryDict


