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
        '1 Jn': '62NT 1 John',
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

weight_reduce = 5

def get_eta_date(target_col='уникални_думи_процент', weighted=True):
    # Load the logs:
    df = pd.read_csv('logs/translated_progress.csv')
    df['дата'] = pd.to_datetime(df['дата'])
    first_date = df['дата'].min()
    # Percent change between the dates:
    df['perc_delta'] = df[target_col].diff()
    # Days between the dates:
    df['days_took'] = (df['дата'] - first_date).dt.days
    df['days_delta'] = df['days_took'].diff()
    # Perc/day rate:
    df['transl_rate'] = df['perc_delta']/df['days_delta']
    df = df.loc[df['дата']>'2024-01-01']
    if weighted:
        weights = df['days_delta']*np.linspace(1, len(df)/weight_reduce, len(df))
    else:
        weights = df['days_delta']
    transl_rate = df['transl_rate'].dot(weights) / sum(weights)
    # Calculate the ETA:
    comp_days = 100/transl_rate
    comp_date = str((first_date + pd.Timedelta(days=comp_days)).date())
    return comp_date

def get_the_final_eta_averaged_by_two_ways(weighted=True):
    # Load the logs:
    df = pd.read_csv('logs/translated_progress.csv')
    df['дата'] = pd.to_datetime(df['дата'])
    first_date = df['дата'].min()
    # Days between the dates:
    df['days_took'] = (df['дата'] - first_date).dt.days
    df['days_delta'] = df['days_took'].diff()
    transl_rates = []
    comp_dayss = []
    for target_col in ['уникални_думи_процент', 'общо_думи_процент', 'стихове_процент']:
        # Percent change between the dates:
        df['perc_delta'] = df[target_col].diff()
        # Perc/day rate:
        df['transl_rate'] = df['perc_delta']/df['days_delta']
        if weighted:
            weights = df.loc[df['дата']>'2024-01-01']['days_delta']*np.linspace(1, len(df)/weight_reduce, len(df)-1) # increasing weights giving more weight to the newest entries: 1,2,3,4...
        else:
            weights = df.loc[df['дата']>'2024-01-01']['days_delta'] # standard average, taking into account the lenght of the observation
        transl_rate = df.loc[df['дата']>'2024-01-01']['transl_rate'].dot(weights) / sum(weights)
        transl_rates.append(transl_rate)
        comp_days = 100/np.mean(transl_rate)
        comp_dayss.append(comp_days)
    # ETA by ave days:
    comp_days_by_days_ave = np.mean(comp_dayss)
    comp_date_by_days_ave = str((first_date + pd.Timedelta(days=comp_days_by_days_ave)).date())
    print('-- date from rates:', comp_date_by_days_ave)
    # ETA by rates:
    ave_transl_rate = np.mean(transl_rates)
    comp_days_by_rate = 100/ave_transl_rate
    comp_date_by_rate = str((first_date + pd.Timedelta(days=comp_days_by_rate)).date())
    print('-- date from days:', comp_date_by_rate)
    # Average of the two:
    ave_days = np.mean([comp_days_by_days_ave, comp_days_by_rate])
    comp_date = str((first_date + pd.Timedelta(days=ave_days)).date())
    return comp_date

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
    orig_word = word
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
    # leave comments like [Исая 40:3] with cap letter or if not for this line it would become [исая 40:3]:
    if orig_word.startswith('[') and len(orig_word) > 2 and orig_word[1].isupper():
        word = '[' + word[1].upper() + word[2:]
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
    return changes_df

def get_translated_word_stats():
    df = get_words_df(use_cache=True)
    total_words = df['word_use_count'].sum()
    translated_words = df.loc[df['word_bg'].fillna(0)!=0]['word_use_count'].sum()
    unique_words = len(df)
    unique_translated_words = len(df.loc[df['word_bg'].fillna(0)!=0])
    return unique_translated_words, unique_words, translated_words, total_words

