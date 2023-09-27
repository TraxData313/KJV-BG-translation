import functions as f

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
    f.estimate_revised_verses_progress(df)

    # Compile the books:
    print()
    print()
    print('(Пре)Компилиранe на английските текстове в книги от [kjb-en/Bible.txt] в [kjb-en/compiled_text_by_books]...')
    f.compile_en_books()
    print('Компилирани на книги с преведен поне един стих:')
    f.compile_bg_books(df)