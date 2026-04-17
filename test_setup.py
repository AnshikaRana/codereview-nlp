# test_setup.py
from transformers import pipeline

pipe = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
result = pipe("this code is great")[0]
print(result)
# Should print: {'label': 'LABEL_2', 'score': ...}