#!/usr/bin/env python3

import speech_recognition as sr
#import time
import os
import markovify
import re
import numpy as np

def generate_sentence(text, n, nchar):
    with open(text) as f:
        data = f.read()

    result = []
    data_model = markovify.NewlineText(data)
    #model_json = data_model.to_json()
    # Here you choose how many sentences do you want to generate
    for i in range(n):
        #print(data_model.make_short_sentence(100,tries=100)) # you can also choose max characters
        temp = data_model.make_short_sentence(nchar, tries=100, max_overlap_ratio = 80, state_size = 3)
        if(temp is not None):
            result.append(temp)
            return(temp)
        else:
            return("I have nothing to say")

    #with open("test.txt", 'a+') as file:
    #    for line in result:
    #        print(line)
    #        file.write(line)
    #        file.write('\n')


#utility function for text cleaning
def text_cleaner(text):
  text = re.sub(r'--', ' ', text)
  text = re.sub('[\[].*?[\]]', '', text)
  text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', text)
  text = ' '.join(text.split())
  return text

# Write text to file
def write_to_file(text):
    with open('/home/pi/Documents/ECO/output.txt', 'a') as f:
        f.write(text + "\n")
        f.close()


# Initialize the recognizer
r = sr.Recognizer()


# Loop for listening and speaking

while(True):
    try:
        # use the microphone as source for input.
        with sr.Microphone() as source2:
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            #listens for the user's input
            audio2 = r.listen(source2)

            # Using ggogle to recognize audio
            MyText = r.recognize_google(audio2)
            #MyText = MyText.lower()
            #MyText = text_cleaner(MyText)
            print("You said:  "+MyText)
            #time.sleep(0.5)
            MyText = MyText.replace("'", "")
            write_to_file(MyText)

            #with open("/home/ju/Documents/TextMarkov/output.txt") as f:
            #    output = f.read()

            #print(MyText_doc.sents)
            os.system("echo "+MyText+" | festival --tts")

            # Markov Model
            new_sentence = generate_sentence("/home/pi/Documents/ECO/output.txt", 1, 50)
            new_sentence = new_sentence.lower()
            print("I say:  "+new_sentence)
            write_to_file(new_sentence)
            new_sentence = new_sentence.replace("'", "")
            os.system("echo "+new_sentence+" | festival --tts")


    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occured")
