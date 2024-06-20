# Български превод на Библията от KJV
Директен превод от King James Version (KJV), запазвайки оригиналната пунктуация, главни/малки букви, словоред и еднакъв превод на словосъчетанията навсякъде в текста, като за момента благозвучието е оставено на втори план.

Използвам python скриптове за автоматизация на първичния превод, поддръжка на логове, контрол на грешките и генериране на готовите стихове по книги в txt и html формат, който хоствам с AWS S3 на [този уебсайт - "BG KJV Книги"](http://site-for-kjv-bg-translation.s3-website-us-east-1.amazonaws.com/)

Не правя превода като академик или критик, а за лично изучаване, като вярващ в Библията. Всичко в репото и в уебсайта е безплатно, без лиценз и може да се цитира, използва и споделя свободно.

## Съдържание

- [Bible.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-en/Bible.txt) - KJV, оригиналният текст, взет от [o-bible.com](https://www.o-bible.com/download/kjv.txt), от който превеждам
- [Библия.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F.txt) - целият текст, частично на български в процес на превод
- [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books) - напълно преведените и готови стихове, компилирани по книги
- [Книги EN](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-en/compiled_text_by_books) - оригиналия KJV текст, компилиран по книги
- [речник](https://github.com/TraxData313/KJV-BG-translation/blob/main/%D1%80%D0%B5%D1%87%D0%BD%D0%B8%D0%BA.txt) - речник с преведените от английски на български думи
- [бележки](https://github.com/TraxData313/KJV-BG-translation/blob/main/translation_decision_notes.txt) - бележки, водени по време на превода
- [progress_translation.py](https://github.com/TraxData313/KJV-BG-translation/blob/main/progress_translation.py) - скрипт, който превежда, използвайки [речника](https://github.com/TraxData313/KJV-BG-translation/blob/main/%D1%80%D0%B5%D1%87%D0%BD%D0%B8%D0%BA.txt), компилира по готовите стихове по [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books), намира грешки и обновява статистиката в секция **Напредък**

## Напредък
- [3804] или [30.72%] от [12384] уникални думи са преведени [ETA 2027-06-20]
- [713922] или [91.29%] от общо [782071] думи са преведени [ETA 2025-07-23]
- [460] или [1.48%] от общо [31102] стиха в [Библия.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F.txt) са преведени и компилирани по книги в [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books) и качени в уебсайта [BG KJV Книги](http://site-for-kjv-bg-translation.s3-website-us-east-1.amazonaws.com/)  [ETA 2076-01-26]
- С текущия темп цялостният груб превод ще завърши около [2035-03-25]
