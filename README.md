# AutomaticLyricsGenerationAI

This code will read and learn from lyrics ingested as input in a text file.
It will create a Pandas Dataframe consisting of a Markov Chain containing words and probabilities to go to another word. A first order chain. 
We could build another order chain by adjusting parameter *pharselenght*
The it will create a song based (lenght specififed) on these chains and with some weighted probability of the lenght of each lyrics' line.

It basically defines and uses these functions:

**openandread**
Get the text file with the lyrics. In my example: a text file containing all lyrics from some **Drake Albums + lyrics from Frank Ocean album** . You need to specify the path of the text file when you call the function. See examples below

**readlyrics**
Reads the lyrics from the file and create a Python list of all the words.

**markovchain**
Builds a Pandas Dataframe representing a Markov chain of first order (when phraselenght is equal to 2 - this can be changed).
First it will compute all word to word occurences and build a Python Dict. We will use the Dict to build the DataFrame
It will contain current word and possible next word and the probabilities of that to happen.

**buildlyrics**
Accept as a parameter the lenght of the lyrics you want to create (number of total words)
It will get the DataFrame obtained from previous funciton and then,  will iterate from the starting word "I", to create a list 
with the created lyrics.

**finalsong**
Gets as input the list of lyrics generated from the prevoous function *buildlyrics* and will create the final song.
Will sort the list into lines of variable lenght, based on weighted probability here:
```
        xx = np.random.choice([10,12,15,5,3], 1, p=[0.25,0.30,0.25,0.10,0.10])  #let's choose the lenght of each line, with different weights
```
In futher developments, that weights will be automatically adjusted based on the lenght of the lines of the input file and corresponding 
probability, ex- text file has a 5% probability to have a line of 5 words, etc.. 

#An example of how to use:
```
#Main Program

lyr = openandread('C:\\Users\\dmanerob\\Downloads\\Hiphop.txt')
lyrlist = readlyrics(lyr)
lymar = markovchain(lyrlist)
lyrics = buildlyrics(lymar,300)
estructuredlyrics = finalsong(lyrics)
```

In my example, ingeting the lyrics from a couple of **Drake albums + Frank Ocean album (Channel Orange)**, this is a sample of what it returns:

```

swear feels like im in abandoned  homes youre beautiful, 
motel  girl around
Concrete  loop  you hate it go showtime  go if shes 
sayin but its fireworks taking pictures to let go go 
go i know you not 
in his yellow  goose  yeah its just done nails  done oh you got a house 
what am i just be throwin understand  i make it 
...
``


