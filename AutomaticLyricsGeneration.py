import pandas as pd
import numpy  as np

def openandread(lypath):
    tabread = open(lypath, 'r')
    lyfull = tabread.read()
    tabread.close()
    return lyfull;

def readlyrics(lyfile):
    finallist = []
    linesraw = lyfile.split("\n")
    for tline in linesraw:
        words = tline.split(" ")
        finallist.append(words)
    flatlist = [y for x in finallist for y in x]
    return(flatlist)

def markovchain(listin):

    lylenght = len(listin)
    pharselenght = 2
    phrasecount = {}

    for elements in range(0, lylenght):
        token = listin[elements:(pharselenght + elements)]  #index the list to take n, n+order elements and added to dictionary or add another occurence
        tokenst = repr(token)
        tokenstr = tokenst[2:-2]                 #A few adjustment when extractig strings from list. Remove some chars
        tokenstr = tokenstr.replace('\'', "")
        tokenstr = tokenstr.replace('\\', "")
        #tokenstr = tokenstr.replace(',',";")
        tokenstr = tokenstr.replace('"',"")
        tokenstr = tokenstr.replace('\\\'',"")
        tokenstr = tokenstr.replace('\\\\',"")
        if tokenstr not in phrasecount:
            phrasecount[tokenstr] = 1
        else:
            phrasecount[tokenstr] += 1

    # Up to here the dictionary has been built, now let's create dataframes

    dictkeys, valuekeys = [], []
    listtoindex, listtocolumn, listtovalue = [], [], []
    dictkeys = phrasecount.keys()  # get the dictonary keys and values into a list to reindex pandaDF lateron
    valuekeys = phrasecount.values()

    for elem in dictkeys:
        sap = str(elem.split(",",1)[0])
        ss = elem.split(",")
        if len(ss) ==  1:       #last word, no chance to compare it with any other
            sop = " is"
        elif len(ss) == 3:   #if the dictionary pair had a coma like, "Yeah, for", the token comes as "Yeah,, for", need to take the 3rd element, as the second is blank
            if ss[2] == "":   # the comma can be like "yeah,,for" or "yeah, god," so need to check well the splits!
                sop = ss[1]
            if ss[1] == "":   # the comma can be like "yeah,,for" or "yeah, god," so need to check well the splits!
                sop = ss[2]

        else:
            if len(ss) == 4: #Could also be something like "Worlds,, Wordls," this is four elements after split
                sop= ss[2]
            else:
                sop = ss[1]
        listtoindex.append(sap)
        listtocolumn.append(sop)


    for elem in valuekeys:
        sip = elem
        listtovalue.append(sip)
        # Create Data Frame and normalize probabilities for "next note candidate" for each note that is our Origin
    dataf = pd.DataFrame({'Next': listtocolumn, 'Origin': listtoindex,  'values': listtovalue}, index=listtoindex)
    dataf['prob'] = dataf.groupby(level=0)['values'].transform(lambda x: x / x.sum())
    #print(dataf[dataf['Origin'] == 'serious'])  #Want to check probabilities? do it here

    return dataf



def buildlyrics(dataff,lenghtl):
     #dataff input is the dataframe with the markov chain
     #lenghtl input is the lenght of the lyrics desired
     #Lyrics are going to start with "I", we can improve that later.

     songc = []
     flag = 0
     initword = 'I'
     elements = dataff.loc[initword,'Next'].values
     probabilities = dataff.loc[initword, 'prob'].values
     x = np.random.choice(elements, 1, p=probabilities)
     songc.append(str(x)[3:-2])
     lastpos = str(x)[3:-2]

     for notes in range(0, lenghtl):  # let's make a song of 500 notes
    # Here we get the event from a discrete mass probibliy function as per the values in the dataframe for the note.
        bb = dataff.loc[lastpos, 'Next']

        if 'str' in str(type(bb)):

            songc.append(bb)
            lastpos = str(bb)[1:]

        if 'Series' in str(type(bb)):
            elements =  dataff.loc[lastpos, 'Next'].tolist()
            probabilities = dataff.loc[lastpos, 'prob'].values
            x = np.random.choice(elements, 1, p=probabilities)  # the value of the event under the mass prob. function
            while x == "":
                x = np.random.choice(elements, 1, p=probabilities)
            y = str(x)[3:-2]
            songc.append(y)
            lastpos = str(x)[3:-2]

     return songc



def finalsong(songl):

     #Now let's build lines from lyrics, we will have 5 types of lines lenght with an assigned probability
    print("Generated Lyrics")
    print("----------------")
    index = 0
    llen=len(songl)
    line = ""
    while (index+15) < llen:   #this check for last index is not the best, I will improve it later with a If then inside the loop with (index+xx9
        xx = np.random.choice([10,12,15,5,3], 1, p=[0.25,0.30,0.25,0.10,0.10])  #let's choose the lenght of each line, with different weights
        too = index + int(xx)
        for n in range(index,too):
            line=line + songl[n].lower() + " "
        print(line)
        index = index + int(xx)
        line=""


    return




#Main Program

lyr = openandread('C:\\SampleLyrics.txt')
lyrlist = readlyrics(lyr)
lymar = markovchain(lyrlist)
lyrics = buildlyrics(lymar,300)
estructuredlyrics = finalsong(lyrics)



