"""Wordle game client for multiplayer gameplay.

This module implements a socket-based client that connects to a Wordle game server.
It allows players to guess words provided by the server and provide their own words
for the server to guess. Players compete based on the number of guesses taken.
"""

import socket
from wordle import Wordle

def play_local_game(game):
    """Play a single round of Wordle with local input.
    
    Prompts the player for guesses and displays color-coded feedback.
    Continues until the word is guessed or max guesses are reached.
    
    Args:
        game (Wordle): The Wordle game instance.
        
    Returns:
        list or int: List of feedback arrays if won, otherwise number of guesses used.
    """
    guesses = []
    done = False

    while len(guesses) < game.max_guesses and not done:
        # Get and validate player's guess
        guess = game.validate_guess(input("Your guess: ").lower())

        # Check guess and get color-coded feedback
        feedback, done = game.check_guess(guess)
        guesses.append(feedback)
        
        # Display all previous guesses with color coding
        for guess in guesses:
            for letter in guess:
                print(letter,end='')
            print('')

        # Early exit if word is correctly guessed
        if guess == game.word:
            return guesses
    
    # Game over - word not guessed within max attempts
    print(f"\nThe word was {game.word}")
    print("Waiting for server")
    return len(guesses)


def main():
    """Main client loop for multiplayer Wordle.
    
    Establishes a socket connection to the server, participates in game rounds,
    and manages round continuation. Alternates between guessing server-provided
    words and having the server guess client-provided words.
    """
    # Initialize socket with IPv4 and TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get server connection details from user
    server_ip = input("Server IP: ")
    port = int(input("Port: "))

    # Connect to server
    client.connect((server_ip, port))
    print("Connected to server.")

    continuing = True
    try:
        while continuing:
            # Receive round info from server
            data = client.recv(1024).decode()
            
            if data == 'your turn':
                # Client's turn: choose a word for server to guess
                length = int(input('Choose word length: '))
                game = Wordle(length)
                word = game.word
                # Send word and length to server in format "length:word"
                client.send(f"{length}:{word}".encode())
            else:
                # Server's turn: guess a server-provided word
                length, word = data.split(":")
                length = int(length)
                game = Wordle(length,word=word)

            game = Wordle(length, word)

            print("\n--- GO ---")
            client_guesses = play_local_game(game)

            # Send number of guesses to server
            client.send(f"{client_guesses}".encode())

            # Receive round result from server
            data = client.recv(1024).decode()
            result, s_guesses, c_guesses, server_score, client_score = data.split(":")

            # Display round results
            print("\n--- Round Result ---")
            print(result)
            print("Client guesses:", c_guesses)
            print("Server guesses:", s_guesses)
            print("Score -> Server:", server_score, "Client:", client_score)

            # Ask if player wants to continue
            continuing = True if input("\nWould you like to play another round(y/n) ").lower() == 'y' else False
            try:
                if continuing:
                    print("Waiting for server...")
                    client.send("continuing".encode())
                    if client.recv(1024).decode() == 'continuing':
                        continue
                else:
                    # End game
                    client.send("done".encode())
                continuing =False
            except:
                print("Server Left, leaving game")
                continuing = False
    except:
        print("Unknown Error(Server likely closed), exiting")
    
    # Clean up connection
    client.close()


if __name__ == "__main__":
    main()