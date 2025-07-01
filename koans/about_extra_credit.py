#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EXTRA CREDIT:
#
# Create a program that will play the Greed Game.
# Rules for the game are in GREED_RULES.TXT.
#
# You already have a DiceSet class and score function you can use.
# Write a player class and a Game class to complete the project.  This
# is a free form assignment, so approach it however you desire.

from functools import reduce
from runner.koan import *
from .about_dice_project import DiceSet
from .about_scoring_project import score_plus

class Player():
    def __init__(self, name):
        self._name = name
        self._score = 0
        self._ingame = False

    def __repr__(self):
        return "{0}: {1} ({2})".format(self._name, self._score, "In the game" if self._ingame else "Not in the game")

    def name(self):
        return self._name
    
    def score(self):
        return self._score

    def take_turn(self):
        print("{0} taking a turn...\n".format(self._name))
        dice = DiceSet()

        roll = True
        non_scoring = 5
        running_total = 0
        while roll:
            dice.roll(non_scoring)
            result = dice.values
            roll_score, non_scoring = score_plus(result)
            print("Rolled {0}, score {1}\n".format(result, roll_score))

            if roll_score == 0:
                print("Rolled zero, out")
                return self._score

            running_total += roll_score
            if non_scoring == 0:
                non_scoring = 5
            roll = self._should_reroll(running_total, non_scoring)

        if not self._ingame and running_total >= 300:
            self._ingame = True

        if self._ingame:
            self._score += running_total

        print("{0} Done.\n".format(self._name))
        return self._score
    
    def in_the_game(self):
        return self._ingame
    
    def _should_reroll(self, running_total, dice_available):
        if (dice_available >=4):
            return True
        else:
            return running_total < 300

class Game():
    def __init__(self, player_count):
        self._round = 0
        if (player_count < 2) or player_count > 10:
            raise TypeError
        
        self._players = []
        for player_id in range(1, player_count + 1):
            self._players.append(Player("Player {0}".format(player_id)))

    def __repr__(self):
        output = "Game with {0} players. Round {1}.\n".format(len(self._players), self._round)
        for player in self._players:
            output += repr(player)+"\n"
        return output
    
    def play(self):
        keep_going = True
        last_round = False
        
        while keep_going:
            self._round += 1
            print(repr(self))

            if last_round:
                print ("It's the last round!")
                keep_going = False

            for player in self._players:
                player.take_turn()
                if player.score() >= 3000:
                    last_round = True

        winner = reduce(lambda acc, p: p if p.score() > acc.score() else acc, self._players, self._players[0])
        print ("The winner is {0} with {1} points!".format(winner.name(), winner.score()))


class AboutExtraCredit(Koan):
    # Write tests here. If you need extra test classes add them to the
    # test suite in runner/path_to_enlightenment.py

    def test_player_init(self):
        player = Player("Adam")
        self.assertEqual("Adam", player.name())
        self.assertEqual(0, player.score())

    def test_player_should_reroll(self):
        player = Player("Adam")
        self.assertTrue(player._should_reroll(0, 5))
        self.assertTrue(player._should_reroll(1000, 5))
        self.assertFalse(player._should_reroll(1000, 1))
        self.assertFalse(player._should_reroll(1000, 3))
        self.assertTrue(player._should_reroll(100, 3))

    def test_player_rep(self):
        player1 = Player("Adam")
        player2 = Player("Bob")

        player1._score = 100
        player2._score = 500

        player2._ingame = True

        self.assertEqual("Adam: 100 (Not in the game)", repr(player1))
        self.assertEqual("Bob: 500 (In the game)", repr(player2))

    def test_game_init(self):
        game = Game(3)
        self.assertEqual(3, len(game._players))
        self.assertEqual(0, game._round)

        with self.assertRaises(TypeError):
            Game(1)

        with self.assertRaises(TypeError):
            Game(-1)

        with self.assertRaises(TypeError):
            Game(15)

    def test_game_rep(self):
        game = Game(3)
        self.assertEqual("Game with 3 players. Round 0.\n{0}\n{1}\n{2}\n".format(repr(game._players[0]), repr(game._players[1]), repr(game._players[2])), repr(game))

    def test_take_turn(self):
        player = Player("Adam")
        player.take_turn()
    
    def test_play(self):
        game = Game(3)
        game.play()
