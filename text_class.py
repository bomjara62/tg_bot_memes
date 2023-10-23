from transformers import pipeline

pipe = pipeline("text-classification", model="MonoHime/rubert-base-cased-sentiment-new")


def text_analyse(text):
    sent_type = pipe([text])
    return sent_type
