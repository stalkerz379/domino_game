import random


def generate():
    stock_pieces = []
    for num_1 in range(0, 7):
        for num_2 in range(0, 7):
            res = [num_1, num_2]
            if res[::-1] not in stock_pieces:
                stock_pieces.append(res)
    return stock_pieces


def computer_arr(stock_pieces):
    computer = []
    while len(computer) != 7:
        rand = random.choice(stock_pieces)
        if rand not in computer:
            computer.extend([rand])
            stock_pieces.remove(rand)
    return computer, stock_pieces


def player_arr(stock_pieces):
    player = []
    while len(player) != 7:
        rand = random.choice(stock_pieces)
        if rand not in player:
            player.extend([rand])
            stock_pieces.remove(rand)
    return player, stock_pieces


def maximum(arr):
    res = []
    for i in arr:
        summ = i[0] + i[1]
        res.append(summ)
    return res


def find_first_step(computer, player):
    c = []
    comp = maximum(computer)
    play = maximum(player)
    if max(comp) > max(play):
        max_ind = comp.index(max(comp))
        c = computer[max_ind]
        computer.remove(computer[max_ind])
    elif max(play) > max(comp):
        max_ind = play.index(max(play))
        c = player[max_ind]
        player.remove(player[max_ind])
    else:
        stock_pieces = generate()
        computer, stock_pieces = computer_arr(stock_pieces)
        player, stock_pieces = player_arr(stock_pieces)
        find_first_step(computer, player)
    return c


def who_make_step(computer, player):
    step = 0
    if len(computer) > len(player):
        step = 0
    elif len(computer) < len(player):
        step = 1
    return step


def game_session(game):
    if len(game) > 6:
        return (*game[0:3], '...', *game[-3:])
    else:
        return game


def boundaries(game):
    if len(game) > 1:
        left = game[0][0]
        right = game[-1][-1]
        return left, right
    else:
        left = game[0][0]
        right = game[0][-1]
        return left, right


def computer_move(computer, game, computer_length, number_of_stock_pieces, stock_pieces):
    left, right = boundaries(game)
    sum_of_subarray = computer_calculations(computer)
    no_possible_comp_steps = 0
    for j in sum_of_subarray.keys():
        a = int(j[0])
        b = int(j[1])
        i = [a, b]
        if i[0] == left:
            answer = i[::-1]
            game.insert(0, answer)
            computer.remove(i)
            computer_length -= 1
            return computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps
        elif i[1] == left:
            answer = i
            game.insert(0, answer)
            computer.remove(i)
            computer_length -= 1
            return computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps
        elif i[0] == right:
            answer = i
            game.extend([answer])
            computer.remove(i)
            computer_length -= 1
            return computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps
        elif i[1] == right:
            answer = i[::-1]
            game.extend([answer])
            computer.remove(i)
            computer_length -= 1
            return computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps
    if len(stock_pieces) > 0:
        rand = random.choice(stock_pieces)
        computer.extend([rand])
        stock_pieces.remove(rand)
        computer_length += 1
        number_of_stock_pieces -= 1
        return computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps
    elif len(stock_pieces) == 0:
        no_possible_comp_steps += 1
        return computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps
    return computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps


def computer_calculations(computer):
    count_numbers = {}
    sum_of_subarray = {}
    for num in computer:
        for el in num:
            if el not in count_numbers.keys():
                count_numbers.setdefault(el, 1)
            elif el in count_numbers.keys():
                count_numbers[el] += 1
    for el in computer:
        if el[0] in count_numbers.keys():
            val = el[0]
            val_1 = el[1]
            add = str(val), str(val_1)
            key = count_numbers[val] + count_numbers[val_1]
            sum_of_subarray.setdefault(add, key)
    return dict(sorted(sum_of_subarray.items(), key=lambda item: item[1], reverse=True))


def user_input(player):
    a = input()
    res = []
    for num in range(-len(player), len(player) + 1):
        res.append(str(num))
    if a not in res:
        print('Invalid input. Please try again.')
        a = user_input(player)
    else:
        return a
    return a


