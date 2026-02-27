# Multiplayer Wordle Game

A Python-based networked implementation of the popular word-guessing game Wordle, featuring real-time multiplayer gameplay over TCP sockets.

## Project Overview

This project implements a competitive multiplayer Wordle game where two players connect over a network and take turns hosting and guessing words. Players compete based on the number of guesses required to solve each word, with color-coded visual feedback for each guess.

### Key Features

- **Network-Based Gameplay**: Server-client architecture using TCP sockets for real-time communication
- **Alternating Rounds**: Players alternate between hosting words for the opponent to guess and guessing opponent-provided words
- **Score Tracking**: Automatic score tracking throughout the game with win/loss/tie determination
- **Color-Coded Feedback**: Visual ANSI color indicators showing guess accuracy:
  - Green: Correct letter in correct position
  - Yellow: Correct letter in wrong position
  - Black: Letter not in word
- **Dynamic Word Generation**: Uses the wonderwords library to generate valid English words of any specified length
- **Flexible Game Length**: Play as many rounds as desired with optional continuation after each round

## Requirements

### Python Version
- Python 3.7 or higher

### Dependencies
- wonderwords - For random English word generation

## Installation & Setup

### Step 1: Clone or Download the Project

Download the files to your desired directory.

### Step 2: Install Dependencies

Install the required Python package using pip:

```bash
pip install wonderwords
```
## Usage Guide

### Starting a Game

The game requires two terminals/machines: one running the server and one running the client.

#### Server Setup (Machine/Terminal 1)

```bash
python server.py
```

You'll be prompted for:
1. Port Number: Enter a port number
   ```
   Enter port number: <your wanted port>
   ```

The server will then wait for a client connection:

#### Client Setup (Machine/Terminal 2)

```bash
python client.py
```

You'll be prompted for:
1. Server IP Address: Enter the server's IP address
   ```
   Server IP: <server ip>
   ```

2. Port Number: Enter the same port number you specified on the server
   ```
   Port: <server port>
   ```

### During Gameplay

#### Round 1 (Server Hosts)
1. Server chooses a word length (e.g., 5)
2. Server is given a random 5-letter word to guess
3. Client receives the word and sees --- GO ---
4. Both players guess the same word simultaneously
5. Color-coded feedback appears after each guess

#### Round 2 (Client Hosts)
1. Client chooses a word length
2. Client provides a word for the server to guess
3. Server receives the word and sees --- GO ---
4. Both players guess the same word simultaneously

#### Round Results
After each round, the game displays:
```
--- Round Result ---
SERVER WIN
Server guesses: 3
Client guesses: 5
Score -> Server: 1 Client: 0
```

The winner is determined by who guesses the word in fewer attempts.

### Continuing the Game

After each round, you'll be asked:
```
Would you like to play another round(y/n) 
```

- y: Continue to the next round
- n: End the game and display final scores

## Game Mechanics

### Guess Validation
- Guesses must be exactly the specified word length
- Invalid guesses will prompt for re-entry
- All input is converted to lowercase for consistency

### Color Feedback System

After each guess, letters are displayed with color backgrounds:

Green: Correct position
Yellow: Wrong position
Black: Not in word

### Scoring
- Win Condition: Guess the word within 6 attempts
- Point System: Fewest guesses wins the round
  - If Server > Client guesses: Client gets 1 point
  - If Client > Server guesses: Server gets 1 point
  - If equal guesses: Neither player scores (TIE)

## Network Communication Protocol

The server and client exchange messages separated by colons:

Host Word: length:word (Server to Client or Client to Server)
Client Turn: your turn (Server to Client)
Guess Count: number (Both directions)
Round Result: result:server_guesses:client_guesses:server_score:client_score (Server to Client)
Continue: continuing (Both directions)
Game End: done (Both directions)


## License

This project is provided as-is for educational purposes.
