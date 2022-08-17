from wordcloud import WordCloud,STOPWORDS
from nltk.corpus import stopwords
import nltk
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()

def remove_stopwords(text):
# Removes stop words that have no use in sentiment analysis 
  text_tokens = word_tokenize(text)
  text = [word for word in text_tokens if not word in stopwords.words()]

  text = ' '.join(text)
  return text

def nltk2wn_tag(nltk_tag):
  if nltk_tag.startswith('J'):
    return wordnet.ADJ
  elif nltk_tag.startswith('V'):
    return wordnet.VERB
  elif nltk_tag.startswith('N'):
    return wordnet.NOUN
  elif nltk_tag.startswith('R'):
    return wordnet.ADV
  else:                    
    return None

def lemmatize_sentence(sentence):
  nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))    
  wn_tagged = map(lambda x: (x[0], nltk2wn_tag(x[1])), nltk_tagged)
  res_words = []
  nouns = []
  verbs = []
  adjectives = []
  adverbs = []
  for word, tag in wn_tagged:
    if tag is None:                        
      res_words.append(word)
    else:
      res_words.append(lemmatizer.lemmatize(word, tag))
      if tag=='n':
        nouns.append(lemmatizer.lemmatize(word, tag))
      elif tag=='v':
        verbs.append(lemmatizer.lemmatize(word, tag))
      elif tag=='a':
        adjectives.append(lemmatizer.lemmatize(word, tag))
      elif tag=='r':
        adverbs.append(lemmatizer.lemmatize(word, tag))
      # Include adverbs
      else:
        print(tag)
  return ' '.join(res_words), ' '.join(nouns), ' '.join(verbs), ' '.join(adjectives), ' '.join(adverbs)

def generate_wordcloud():
    df = pd.read_csv('headlines.csv')
    df['cleaned_headline'] = df['Headline'].apply(lambda text: lemmatize_sentence(remove_stopwords(text))[0])

    df['nouns'] = df['Headline'].apply(lambda text: lemmatize_sentence(remove_stopwords(text))[1])
    df['verbs'] = df['Headline'].apply(lambda text: lemmatize_sentence(remove_stopwords(text))[2])
    df['adjectives'] = df['Headline'].apply(lambda text: lemmatize_sentence(remove_stopwords(text))[3])
    df['adverbs'] = df['Headline'].apply(lambda text: lemmatize_sentence(remove_stopwords(text))[4])

    text = " ".join(splitted for cleaned in df.cleaned_headline for splitted in cleaned.split())
    text_n = " ".join(splitted for cleaned in df.nouns for splitted in cleaned.split())
    text_v = " ".join(splitted for cleaned in df.verbs for splitted in cleaned.split())
    text_a = " ".join(splitted for cleaned in df.adjectives for splitted in cleaned.split())
    text_r = " ".join(splitted for cleaned in df.adverbs for splitted in cleaned.split())

    word_cloud = WordCloud(collocations = True, background_color = 'white', min_word_length=4, collocation_threshold=30).generate(text)
    word_cloud.to_file("/content/gdrive/My Drive/PPL Project/news_api-main/myflask/static/images/wc.png")