def user_interaction(game, player, number_of_stock_pieces, stock_pieces):       # logic of user game actions
    a = user_input(player)              # calling user_input function for validation of the input
    left, right = boundaries(game)      # calling boundaries function
    no_possible_steps = 0
    if int(a) > 0:
        user_step_choice = player[int(a) - 1]
        if user_step_choice[0] == right:
            game.extend([user_step_choice])
            player.remove(user_step_choice)
            return player, number_of_stock_pieces, stock_pieces, no_possible_steps
        elif user_step_choice[1] == right:
            game.extend([user_step_choice[::-1]])
            player.remove(user_step_choice)
            return player, number_of_stock_pieces, stock_pieces, no_possible_steps
        else:
            print("Illegal move. Please try again.")
            user_interaction(game, player, number_of_stock_pieces, stock_pieces)       # recursion if the user makes illegal move
    elif int(a) < 0:
        user_step_choice = player[abs(int(a)) - 1]
        if user_step_choice[0] == left:
            game.insert(0, user_step_choice[::-1])
            player.remove(user_step_choice)
            return player, number_of_stock_pieces, stock_pieces, no_possible_steps
        elif user_step_choice[1] == left:
            game.insert(0, user_step_choice)
            player.remove(user_step_choice)
            return player, number_of_stock_pieces, stock_pieces, no_possible_steps
        else:
            print("Illegal move. Please try again.")
            user_interaction(game, player, number_of_stock_pieces, stock_pieces)    # recursion if the user makes illegal move
    elif int(a) == 0:                                                               # taking a random domino from the stock
        if number_of_stock_pieces > 0:
            number_of_stock_pieces -= 1
            rand = random.choice(stock_pieces)
            player.extend([rand])
            stock_pieces.remove(rand)
        elif number_of_stock_pieces == 0:
            no_possible_steps += 1
            return player, number_of_stock_pieces, stock_pieces, no_possible_steps
        return player, number_of_stock_pieces, stock_pieces, no_possible_steps
    return player, number_of_stock_pieces, stock_pieces, no_possible_steps


def printing_results(game, computer, player, number_of_stock_pieces):
    print('=' * 70, sep='')
    print("Stock size:", number_of_stock_pieces)
    print("Computer pieces:", computer_length, '\n')
    print(*game_session(game), sep='')
    print()
    print("Your pieces:")
    for i in enumerate(player, 1):
        print(*i, sep=':')
    return ''

def check_game_result(game, computer, player, number_of_stock_pieces):            # validating game results
    if len(game) >= 8:
        left, right = boundaries(game)  # calling boundaries function
        times = 0                       # couting how many times a border was met
        for i in game:
            if left == i[0] or left == i[1]:
                times += 1
        if left == right and times >= 8:
            game_result(game, computer, player, number_of_stock_pieces)    # calling printing_results function
            return "Status: The game is over. It's a draw!", printing_results(game, computer, player, number_of_stock_pieces)
        else:
            return game_result(game, computer, player, number_of_stock_pieces)
    else:
        return printing_results(game, computer, player, number_of_stock_pieces)
    return printing_results(game, computer, player, number_of_stock_pieces)


def game_result(game, computer, player, number_of_stock_pieces):        # checks game results
    if len(player) < len(computer):
        print(printing_results(game, computer, player, number_of_stock_pieces))
        return "Status: The game is over. You won!"
    elif len(player) > len(computer):
        print(printing_results(game, computer, player, number_of_stock_pieces))
        return 'Status: The game is over. The computer won!'
    else:
        print(printing_results(game, computer, player, number_of_stock_pieces))
        return "Status: The game is over. It's a draw!"


stock_pieces = generate()     # all stock pieces that take a part in a game
computer, stock_pieces = computer_arr(stock_pieces)   # computer's dominoes
player, stock_pieces = player_arr(stock_pieces)     # player's dominoes
c = find_first_step(computer, player)     # removing max value for the first step
step = who_make_step(computer, player)      # determine who makes the first step
game = []   # array for the game session
game.extend([c])    # putting first element into the game session
number_of_stock_pieces = len(stock_pieces)      # counting if user used additional stock pieces
computer_length = len(computer)

printing_results(game, computer, player, number_of_stock_pieces)
while player and computer:                                                # game session
    if step == 0:
        a = input("Status: Computer is about to make a move. Press Enter to continue...\n")
        computer, computer_length, number_of_stock_pieces, stock_pieces, no_possible_comp_steps = computer_move(computer, game, computer_length, number_of_stock_pieces, stock_pieces)
        step = 1
        check_game_result(game, computer, player, number_of_stock_pieces)     # calling check_game_result function
        if no_possible_comp_steps == 1:
            break
    elif step == 1:
        print('Status: It\'s your turn to make a move. Enter your command.')
        player, number_of_stock_pieces, stock_pieces, no_possible_steps = user_interaction(game, player, number_of_stock_pieces, stock_pieces)
        step = 0
        check_game_result(game, computer, player, number_of_stock_pieces)     # calling check_game_result function
        if no_possible_steps == 1:
            break
print(check_game_result(game, computer, player, number_of_stock_pieces))
