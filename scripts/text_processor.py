from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

class TextProcessor:
    
    def __init__(self):
        self.lemma = WordNetLemmatizer()
        self.tag_map = defaultdict(lambda : "n")
        self.tag_map['J'] = "a"
        self.tag_map['V'] = "v"
        self.tag_map['R'] = "r"
        self.stops = stopwords.words('english')
        
    def get_wordnet_tags(self, tokens):
        return [(x[0], self.tag_map[x[1][0]])
                for x in tokens]
        
    def clean_text(self, text):
        tokens = word_tokenize(text.lower())

        tokens = self.get_wordnet_tags(pos_tag(tokens))
        tokens = [self.lemma.lemmatize(x[0], x[1])
                  for x in tokens]
        tokens = [x for x in tokens
                  if x not in self.stops
                  and len(x) > 2]
        return " ".join(tokens)