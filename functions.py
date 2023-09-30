import pandas as pd
import numpy as np
import nltk
import os

books_short_to_full_name_dict = {
        'Ge': '01OT Genesis',
        'Exo': '02OT Exodus',
        'Lev': '03OT Leviticus',
        'Num': '04OT Numbers',
        'Deu': '05OT Deuteronomy',
        'Josh': '06OT Joshua',
        'Jdgs': '07OT Judges',
        'Ruth': '08OT Ruth',
        '1 Sm': '09OT 1 Samuel',
        '2 Sm': '10OT 2 Samuel',
        '1 Ki': '11OT 1 Kings',
        '2 Ki': '12OT 2 Kings',
        '1 Chr': '13OT 1 Chronicles',
        '2 Chr': '14OT 2 Chronicles',
        'Ezra': '15OT Ezra',
        'Neh': '16OT Nehemiah',
        'Est': '17OT Esther',
        'Job': '18OT Job',
        'Psa': '19OT Psalms',
        'Prv': '20OT Proverbs',
        'Eccl': '21OT Ecclesiastes',
        'SSol': '22OT Song of Solomon',
        'Isa': '23OT Isaiah',
        'Jer': '24OT Jeremiah',
        'Lam': '25OT Lamentations',
        'Eze': '26OT Ezekiel',
        'Dan': '27OT Daniel',
        'Hos': '28OT Hosea',
        'Joel': '29OT Joel',
        'Amos': '30OT Amos',
        'Obad': '31OT Obadiah',
        'Jonah': '32OT Jonah',
        'Mic': '33OT Micah',
        'Nahum': '34OT Nahum',
        'Hab': '35OT Habakkuk',
        'Zep': '36OT Zephaniah',
        'Hag': '37OT Haggai',
        'Zec': '38OT Zechariah',
        'Mal': '39OT Malachi',
        'Mat': '40NT Matthew',
        'Mark': '41NT Mark',
        'Luke': '42NT Luke',
        'John': '43NT John',
        'Acts': '44NT The Acts',
        'Rom': '45NT Romans',
        '1 Cor': '46NT 1 Corinthians',
        '2 Cor': '47NT 2 Corinthians',
        'Gal': '48NT Galatians',
        'Eph': '49NT Ephesians',
        'Phi': '50NT Philippians',
        'Col': '51NT Colossians',
        '1 Th': '52NT 1 Thessalonians',
        '2 Th': '53NT 2 Thessalonians',
        '1 Tim': '54NT 1 Timothy',
        '2 Tim': '55NT 2 Timothy',
        'Titus': '56NT Titus',
        'Phmn': '57NT Philemon',
        'Heb': '58NT Hebrews',
        'Jas': '59NT James',
        '1 Pet': '60NT 1 Peter',
        '2 Pet': '61NT 2 Peter',
        'Jn': '62NT 1 John',
        '2 Jn': '63NT 2 John',
        '3 Jn': '64NT 3 John',
        'Jude': '65NT Jude',
        'Rev': '66NT Revelation'
    }

def load_original_Bible():
    df = pd.read_csv('kjb-en/Bible.txt', sep='<', header=None)
    df.columns = ['verse']
    return df

def load_translated_Bible():
    file = 'kjb-bg/Библия.txt'
    if os.path.exists(file):
        df = pd.read_csv(file, sep='<', header=None)
    else:
        df = pd.read_csv('kjb-en/Bible.txt', sep='<', header=None)
        df.to_csv(file, sep='<', header=None)
    df.columns = ['verse']
    return df

def get_original_words(original_df):
    # Get all the words:
    words = []
    chars_to_remove = [',', '.', ';', ')', '(', '?', "'s", "'", ' ', '!']
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
        transl_dict[row['word']] = row['word_bg']
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
        #new_verse, changed_words_part = translate_verse(verse, transl_dict)
        try:
            new_verse, changed_words_part = translate_verse(verse, transl_dict)
        except Exception as e:
            raise Exception(f"ERROR: Could not transpate verse [{verse}] due to [{e}]. Breaking!")
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

