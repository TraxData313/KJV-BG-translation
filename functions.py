import pandas as pd
import nltk
import os

def load_original_Bible():
    df = pd.read_csv('kjb-en/Bible.txt', sep='<', header=None)
    df.columns = ['verse']
    return df

def load_translated_Bible():
    df = pd.read_csv('kjb-bg/Библия.txt', sep='<', header=None)
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
    cache = 'речник.txt'
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


def load_the_transl_dict():
    df = pd.read_csv('речник.txt', sep=':')
    transl_dict = {}
    for index, row in df.iterrows():
        transl_dict[row['word'].replace(' ', '')] = row['word_bg'].replace(' ', '') #making sure there are no white spaces
    return transl_dict

def translate_word(word, transl_dict):
    chars_to_remove = [',', '.', ';', ')', '(', '?', "'s", "'", ' ', ':', "s'", '!']
    # Uppercase checks:
    begins_with_CAP = word[0].isupper() and word!='I'
    if len(word)>1:
        is_all_CAPS = begins_with_CAP & word[1].isupper()
    else:
        is_all_CAPS = False
    # Replace cond:
    word = word.lower()
    pruned_word = word
    for char in chars_to_remove:
        pruned_word = pruned_word.replace(char, '')
    if pruned_word in transl_dict.keys():
        word = word.replace(pruned_word, transl_dict[pruned_word])
    else:
        pruned_word = None
    # Uppercase restoration:
    if begins_with_CAP:
        word = word.capitalize()
    if is_all_CAPS:
        word = word.upper()
    return word, pruned_word

def translate_verse(verse, transl_dict):
    words = []
    changed_words = []
    for i, word in enumerate(verse.split(' ')):
        if i != 0: #the first word is the name of the book, skip it
            word, pruned_word = translate_word(word, transl_dict)
            if pruned_word is not None:
                changed_words.append(pruned_word)
        words.append(word)
    new_verse = ' '.join(words)
    return new_verse, changed_words

def translate_df(save=True):
    # Load the data:
    df = load_translated_Bible()
    transl_dict = load_the_transl_dict()
    # Translate:
    new_verses = []
    changed_words = []
    for verse in df['verse']:
        new_verse, changed_words_part = translate_verse(verse, transl_dict)
        changed_words += changed_words_part
        new_verses.append(new_verse)
    new_df = pd.DataFrame({'verse': new_verses})
    # The changes:
    changes_df = pd.DataFrame({'changed_word': changed_words})
    changes_df = pd.DataFrame(changes_df['changed_word'].value_counts()).reset_index()
    changes_df.columns = ['word', 'translated_count']
    changes_df['translate_ts'] = pd.Timestamp.now()
    if save:
        # Save the Bible:
        save_file = 'kjb-bg/Библия.txt'
        new_df.to_csv(save_file, index=False, header=False, sep='>')
        # Log the changes:
        word_change_log_file = 'logs/word_change_log_file.csv'
        if os.path.exists(word_change_log_file):
            changes_df.to_csv(word_change_log_file, index=False, header=False, mode='a')
        else:
            changes_df.to_csv(word_change_log_file, index=False, header=True)
    return changes_df