import random
from itertools import combinations_with_replacement, combinations
from typing import Iterator


class Domino:

    def __init__(self, front: int, bottom: int):
        self.front = front
        self.bottom = bottom

    def __str__(self) -> str:
        return f"[{self.front}, {self.bottom}]"

    def __eq__(self, other):
        """Two dominoes are equal in case domino1.front == domino2.front and domino1.bottom == domino2.bottom
        or  domino1.front == domino2.bottom and domino1.bottom == domino2.front"""
        return (self.front == other.front and self.bottom == other.bottom) or \
               (self.front == other.bottom and self.bottom == other.front)

    def __reversed__(self):
        """Returns new Domino object when front and bottom are swapped.
        E.g old Domino(1, 5) -> New Domino(5, 1)"""
        return Domino(self.bottom, self.front)

    def __hash__(self):
        return self.bottom + self.front


class DeckIterator(Iterator):

    def __init__(self, deck):
        self._deck = deck
        self._index = 0

    def __iter__(self):
        if self._index < len(self._deck.domino_deck):
            result = (self._deck.domino_deck[self._index])
            self._index += 1
            return result
        raise StopIteration

    def __next__(self):
        if self._index < len(self._deck.domino_deck):
            result = self._deck.domino_deck[self._index]
            self._index += 1
            return result
        raise StopIteration


class Deck:

    def __init__(self) -> None:
        self.domino_deck = []

    def __str__(self) -> str:
        return ''.join([str(domino) for domino in self.domino_deck])

    def __len__(self) -> int:
        return len(self.domino_deck)

    def __iter__(self) -> Iterator:
        return DeckIterator(self)

    def __getitem__(self, item):
        """Returns the Domino from dominoes deck by the index. In case the Index is out of range -
                raises IndexError. Index starts with 1 not 0. So, the first Domino index is 1, second - 2 etc.
                Negative index starts with 0. The last elements is 0, pre-last -1 etc"""
        if item <= len(self):    # Index counting starts with 1, not 0. to get the last item use 0, prelast -1 etc
            return self.domino_deck[item - 1]
        raise IndexError(f'The index is out of range. Given: {item}. Deck length is {len(self)}')

    def __contains__(self, item):
        if isinstance(item, Domino):
            return item in self.domino_deck
        else:
            print(f'Error. The item should be an instance of <class Domino>. Given {type(item)}')

    def __bool__(self):
        """Returns true if the length of the deck is > 0"""
        return len(self) > 0

    def __eq__(self, other):
        if len(self) != len(other):     # if length is different - no need to check further
            return False
        for domino in self:
            if domino not in other:
                return False
        return True

    def __add__(self, other):
        """Add dominoes to deck from the left if domino not added already"""
        for domino in other:
            self.add_domino(domino)

    def add_domino(self, domino: Domino):
        if isinstance(domino, Domino):
            if domino not in self:
                self.domino_deck.append(domino)
        else:
            print(f'Sorry. The domino should be an instance of <class Domino>. Given: {type(domino)}')

    def remove(self, domino: Domino):
        """Iterates over domino deck and looks for a domino that is equal to a given domino. In case
        the match is found - pop the domino"""
        for ind, piece in enumerate(self.domino_deck, 0):
            if piece == domino:
                self.domino_deck.pop(ind)
                break

    def _append_to_game_deck(self, domino: Domino):
        """Method is used to append the Domino to the end of the game deck in the correct order.
        E.g. game deck is (1, 3)(2, 5), User Domino is (1, 5). This method will append the reversed domino
        to the game deck if needed. Game deck after: (1, 3)(2, 5)(5, 1). Not supposed to be called directly
        most of the time"""
        if len(self) == 0:  # check if the game deck is empty. If yes - then just add the domino to the deck
            self.add_domino(domino)     # TODO add choice for the user what side to put the first domino
        else:
            self.add_domino(domino) if domino.front == self[0].bottom else self.add_domino(domino.__reversed__())

    def is_valid_move(self, domino: Domino):
        """Method is used to check if the Domino is possible to append to the game deck"""
        if len(self) == 0:  # check if the game deck is empty. If yes - then just add the domino to the deck
            return True
        else:
            if domino.front == self[0].bottom:  # if the last domino matches the front of the given domino
                return True
            elif domino.bottom == self[0].bottom:   # if the last domino matches the given domino bottom
                return True
            else:
                return False


