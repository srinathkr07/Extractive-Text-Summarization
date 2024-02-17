# Extractive-Text-Summarization

A simple news article text summarizer made from scratch.

## Working of the application

- Given a news article's link from [The Hindu](https://www.thehindu.com/) and the number of sentences to be present in the summary as input, using BeautifulSoup library, scrape the text of the article which is called document.

- Tokenize the entire document into sentences and sentences into words. We need individual words in order to determine their relative frequency in the document, and assign a corresponding score; we need individual sentences to subsequently sum the scores of each word within in order to determine 'sentence importance'.

- Count the occurence of each word in the document. After finding the counts, we build a frequency distribution of words. To get the distribution, divide the occurrence of each word by the frequency of the most occurring word.

- Next, assign a score to the sentences by using the frequency distribution generated. This is simply summing up the scores of each word in a sentence. This function takes a max_len argument which sets a maximum length to sentences which are to be considered for use in the summarization.

- Based on the scores, select the top 'k' sentences that represent the summary of the article. Display the summary along with the top 'k' sentences and their sentence scores.

## Tech Stack used

- Python. 
- [Streamlit](https://www.streamlit.io/), an open source app framework. 
- [Heroku](https://www.heroku.com/), a cloud application platform. 

## Screenshots

![](/Screenshots/Image1.png)

![](/Screenshots/Image2.png)

![](/Screenshots/Image3.png)

## Developed by

[Srinath K R](https://github.com/srinathkr07).
