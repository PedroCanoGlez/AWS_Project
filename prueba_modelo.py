import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

model = load_model("language_model.keras")

with open("tokenizer.pkl", 'rb') as tokenizer_file:
    tokenizer = pickle.load(tokenizer_file)

seed_text = "import"

for _ in range(4):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=model.input_shape[1], padding='pre')
    probabilities = model.predict(token_list, verbose=0)[0]
    predicted_index = np.argmax(probabilities)
    predicted_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted_index:
            predicted_word = word
            break
    seed_text += " " + predicted_word

print("Generated Text:", seed_text)