class Player:

    def __init__(self, name):
        self.name = name
        self.player_domino_deck = Deck()   # Deck[Domino]

    def __str__(self) -> str:
        """Returns string representation of the Player's game deck in a format: {index}:{domino}. E.g.:
        1:[5, 6]
        2:[3, 4]
        """
        return "\n".join([f"{ind}:{domino}" for ind, domino in enumerate(self.player_domino_deck, 1)])

    def add_dominoes_to_deck(self, dominoes: list[Domino]) -> None:
        for domino in dominoes:
            self.player_domino_deck.add_domino(domino)

    def select_dominoes(self, game_deck: Deck, limit: int) -> None:
        """Randomly selects the dominoes from the game.__all_dominoes deck"""
        for _ in range(limit):
            domino = random.choice(game_deck)
            self.player_domino_deck.add_domino(domino)
            game_deck.remove(domino)

    def make_move(self, domino: Domino, game_deck: Deck) -> None:
        if domino in self.player_domino_deck and game_deck.is_valid_move(domino):
            game_deck._append_to_game_deck(domino)
            self.player_domino_deck.remove(domino)
        else:
            print("Illegal move. Please try again")

    def take_domino_from_stock(self, all_dominoes: Deck):
        """If no available options anymore, the user can take a random domino from the game_deck.__all_dominoes"""
        if all_dominoes:
            domino = random.choice(all_dominoes)
            self.player_domino_deck.add_domino(domino)
            all_dominoes.remove(domino)
        else:
            print('Sorry, the Game stock is empty')


class Computer(Player):

    def __calculate_dominoes_rate_in_deck(self):
        if len(self.player_domino_deck) <= 1:   # no need to sort in case only 1 domino in the deck
            return
        numbers_in_deck = {}    # how many times each number met in deck of dominoes
        for domino in self.player_domino_deck:
            numbers_in_deck[domino.front] = numbers_in_deck.get(domino.front, 0) + 1
            numbers_in_deck[domino.bottom] = numbers_in_deck.get(domino.bottom, 0) + 1
        rated_dominoes = {}
        for domino in self.player_domino_deck:
            rated_dominoes[domino] = numbers_in_deck.get(domino.front, 0) + numbers_in_deck.get(domino.bottom, 0)
        rated_dominoes = dict(sorted(rated_dominoes.items(), key=lambda item: item[1], reverse=True))   # sort by values
        self.player_domino_deck = Deck()
        self.add_dominoes_to_deck(list(rated_dominoes.keys()))

    def make_move(self, game_deck: Deck, all_dominoes: Deck) -> None:
        self.__calculate_dominoes_rate_in_deck()
        for domino in self.player_domino_deck:
            if game_deck.is_valid_move(domino):
                game_deck._append_to_game_deck(domino)
                self.player_domino_deck.remove(domino)
                return                          # breaks the further iteration if the move is valid
        if all_dominoes:                        # only if the deck has any Dominoes - then pick up one from the deck
            self.take_domino_from_stock(all_dominoes)  # if no valid move, take one domino to the computers deck