def print_translated_word_stats(weighted=True):
    unique_translated_words, unique_words, translated_words, total_words = get_translated_word_stats()
    unique_words_eta = get_eta_date(target_col='уникални_думи_процент', weighted=weighted)
    total_words_eta = get_eta_date(target_col='общо_думи_процент', weighted=weighted)
    unique_translated_words_perc = round(unique_translated_words*100/unique_words,1)
    translated_words_perc = round(translated_words*100/total_words,1)
    # - 10000 -> 10 000 formatting:
    unique_translated_words = f"{unique_translated_words:,}".replace(",", " ")
    unique_words = f"{unique_words:,}".replace(",", " ")
    translated_words = f"{translated_words:,}".replace(",", " ")
    total_words = f"{total_words:,}".replace(",", " ")
    # - Final message:
    progr_mes = f'- Речник: [{unique_translated_words_perc}%] или [{unique_translated_words} от {unique_words}], ETA: [{unique_words_eta}]\n'
    progr_mes += f'- Думи в текста: [{translated_words_perc}%] или [{translated_words} от {total_words}], ETA: [{total_words_eta}]\n'
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
    
def get_estimate_revised_verses_progress(df=None):
    if df is None: df = load_translated_Bible()
    df = df.copy()
    df['verse'] = df['verse'].str.split(' ', expand=True)[0]
    total_verses_count = len(df)
    revised_verses_count = total_verses_count - df['verse'].str.count(':').sum()
    return revised_verses_count, total_verses_count

