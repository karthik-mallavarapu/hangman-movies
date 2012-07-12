#!/usr/bin/python 

""" 
Hangman server
Author: Karthik 
""" 

import socket 
import sys
import random

class HangmanServer:
    host = 'localhost'
    port = 50000
    backlog = 5
    size = 1024
    filename = "movies.txt"
    movie_counter = 0
    movie_list = []
    def __init__(self):
        self.movie_counter = 0
        f = open(self.filename,'rU')
        for line in f:
            line.rstrip()
            self.movie_list.append(line.lower())
#Fetch a movie name randomly from the list of movies in the file movies.txt
    def GetMovieName(self):
        self.movie_counter += 1
        movie_random_index = random.randint(0,len(self.movie_list) - 1)
        moviename = self.movie_list[movie_random_index].rstrip()
        return moviename.split(' ')
#Connect function does all the important work beginning with picking out a random movie name 
#with the help of function GetMovieName and listens for incoming connections.
#Server hides all the letters in the movie name, except for the first letter and sends it to 
#the client. Movie names can also have multiple words and so spaces are to be treated seperately. 
#Once a movie name is correctly guessed, servers picks out a new movie name and the game continues.
    def Connect(self):
        print "Welcome to movie hangman!\nGuess the name of the hollywood movie\n" 
        host = ''
        port = 50000
        backlog = 5
        size = 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind((host,port)) 
        s.listen(backlog)
        while len(self.movie_list) != self.movie_counter:
            cleartext = [] 
            cleartext = self.GetMovieName()
            print cleartext
            counter1 = 0
            hiddentext = []
            for word in cleartext:
                text = ""
                for c in word:
                    if counter1 == 0:
                        text += c
                    else:
                        text += "*"
                    counter1 += 1
                hiddentext.append(text)
            client, address = s.accept()
            joinedtext = ""
            for text in hiddentext:
                joinedtext = joinedtext + text.rstrip() + " "
            client.send(joinedtext.rstrip())
            print hiddentext 
            data = client.recv(size)
            client.close()
            newinput = ""
            while hiddentext != cleartext:
                data = data.rstrip("\n")
                if data:
                    i=0;
                    for word in cleartext:
                        l = 0
                        while l != len(word):
                            temp_word = hiddentext[i] 
                            if word[l] == data:
                                hiddentext[i] = temp_word[:l]+data+temp_word[(l+1):]
                            l += 1
                        i += 1
                client, address = s.accept()
                joined = ""
                for text in hiddentext:
                    joined = joined + text.rstrip() + " "
                client.send(joined.rstrip())
                print hiddentext 
                data = client.recv(size)
                client.close()
         
