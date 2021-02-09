import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def get_name(text):
    name = ''
    person = []
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    tree = nltk.ne_chunk(tags,binary=False)

    for subtree in tree.subtrees(filter=lambda t: t.node == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])

        if len(person)>1:
            for part in person:
                name += part + ' '

    return name

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


    """ idea for finding treatment options: look for a verb the following may have the 
        treatment needed. Typically would go at the end. Issues tend to appear first."""

    def get_symptoms(text):
        None
    