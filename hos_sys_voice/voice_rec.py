import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


#nltk.download('popular')
#print(sr.Microphone.list_microphone_names())

#params: r =  recognizer, mic = microphone
#returns the audio input as a string
def input_speech (r, mic):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('(CLICK ENTER WHEN DONE) speak now...')
        audio=r.listen(source)
        print ('recognizing...')
    try:
        entry = r.recognize_google(audio)
    except sr.RequestError:
        print("API unavailable. Check internet connection and try again")
    except sr.UnknownValueError:
        print("Could understand what you said. Please try again")

    return entry

def input_cleaning(entry):
    #insert cleaning code with nltk
    #store patient name, dr. name, medication/dosage, symptoms, diagnosis
    tokens = nltk.word_tokenize(entry)
    #tagged_tokens = nltk.pos_tag(tokens)

    #remove filler words / stop words
    remove =  set(stopwords.words('english'))
    stems = WordNetLemmatizer()
    cleaned_entry = []
    wordlist = []
    for word in tokens:
        if word not in remove:
            wordlist.append(stems.lemmatize(word))
    cleaned_entry.append(' '.join(wordlist))
    print (cleaned_entry)
    return cleaned_entry

def input_breakdown(cleaned_entry):
    tokens = nltk.word_tokenize(cleaned_entry) #error here (expected string)
    keywords = ['patient', 'diagnose', 'give']

    split_entry = {
        'patient': None,
        'diagnose': None,
        'give': None
    }

    for i in range(len(tokens)):
        if tokens[i] in keywords:
            last_key = tokens[i]
            i+=1
        else:
            sentence = []
            while tokens[i] not in keywords:
                sentence.append(tokens[i])
                i+=1
            split_entry[last_key] = ' '.join(sentence)
    print (split_entry)
    return split_entry


#setup
r = sr.Recognizer()
mic = sr.Microphone()



entry = input_speech(r, mic)
#entryWords = entry.split()
entry = input_cleaning(entry)
split_entry = input_breakdown(entry)
#resultwords  = [word for word in entryWords if word.lower() not in ['the', 'and']]
#entry.replace("the", "")
print("entry = "+entry)


#Microphone(device_index: Union[int,None] = None, sample_rate: int = 16000,
#chunk_size: int = 1024) -> Microphone
