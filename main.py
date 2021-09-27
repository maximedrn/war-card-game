"""@author: Maxime."""


from colorama import init, Fore, Style, Back  # pip install colorama
from datetime import datetime
import random
import time
import os
import re


"""Colorama module constants."""
init()  # Init colorama module.
red = Fore.RED  # Red color.
green = Fore.GREEN  # Green color.
black = Fore.BLACK  # Black color.
yellow = Fore.YELLOW  # Yellow color.
magenta = Fore.MAGENTA  # Magenta color.
red_b = Back.RED  # Red background color.
cyan_b = Back.CYAN  # Cyan background color.
white_b = Back.WHITE  # White background color.
green_b = Back.GREEN  # Green background color.
reset = Style.RESET_ALL  # Reset color attribute.

"""Indents constants."""
ten_spaces = ' ' * 10
five_hyphens = '-' * 5
equals = '=' * 38


class War:
    """Main class of War card game."""

    def __init__(self, timer: int, re_shuffle: bool, interface: bool,
                 first_player: str, second_player: str,
                 scoreboard: bool = True) -> None:
        """Init colors and values with ranks and generate a deck of cards."""
        self.colors = {'♣': '', '♠': '', '♦': f'{red}', '♥': f'{red}'}
        self.values = {'A': 13, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,
                       '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12}
        self.deck = [f'{value}:{color}'
                     for value in self.values for color in self.colors]
        self.first_stash = []  # Actual stash of the first player.
        self.second_stash = []  # Actual stash of the second player.
        self.first_player = first_player if first_player != '' else 'Player_1'
        self.second_player = second_player \
            if second_player != '' else 'Player_2'
        self.re_shuffle = re_shuffle
        self.scoreboard = scoreboard
        self.interface = interface
        self.timer = timer
        self.game = 1

    def shuffle_deck(self, deck: list = []) -> list:
        """Shuffle the cards in random order."""
        # Increase chances of short games (-500 rounds).
        for _ in range(random.randint(1, 20)):
            # Use random's shuffle method.
            random.shuffle(self.deck) if deck == [] else random.shuffle(deck)
        return deck

    def card_rank(self, card: str) -> int:
        """Get rank of the card."""
        # Return an int in function of value of the card, e.g.: 5♠ has rank 4,
        # A♠ has rank 14 and J♠ has rank 10, etc.
        return self.values[card.split(':')[0]]

    def war(self, stash: list, card: list, deck: list) -> tuple:
        """In case of war."""
        stash.extend([card] + deck[-3:])  # Create stash for the player.
        deck = deck[:-3]  # Remove 3 cards from the player deck.
        deck.append(stash.pop())  # Add last card of stash to deck.
        return deck, stash

    def win(self, deck) -> list:
        """In case of a round win."""
        # Add played cards and the 4 cards from stash at the start of the deck.
        # It corresponds with the end of the deck during game.
        deck = [self.first_card, self.second_card] \
            + self.first_stash + self.second_stash + deck
        self.first_stash = []  # Reset stashes.
        self.second_stash = []
        return deck

    def ascii_card(self) -> str:
        """Get ASCII cards."""
        # Split card: value:color. It gives a list, e.g.: ['10', '♠'].
        first_card = self.first_card.split(':')
        second_card = self.second_card.split(':')

        # Get color in function of card and replace characters.
        def color(character, card):
            return character, f'{self.colors[card[1]]}{character}{reset}'
        first_color_at, first_color_tag = \
            tuple(color(char, first_card) for char in ['@', '#'])
        second_color_at, second_color_tag = \
            tuple(color(char, second_card) for char in ['@', '#'])

        # Create ascii_card with color.
        first_ascii_card = open(f'assets/{"".join(first_card)}.txt') \
            .read().replace(first_color_at[0], first_color_at[1]).replace(
                first_color_tag[0], first_color_tag[1]).split('\n')

        second_ascii_card = open(f'assets/{"".join(second_card)}.txt') \
            .read().replace(second_color_at[0], second_color_at[1]).replace(
                second_color_tag[0], second_color_tag[1]).split('\n')

        # Return fusionated cards.
        return ''.join([f'\n{first_card}{ten_spaces}{second_card}'
                        for first_card, second_card in
                        zip(first_ascii_card, second_ascii_card)])

    def show_results(self, first_deck: list, second_deck: list) -> None:
        """Show results of each round."""
        # Split card: value:color. It gives a list, e.g.: ['10', '♠'].
        first_card = self.first_card.split(':')
        second_card = self.second_card.split(':')

        # Print results.
        print(
            self.ascii_card() +
            f'\n\n'
            f'{yellow}{self.first_player}{reset} has {yellow}{len(first_deck)}'
            f'{reset} cards and {yellow}{self.second_player}{reset} has'
            f'{yellow} {len(second_deck)}{reset} cards.\n\n'

            f'{magenta}{self.first_player}{reset} played {first_card[0]} of '
            f'{self.colors[first_card[1]]}{first_card[1]}{reset} and '
            f'{magenta}{self.second_player}{reset} played {second_card[0]} '
            f'of {self.colors[second_card[1]]}{second_card[1]}{reset}.\n'
            f'{green}-->{reset} {green_b} {self.round_win} {reset} {green}won '
            f'the round n°{self.round}.{reset}')

    def show_scoreboard(self) -> None:
        """Show scoreboard from scoreboard.txt."""
        print(f'\n{yellow}Loading scoreboard...{reset}')
        time.sleep(10)  # Wait 10 seconds before clear console.
        cls()  # Clear console.
        # Print scoreboard.
        print(f'{cyan_b} Scoreboard: {reset} \n\n'
              f'{open("scoreboard.txt", "r", encoding="utf-8").read()}'
              .replace('vs.', f'{red}vs.{reset}'))

    def save_results(self, winner: str, round: int) -> None:
        """Save results in scoreboard.txt."""
        now = datetime.now()  # Get actual date time.
        with open('scoreboard.txt', 'r+', encoding='utf-8') as file:
            winners = file.read().split('\n')  # Read each line an make a list.
            number = winners[len(winners) - 1]  # Get last score.
            number = int(re.search(r"\[(.*)\]", number).group(1)) \
                + 1 if len(number) != 0 else 1  # Add 1 to score number.
            # If scoreboard.txt is not empty: break line.
            line_break = '\n' if len(winners[0]) > 0 else ''
            # Write results.
            file.write(f'{line_break}[{number}] '
                       f'{self.first_player} vs. {self.second_player}: '
                       f'{winner} wins - round n°{round} '
                       f'({now.strftime("%d/%m/%Y %H:%M:%S")}).')

    def play_game(self) -> None:
        """Play the War game, check who wins and if war."""
        cls()  # Clear console.
        self.round = 1  # Set round variable.
        # Get the first part of deck.
        first_deck = self.deck[:len(self.deck) // 2]
        # Get the second part of deck.
        second_deck = self.deck[len(self.deck) // 2:]
        war = False  # Is war boolean.

        # Print number of party if it's automatic games.
        print(f'Game n°{game + 1}.', end=' ') if not self.scoreboard else None

        # While the 2 decks are not empty.
        while first_deck and second_deck:

            if not war:  # Print round.
                cls() if self.scoreboard else None  # Clear console.
                print(f'\n{cyan_b} {equals} ROUND N°{self.round} '
                      f'{equals} {reset}') if self.interface else None

            # Playing from the end forward: getting last card from each deck.
            self.first_card = first_deck.pop()
            self.second_card = second_deck.pop()

            # In case of equality: start war.
            if self.card_rank(self.first_card) \
                    == self.card_rank(self.second_card):
                print(f'{red_b} {five_hyphens}> War!{reset} - '
                      f'{self.first_card} vs {self.second_card}') \
                        if self.interface else None
                first_deck, self.first_stash = self.war(
                    self.first_stash, self.first_card, first_deck)
                second_deck, self.second_stash = self.war(
                    self.second_stash, self.second_card, second_deck)
                war = True  # Set war boolean to True.

            else:

                # In case of first player has the highest card.
                if self.card_rank(self.first_card) \
                        > self.card_rank(self.second_card):
                    first_deck = self.win(first_deck)
                    self.round_win = self.first_player

                # In case of second player has the highest card.
                elif self.card_rank(self.first_card) \
                        < self.card_rank(self.second_card):
                    second_deck = self.win(second_deck)
                    self.round_win = self.second_player

                # Print results of each round.
                self.show_results(first_deck, second_deck) \
                    if self.interface else None
                self.round += 1  # Add one round.

                # Shuffle each decks.
                if self.round % 50 == 0 and self.re_shuffle:
                    first_deck = self.shuffle_deck(first_deck)
                    second_deck = self.shuffle_deck(second_deck)

                war = False  # Reset war boolean.
            # Wait X seconds between each round.
            time.sleep(self.timer) \
                if self.interface or self.scoreboard else None

        if not self.scoreboard:
            self.game += 1
            print(f'Game n°{game + 1} ends.{reset}')

        # Print winner.
        winner = self.first_player if len(first_deck) \
            == 52 else self.second_player
        print(f'\n {five_hyphens}> {winner.upper()} '
              f'{green}WINS THE WAR!{reset}')
        self.save_results(winner, self.round)


def cls() -> None:
    """Clear console function."""
    # Clear console for Windows using 'cls' and Linux & Mac using 'clear'.
    os.system('cls' if os.name == 'nt' else 'clear')


def input_answer(question: str, text: str) -> bool:
    """Analyse answer of inputs."""
    answer = input(question).lower()
    if answer == 'y':
        print(f'{green}{text} is enabled.{reset}')
        return True
    else:
        print(f'{red}{text} is disabled.{reset}')
        return False


if __name__ == '__main__':

    cls()  # Clear console.
    print(open('rules.txt', 'r', encoding='utf-8').read()  # Print rules.
          .replace('{green}', green).replace('{reset}', reset))

    # Wait until players press any key.
    input('PRESS ANY KEY TO START THE GAME ')

    # Ask if automation is enabled.
    automation = input_answer('\nPlay games automatically? ', 'Autoplaying')
    number_of_game = 1  # Default value.

    if not automation:

        # Ask timer.
        timer = input('\nHow many seconds do you have to wait each round? ')
        # If timer variable is interpreted as a float/int and is positive.
        if timer.replace('.', '').isdigit():
            timer = float(timer)
        else:
            timer = 1  # Set timer to default value.
            print(f'{red}Invalid input:{reset} '
                  'timer must be an integer or a float, and must be '
                  f'positive.\nTimer default value set to '
                  f'{white_b}{black}1 second{reset}.')

        # Ask if re shuffle can be enable.
        re_shuffle = input_answer(
            '\nEnable re-shuffle of decks every 50 rounds? (y/n)\n'
            'Note: (It reduces playing time) ', 'Re shuffle')

        # Ask if interface can be enabled.
        interface = input_answer(
            '\nEnable visual interface? (y/n) ', 'Visual interface')

        # Ask for players name.
        first_player = input('\nWhat is the name of the first player? ')
        second_player = input('What is the name of the second player? ')
        # If player names are identical.
        if first_player == second_player and len(first_player) > 0:
            first_player += '_1'
            second_player += '_2'

    # If automatic games.
    else:
        timer = 0
        re_shuffle = True
        interface = False
        number_of_game = 50
        first_player = ''
        second_player = ''

    # For each game: default 1, max: 50.
    for game in range(number_of_game):

        scoreboard = True if not automation else False

        # Init War class.
        war = War(timer, re_shuffle, interface,
                  first_player, second_player, scoreboard)
        war.shuffle_deck()  # Shuffle deck of cards.
        war.play_game()  # Start War card game.

    # Display scoreboard at the end of game.
    war.show_scoreboard()
