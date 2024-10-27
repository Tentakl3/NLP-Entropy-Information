from bs4 import BeautifulSoup
from count import Count
import spacy
import nltk

class Prepro:
    """Class represent preprocesing of text"""
    def __init__(self, file_name, file_stopwords):
        self.file_name = file_name
        self.file_stopwords = file_stopwords
        self.tokens = []
        self.vocabulary = []
    
    def main(self):
        """Main method"""
        norm_string = self.beautiful_html(self.read_corpus())
        raw_tokens = self.raw_tokens(norm_string)
        clean_tokens = self.clean_tokens(raw_tokens)
        tokens = self.delete_stopwords(clean_tokens)
        lemmatize_tokens = self.lemmatize(tokens)

        raw_phrases = self.raw_phrases(raw_tokens)
        clean_phrases = self.clean_phrases(raw_phrases)
        lemma_phrases = self.lemmatize_phrases(clean_phrases)
        phrases = self.clean_phrases(lemma_phrases)

        self.tokens = self.delete_stopwords(lemmatize_tokens)
        self.vocabulary = sorted(list(set(self.tokens)))
        return [self.vocabulary, phrases]

    def read_corpus(self):
        """Read Corpus and lower case letters"""
        f = open(self.file_name, encoding="utf-8")
        text_string = f.read()
        f.close()
        text_string = text_string.lower()
        return text_string
    
    def beautiful_html(self, text_string):
        """Normalize the lxml text from Corpus."""
        soup = BeautifulSoup(text_string, "html.parser")
        norm_string = soup.get_text()
        return norm_string

    def raw_tokens(self, norm_string):
        """Reciebes prepoces text and return raw tokens."""
        raw_tokens=nltk.Text(nltk.word_tokenize(norm_string))
        return raw_tokens
        
    def clean_tokens(self, raw_tokens):
        """Receives a list of raw tokens and returns tokens of letters only."""
        clean_tokens=[]
        for tok in raw_tokens:
            t=[]
            for char in tok:
                if char.isalpha():
                    t.append(char)
            letter_token=''.join(t)
            if letter_token !='':
                clean_tokens.append(letter_token)
        return clean_tokens

    def delete_stopwords(self, clean_tokens):
        """Receives a list of tokens and eliminates stopwords using a file of stopwords."""
        f=open(self.file_stopwords, encoding='utf-8')
        words=f.read()
        stopwords=words.split()
        f.close()
        
        tokens_without_stopwords=[]
        for tok in clean_tokens:
            if tok not in stopwords:
                tokens_without_stopwords.append(tok)
        
        return tokens_without_stopwords

    def lemmatize(self, tokens):
        """Lemmatize the list of tokens"""
        nlp = spacy.load("es_core_news_sm")
        doc = nlp(" ".join(tokens))
        lemmatized_tokens = [token.lemma_ for token in doc if " " not in token.lemma_]
        return lemmatized_tokens
    
    def raw_phrases(self, raw_tokens):
        f=open(self.file_stopwords, encoding='utf-8')
        words=f.read()
        stopwords=words.split()
        f.close()

        phrases = []
        holder = ""
        for token in raw_tokens:
            holder = holder + " " + token
            if token == '.':
                phrases.append(holder)
                holder = ""

        raw_phrases=[]
        t = ""
        for phrase in phrases:
            for char in phrase:
                if char.isalpha():
                    t = t + char
                else:
                    if char == " ":
                        t = t + char
            if t !="":
                raw_phrases.append(t.split())
                t = ""
        
        return raw_phrases
    
    def clean_phrases(self, raw_phrases):
        f=open(self.file_stopwords, encoding='utf-8')
        words=f.read()
        stopwords=words.split()
        f.close()

        clean_phrases = []
        for phrase in raw_phrases:
            t = []
            for token in phrase:
                if token not in stopwords:
                    t.append(token)
            clean_phrases.append(t)
        
        return clean_phrases

    def lemmatize_phrases(self, clean_phrases):
        nlp = spacy.load("es_core_news_sm")
        lemmatized_phrases = []
        for phrase in clean_phrases:
            doc = nlp(" ".join(phrase))
            lemmatized_phrase = [token.lemma_ for token in doc if " " not in token.lemma_]
            lemmatized_phrases.append(lemmatized_phrase)
        
        return lemmatized_phrases

if __name__ == "__main__":
    prepro = Prepro("corpus/e990519_mod.htm", "corpus/stopwords.txt")
    vocabulary, phrases = prepro.main()
    count = Count(vocabulary, phrases)
    count.main()