# python-connect4
Connect4 game with implemented Computer AI (minimax algorithm)

Scoring system:
To increase the ‘intelligence’ of the AI, I created a scoring system based on placing
moves for 2 in a row, 3 in a row, and 4 in a row. As this solution was designed with the
intention of implementing the minimax algorithm, my scoring system also includes scores
for the opponents 2 in a row, 3 in a row, and 4 in a row.

Moves are scored as follows:
- Any move that creates a four in a row for the AI: 1000 points
- Any move that creates a three in a row for the AI: 5 points
- Any move that creates a 2 in a row for the AI: 2 points
- Any move for the opponent that creates a four in a row: -1000 points
- Any move for the opponent that creates a three in a row: -100 points
- Any move for the opponent that creates a two in a row: -2 points

Note: The scoring is done based on the entire board, rather than the most recent move and
cumulates the total score of all the past 2s, 3s, and 4s in a row already on the board.

How do my scoring functions work?
I have implemented two scoring functions:
1. evaluate_board (player, scoring_for_final_score = False)
2. evaluate_window (self, window, point, scoring_for_final_score)

evaluate_board (player, scoring_for_final_score = False):

This function loops through all the horizontal, vertical, positive and negative diagonal
‘windows’ within the game board. ‘Windows’ are arrays of four consecutive positions on the
board (consecutive based on whether we are scoring for horizontal, vertical, positive or
negative diagonal), and are evaluated for their points by calling the second function
evaluate_window.

evaluate_window (self, window, point, scoring_for_final_score)

This function takes a window as a parameter and totals the score of this window based on
the scoring system.

My minimax algorithm uses two functions:
1. choose_move (self, player)
2. choose_move_for_minimax_points (self, player_to_play, player_to_evaluate, should_maximise, depth)

choose_move (self, player)

This function has two purposes: (1) to call the minimax algorithm, and (2) to return the
column of the best move to make, based on evaluating all options three moves ahead.

choose_move_for_minimax_points (self, player_to_play, player_to_evaluate, should_maximise, depth)

This function is the minimax algorithm. It recursively calls itself to check all of the possible
locations up to three moves ahead and returns the points and location of the best move
each time. To ensure that I am not changing the state of the board by adding and removing
points (as I was originally doing in Ass.py), I have added an additional function ‘copy (self)’
that copies the board, so each of the recursive moves are completed on a copy of the board,
rather than on the board to display.
