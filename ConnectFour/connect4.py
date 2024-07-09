import numpy as np
import winsound
import pygame
import random
import os
import sys
import time

pygame.init() # Initializes all imported Pygame modules
pygame.mixer.init() # Initializes the mixer module for sound playback

# List of songs to be played during the game
songs_for_rounds = [
    r"C:\Users\rasjr\Documents\GitHubProjects\ConnectFour\C4Music\outofbody.wav",
    r"C:\Users\rasjr\Documents\GitHubProjects\ConnectFour\C4Music\battle.wav",
    r"C:\Users\rasjr\Documents\GitHubProjects\ConnectFour\C4Music\MGS.wav",
    r"C:\Users\rasjr\Documents\GitHubProjects\ConnectFour\C4Music\mgsfinalbattle.wav",
]

# The board size. Can change the row count and column count to any number.
ROW_COUNT = 6
COLUMN_COUNT = 7

# Player 1 + Player 2 enters the name of their choice.
player1Name = input('Player 1, enter your name: ')
player2Name = input('Player 2, enter your name: ')

# Function to create the board based on the row and column count specified.
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Function to drop the piece in the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check if the column is full
def is_valid_location(board, col):
    return board[5][col] == 0

# Function to get the next open row
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Function to print the board        
def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    #Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            
    #Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    #Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    #Check negatively sloped diagonals        
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Function to play a random song from the list
def play_random_song():
    pygame.mixer.music.stop() # Stops the current song so multiple don't play at once
    song_to_play = random.choice(songs_for_rounds) # Chooses a random song from the list
    pygame.mixer.music.load(song_to_play) # Loads the song
    pygame.mixer.music.play(3) # Plays the song 3 times

# Function to initialize the board
def initialize_board():
    return [[0 for _ in range(7)] for _ in range(6)]

# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

player1_wins = 0 # Tracks the number of wins for player 1
player2_wins = 0 # Tracks the number of wins for player 2

while player1_wins < 3 and player2_wins < 3:

    board = create_board() # Creates the board
    print_board(board) # Prints the board at the start of the game
    game_over = False # Game over is set to false at the start of the game
    turn = 0 # Player 1 starts the game
    round_number = 1 # Round number starts at 1
    
    # Explains the game on round 1 and plays a random song.
    if round_number == 1:
        print("Connect 4 in a row to win. Whoever gets 3 wins first becomes the Connect 4 champion! Good luck!")
        play_random_song()

    while not game_over:
        # Ask for Player 1 Input
        if turn == 0:
            while True:
                try:
                    col = int(input(f"{player1Name}, Type in a Number (0-6):"))
                    if col < 0 or col > 6:
                        raise ValueError
                    break
                except ValueError:
                    print("Please enter a valid number between 0 and 6.") # Error message if the player enters an invalid number
            
            # Checks if the location is valid
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    print(f"{player1Name} wins Round {round_number}!")
                    game_over = True
                    player1_wins += 1 # Increases player 1's win count by 1
                    if player1_wins == 3:
                        print(f"{player1Name} wins the game! Congratulations!")
                        time.sleep(6) # Waits 6 seconds before closing the game
                        break # Breaks out of the game loop if player 1 wins the game

        # Ask for Player 2 Input
        else:
            while True:
                try:
                    col = int(input(f"{player2Name}, Type in a Number (0-6):"))
                    if col < 0 or col > 6:
                        raise ValueError
                    break
                except ValueError:
                    print("Please enter a valid number between 0 and 6.") # Error message if the player enters an invalid number
            
            if is_valid_location(board, col):
                row = get_next_open_row(board, col) # Checks if the row is available
                drop_piece(board, row, col, 2) # 'Drops' the piece in the selected column.

                if winning_move(board, 2):
                    print(f"{player2Name} wins Round {round_number}!") # Prints the winner of the round
                    game_over = True
                    player2_wins += 1 # Increases player 2's win count by 1
                    if player2_wins == 3:
                        print(f"{player2Name} wins the game! Congratulations!")
                        time.sleep(6) # Waits 6 seconds before closing the game
                        break # Breaks out of the game loop if player 2 wins the game
        if game_over:
            print(f"Round {round_number} finished.")
            
            round_number += 1  # Increment the round counter
            
            play_again = input("Play another round? (Y/N): ").lower()
            if play_again == 'y':
                game_over = False
                board = initialize_board() # Reset the board for a new round
                
                turn = random.randint(0,1) # Randomly chooses which player gets to go first in the next round
                    
            else:
                print(f" The game will now exit in 5 seconds.")
                time.sleep(5) # Allows players to see the final board before the game ends
                sys.exit() # Closes the game

        clear_screen() # Clears the screen after each turn to prevent clutter.
        print(f"        Round {round_number}") # Displays the current round number.
        print() # Adds a space between the round number and the board.    
        print_board(board)
        turn += 1 # Increments the turn by 1
        turn = turn % 2 # Alternates between player 1 and player 2