import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import mysql.connector as sqlcon
from mysql.connector import errorcode


#global variables
mydb = None
r = sr.Recognizer()
mic = sr.Microphone()

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

def getPatient(name):
        try:
            mydb = sqlcon.connect(
                host = 'localhost',
                user = 'root',
                password = 'password',
                database = 'medical'
            )

        except sqlcon.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        print(f"connected to database ({mydb.database})")
        mycursor = mydb.cursor()
        #mycursor.execute("INSERT INTO patients (PName, PAge, PHistory) VALUES ('Ben Taylor', '22', 'Back pain, Fever');")
        mycursor.execute("SELECT {name} FROM patients")
        initres =  mycursor.fetchall()
        return initres
#Button Press logic

def buildInput(elems):
    #get old input
    mycursor = mydb.cursor()
    #mycursor.execute("INSERT INTO patients (PName, PAge, PHistory) VALUES ('Ben Taylor', '22', 'Back pain, Fever');")
    mycursor.execute("SELECT (PMedHist, PHealthHist) FROM patients WHERE 'pName' = {elems.patient}")
    result = mycursor.fetchall()
    
    #update the values health history and then med
    updateHist = result[0]+" " +elems.diagnosis
    updateMed = result[1] + " "+ elems.treatment
    #update the values in the table
    mycursor.execute(f"UPDATE patients SET PHealthHist = {updateHist}, PMedHist = {updateMed}")
    mydb.commit()


#setup of all things backend
def begin():
    try:
        mydb = sqlcon.connect(
            host = 'localhost',
            user = 'root',
            password = 'password',
            database = 'medical'
        )

    except sqlcon.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    print(f"connected to database ({mydb.database})")
    mycursor = mydb.cursor()
    #mycursor.execute("INSERT INTO patients (PName, PAge, PHistory) VALUES ('Ben Taylor', '22', 'Back pain, Fever');")
    mycursor.execute("SELECT * FROM patients")
    initres =  mycursor.fetchall()

    for x in initres:
        print(x)

    mydb.commit()


def speech_option():
    entry = input_speech(r, mic)
    #entryWords = entry.split()
    entry = input_cleaning(entry)
    split_entry = input_breakdown(entry)
    #resultwords  = [word for word in entryWords if word.lower() not in ['the', 'and']]
    #entry.replace("the", "")
    print("entry = "+ str(split_entry))
    
    print (split_entry)
    return split_entry

#finds the patient name in the input and returns it
def get_name(text):
    name = ''
    person = []
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    tree = nltk.ne_chunk(pos,binary=False)

    for subtree in tree.subtrees(filter=lambda t: t.node == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])

        if len(person)>1:
            for part in person:
                name += part + ' '

    return name
    