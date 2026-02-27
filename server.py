"""Wordle game server for multiplayer gameplay.

This module implements a socket-based server that manages multiplayer Wordle matches.
It alternates between hosting words for clients to guess and guessing client-provided words.
Players compete based on the number of guesses taken to solve each word.
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
    print("Waiting for client")
    return len(guesses)

def main():
    """Main server loop for multiplayer Wordle.
    
    Sets up a socket server, waits for client connections, and orchestrates
    game rounds. Alternates between hosting and guessing words, tracks scores,
    and manages round continuation.
    """
    # Initialize socket with IPv4 and TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get port from user and bind server
    port = int(input("Enter port number: "))
    server.bind(('', port))
    server.listen(1)

    print("Waiting for connection...")
    conn, addr = server.accept()
    print("Connected to", addr)

    # Initialize game state variables
    server_score = 0
    client_score = 0
    rounds = 0
    continuing = True
    try:
        while continuing:
            rounds += 1
            
            # Even rounds: server hosts the word
            if rounds % 2 == 0:
                length = int(input("Choose word length: "))
                game = Wordle(length)
                word = game.word

                # Send word and length to client in format "length:word"
                conn.send(f"{length}:{word}".encode())
            else:
                # Odd rounds: client hosts the word
                conn.send("your turn".encode())
                data = conn.recv(1024).decode()
                length, word = data.split(":")
                length = int(length)
                game=Wordle(length,word=word)

            # Both players play with the same word
            print("\n--- GO ---")
            server_guesses = play_local_game(game)

            # Receive client result
            data = conn.recv(1024).decode()
            client_guesses = int(data)

            # Compare results and determine round winner
            if server_guesses < client_guesses:
                server_score += 1
                result = "SERVER WIN"
            elif client_guesses < server_guesses:
                client_score += 1
                result = "CLIENT WIN"
            else:
                result = "TIE"

            # Send round result to client
            conn.send(f"{result}:{server_guesses}:{client_guesses}:{server_score}:{client_score}".encode())

            # Display round results
            print("\n--- Round Result ---")
            print(result)
            print("Server guesses:", server_guesses)
            print("Client guesses:", client_guesses)
            print("Score -> Server:", server_score, "Client:", client_score)

            # Ask if players want to continue
            continuing = True if input("\nWould you like to play another round(y/n) ").lower() == 'y' else False
            try:
                if continuing:
                    print("Waiting for client...")
                    conn.send("continuing".encode())
                    if conn.recv(1024).decode() == 'continuing':
                        continue
                else:
                    # End game
                    conn.send("done".encode())
                continuing =False
            except:
                continuing = False
                print("Client Exited, leaving game")
    except:
        print("Unknown Error(Client likely closed connection), please restart")
    
    # Clean up connections
    conn.close()
    server.close()


if __name__ == "__main__":
    main()