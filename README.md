# Български превод на Библията от KJV
**[Уебсайт BG KJV Книги](http://site-for-kjv-bg-translation.s3-website-us-east-1.amazonaws.com/)** - преведените стихове по книги, съпоставени с оригиналната им версия.

Директен превод от [King James Version (KJV) от 1611 г.](https://bg.wikipedia.org/wiki/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F_%D0%BD%D0%B0_%D0%BA%D1%80%D0%B0%D0%BB_%D0%94%D0%B6%D0%B5%D0%B9%D0%BC%D1%81), запазвайки оригиналната пунктуация, главни/малки букви, словоред и в повечето случаи, покоренов мапинг на думите за сметка на благозвучие на текущия български език.

Аз съм християнин и правя превода с вяра в Библията, не като академик или критик, за лично изучаване, използване и споделяне с близки. Всичко е безплатно, без лиценз и може да се цитира, използва и споделя свободно.

Използвам python скриптове за автоматизация на първичния превод, поддръжка на логове, контрол на грешките и генериране на готовите стихове по книги в txt и html формат, който хоствам с AWS S3 на [ТОЗИ ЛИНК](http://site-for-kjv-bg-translation.s3-website-us-east-1.amazonaws.com/)

## Съдържание

- [Bible.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-en/Bible.txt) - KJV, оригиналният текст, взет от [o-bible.com](https://www.o-bible.com/download/kjv.txt), от който превеждам
- [Библия.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F.txt) - целият текст, частично на български в процес на превод
- [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books) - напълно преведените и готови стихове, компилирани по книги
- [Книги EN](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-en/compiled_text_by_books) - оригиналия KJV текст, компилиран по книги
- [речник](https://github.com/TraxData313/KJV-BG-translation/blob/main/%D1%80%D0%B5%D1%87%D0%BD%D0%B8%D0%BA.txt) - речник с преведените от английски на български думи
- [бележки](https://github.com/TraxData313/KJV-BG-translation/blob/main/translation_decision_notes.txt) - бележки, водени по време на превода
- [progress_translation.py](https://github.com/TraxData313/KJV-BG-translation/blob/main/progress_translation.py) - скрипт, който превежда, използвайки [речника](https://github.com/TraxData313/KJV-BG-translation/blob/main/%D1%80%D0%B5%D1%87%D0%BD%D0%B8%D0%BA.txt), компилира по готовите стихове по [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books), намира грешки и обновява статистиката в секция **Напредък**

## Напредък
- [2611] или [21.09%] от [12379] уникални думи са преведени
- [684792] или [87.64%] от общо [781393] думи са преведени
- [193] или [0.62%] от общо [31102] стиха в [Библия.txt](https://github.com/TraxData313/KJV-BG-translation/blob/main/kjb-bg/%D0%91%D0%B8%D0%B1%D0%BB%D0%B8%D1%8F.txt) са преведени и компилирани по книги в [Книги BG](https://github.com/TraxData313/KJV-BG-translation/tree/main/kjb-bg/compiled_text_by_books) и качени в уебсайта [BG KJV Книги](http://site-for-kjv-bg-translation.s3-website-us-east-1.amazonaws.com/)