def estimate_revised_verses_progress(df=None, weighted=True):
    if df is None: df = load_translated_Bible() #easier to read the expected input and works ok by default
    revised_verses_count, total_verses_count = get_estimate_revised_verses_progress(df)
    eta = get_eta_date(target_col='стихове_процент', weighted=weighted)
    revised_verses_perc = round(revised_verses_count*100/total_verses_count, 1)
    revised_verses_count = f"{revised_verses_count:,}".replace(",", " ")
    total_verses_count = f"{total_verses_count:,}".replace(",", " ")
    progr_mes = f'- Стихове: [{revised_verses_perc}%] или [{revised_verses_count} от {total_verses_count}], ETA: [{eta}]\n'
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
    #df['book'] = df['verse'].str.split(' ', expand=True)[0].str.replace('\d+', '').str.replace(':', '')
    df['book'] = df['verse'].str.split(' ', expand=True)[0]
    chars_to_remove = [' ', ':', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    for char in chars_to_remove:
        df['book'] = df['book'].str.replace(char, '')
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
        book_df = df.loc[df['book']==book]['verse'].copy()
        if book_df.values[0][0:2] in ['11', '21', '31']:
            # this happens for the numbered books (like 1 Peter) - adds 1 to the start (1:12 -> 11:12), so this line fixes this issue:
            book_df = book_df.str[1:]
        book_df.to_csv(save_file, index=False, header=False, sep='>')
    print('- готово!')

def update_progress_in_the_readme_md(progr_mes):
    fileName = 'README.md'
    readMe = open(fileName, 'r', encoding='utf-8').readlines()
    readMe = readMe[:-4]
    readMe += [f"{mes}\n" for mes in progr_mes.split('\n')[:-1]]
    saveFile = open(fileName, 'w', encoding='utf-8')
    for line in readMe:
        saveFile.write(line)
    saveFile.close()

def log_translated_progress(df=None):
    progress_file = 'logs/translated_progress.csv'
    unique_translated_words, unique_words, translated_words, total_words = get_translated_word_stats()
    if df is None: df = load_translated_Bible()
    revised_verses_count, total_verses_count = get_estimate_revised_verses_progress(df)
    # Add the new data:
    new_df = pd.DataFrame({
            'дата': ['2023-09-01', pd.Timestamp.now().date()],
            'уникални_думи_брой': [1, unique_translated_words],
            'уникални_думи_процент': [100/unique_words, unique_translated_words*100/unique_words],
            'общо_думи_брой': [1, translated_words],
            'общо_думи_процент': [100/total_words, translated_words*100/total_words],
            'стихове_брой': [1, revised_verses_count],
            'стихове_процент': [100/total_verses_count, revised_verses_count*100/total_verses_count]
        })
    # Combine and remove the duplicates:
    if os.path.exists(progress_file):
        current_df = pd.read_csv(progress_file)
        df = pd.concat([current_df, new_df])
    else:
        df = new_df
    df['дата'] = pd.to_datetime(df['дата'])
    df = df.sort_values('дата', ascending=True)
    df = df.drop_duplicates('дата', keep='last') #leave the newest entry for that day
    # Write to the file:
    df.to_csv(progress_file, index=False)
    return df


#####################################################
# Generate the complexes
#####################################################
from collections import Counter
from itertools import tee, zip_longest
import time, os

def get_en_book_lines_for_complex_compilation():
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
    texts = []
    dfs = []
    for book in books:
        save_file = f'kjb-en/compiled_text_by_books/{book}.txt'
        book_df = df.loc[df['book']==book]['verse'].copy()
        if book_df.values[0][0:2] in ['11', '21', '31']:
            # this happens for the numbered books (like 1 Peter) - adds 1 to the start (1:12 -> 11:12), so this line fixes this issue:
            book_df = book_df.str[1:]
        book_df = pd.DataFrame({'line': book_df, 'book': book})
        book_df['line'] = book_df['line'].str.split(' ', 1).str[1]
        book_df['line'] = book_df['line'].str.replace("'", '') #make "wife's" -> "wifes"
        book_df['line'] = book_df['line'].str.replace('[^a-zA-Z]', ' ').str.lower() #remove all non letter chars and make lowercase
        book_df['line'] = book_df['line'].str.replace('  ', ' ')
        #text = ' '.join(book_df['line']).replace('  ', ' ')
        #texts.append(text)
        book_df['word_count'] = book_df['line'].str.count(' ') #df['line'].apply(lambda x: len(x.split()))
        dfs.append(book_df)
    #df = pd.DataFrame({'text': texts, 'book': books})
    df = pd.concat(dfs)
    return df

def generate_permutations(text, permutation_size):
    """
from collections import Counter
from itertools import tee, zip_longest

# Example usage:
text = 'in the beginning god created the heaven and the earth and the earth was without form and void'
permutation_size = 19

result_df = generate_permutations(text, permutation_size=3)
result_df
    """
    # Split the text into words
    words = text.split()

    # Generate all word permutations of the specified size
    word_permutations = [' '.join(words[i:i+permutation_size]) for i in range(len(words)-permutation_size+1)]

    # Count the occurrences of each permutation
    permutation_counts = Counter(word_permutations)

    # Create a DataFrame from the counts
    df = pd.DataFrame(list(permutation_counts.items()), columns=['permutation', 'permutation_count'])
    df['permutation_size'] = permutation_size

    # Sort the DataFrame by permutation_count in descending order
    df = df.sort_values(by='permutation_count', ascending=False).reset_index(drop=True)
    return df

# Function to format seconds into HH:MM:SS
def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

def get_the_complexes_df(use_cache=True):
    cache = 'data/complexes_data.csv'
    if use_cache and os.path.exists(cache):
        res = pd.read_csv(cache)
    else:
        print(f'Calculating the complexes and saving the result to [{cache}]...')
        df = get_en_book_lines_for_complex_compilation()
        # Get the start time
        start_time = time.time()
        min_len = df['word_count'].min()
        max_len = df['word_count'].max()
        res = None
        for word_count in range(max_len, min_len-1, -1):
            tdf = df.loc[df['word_count']>=word_count] #take only the lines with enough words
            len_tdf = len(tdf)
            data = []
            for j, line in enumerate(tdf['line']):
                if j%25 == 0:
                    # Calculate elapsed time
                    elapsed_time = time.time() - start_time
                    formatted_elapsed_time = format_time(elapsed_time)
                    print(f'- Elapsed Time: {formatted_elapsed_time}. Doing complex length [{word_count}/{max_len}]. Parsing Bible line [{j}/{len_tdf}]...       ', end='\r', flush=True)
                ttdf = generate_permutations(line, permutation_size=word_count)
                data.append(ttdf)
            tdf = pd.concat(data)
            tdf = tdf.groupby('permutation').agg({'permutation_count': 'sum', 'permutation_size': 'max'})
            tdf = tdf.loc[tdf['permutation_count']>1].reset_index()
            if res is None:
                res = tdf
            else:
                def has_longer_version(current_permutation):
                    other_permutations = res[res['permutation'] != current_permutation]['permutation']
                    return 1 if any(current_permutation in other_permutation for other_permutation in other_permutations) else 0
                tdf = tdf.loc[tdf['permutation'].apply(has_longer_version)==0]
                res = pd.concat([res, tdf])
        res = res.sort_values(['permutation_size', 'permutation_count'], ascending=False).reset_index(drop=True)
        res.to_csv(cache, index=False)
    return res
#####################################################
# END Generate the complexes
#####################################################




#####################################################
# Compile the HTML side-by-sides
#####################################################


page_title = 'Библия KJV'
description = ""
quote_of_the_day = 'Бог не е Богът на мъртвите, но на живеещите. [Матей 22:32]'
footer = f"""<b style="color: #73AD21"><i>{quote_of_the_day}</i></b><br>
<br>
Всичко в репото и в уебсайта е безплатно, без лиценз и може да се цитира, използва и споделя свободно.
<ul>
    <li><b>Email</b>: <a href='mailto:antongeorgiev313@gmail.com'>antongeorgiev313@gmail.com</a></li> 
    <li><b>Repository</b>: <a href='https://github.com/TraxData313/KJV-BG-translation'>https://github.com/TraxData313/KJV-BG-translation</a></li> 
</ul>
"""
html_style = """
<style>
    table {
        border-collapse: collapse;
        width: 100%;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 10px;
        text-align: left;
    }
    .container {
        overflow-x: auto;
    }
    .center {
        margin: auto;
        width: 90%;
        min-height: 95vh;
        border: 3px solid #73AD21;
        padding: 10px;
        background-color: #f0f0f0; /* background color for the center (gray) */
    }
</style>
"""

chapter_names_dict = {
    '01OT Битие': {
        1: 'Сътворението на света',
        2: 'Сътворението на човека и градината на Едем',
        3: 'Грехопадението',
        4: 'Каин и Авел',
        5: 'Родовата линия от Адам до Ной',
        6: 'Покварата на човечеството и началото на потопа',
        7: 'Потопът и спасението на Ной',
        8: 'Краят на потопа и Божият завет с Ной',
        9: 'Заветът с Ной и проклятието на Хам',
        10: 'Народите, произлезли от Ной',
        11: 'Кулата във Вавилон и родословието на Авраам',
        12: 'Призивът на Авраам и пътуването му в Египет',
        13: 'Авраам и Лот се разделят',
        14: 'Авраам спасява Лот и срещата с Мелхиседек',
        15: 'Божият завет с Авраам',
        16: 'Агар и Исмаил',
        17: 'Заветът за обрязването',
        18: 'Посещението на тримата мъже и застъпничеството за Содом',
        19: 'Унищожаването на Содом и Гомор',
        20: 'Авраам и Авимелех',
        21: 'Раждането на Исак и прогонването на Агар и Исмаил',
        22: 'Изпитанието на Авраам и жертвоприношението на Исак',
        23: 'Смъртта и погребението на Сара',
        24: 'Изпращането на слугата за съпруга на Исак',
        25: 'Смъртта на Авраам и раждането на Исав и Яков',
        26: 'Исак и Авимелех',
        27: 'Яков отнема благословията на Исав',
        28: 'Сънят на Яков за стълбата към небето',
        29: 'Яков и Лия, Яков и Рахил',
        30: 'Децата на Яков и неговото богатство',
        31: 'Бягството на Яков от Лаван',
        32: 'Яков се готви да срещне Исав',
        33: 'Яков и Исав се срещат и се помиряват',
        34: 'Оскверняването на Дина и отмъщението на братята й',
        35: 'Божието потвърждение на завета с Яков',
        36: 'Потомците на Исав',
        37: 'Йосиф и сънищата му',
        38: 'Юда и Тамар',
        39: 'Йосиф в дома на Потифар',
        40: 'Сънищата на виночерпеца и хлебаря в затвора',
        41: 'Йосиф тълкува сънищата на фараона',
        42: 'Братята на Йосиф идват в Египет',
        43: 'Второто посещение на братята на Йосиф',
        44: 'Изпитанието на братята чрез сребърната чаша',
        45: 'Йосиф разкрива самоличността си',
        46: 'Яков и семейството му слизат в Египет',
        47: 'Яков и семейството му се заселват в Египет',
        48: 'Яков благославя синовете на Йосиф',
        49: 'Яков благославя своите синове',
        50: 'Смъртта на Яков и смъртта на Йосиф'
    },
    '40NT Матей': {
        1: 'Родовата линия на Исус и Неговото раждане',
        2: 'Посещението на мъдреците и бягството в Египет',
        3: 'Кръщението на Исус',
        4: 'Изкушението на Исус и началото на Неговото служение',
        5: 'Проповедта на планината: Кои са благословенни, светила и сол, заповедите',
        6: 'Проповедта на планината: Молитвата, небесните съкровища в тайно, търсете Царството, другото ще ви се добави',
        7: 'Проповедта на планината: Съдене на другите и Здравата Основа',
        8: 'Чудеса на изцеление, командване на ветровете и морето и изгонване на дяволите в свинете',
        9: 'Чудесата през очите на Фарисеите и постановедите и истинската Жетва',
        10: 'Изпращане на дванадесетте апостоли',
        11: 'Йоан Кръстител и неверието на народа',
        12: 'Господарят на съботата и знакът на пророкът Иона',
        13: 'Притчите за Царството небесно',
        14: 'Смъртта на Йоан Кръстител и нахранването на петте хиляди',
        15: 'Обичаите заместиха Заповедите, нещата които изхождат от сърцето и вярата на ханаанската жена',
        16: 'Отца разбулва на Петър кой е Исус и предсказването на Неговата смърт',
        17: 'Преображението и дяволът, който учениците не успяха да изгонят',
        18: 'Кой е най-великият в небесното царство и Прошката',
        19: 'Учение за развода и богатия младеж',
        20: 'Притчата за работниците в лозето, Началника да бъде служител и Двамата слепци, не спряха да викат',
        21: 'Тържественият вход в Йерусалим и състоянието на храма',
        22: 'Притчата за сватбената трапеза',
        23: 'Горко на книжниците и фарисеите',
        24: 'Знаците за края на времето',
        25: 'Притчата за десетте девици и последният съд',
        26: 'Заговорът за убийството на Исус и Тайната вечеря',
        27: 'Разпятието на Исус',
        28: 'Възкресението на Исус и Великото поръчение'
    },
    '66NT Откровение': {
        1: 'Видението на Йоан за Христос',
        2: 'Посланията до църквите в Ефес, Смирна, Пергам и Тиатир',
        3: 'Посланията до църквите в Сардис, Филаделфия и Лаодикия',
        4: 'Видението на небесния престол',
        5: 'Книгата със седемте печата',
        6: 'Отварянето на шестте печата',
        7: '144,000 запечатани и великото множество',
        8: 'Седмият печат и седемте тръби',
        9: 'Петата и шестата тръба',
        10: 'Ангелът с малката книга',
        11: 'Двамата свидетели и седмата тръба',
        12: 'Жената, Драконът и Детето',
        13: 'Звярът от морето и звярът от земята',
        14: 'Агнето и събраните на Сион',
        15: 'Песента на победителите и седемте чаши',
        16: 'Изливането на седемте чаши на гнева',
        17: 'Голямата блудница и звярът',
        18: 'Падението на Вавилон',
        19: 'Победата на Христос и бракът на Агнето',
        20: 'Хилядогодишното царство и последният съд',
        21: 'Новото небе и новата земя',
        22: 'Реката на живота и обещанията на Христос'
    }
}

def generate_html_file(english_file_path="kjb-en/compiled_text_by_books/01OT Genesis.txt", bulgarian_file_path="kjb-bg/compiled_text_by_books/01OT Битие.txt"):
    # Extract file names without extensions
    english_file_name = os.path.splitext(os.path.basename(english_file_path))[0]
    bulgarian_file_name = os.path.splitext(os.path.basename(bulgarian_file_path))[0]
    bg_github_txt_link = f"https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/compiled_text_by_books/{bulgarian_file_name.replace(' ', '%20')}.txt"
    en_github_txt_link = f"https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-en/compiled_text_by_books/{english_file_name.replace(' ', '%20')}.txt"
    
    # Read content from files
    with open(english_file_path, 'r', encoding='utf-8') as english_file:
        english_lines = [line.strip() for line in english_file]
    with open(bulgarian_file_path, 'r', encoding='utf-8') as bulgarian_file:
        bulgarian_lines = [line.strip() for line in bulgarian_file]

    # Generate chapter links and content with chapter markers
    chapter_links = []
    chaptered_lines = []
    current_chapter = None

    for line_bulgarian, line_english in zip(bulgarian_lines, english_lines):
        # Extract chapter number from the verse (assuming the format "Chapter:Verse")
        bulgarian_chapter, _ = line_bulgarian.split(":", 1)
        english_chapter, _ = line_english.split(":", 1)
        
        if bulgarian_chapter != current_chapter:
            current_chapter = bulgarian_chapter
            # Add chapter link to the TOC
            chapter_links.append(f"<a href='#{current_chapter}'>{current_chapter}</a>")
            # Add chapter marker in the text
            chaptered_lines.append(f"<tr id='{current_chapter}'><td colspan='2' style='text-align: center;'><a href='#top'><strong>Глава {current_chapter}</strong></a></td></tr>")
        
        # Add verse line to the table
        chaptered_lines.append(f"<tr><td>{line_bulgarian}</td><td>{line_english}</td></tr>")
    
    # Generate HTML content
    toc = "<strong>Глави:</strong> " + ", ".join(chapter_links)
    lines = "\n".join(chaptered_lines)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=0.8">
        {html_style}
        <title>{bulgarian_file_name} KJV</title>
    </head>
    <div class="center">
    <body style="background-color: black;" id="top">
        <div>
            <h1 style="text-align: center; color: blue"><a href='index.html'>{page_title}</a></h1>
            <div style="text-align: center;">{toc}</div>
            <br><br><br>
            <div class="container">
                <table>
                    <thead>
                        <tr>
                            <th>{bulgarian_file_name}</th>
                            <th>{english_file_name}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lines}
                    </tbody>
                </table>
            </div>
        </div>
    <footer>
        <p>{footer}</p>
        Текст в обикновен txt формат: <a href='{bg_github_txt_link}'>БГ</a> | <a href='{en_github_txt_link}'>EN</a>
        <br><a href='index.html'>Обратно към всички книги</a>
    </footer>  
    </body>
    </div>
    </html>
    """
    
    # Write HTML content to a new file
    output_folder = 'kjv-side-by-side'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path = f"{output_folder}/{bulgarian_file_name}.html"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)
    print(f"- HTML file '{output_file_path}' generated successfully.")


def generate_dict_page():
    df = get_word_dict()
    df = df.sort_values('word').reset_index(drop=True)
    dict_filename = '00EN-BG dictionary'

    # Generate alphabet navigation
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alphabet_links = " | ".join(f"<a href='#{letter}'>{letter}</a>" for letter in alphabet)

    # Generate dictionary rows with anchor points for each letter
    lines = []
    current_letter = ""
    for numb, word_en, word_bg in zip(df.index, df['word'], df['word_bg']):
        first_letter = word_en[0].upper()
        if first_letter != current_letter:
            lines.append(f"<tr><td colspan='2' style='text-align: center;'><a href='#top'><strong id='{first_letter}' style='color: blue;'>{first_letter}</strong></a></td></tr>")
            current_letter = first_letter
        lines.append(f"<tr><td>{numb+1}</td><td>{word_en}</td><td>{word_bg}</td></tr>")
    lines = "\n".join(lines)

    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=0.8">
        {html_style}
        <title>Речник KJV</title>
    </head>

    <div class="center">
    <body style="background-color: black;">
        <div>
            <h1 style="text-align: center; color: blue"><a href='index.html' style='color: blue;'>{page_title}</a></h1>
            {description}<br><br><br>
            
            <!-- Alphabet Navigation Links -->
            <div class="alphabet-nav" style="text-align: center;">
                {alphabet_links}
            </div>
            <br><br><br>

            <div class="container">
                <table>
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>Английска Дума</th>
                            <th>Българска Дума</th>
                        </tr>
                    </thead>
                    <tbody>
                        {lines}
                    </tbody>
                </table>
            </div>
        </div>
    <footer>
        <p>{footer}</p>
        Речник в обикновен txt формат: <a href='https://github.com/TraxData313/KJV-BG-translation/blob/main/%D1%80%D0%B5%D1%87%D0%BD%D0%B8%D0%BA.txt'>ТУК</a>
        <br><a href='index.html'>Обратно към всички книги</a>
    </footer>  
    </body>
    </div>
    </html>
    """
    # Write HTML content to a new file
    output_folder = 'kjv-side-by-side'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    output_file_path = f"{output_folder}/{dict_filename}.html"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)
    print(f"- HTML file '{output_file_path}' generated successfully.")

