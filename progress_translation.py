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
    f.log_translated_progress(df)
    #estimate_letter_progress(df)
    weighted_eta_est = True
    progr_mes = f.print_translated_word_stats(weighted=weighted_eta_est)
    progr_mes += f.estimate_revised_verses_progress(df, weighted=weighted_eta_est)
    progr_mes += f"- С текущия темп преводът ще завърши около [{f.get_the_final_eta_averaged_by_two_ways(weighted=weighted_eta_est)}]\n"
    print(progr_mes)
    f.update_progress_in_the_readme_md(progr_mes)

    # Compile the books:
    print()
    print()
    print('(Пре)Компилиранe на английските текстове в книги от [kjb-en/Bible.txt] в [kjb-en/compiled_text_by_books]...')
    f.compile_en_books()
    print('Компилирани на книги с преведен поне един стих:')
    f.compile_bg_books()
    print('Компилирани на книги в HTML side-by-side формат:')
    f.generate_html_side_by_side_translations()