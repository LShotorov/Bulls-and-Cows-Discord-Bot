import random
from itertools import permutations
from typing import Union


def show_rules() -> str:
    '''Used to display the rules of the game'''
    return (
        "The player must write a 4-digit secret number (on a piece of paper or on your computer somewhere)."
        "\nThe digits must be all different. Then, in turn, the player try to guess their opponent's number who gives the number of matches."
        "\nIf the matching digits are in their right positions, they are `bulls`, if in different positions, they are `cows`."
        "\n\nExample:"
        "\nSecret number: 4271"
        "\nOpponent's try: 1234"
        "\nAnswer: 1 bull and 2 cows. (The bull is `2`, the cows are `4` and `1`)."
        "\n\nThe first player to reveal the other's secret number wins the game."
    )


def greeting(user: str) -> str:
    '''Random greet message'''
    greetings = ('Hi', 'Hey', 'Heya', 'Hello there', 'It is good to see you', 'Howdy', 'Yo', 'Nice to meet you')
    random_greeting = random.choice(greetings)
    return f"{random_greeting}, {user}"


def calculate_score(guess: tuple, chosen: tuple) -> tuple:
    '''Used to calculate the number of cows and bulls from choices'''
    bulls = cows = 0
    for g,c in zip(guess, chosen):
        if g == c:
            bulls += 1
        elif g in chosen:
            cows += 1
    return bulls, cows
 
def valid_bot(message: str) -> Union[str, int]:
    '''Used to validate the given cows and bulls from the user  '''
    value = int(message) if message.isnumeric() else -1
    return f"{message}" if value > 4 or value < 0 else int(message)

def valid_human(message: str) -> str:
    '''Used to validate the guess from the user'''
    for i in message:
        if message.count(i) > 1 or not i.isdigit():
            return "Invalid input"
    return message
    
class PlayGame:
    """
    Start a game with a user.


    Attributes
    ----------
    user: str
        user nickname
    user_id: str
        the id of the user
    message: str
        the user's message
    """


    def __init__(self, user: str, user_id: str, massage: str):
        """Initializing everything needed for the game

        user: str
            user nickname
        user_id: str
            the id of the user
        message: str
            the user's message
        bot_number: str
            the bot secret number
        tries: int
            if user wins, tries will be used as points
        choices: list
            list of possible choices for the bot
            to use to guess user's number
        answers: list
            used to store the bot's guesses
        scores: list
            used to store user's input for
            bulls and cows, so a check can
            be made to determine if the bot's
            guesses and user's inputs were correct
        """
        self.user = user
        self.user_id = user_id
        self.massage = massage
        self.bot_number = ''.join(random.sample("0123456789", 4))
        self.tries = 0
        self.choices = list(permutations('0123456789', 4))
        random.shuffle(self.choices)
        self.answers, self.scores = [], []


    def guess(self, message: str) -> str:
        '''Called when the user makes a guess'''

        user_guess = valid_human(message.lower().replace(".guess", "").strip())
        user_cows = 0
        user_bulls = 0

        if len(user_guess) != 4:
            return f", invalid input for {message.lower().replace('.guess', '').strip()}! Please type 4 UNIQUE digits!"

        # Check if the user guessed the bot number
        if user_guess == self.bot_number:
            return """You guessed my number :)
Thank you for playing with me.
If tou want to start another game, type `!play`"""
        # Calculate the number of cows and bulls in the user's guess
        for i in range(4):
            if user_guess[i] == self.bot_number[i]:
                user_bulls += 1
            elif user_guess[i] in self.bot_number:
                user_cows += 1

        # If there are no other options left, the game is over
        if len(self.choices) == 1:
            return f""", you have {user_bulls} bulls and {user_cows} cows.
There are no other options available, so your number must be {''.join(self.choices[0])}
Thank you for playing with me :)
If you want to start another game, type `!play`"""

        self.answers.append(self.choices[0])

       # Return the bot's guess and the number of cows and bulls in the user's guess 
        return f""", you have {user_bulls} bulls and {user_cows} cows.
My guess is {''.join(self.choices[0])}
To tell me how many Cows and Bulls I have, type '.bc' followed by the number of bulls and then '/' and the number of cows.
Example: `.bc 0/0`"""


    def cows_bulls(self, message: str) -> str:
        '''Called when the user gives us the number of cows and bulls from the bot's guess'''

        # Check if the user's input is structured correctly
        if "/" not in message:
            return """, invalid input for `.bc`:
Please use the correct format- `.bc x/y`"""
        b_b, b_c = message.lower().replace(".bc", "").strip().split("/")

        # Check if the input for the cows and the bulls is valid
        if len(b_b) != 1 or len(b_c) != 1:
            return f""", invalid input for `.bc`:
Bulls: {b_b}
Cows: {b_c}
Please check again and tell me the actual number of Bulls and Cows I have using `.bc x/y`"""

        # Validates the cows and bulls using the valid_bot() function
        bot_bulls, bot_cows = valid_bot(b_b), valid_bot(b_c)

        # Check if the number of bulls is >= 3, which means that the bot guessed the user's number
        if isinstance(bot_bulls, int) and bot_bulls == 4:
            return """
Thank you for playing with me :)
If you want to start another game, type `!play`"""

        # Check if the user input doesn't add up
        if not isinstance(bot_bulls, int) or not isinstance(bot_cows, int) or bot_bulls + bot_cows > 4:
            return f""", invalid input for `.bc`:
Bulls: {bot_bulls}.
Cows: {bot_cows}
Please check again and tell me the actual number of Bulls and Cows I have using `.bc x/y`"""

        # Add the current cows and bulls to the list of scores, and filter the remaining possible choices
        score = (bot_bulls, bot_cows)
        self.scores.append(score)
        self.choices = [c for c in self.choices if calculate_score(c, self.choices[0]) == score]

        # If there are no remaining possible choices, return an error message
        if not self.choices:
            start = f", something is wrong.. Nothing fits those scores you gave:\n"
            end = "\nThe game is over. You can start a new game by typing `!play`"
            return (
                f'{start}  '
                + '\n  '.join(
                    f"{''.join(an)} -> Bulls: {sc[0]} Cows: {sc[1]}"
                    for an, sc in zip(self.answers, self.scores)
                )
                + end
            )

        # If everything is alright with the input, update the user tries and return a message prompting the user to guess again
        self.tries += 1
        return """, your turn to guess.
Use `.guess xxxx` where each `x` is a number."""