def print_translated_word_stats():
    df = get_words_df(use_cache=True)
    total_words = df['word_use_count'].sum()
    translated_words = df.loc[df['word_bg'].fillna(0)!=0]['word_use_count'].sum()
    unique_words = len(df)
    unique_translated_words = len(df.loc[df['word_bg'].fillna(0)!=0])
    progr_mes = f'- [{unique_translated_words}] или [{round(unique_translated_words*100/unique_words,2)}%] от [{unique_words}] уникални думи са преведени\n'
    progr_mes += f'- [{translated_words}] или [{round(translated_words*100/total_words,2)}%] от общо [{total_words}] думи са преведени\n'
    return progr_mes

def estimate_letter_progress(df):
    df = df.copy()
    df['verse'] = df['verse'].str.lower()
    lat_ltrs = {ltr: '<' for ltr in 'abcdefghijklmnopqrstuvwxyz'}
    cyr_ltrs = {ltr: '>' for ltr in 'абвгдежзийклмнопрстуфхцчшщъьюя'}
    for key in lat_ltrs:
        df['verse'] = df['verse'].str.replace(key, lat_ltrs[key])
    for key in cyr_ltrs:
        df['verse'] = df['verse'].str.replace(key, cyr_ltrs[key])
    # Statistics:
    lat_count = df['verse'].str.count('<').sum()
    cyr_count = df['verse'].str.count('>').sum()
    translated_letters_ratio = cyr_count/lat_count
    print(f'- [{cyr_count}] или [{round(translated_letters_ratio*100, 1)}%] от общо [{lat_count+cyr_count}] букви в kjb-bg/Библия.txt вече са на български.')
    
def estimate_revised_verses_progress(df):
    df = df.copy()
    df['verse'] = df['verse'].str.split(' ', expand=True)[0]
    revised_verses_count = len(df) - df['verse'].str.count(':').sum()
    progr_mes = f'- [{revised_verses_count}] или [{round(revised_verses_count*100/len(df), 2)}%] от общо [{len(df)}] стиха в [Библия.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F.txt) са преведени и компилирани по книги в [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books)\n'
    return progr_mes

def compile_bg_books():
    df = load_translated_Bible()
    df = df.loc[~df['verse'].str.split(' ', expand=True)[0].str.contains(':')]
    if len(df)>0:
        books = list(df['verse'].str.split(' ', expand=True)[0].unique())
        for book in books:
            book_df = df.loc[df['verse'].str.split(' ', expand=True)[0]==book].copy()
            book = book.replace('_', ' ')
            save_file = f'kjb-bg/compiled_text_by_books/{book}.txt'
            print(f'- компилиране на [{book}] във файл [{save_file}]...')
            book_df['verse'] = book_df['verse'].str.split(n=1).str[1].astype(str)
            book_df.to_csv(save_file, index=False, header=False, sep='>')
        print('- готово!')
    else:
        print('- все още няма!')
    return df

def compile_en_books():
    df = load_original_Bible()
    # Get the book:
    df['book'] = df['verse'].str.split(' ', expand=True)[0].str.replace('\d+', '').str.replace(':', '')
    df['book'] = np.where(df['verse'].str[0].isin(['1','2','3']), df['verse'].str[0].astype(str) + ' ' + df['book'].astype(str), df['book'])
    df['book'] = df['book'].map(books_short_to_full_name_dict)
    # Remove the book from the verse:
    #df['verse'] = df['verse'].str.split(n=1).str[1].astype(str)
    df['verse_start'] = df['verse'].str.split(n=1).str[0].str.lower()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        df['verse_start'] = df['verse_start'].str.replace(letter, '')
    df['verse'] = df['verse_start'].astype(str) + ' ' + df['verse'].str.split(n=1).str[1]
    # Save the books:
    books = list(df['book'].unique())
    for book in books:
        save_file = f'kjb-en/compiled_text_by_books/{book}.txt'
        book_df = df.loc[df['book']==book].copy()
        book_df.to_csv(save_file, index=False, header=False, sep='>')
    print('- готово!')

def update_progress_in_the_readme_md(progr_mes):
    fileName = 'README.md'
    readMe = open(fileName, 'r', encoding='utf-8').readlines()
    readMe = readMe[:-3]
    readMe += [f"{mes}\n" for mes in progr_mes.split('\n')[:-1]]
    saveFile = open(fileName, 'w', encoding='utf-8')
    for line in readMe:
        saveFile.write(line)
    saveFile.close()