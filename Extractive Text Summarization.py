import streamlit as st

from bs4 import BeautifulSoup
import requests
import re
from collections import Counter 
from string import punctuation
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stop_words
import pandas as pd
    
def tokenizer(s):
    tokens = []
    for word in s.split(' '):
        tokens.append(word.strip().lower())
        
    return tokens

def sent_tokenizer(s):
    sents = []
    for sent in s.split('.'):
        sents.append(sent.strip())
        
    return sents

def count_words(tokens):
    word_counts = {}
    for token in tokens:
        if token not in stop_words and token not in punctuation:
            if token not in word_counts.keys():
                word_counts[token] = 1
            else:
                word_counts[token] += 1
                
    return word_counts

def word_freq_distribution(word_counts):
    freq_dist = {}
    max_freq = max(word_counts.values())
    for word in word_counts.keys():  
        freq_dist[word] = (word_counts[word]/max_freq)
        
    return freq_dist

def score_sentences(sents, freq_dist, max_len=40):
    sent_scores = {}  
    for sent in sents:
        words = sent.split(' ')
        for word in words:
            if word.lower() in freq_dist.keys():
                if len(words) < max_len:
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = freq_dist[word.lower()]
                    else:
                        sent_scores[sent] += freq_dist[word.lower()]
                        
    return sent_scores

def summarize(sent_scores, k):
    top_sents = Counter(sent_scores) 
    summary = ''
    scores = []
    
    top = top_sents.most_common(k)
    
    for t in top: 
        summary += t[0].strip() + '. '
        scores.append((t[1], t[0]))
        
    return summary[:-1], scores


st.title('Extractive Text Summarization')
st.subheader('A simple news article text summarizer made from scratch')

st.sidebar.subheader('Working of the application')

st.sidebar.markdown("* Given an article's link and the number of sentences to be present in the summary as input, using BeautifulSoup library, scrape the text of the article which is called document. ")
st.sidebar.markdown("* Tokenize the entire document into sentences and sentences into words. We need individual words in order to determine their relative frequency in the document, and assign a corresponding score; we need individual sentences to subsequently sum the scores of each word within in order to determine 'sentence importance'. ")
st.sidebar.markdown("* Count the occurence of each word in the document. After finding the counts, we build a frequency distribution of words. To get the distribution, divide the occurrence of each word by the frequency of the most occurring word. ")
st.sidebar.markdown("* Next, assign a score to the sentences by using the frequency distribution generated. This is simply summing up the scores of each word in a sentence. This function takes a max_len argument which sets a maximum length to sentences which are to be considered for use in the summarization. ")
st.sidebar.markdown("* In the final step, based on the scores, select the top 'k' sentences that represent the summary of the article. ")
st.sidebar.markdown("* Display the summary along with the top 'k' sentences and their sentence scores.")

url = st.text_input('\nEnter URL of news article from thehindu.com: ')
no_of_sentences = st.number_input('Choose the no. of sentences in the summary', min_value = 1)

if url and no_of_sentences and st.button('Summarize'):
    text = ""
    
    r=requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser') 
    content = soup.find('div', attrs = {'id' : re.compile('content-body-14269002-*')})
    
    for p in content.findChildren("p", recursive = 'False'):
        text+=p.text+" "
            
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    st.subheader('Original text: ')
    st.write(text)
    
    tokens = tokenizer(text)
    sents = sent_tokenizer(text)
    word_counts = count_words(tokens)
    freq_dist = word_freq_distribution(word_counts)
    sent_scores = score_sentences(sents, freq_dist)
    summary, summary_sent_scores = summarize(sent_scores, no_of_sentences)
    
    st.subheader('Summarised text: ')
    st.write(summary)
    
    subh = 'Summary sentence score for the top ' + str(no_of_sentences) + ' sentences: '

    st.subheader(subh)
    
    data = []

    for score in summary_sent_scores: 
        data.append([score[1], score[0]])
        
    df = pd.DataFrame(data, columns = ['Sentence', 'Score'])

    st.table(df)
    st.info('An application made by Srinath K R.')
