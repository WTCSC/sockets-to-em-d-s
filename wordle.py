"""Wordle game logic module.

This module provides the core Wordle game mechanics including word generation,
guess validation, and feedback checking with color-coded terminal output.
"""

from wonderwords import RandomWord

class Wordle:
    """Manages a single Wordle game instance.
    
    Attributes:
        length (int): The number of letters in the target word.
        word (str): The target word to be guessed.
        max_guesses (int): Maximum number of guesses allowed (default: 6).
    """

    def __init__(self, length, word=None):
        """Initialize a Wordle game.
        
        Args:
            length (int): The length of the word to guess.
            word (str, optional): A specific word to use. If None, generates a random word.
        """
        self.length = length
        self.max_guesses = 6
        if word == None:
            self.word = self.generate_word(length)
        else:
            self.word = word

    def generate_word(self, length, get_new_length=False):
        """Generate a random word of the specified length.
        
        Uses the RandomWord library to fetch a valid English word. If a word
        of the exact length cannot be found, prompts the user for a different length.
        
        Args:
            length (int): The desired length of the word.
            get_new_length (bool): If True, prompts user for a new word length.
            
        Returns:
            str: A random English word of the specified length.
        """
        if get_new_length == True:
            try:
                return self.generate_word(input("Please input a shorter word"))
            except:
                print("Make sure syntax is correct")
                return self.generate_word(length,get_new_length=True) 
        r = RandomWord()
        try:
            word = r.word(word_min_length=length, word_max_length=length)
        except:
            word = self.generate_word(length,get_new_length=True)
            
        return word

    def validate_guess(self, guess):
        """Validate that a guess is the correct length.
        
        Args:
            guess (str): The guessed word to validate.
            
        Returns:
            str: The validated guess, or prompts for a new one if invalid.
        """
        if len(guess) != self.length:
            guess = self.new_guess()
        return guess

    def new_guess(self):
        """Prompt the user to enter a new guess with proper validation.
        
        Returns:
            str: A valid guess of the correct length.
        """
        return self.validate_guess(input("Bad syntax make sure your guess is the correct number of letters: ").lower())

    def check_guess(self, guess):
        """Check a guess against the target word and provide color-coded feedback.
        
        Uses ANSI color codes:
        - Green (\\033[42m): Letter in correct position
        - Yellow (\\033[43m): Letter in word but wrong position
        - Black (\\033[40m): Letter not in word
        
        Args:
            guess (str): The guessed word to check.
            
        Returns:
            tuple: (result_list, is_correct)
                - result_list: List of color-coded letter strings
                - is_correct (bool): True if all letters are in correct positions
        """
        result = []
        correct = 0
        for i in range(self.length):
            if guess[i] == self.word[i]:
                # Correct letter in correct position - green background
                result.append('\033[42m' + f'{guess[i]}' + '\033[0m')
                correct += 1
            elif guess[i] in self.word:
                # Letter in word but wrong position - yellow background
                result.append('\033[43m' + f'{guess[i]}' + '\033[0m')
            else:
                # Letter not in word - black background
                result.append('\033[40m' + f'{guess[i]}' + '\033[0m')
        
        if correct == self.length:
            return result, True
        return result, False