import speech_recognition as sr
import nltk 
nltk.download('popular')
#print(sr.Microphone.list_microphone_names())

#params: r =  recognizer, mic = microphone
#returns the audio input as a string
def input_speech (r, mic):
    with mic as source:
        r.adjust_for_ambient_noise(source)
        print('(CLICK ENTER WHEN DONE) speak now...')
        audio=r.listen(source)
        print ('recognizing...')
    return r.recognize_google(audio)

#setup
r = sr.Recognizer()
mic = sr.Microphone()



entry = input_speech(r, mic)
entryWords = entry.split()
resultwords  = [word for word in entryWords if word.lower() not in ['the', 'and']]
#resultwords  = ["what the hell is even that" for word in entryWords if word.lower() == 'daddy' and entryWords[-1] == 'chill']
#entry.replace("the", "")
entry = ' '.join(resultwords)
print("entry = "+entry)


#Microphone(device_index: Union[int,None] = None, sample_rate: int = 16000,
#chunk_size: int = 1024) -> Microphone
