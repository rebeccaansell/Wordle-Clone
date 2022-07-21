import random
from termcolor import cprint
import os


def getInput():
  while True:
    print()
    guess = input("Enter your guess: ").lower()
    if len(guess) != 5 or not guess.isalpha():
      print("Guess must be 5 letters")
    elif guess not in guessWords:
      print("Word not in dictionary")
    else:
      return guess


def colorResult(guess, word):
  guessColors = ['on_grey'] * 5 
  # default to grey

  # find greens
  for i in range(len(word)):
    if word[i] == guess[i]:
      guessColors[i] = 'on_green'

  # find yellows
  left = [x for x in range(len(word)) if guessColors[x] != 'on_green']
  for wordIndex in left:
    for guessIndex in left:
      if word[wordIndex] == guess[guessIndex] and guessColors[guessIndex] == 'on_grey':
        guessColors[guessIndex] = 'on_yellow'
        break

  # print guess
  for i, x in enumerate(guess):    
    cprint(x.upper(), 'white', guessColors[i], attrs=['bold'], end=' ')
  print()
  return guessColors


def printLetterBank(targetWord, guesses, guessColorsList):
  keyboard = list("qwertyuiopasdfghjklzxcvbnm")
  keyColors = {}
  for k in keyboard:
    keyColors[k] = 'on_grey' # default color if it hasn't been guessed

  #determine colors for keyboard
  for letter in keyboard:
    for g in range(len(guesses)):
      guess = guesses[g]
      guessColors = guessColorsList[g]
      for guessLetterInd in range(len(guess)):
        if guess[guessLetterInd] == letter: #found a matching letter
          guessColor = guessColors[guessLetterInd]
          if guessColor == 'on_green':
            keyColors[letter] = 'on_green'
          elif guessColor == 'on_yellow':
            if keyColors[letter] != 'on_green':
              keyColors[letter] = 'on_yellow'
          elif guessColor == 'on_grey':
            if keyColors[letter] != 'on_green' and keyColors[letter] != 'on_yellow':
              keyColors[letter] = 'wrong' # used as a key, not an actual color

  #print keyboard
  print()
  for k in keyboard:
    if keyColors[k] == 'wrong': # a wrong guess will be dark
      cprint(k.upper(), 'white', 'on_grey', attrs=['bold', 'dark'], end=' ')
    else:
      cprint(k.upper(), 'white', keyColors[k], attrs=['bold'], end=' ')
    if k == 'p':
      print('\n ', end='')
    elif k == 'l':
      print('\n   ', end='')
  print()

            


os.system('clear')
print("Welcome to Replit Wordle!")

# read in word banks
with open('targetWords.txt', 'r') as FILE:
  words = [word.rstrip() for word in FILE]
choices = [w for w in words if len(w) == 5]
with open('guessWords.txt', 'r') as FILE:
  words = [word.rstrip() for word in FILE]
guessWords = words + choices

# randomly choose a target word
word = random.choice(choices)
guesses = []

# start game
print("You have 6 guesses to guess the 5-letter word.")
while True:
  # prompt player for guess
  guess = getInput()
  guesses.append(guess)

  # print guess results
  os.system('clear')
  guessColorsList = []
  for g in guesses:
    guessColorsList.append(colorResult(g, word))
  print('\n' + str(len(guesses)) + "/6 guesses" )

  # print keyboard
  printLetterBank(word, guesses, guessColorsList)

  # check for win/lose
  if guess == word:
    print('\nYou Win!')
    break
  elif len(guesses) == 6:
    print("\nSorry, you ran out of guesses.")
    print("The word was:", word.upper())
    break