def count_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        line_count = 0
        for line in file:
            line_count += 1
    return line_count

def get_translated_progress_by_book(bulgarian_file_path = "kjb-bg/compiled_text_by_books/01OT Битие.txt", english_file_path = "kjb-en/compiled_text_by_books/01OT Genesis.txt"):
    total_lines = count_lines(english_file_path)
    translated_lines = count_lines(bulgarian_file_path)
    translated_perc = int(round(translated_lines*100/total_lines,0))
    translated_lines = f"{translated_lines:,}".replace(",", " ")
    total_lines = f"{total_lines:,}".replace(",", " ")
    if translated_lines == total_lines:
        transl_str = f'<tag style="color:lightblue">завършен на <b>{translated_perc}%</b> ({total_lines} стиха)<tag>'
    else:
        transl_str = f'<tag style="color:lightblue">завършен на <b>{translated_perc}%</b> ({translated_lines} от {total_lines} стиха)<tag>'
    return transl_str

def generate_html_side_by_side_translations():
    bg_folder = "kjb-bg/compiled_text_by_books"
    en_folder = "kjb-en/compiled_text_by_books"
    bg_files = list(np.sort(os.listdir(bg_folder)))
    en_files = os.listdir(en_folder)
    unique_translated_words, unique_words, translated_words, total_words = get_translated_word_stats()
    unique_translated_words_perc = int(round(unique_translated_words*100/unique_words,0))
    unique_translated_words = f"{unique_translated_words:,}".replace(',', ' ')
    unique_words = f"{unique_words:,}".replace(',', ' ')
    word_dict_progr_str = f'<tag style="color:lightblue">завършен на <b>{unique_translated_words_perc}%</b> ({unique_translated_words} от {unique_words} думи)<tag>'
    generate_dict_page()
    book_tuples = []
    for bg_file in bg_files:
        # Extracting the common prefix (e.g., 01OT) from BG file
        common_prefix = bg_file.split(' ', 1)[0]
        # Finding corresponding EN file with the same prefix
        en_file = next((en for en in en_files if common_prefix in en), None)
        # If corresponding EN file is found, create a tuple and add it to the list
        if en_file:
            english_file_path = f"kjb-en/compiled_text_by_books/{en_file}"
            bulgarian_file_path = f"kjb-bg/compiled_text_by_books/{bg_file}"
            book_transl_progress_str = get_translated_progress_by_book(bulgarian_file_path, english_file_path)
            book_tuples.append((bg_file, en_file, book_transl_progress_str))
            generate_html_file(english_file_path, bulgarian_file_path)
    # Generate links to the pages in a separate index.html file
    index_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
        {html_style}
        <title>Библия KJV</title>
    </head>

    <div class="center">
    <body style="background-color: black;">
        <h1 style="text-align: center; color: blue"><a href='index.html'>{page_title}</a></h1>
        {description}
        <br><br><hr>
        <h3>Съдържание:</h3>
        <ul>
            {"".join(f"<li><a href='{book_info[0].split('.')[0]}.html'>{book_info[0].split('.')[0]}</a> <i>{book_info[2]}</i></li>" for book_info in book_tuples)}
            <li><a href='00EN-BG dictionary.html'>EN:BG Речник</a> <i>{word_dict_progr_str}</i></li>
        </ul>
        <i>OT/NT: Стар/Нов Завет</i>
    <br><br><hr>
    <footer>
        <p>{footer}</p>
    </footer>  
    </body>
    </div>
    </html>
    """
    # Write index HTML content to a file
    output_folder = 'kjv-side-by-side'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    index_file_path = f"{output_folder}/index.html"
    with open(index_file_path, 'w', encoding='utf-8') as index_file:
        index_file.write(index_content)
    print(f"- Index file '{index_file_path}' generated successfully.")

#####################################################
# END Compile the HTML side-by-sides
#####################################################