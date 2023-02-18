#Ghaida Alshiddi
#Assignement 2
#2/18/23
#cs 4395
import sys
import nltk
from nltk.corpus import stopwords
from random import randint
nltk.download("all")
from nltk import word_tokenize, WordNetLemmatizer

def preprocess(text):
    #tokenize the text
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens]
    #reduce tokens
    tokens1 = [i for i in tokens if i.isalpha() and
              i not in stopwords.words('english') and len(i) > 5]
    # get the lemmas from the reduced tokens
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens1]
    # get the unique lemmas and add them to a list
    lemmas_unique = list(set(lemmas))  # ?
    #creating the POS tagging on the unique lemmas and printing the first 20 results
    tags = nltk.pos_tag(lemmas_unique)
    print("first 20 tag pos: ", tags[:20])
    # get the list of nouns
    nouns = [(n,i) for n, i in tags if i.startswith('N')]
    #print the number of nouns and tokens then return the tokens and nouns
    print('numebr of tokens', len(tokens1), '\nnumber of nouns', len(nouns))
    return tokens1, nouns

currlist = []
#helper function for the guessing game function
def comp (ent, l):
    #if no entry, print an empty _
    if ent=='':
        for i in range(len(l)):
            print('_ ', end=' ')
    #if user entred a letter
    else:
        #iterate through the word
        for i in range(len(l)):
            #if letter is in word and not repeated then append to list and
            #print the letter
            if l[i]==ent and ent not in currlist:
                currlist.append(l[i])
                print(l[i], " ", end=' ')
            #to print letters in the list
            elif l[i] in currlist:
                print(l[i], " ", end=' ')
                if l[i]==ent:
                    currlist.append(l[i])
            # print _
            else:
                #currlist.append('_ ')
                print('_ ', end=' ')
#the guessing game
def guess(cwords):
    #player starts with 5 pts
    #initalize the game
    points=5
    entry=''
    word = cwords[randint(0, 49)]
    comp(entry, word)
    #game works if user didnt exit and has points
    while points>0 and entry!= '!':
        entry = input('\nGuess a letter:')
        #print error message
        if len(entry)>1 or len(entry)<1:
            print("Please enter one letter only")
        # increase points and print message and call helper function
        elif entry in word and entry not in currlist:
            comp(entry, word)
            points+=1
            print('\nRight! Score is ', points)
            print(len(word) , len(currlist))
            #when user guesses the word correct, ask for another word
            if len(word) == len(currlist) :
                print('You solved it!')
                print('Guess another word')
                word = cwords[randint(0, 49)]
                currlist.clear()
                comp(entry, word)
        #when user enters the same letters the guessed before
        elif entry in currlist:
            print("Please enter a different letter.")
        #print message when user wants to exit
        elif points<1 and entry== '!':
            print('Thanks for playing!')
        # when user gessues wrong, take out 1 point
        else:
            comp(entry, word)
            points -= 1
            print('\nSorry, guess again. Score is ', points)


# main code
if __name__ == '__main__':
    #checks for args and print error message
    if len(sys.argv)<1:
        print("Please enter a filename as sys arg")
        quit()
    #save filename
    rel_path=sys.argv[1]
    with open(rel_path, 'r') as f:
        text_file = f.read()
    #tokenize the text from file
    tokens = word_tokenize(text_file)
    #get the set of tokens
    setT= set(tokens)
    #calculate the lexical diversity
    lexDiv = len(setT) / len(tokens)
    print(f'Lexical diversity: {lexDiv:.2f}')
    #call preprocessor function and get the tokens and nouns
    t,n = preprocess(text_file)

    noun_dict = {}
    #create a dict of nouns and tokens (and the number of times a noun is mentioned in the tokens (t))
    for c,i in n:
        for d in t:
            if c not in noun_dict and c==d:
                noun_dict[c]=1
            elif c in noun_dict and c==d:
                noun_dict[c] += 1

    #sort the list and get the top 50 common words in game and print them
    sortList = [(j,noun_dict[j]) for j in sorted(noun_dict, key=noun_dict.get, reverse=True)]
    top50 = sortList[:50]
    print('top 50 common words: ', top50)
    #create a list of the top 50 common words without count
    cword = [i for i, j in top50]

    #call guessing game
    guess(cword)



