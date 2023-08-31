import pandas as pd

def load_translated_Bible():
    df = pd.read_csv('kjb-bg/Библия.txt', sep='<', header=None)
    df.columns = ['verse']
    return df

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

print('Прогрес:')
df = load_translated_Bible()
estimate_letter_progress(df)
estimate_revised_verses_progress(df)