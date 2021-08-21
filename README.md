# domino_game
Simple domino game with a command line interface

## Description
To play domino, you need a full domino set and at least two players. In this project, the game is played by you and the computer.

At the beginning of the game, each player is handed 7 random domino pieces. The rest are used as stock (the extra pieces).

To start the game, players determine the starting piece. The player with the highest domino or the highest double ([6,6] or [5,5] for example) will donate that domino as a starting piece for the game. After doing so, their opponent will start the game by going first. If no one has a double domino, the pieces are reshuffled and redistributed.

### Requirements
#### Stage 1
- [x] Generate a full domino set. Each domino is represented as a list of two numbers. A full domino set is a list of 28 unique dominoes.
- [x] Split the full domino set between the players and the stock by random. You should get three parts: Stock pieces (14 domino elements), Computer pieces (7 domino elements), and Player pieces (7 domino elements).
- [x] Determine the starting piece and the first player. Modify the parts accordingly. You should get four parts with domino pieces and one string indicating the player that goes first: either "player" or "computer"
If the starting piece cannot be determined (no one has a double domino), reshuffle, and redistribute the pieces (step 3).
- [x] Output all five variables.
#### Stage 2: The Interface
- [x] Print the header using seventy equal sign characters (=).
- [x] Print the number of dominoes remaining in the stock – Stock size: [number].
- [x] Print the number of dominoes the computer has – Computer pieces: [number].
- [x] Print the domino snake. At this stage, it consists of the only starting piece.
- [x] Print the player's pieces, Your pieces:, and then one piece per line, enumerated.
- [x] Print the status of the game:
If status = "computer", print "Status: Computer is about to make a move. Press Enter to continue..."
If status = "player", print "Status: It's your turn to make a move. Enter your command."
Note that both these statuses suppose that the next move will be made, but at this stage, the program should stop here. We will implement other statuses (like "win", "lose", and "draw") in the stages to come.
#### Stage 3: Taking Turns
Modify your Stage 2 code:

- [x] At the end of the game, print one of the following phrases:
* Status: The game is over. You won!
* Status: The game is over. The computer won!
* Status: The game is over. It's a draw!

- [x] Print only the first and the last three pieces of the domino snake separated by three dots if it exceeds six dominoes in length.

- [x] Add a game loop that will repeat the following steps until the game ends:

* Display the current playing field (stage 2).

* If it's a user's turn, prompt the user for a move and apply it. If the input is invalid (a not-integer or it exceeds limitations), request a new input with the following message: Invalid input. Please try again..

* If it's a computer's turn, prompt the user to press Enter, randomly generate a move, and apply it.

* Switch turns.

Keep in mind that at this stage we have no rules! Both the player and the computer can place their dominoes however they like.
#### Stage 4: Enforcing Rules
Add the following functionality to your code. When it's a player's turn, the program should:

- [x] Verify that the move entered by the player is legal (requirement #1).
If not, request a new input with the following message: Illegal move. Please try again..
- [x] Place dominoes with the correct orientation (requirement #2).
When it's a computer's turn, the program should:

- [x] Try random moves until it finds a legal one.
A set of possible moves ranges from -computer_size to computer_size (where the computer_size is the number of dominoes the computer still has). Skipping a turn (move 0) is always legal.
- [x] Place dominoes with the correct orientation.
#### Stage 5: The AI
The AI should use the following algorithm to calculate the score:
- [x] Count the number of 0's, 1's, 2's, etc., in your hand, and in the snake.
- [x] Each domino in your hand receives a score equal to the sum of appearances of each of its numbers.
The AI will now attempt to play the domino with the largest score, trying both the left and the right sides of the snake. If the rules prohibit this move, the AI will move down the score list and try another domino. The AI will skip the turn if it runs out of options.