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
    progr_mes = f'- [{revised_verses_count}] или [{round(revised_verses_count*100/len(df), 2)}%] от общо [{len(df)}] стиха в [Библия.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F.txt) са преведени и компилирани по книги в [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books) и качени в уебсайта [BG KJV Книги](http://site-for-kjv-bg-translation.s3-website-us-east-1.amazonaws.com/)\n'
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
        book_df = df.loc[df['book']==book]['verse'].copy()
        if book_df.values[0][0:2] in ['11', '21', '31']:
            # this happens for the numbered books (like 1 Peter) - adds 1 to the start (1:12 -> 11:12), so this line fixes this issue:
            book_df = book_df.str[1:]
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


page_title = 'Български превод на Библията от KJV'
description = "Директен превод от <a href='https://bg.wikipedia.org/wiki/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F_%D0%BD%D0%B0_%D0%BA%D1%80%D0%B0%D0%BB_%D0%94%D0%B6%D0%B5%D0%B9%D0%BC%D1%81'>King James Version (KJV) от 1611 г.</a>, запазвайки оригиналната пунктуация, главни/малки букви, словоред и в повечето случаи, покоренов мапинг на думите за сметка на благозвучие на текущия български език."
footer = """Всичко в сайта е без лиценз и може да се цитира, използва и споделя свободно.
<ul>
    <li><b>Email</b>: <a href='mailto:antongeorgiev313@gmail.com'>antongeorgiev313@gmail.com</a></li> 
    <li><b>Repository</b>: <a href='https://github.com/TraxData313/KJV-BG-translation'>https://github.com/TraxData313/KJV-BG-translation</a></li> 
</ul>
"""


def generate_html_file(english_file_path, bulgarian_file_path):
    # Extract file names without extensions
    english_file_name = os.path.splitext(os.path.basename(english_file_path))[0]
    bulgarian_file_name = os.path.splitext(os.path.basename(bulgarian_file_path))[0]
    # Read content from files
    with open(english_file_path, 'r', encoding='utf-8') as english_file:
        english_lines = [line.strip() for line in english_file]
    with open(bulgarian_file_path, 'r', encoding='utf-8') as bulgarian_file:
        bulgarian_lines = [line.strip() for line in bulgarian_file]
    # Generate HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=0.8">
        <style>
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 10px;
                text-align: left;
            }}
            .container {{
                overflow-x: auto;
            }}
        .center {{
        margin: auto;
        width: 90%;
        border: 3px solid #73AD21;
        padding: 10px;
        }}
        </style>
        <title>{bulgarian_file_name}</title>
    </head>

    <div class="center">
    <body>
        <div>
            <h1>{page_title}</h1>
            <a href='index.html'>ВСИЧКИ КНИГИ</a><br><br>
            <div class="container">
                <table>
                    <thead>
                        <tr>
                            <th>{bulgarian_file_name}</th>
                            <th>{english_file_name}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(f"<tr><td>{line_bulgarian}</td><td>{line_english}</td></tr>" 
                                for line_bulgarian, line_english in zip(bulgarian_lines, english_lines))}
                    </tbody>
                </table>
            </div>
        </div>
    <footer>
        <p>{footer}</p>
    </footer>  
    </body>
    </div>
    </html>
    """
    # Write HTML content to a new file
    output_folder = 'kjv-side-by-side'
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    output_file_path = f"{output_folder}/{bulgarian_file_name}.html"
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)
    print(f"- HTML file '{output_file_path}' generated successfully.")

def generate_html_side_by_side_translations():
    bg_folder = "kjb-bg\compiled_text_by_books"
    en_folder = "kjb-en\compiled_text_by_books"
    bg_files = os.listdir(bg_folder)
    en_files = os.listdir(en_folder)
    file_tuples = []
    for bg_file in bg_files:
        # Extracting the common prefix (e.g., 01OT) from BG file
        common_prefix = bg_file.split(' ', 1)[0]
        # Finding corresponding EN file with the same prefix
        en_file = next((en for en in en_files if common_prefix in en), None)
        # If corresponding EN file is found, create a tuple and add it to the list
        if en_file:
            file_tuples.append((bg_file, en_file))
            english_file_path = f"kjb-en/compiled_text_by_books/{en_file}"
            bulgarian_file_path = f"kjb-bg/compiled_text_by_books/{bg_file}"
            generate_html_file(english_file_path, bulgarian_file_path)
            
    # Generate links to the pages in a separate index.html file
    index_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style type="text/css">
        label {{
            color: black;
            font-weight: bold;
            text-size: 1em;
        }}
        descr {{
            color: green;
            font-style: italic;
        }}
        tech {{
            color: blue;
        }}
        .center {{
        margin: auto;
        width: 90%;
        border: 3px solid #73AD21;
        padding: 10px;
        }}
        </style>
        <title>BG KJV Книги</title>
    </head>

    <div class="center">
    <body>
        <h1>{page_title}</h1>
        {description}
        <br><br><hr><br><br>
        <h3>Книги:</h3>
        <ul>
            {"".join(f"<li><a href='{file[0].split('.')[0]}.html'>{file[0].split('.')[0]}</a></li>" for file in file_tuples)}
        </ul>
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