'''
pip install -q youtube_transcript_api
pip install -U spacy
python -m spacy download en_core_web_lg


!!! do install the above to run the code !!! 
'''

from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation


fallout=request.form.to_dict()
youtube_video = fallout
video_id = youtube_video.split("=")[1]

transcript = YouTubeTranscriptApi.get_transcript(video_id)

result = ""
for i in transcript:
  result += ' '+ i['text']

stopwords = list(STOP_WORDS)

nlp = spacy.load('en_core_web_lg')
doc = nlp(result)
tokens = [token.text for token in doc]


punctuation = punctuation + "\n"


word_frequencies = {}

for word in doc: 
      if word.text.lower() not in stopwords:
        if word.text.lower() not in punctuation:
          if word.text not in word_frequencies.keys():
            word_frequencies[word.text] = 1
          else:
            word_frequencies[word.text] += 1

# word_frequencies

max_frequency = max(word_frequencies.values())
# max_frequency

for word in word_frequencies.keys():
  word_frequencies[word] = word_frequencies[word]/max_frequency


sentence_tokens = [sent for sent in doc.sents]
# print(sentence_tokens)

sentence_scores = {}

for sent in sentence_tokens:
    for word in sent:
      if word.text.lower() in word_frequencies.keys():
        if sent not in sentence_scores.keys():
          sentence_scores[sent] = word_frequencies[word.text.lower()]
        else:
          sentence_scores[sent] += word_frequencies[word.text.lower()]


from heapq import nlargest
select_length = int (len(sentence_tokens)*0.1)

summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
# print(len(summary))
print(summary)

