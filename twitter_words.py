import os
import tweepy
import json
from flask import Flask,render_template,send_from_directory,request
import re
from nltk.corpus import stopwords
import nltk

app = Flask(__name__)

@app.route('/data', methods=['GET', 'POST'])
def data():
    auth = tweepy.OAuthHandler(consumer_key=os.environ.get('CONS_KEY'), consumer_secret=os.environ.get('CONS_SECRET'))
    auth.set_access_token(os.environ.get('TOK_KEY'), os.environ.get('TOK_SECRET'))

    api = tweepy.API(auth)

    query = 'umich'

    result = api.search(q=query)

    resDict = {}

    stopwds = ['a','able','about','across','after','all','almost','also','am','among',
             'an','and','any','are','as','at','be','because','been','but','by','can',
             'cannot','could','dear','did','do','does','either','else','ever','every',
             'for','from','get','got','had','has','have','he','her','hers','him','his',
             'how','however','i','if','in','into','is','it','its','just','least','let',
             'like','likely','may','me','might','most','must','my','neither','no','nor',
           'not','of','off','often','on','only','or','other','our','own','rather','said',
             'say','says','she','should','since','so','some','than','that','the','their',
             'them','then','there','these','they','this','tis','to','too','twas','us',
             'wants','was','we','were','what','when','where','which','while','who',
             'whom','why','will','with','would','yet','you','your']

    for i in range(0, len(result)):
        innerArr = result[i].text.split(" ")
        for j in range(0, len(innerArr)):
            word = re.sub('["#:,.!?\[\]\)\(]', '', innerArr[j]).lower()
            if (len(word) == 1) or (word in stopwds) or ("http" in word) or ("rt" in word) or ("@" in word):
                continue
            if word in resDict:
                resDict[word] = resDict[word] + 1
            else:
                resDict[word] = 1

    return json.dumps(resDict)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('twitter_words.html')

@app.route('/cloudify', methods=['GET', 'POST'])
def cloud():
    return render_template('cloud.html')


if __name__ == '__main__':
    # Bind to PORT if defined (environment variable on heroku)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)