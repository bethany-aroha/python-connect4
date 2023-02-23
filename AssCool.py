#Bethany Yates (byat757): 651423594
#This program utilises classes and recursion to create a simple connect 4 game. 
#The AI uses the minimax algorithm to look three moves ahead and pick the best move based on this algorithm. 


#----------------------Naming Conventions; points, point, and score------------------------#

#Score refers to overall score of players
#Point refers to a specific 'point' placed on the board
#Points refers to the number of points associated with each move according to the minimax algorithm

#---------------------Naming Conventions; c vs. column, r vs. row---------------------------#

#c and r are used when iterating through lists of rows and columns. Row and Column are used when refering to a specific column or location / when 
#rows or columns are used outside of for loops


import math
import copy
class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
    
    #--------------------Create a copy of the current board----------------------#
    def copy(self):
        new_board = GameBoard(self.size)
        new_board.num_entries = self.num_entries.copy()
        new_board.items = copy.deepcopy(self.items)
        return new_board

    #---------------------------Displaying the Board-----------------------------#
    def display(self):
        row_list = self.get_row_list()
        for r in row_list:
            for item in range(0, len(r)):
                if r[item] == 0:
                    r[item] = ' '
                elif r[item] == 1:
                    r[item] = 'o'
                elif r[item] == 2:
                    r[item] = 'x'

        for r in range(len(row_list)):
            print(*row_list[r], sep = ' ')

        print('-'*((self.size*2)-1))
        for num in range(0, self.size):
            print(num, end = " ")


    #----------------------------General Board Information-------------------------#
    
    def num_free_positions_in_column(self, column):
        return self.size - self.num_entries[column]

    #Generates list of all valid columns in the current board
    def get_valid_locations(self):
        valid_locations = []

        for c in range(self.size):
            if self.num_free_positions_in_column(c) > 0:
                valid_locations.append(c)

        return valid_locations

    
    #Used to display board in row by row fashion
    def get_row_list(self):
        row_list = []
        row_length = self.size - 1
        while row_length >= 0:
            row_list.append([column[row_length] for column in self.items])
            row_length -= 1

        return row_list


    #Used to change between player 1 and 2 and point type 'o' and 'x'
    def get_point_type(self, player):
        point = ''
        if player == 1:
            point = 'o'

        elif player == 2:
            point = 'x'

        return point

    
    def game_over(self):
        for c in self.num_entries:
            if c < self.size:
                return False
        return True



    #----------------------------Adding to the board----------------------#

    def add(self, column, player):
        if self.num_entries[column] >= self.size or column < 0 or column >= self.size:
            return False

        row_number = self.num_entries[column]

        if player == 1:
            self.items[column][row_number] = 'o'

        else:
            self.items[column][row_number] = 'x'

        self.num_entries[column] += 1

        return True



    #------------------------------------Where should AI place piece?------------------------------#

    #Implementation of the minimax algorithm: this algorithm looks 3 moves ahead (depth = 3)
    def choose_move(self, player):
        location_of_best_move = self.choose_move_for_minimax_points(player, player, True, 3)
        return location_of_best_move



    def choose_move_for_minimax_points(self, player_to_play, player_to_evaluate, should_maximise, depth):
        valid_locations = self.get_valid_locations()
        list_of_possible_points = []
        
        for location in valid_locations:
            new_board = self.copy()
            new_board.add(location, player_to_play)

            if new_board.game_over() or depth == 0:
                points = new_board.evaluate_board(player_to_evaluate)

            else:
                if player_to_play == 1:
                    next_player_to_play = 2
                else:
                    next_player_to_play = 1

                points = new_board.choose_move_for_minimax_points(next_player_to_play, player_to_evaluate, not should_maximise, depth - 1)

            list_of_possible_points.append((points, location))


        if should_maximise:
            return max(list_of_possible_points)
        return min(list_of_possible_points)



    #Scoring system for the minimax algorithm: takes 1 window of four moves at a time
    #Uses 'evaluate_window()'to score each window based on the number of 4s, 3s, and 2s in a row
    #scoring_for_final_score used to evaluate total player score once game is over
    def evaluate_board(self, player, scoring_for_final_score = False):
        points = 0
        point = self.get_point_type(player)
        row_list = self.get_row_list()

        #Checking for horizontal points
        for r in range(self.size):
            row_array = [i for i in list(row_list[r])]
            for c in range(self.size - 3):
                window = row_array[c:c+4]
                points += self.evaluate_window(window, point, scoring_for_final_score)


        #Checking for vertical points
        for c in range(self.size):
            column_array = [i for i in list(self.items[c])]
            for r in range(self.size - 3):
                window = column_array[r:r+4]
                points += self.evaluate_window(window, point, scoring_for_final_score)
            
        #Checking for positive diagonal points
        for r in range(self.size - 3):
            for c in range(self.size - 3):
                window = [self.items[r + i][c + i] for i in range(4)]
                points += self.evaluate_window(window, point, scoring_for_final_score)

        #Checking for negative diagonal points
        for r in range(self.size - 3):
            for c in range(self.size - 3):
                window = [self.items[r + 3 - i][c + i] for i in range(4)]
                points += self.evaluate_window(window, point, scoring_for_final_score)

 
        return points


    def evaluate_window(self, window, point, scoring_for_final_score):
        points = 0

        if scoring_for_final_score:
            if window.count(point) == 4:
                points += 1
            return points

        
        if window.count(point) == 4:
            points += 1000

        if window.count(point) == 3 and window.count(0) == 1:
            points += 5

        if window.count(point) == 2 and window.count(0) == 2:
            points += 2
        
        if window.count('o') == 4:
            points -= 1000

        if window.count('o') == 3 and window.count(0) == 1:
            points -= 100

        if window.count('o') == 2 and window.count(0) == 2:
            points -= 2

        

        return points


class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            else:
                                print("Column ", column, "is alrady full. Please choose another one.")
            else:
                
                (max_points, best_column)=self.board.choose_move(2)
                column = best_column
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        
        total_player_score_player_one = self.board.evaluate_board(1, True)
        total_player_score_player_two = self.board.evaluate_board(2, True)

        print('\nTotal Player 1 score: ', total_player_score_player_one)
        print('Total Player 2 score: ', total_player_score_player_two)
        
        if (total_player_score_player_one>total_player_score_player_two):
            print("Player 1 (circles) wins!")
        elif (total_player_score_player_one<total_player_score_player_two):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")

            
game = FourInARow(6)
game.play()        