class DominoGame:
    __double_dominoes = deck(Domino(0, 0), Domino(1, 1), Domino(2, 2), Domino(3, 3), Domino(4, 4), Domino(5, 5), Domino(6, 6))

    def __init__(self):
        self.__all_dominoes: Deck = Deck()
        self.game_deck: Deck = Deck()
        self.computer: Computer = Computer('Computer')
        self.__players = []     # TODO allow up to 4 players in one game

    def __str__(self):
        """Printing game state in the next format:
        ======================================================================

        Stock size: 14
        Computer pieces: 6

        [1, 2][2, 4][4, 1]...[5, 5][5, 6][6, 1]

        """
        result = "======================================================================\n"
        if len(self.game_deck) <= 6:
            return f"{result}Stock Size: {len(self.all_dominoes)}\nComputer pieces: " \
                   f"{len(self.computer.player_domino_deck)}\n\n{self.game_deck}\n\n"
        return f"{result}Stock Size: {len(self.all_dominoes)}\nComputer pieces: " \
               f"{len(self.computer.player_domino_deck)}\n\n{self.game_deck[1]}{self.game_deck[2]}{self.game_deck[3]}..." \
               f"{self.game_deck[-2]}{self.game_deck[-1]}{self.game_deck[0]}\n\n"

    @property
    def all_dominoes(self):
        return self.__all_dominoes

    @property
    def double_dominoes(self):
        return DominoGame.__double_dominoes

    @property
    def players(self):
        return self.__players

    def add_player(self, player: Player):
        if isinstance(player, Player):
            self.players.append(player)
        else:
            print(f'Error. The player should be an instance of <class Player>. Given: {type(player)}')

    def generate_game_deck(self) -> None:
        all_dominoes = combinations(range(0, 7), 2)
        for domino in all_dominoes:
            self.all_dominoes.add_domino(Domino(*domino))

    def check_winner(self, player: Player):
        if not player.player_domino_deck:
            print("The game is over. You won!")
            exit()
        elif not self.computer.player_domino_deck:
            print("The game is over. The computer won!")
            exit()
        elif not self.all_dominoes:
            is_steps_possible = self.__check_if_moves_possible([player.player_domino_deck, self.computer.player_domino_deck])
            if not is_steps_possible:
                print('The game is over. It\'s a draw!')
                print(f'Game deck: {self.game_deck}')   # print full game deck
                print(f'Computer\'s dominoes left: {self.computer.player_domino_deck}')
                exit()

    def __check_if_moves_possible(self, decks: list[Deck]) -> bool:
        for deck in decks:
            for domino in deck:
                if self.game_deck.is_valid_move(domino):
                    return True
        return False

    def start(self):
        for player in self.players:
            print(self)
            if isinstance(player, Computer):
                input('Status: Computer is about to make a move. Press Enter to continue...\n')
                self.computer.make_move(self.game_deck, self.all_dominoes)
            else:
                print("Your pieces:", player, sep='\n')
                print("Status: It's your turn to make a move. Enter your command.")
                user = read_user_input(player.player_domino_deck, self.game_deck)
                if user == 0:
                    player.take_domino_from_stock(self.all_dominoes)
                else:
                    domino = player.player_domino_deck[user]
                    player.make_move(domino, self.game_deck)
            self.check_winner(player)


def read_user_input(user_deck: Deck, game_deck: Deck) -> int:
    while True:
        try:
            user_choice = int(input('Make your move, player or enter "0" to take one domino from the stock if available: '))
            if user_choice == 0:
                return user_choice
            if 0 < user_choice <= len(user_deck):
                domino = user_deck[user_choice]
                if game_deck.is_valid_move(domino):
                    return user_choice
                raise IndexError    # if step is not valid - raise IndexError
            raise ValueError    # if input is invalid, or not in range of the user's deck length - raise ValueError
        except ValueError:
            print("Invalid input. Please try again.")
        except IndexError:
            print("Illegal move. Please try again.")


def deck(*args) -> Deck:
    deck_ = Deck()
    for arg in args:
        deck_.add_domino(arg)
    return deck_


def main():
    game = DominoGame()
    game.generate_game_deck()
    player = Player('Player')
    name = random.choice([player.name, game.computer.name])
    domino = random.choice(game.double_dominoes)
    game.double_dominoes.remove(domino)
    game.add_player(player)
    game.add_player(game.computer)
    game.game_deck.add_domino(domino)
    game.all_dominoes + game.double_dominoes    # merge double dominoes with unique dominoes
    if name == 'Player':
        player.select_dominoes(game.all_dominoes, 6)
        game.computer.select_dominoes(game.all_dominoes, 7)
    else:
        game.computer.select_dominoes(game.all_dominoes, 6)
        player.select_dominoes(game.all_dominoes, 7)
    # sort players by the Deck length. Players with longer deck are first
    game.players.sort(key=lambda play: len(play.player_domino_deck), reverse=True)
    while True:
        game.start()


if __name__ == "__main__":
    main()
