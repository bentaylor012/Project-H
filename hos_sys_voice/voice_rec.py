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
    wordlist = []
    for word in tokens:
        if word not in remove:
            wordlist.append(stems.lemmatize(word))
    cleaned_entry=' '.join(wordlist)
    print (cleaned_entry)
    return cleaned_entry

def input_breakdown(cleaned_entry):
    tokens = nltk.word_tokenize(cleaned_entry) #error here (expected string)
    keywords = ['patient', 'diagnosed', 'give']

    split_entry = {
        'patient': None,
        'diagnosed': None,
        'give': None
    }

    last_key = None
    i = 0
    while i < len(tokens):
        print(i)
        if tokens[i] in keywords:
            last_key = tokens[i]
            
        else:
            sentence = []
            sentence.append(tokens[i])
            #j = i
            while i < len(tokens)-1 and tokens[i+1] not in keywords:
                i+=1
                print(i)
                sentence.append(tokens[i])
                print(' '.join(sentence))
            if (last_key == None):
                print("ERROR: Please format correctly")
                return None
           
            
            print(' '.join(sentence))
            split_entry[last_key] = ' '.join(sentence)
        i+=1
    
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
print("entry = "+ str(split_entry))


#Microphone(device_index: Union[int,None] = None, sample_rate: int = 16000,
#chunk_size: int = 1024) -> Microphone
