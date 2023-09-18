import pandas as pd
import functions as f


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
    print(f'- [{revised_verses_count}] или [{round(revised_verses_count*100/len(df), 2)}%] от [{len(df)}] стиха в kjb-bg/Библия.txt вече са напълно ревизирани.')

def compile_bg_books(df):
    df = df.loc[~df['verse'].str.split(' ', expand=True)[0].str.contains(':')]
    if len(df)>0:
        books = list(df['verse'].str.split(' ', expand=True)[0].unique())
        for book in books:
            save_file = f'kjb-bg/compiled_text_by_books/{book}.txt'
            print(f'- компилиране на [{book}] във файл [{save_file}]...')
            book_df = df.loc[df['verse'].str.split(' ', expand=True)[0]==book].copy()
            book_df['verse'] = book_df['verse'].str.split(n=1).str[1].astype(str)
            book_df.to_csv(save_file, index=False, header=False, sep='>')
        print('- готово!')
    else:
        print('- все още няма!')




if __name__=='__main__':
    # Translate the words:
    print()
    print()
    print('Преведени думи:')
    changes_df = f.translate_df(save=True)
    print(changes_df)

    # Print the progress:.
    print()
    print()
    print('Прогрес:')
    df = f.load_translated_Bible()
    #estimate_letter_progress(df)
    f.print_translated_word_stats()
    estimate_revised_verses_progress(df)

    # Compile the books:
    print()
    print()
    print('Компилирани на книги с преведен поне един стих:')
    compile_bg_books(df)