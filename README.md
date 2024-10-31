# Български превод на Библията от KJV


## Характеристики
- Всяка дума и словосъчетание превеждам по един и същ уникален начин навсякъде в текста
- Напълно запазвам пунктуацията ,.-;!?:() - до последната йота (<u title="Докато небето и земята не минат, ни една йота или ни една точка не ще по никой начин мине от закона, докато всичко не се изпълни.">Матей 5:18</u>)
- Напълно запазвам ГЛАВНИ/малки букви
- Не добавям или премахвам нищо (коментари, препратки, заглавия, мисли, цели стихове... всичко е както в [KJV Standard](https://www.kingjamesbibleonline.org))
- Използвам автоматични алгоритми за минимизиране на грешките, поддръжка на логове и компилиране на уебсайта [BG KJV Книги](http://site-for-kjv-bg-translation.s3-website-us-east-1.amazonaws.com/), който хоствам с AWS S3
- Не правя превода като академик или критик, а от любов и благодарност към Бог, вярващ в запазеното Му Слово (Псалми 12:6-7, Исая 40:8, Матей 24:35)
- Всичко в репото и в уебсайта е безплатно, без лиценз и може да се цитира, използва и споделя свободно


## Съдържание
- [Bible.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-en/Bible.txt) - KJV, оригиналният текст, взет от [o-bible.com](https://www.o-bible.com/download/kjv.txt), от който превеждам
- [Библия.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F.txt) - целият текст, частично на български в процес на превод
- [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books) - напълно преведените и готови стихове, компилирани по книги
- [Книги EN](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-en/compiled_text_by_books) - оригиналия KJV текст, компилиран по книги
- [речник](https://github.com/TraxData313/KJV-BG-translation/blob/main/%D1%80%D0%B5%D1%87%D0%BD%D0%B8%D0%BA.txt) - речник с преведените от английски на български думи
- [бележки](https://github.com/TraxData313/KJV-BG-translation/blob/main/translation_decision_notes.txt) - бележки, водени по време на превода
- [progress_translation.py](https://github.com/TraxData313/KJV-BG-translation/blob/main/progress_translation.py) - скрипт, който превежда, използвайки [речника](https://github.com/TraxData313/KJV-BG-translation/blob/main/%D1%80%D0%B5%D1%87%D0%BD%D0%B8%D0%BA.txt), компилира по готовите стихове по [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books), намира грешки и обновява статистиката в секция **Напредък на превода**


## Напредък
- Думи в речника: [39.2%] или [4849 от 12384], ETA: [2027-09-11]
- Думи в текста: [93.7%] или [732590 от 781498], ETA: [2028-08-01]
- Стихове: [3.6%] или [1106 от 31102], ETA: [2044-02-19]
- С текущия темп цялостният груб превод ще завърши около [2031-07-30]
