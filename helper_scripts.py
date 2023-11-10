import pandas as pd

def find_unique_words_with_a_string():
    print()
    print()
    print('Find all the unique words containing a string')
    print('- please enter the searched string:')
    string = input('>>> ').lower()
    df = pd.read_csv('data/words_df.csv', sep=':')[['word']]
    words = list(df.loc[df['word'].str.contains(string)].sort_values('word')['word'])
    print()
    print(f'- showing the [{len(words)}] words containing [{string}]:')
    for word in words:
        print(word)


def chose_script():
    print()
    print()
    print('Please chose a script you need from the list:')
    print('1: find_unique_words_with_a_string()')
    choice = int(input('>>> '))
    if choice == 1:
        find_unique_words_with_a_string()
    else:
        raise Exception(f'ERROR: Could not find script by input [{choice}]')
        
if __name__=='__main__':
    #chose_script()
    find_unique_words_with_a_string()