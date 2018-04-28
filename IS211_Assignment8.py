import argparse
from datetime import datetime, timedelta
import random


class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.tally = 0


    def next_turn(self, start_time, max_time):
        self.my_turn()
        elapsed_time = datetime.now() - start_time
        if elapsed_time >= max_time:
            self.tally = 0

        # current player holds
        # display current roll total and total players
        self.score += self.tally
        self.tally = 0
        print('{} score is: {}'.format(self.name, self.score))


class Human(Player):
    def my_turn(self):
        print('{} score is: {}'.format(self.name, self.score))
        # current player must choose roll or hold
        choice = 'pig'
        # check if correct input given
        while choice not in ['r', 'h']:
            choice = raw_input('{} enter r or h to continue: '.format(self.name))

        while choice == 'r':
            # current player rolls
            # display current roll total and total players
            die_roll = Die().roll()
            print('You rolled {}'.format(die_roll))

            # roll anything other than 1, add to tally
            if die_roll != 1:
                self.tally += die_roll
                print('Your roll tally is: {}'.format(self.tally))
                # roll another turn
                choice = 'anything'
                while choice not in ['r', 'h']:
                    choice = raw_input('{} enter r or h to continue: '.format(self.name))
            else:
                self.tally = 0
                choice = 'not r'


class Computer(Player):
    def my_turn(self):
        print('{} score is: {}'.format(self.name, self.score))
        # current player must choose roll or hold
        choice = 'r'

        while choice == 'r':
            # current player rolls
            # display current roll total and total players
            die_roll = Die().roll()
            print('You rolled {}'.format(die_roll))

            # roll anything other than 1, add to tally
            if die_roll != 1:
                self.tally += die_roll
                print('Your roll tally is: {}'.format(self.tally))
                # roll another turn
                # if computer tally is lesser of 25 or 100-score, then hold
                hold = 100 - self.score
                if 25 < 100 - self.score:
                    hold = 25

                if self.tally >= hold:
                    choice = 'h'
            else:
                self.tally = 0
                choice = 'not r'


class Die(object):
    def roll(self):
        return random.randint(1, 6)

class Player_Factory(object):
    def __init__(self):
        self.comp_names = ['Johnny 5', 'T-1000', 'R2D2', 'Dalek', 'Kit', 'Optimus Prime']
        self.last_comp_name = None



    def create_player(self, player_type):
        if player_type == 'Human':
            return Human(raw_input('Please enter your name: '))
        else:
            comp_player = random.choice(self.comp_names)
            while comp_player == self.last_comp_name:
                comp_player = random.choice(self.comp_names)
            self.last_comp_name = comp_player
            return Computer(comp_player)



class Game(object):
    def __init__(self, args):
        self.die = Die()
        player_creator = Player_Factory()
        self.player1 = player_creator.create_player(args['player1'])
        self.player2 = player_creator.create_player(args['player2'])


        # set current player
        self.current_player = self.player1

        # game timer
        self.start_time = datetime.now()
        self.max_time = timedelta(0, 60)
        self.elapsed_time = timedelta()

    def next_turn(self):
        self.current_player.next_turn(self.start_time, self.max_time)
        # shifting the baton
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

        self.elapsed_time = datetime.now() - self.start_time


if __name__ == '__main__':
    # setting up argparse
    parser = argparse.ArgumentParser(description='pig game')
    parser.add_argument('--player1', type=str, help='Player Type', required=True, choices={'Human', 'Computer'})
    parser.add_argument('--player2', type=str, help='Player Type', required=True, choices={'Human', 'Computer'})
    args = vars(parser.parse_args())

    # create game
    pig = Game(args)


    # run game
    while pig.player1.score < 100 and pig.player2.score < 100 and pig.elapsed_time <= pig.max_time:
        pig.next_turn()
    if pig.player1.score > pig.player2.score:
        winner = pig.player1
        print('The winner is: {}'.format(winner.name))
    elif pig.player1.score < pig.player2.score:
        winner = pig.player2
        print('The winner is: {}'.format(winner.name))
    else:
        print('Game Over, time limit reached: Tie-Score! {}'.format(pig.player1.score))
