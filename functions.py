import pandas as pd
import nltk
import os

def load_original_Bible():
    df = pd.read_csv('kjb-en/Bible.txt', sep='<', header=None)
    df.columns = ['verse']
    return df

def get_original_words(original_df):
    # Get all the words:
    words = []
    chars_to_remove = [',', '.', ';', ')', '(', '?', "'s", "'", ' ']
    for index, row in original_df.iterrows():
        for word in [word for word in row['verse'].split(' ') if ':' not in word]:
            word = word.lower()
            for char in chars_to_remove:
                word = word.replace(char, '')
            if word.replace(' ', '')!='':
                words.append(word)
    # Count and prep:
    res = pd.DataFrame({
        'word': words
    })
    index_df = res.drop_duplicates('word', keep='first')
    index_df = index_df.reset_index(drop=True).reset_index()
    index_df.columns = ['word_appear_place', 'word']
    index_df['word_appear_place'] = index_df['word_appear_place'] + 1 #start counting from 1
    word_count_df = pd.DataFrame(res['word'].value_counts()).reset_index()
    word_count_df.columns = ['word', 'word_use_count']
    words_df = index_df.merge(word_count_df, on='word', how='left').sort_values('word_appear_place')
    return words_df

def get_word_info_by_nltk(words_df):
    # NLP Stemming (affected -> affect) NLTK.py : pst=PorterStemmer(), pst.stem("given") -> give
    # NLP Lemmatization (went -> go) NLTK.py : lem=WordNetLemmatizer()
    # NLP POS (Parts Of Speech) : nltk.pos_tag(token) -> Verb, Noun... ex tuple: ('John', 'NNP')
    pst=nltk.PorterStemmer()
    lem=nltk.WordNetLemmatizer()
    words = []
    stems = []
    #lemmas = []
    #poss = []
    for word in words_df['word']:
        words.append(word)
        stems.append(pst.stem(word))
        #lemmas.append(lem.lemmatize(word))
        #poss.append(nltk.pos_tag([word])[0][1])
    res = pd.DataFrame({
        'word': words
        ,'nltk_stem': stems
        #,'lemma': lemmas
        #,'part_of_speech': poss
    })
    words_df = words_df.merge(res, on='word', how='left').sort_values('word_appear_place')
    return words_df

def get_word_dict():
    cache = 'речник.csv'
    csv_sep = ':'
    if os.path.exists(cache):
        df = pd.read_csv(cache, sep=csv_sep)
    else:
        df = pd.DataFrame(columns=['word','root','root_bg','word_bg','comment'])
        df.to_csv(cache, index=False, sep=csv_sep)
    return df


def get_words_df(use_cache=True):
    cache = 'data/words_df.csv'
    csv_sep = ':'
    if os.path.exists(cache) and use_cache:
        df = pd.read_csv(cache, sep=csv_sep)
    else:
        df = load_original_Bible()
        df = get_original_words(df)
        df = get_word_info_by_nltk(df)
        df.to_csv(cache, index=False, sep=csv_sep)
    df = df.merge(get_word_dict(), on='word', how='left')
    return df