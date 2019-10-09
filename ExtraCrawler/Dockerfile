FROM python:3

WORKDIR /Crawler

ADD extra.py /Crawler

RUN mkdir ./results

RUN touch ./results/english_words.csv
RUN touch ./results/words.txt

RUN pip install requests

RUN pip install beautifulsoup4

CMD ["python", "extra.py"]