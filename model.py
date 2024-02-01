import os
import glob
import pickle
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

def read_text_files(directory, extensions, num_files=35):
    text_data = []
    for ext in extensions:
        files = glob.glob(os.path.join(directory, f'*.{ext}'))
        selected_files = random.sample(files, min(num_files, len(files)))
        for file_path in selected_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_data.append(file.read())
    return text_data

python_directory = 'C:/Users/pedro/Documents/Clases/4º/TSCD/CodigoEntreno/Python'
python_extensions = ['py']

c_directory = 'C:/Users/pedro/Documents/Clases/4º/TSCD/CodigoEntreno/C'
c_extensions = ['c']

java_directory = 'C:/Users/pedro/Documents/Clases/4º/TSCD/CodigoEntreno/Java'
java_extensions = ['java']

javascript_directory = 'C:/Users/pedro/Documents/Clases/4º/TSCD/CodigoEntreno/JavaScript'
javascript_extensions = ['js']

python_text = read_text_files(python_directory, python_extensions)
c_text = read_text_files(c_directory, c_extensions)
java_text = read_text_files(java_directory, java_extensions)
javascript_text = read_text_files(javascript_directory, javascript_extensions)

all_text = python_text + c_text + java_text + javascript_text

tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_text)
total_words = len(tokenizer.word_index) + 1

print(f"Vocabulary Size: {total_words}")

input_sequences = []
for text in all_text:
    token_list = tokenizer.texts_to_sequences([text])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

print("First few input sequences:")
for seq in input_sequences[:5]:
    print(seq)

max_sequence_length = max(len(seq) for seq in input_sequences)
input_sequences = pad_sequences(input_sequences, maxlen=max_sequence_length, padding='pre')

print("Padded sequences:")
print(input_sequences)

X, y = input_sequences[:, :-1], input_sequences[:, -1]
y = tf.keras.utils.to_categorical(y, num_classes=total_words)

print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")

model = Sequential()
model.add(Embedding(total_words, 100, input_length=max_sequence_length-1))
model.add(LSTM(100))
model.add(Dense(total_words, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print("Model Summary:")
model.summary()

model.fit(X, y, epochs=30, verbose=1)

model.save("language_model.keras")

tokenizer_path = "C:/Users/pedro/Documents/Clases/4º/TSCD/tokenizer.pkl"
with open(tokenizer_path, 'wb') as tokenizer_file:
    pickle.dump(tokenizer, tokenizer_file)