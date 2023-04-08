import discord
from dotenv import load_dotenv
import os
import gamelogic
load_dotenv()

# Empty dictionary to store the active games
games = {}

class MyClient(discord.Client):
    async def on_ready(self):
        print("Bot is active!")

    async def on_message(self, message):
        # Check if the message is in the channel named "bot"
        if message.channel.name != "bot":
            return
        # Ignore messages sent by the bot itself
        if message.author.id == self.user.id:
            return

        global games # access the global dictionary

        # Convert the message.content to lower case and get the user nickname, if any, or the user name
        message_content = message.content.lower()
        user_nick = message.author.nick if message.author.nick != None else message.author.name
        mention_user = message.author.mention 

        # If message starts with '.help', send help message
        if message_content.startswith('.help'):
            help_message = "Try typing one of these commands:\n" \
                            "`.hi` - Exchange greetings with me :)\n" \
                            "`.rules` - See the rules of the game.\n" \
                            "`!play` - You start a game with me."
            await message.channel.send(help_message)

        # If message starts with '.rules', send the rules of the game
        if message_content.startswith('.rules'):
            await message.channel.send(gamelogic.show_rules())
        
        # If message is a greeting, respond with a greeting
        if message_content in ('.hi', '.hey', '.heya', '.hello', '.helo'):
            await message.channel.send(f"{gamelogic.greeting(user_nick)}")

        # If message starts with '!play', start a new game
        if message_content.startswith('!play'):
            # If the user is already playing, send appropriate message
            if message.author.id in games:
                await message.channel.send(f"{mention_user}, you are already playing.\n" \
                                            "If you want to quit the current game, type `.quit`")

            else:
                # If the user is not already playing, start a new game and add to the 'games' dictionary
                games[message.author.id] = gamelogic.PlayGame(user_nick, message.author.id, message.content)
                await message.channel.send(f"{mention_user}, let's play bulls and cows!\n" \
                                            "To guess, type `.guess` followed by your 4-digit guess. Example: `.guess 1234`\n" \
                                            "To quit, type `.quit`")

        # If message starts with '.quit', stop the current game
        if message_content.startswith('.quit'):
            # If the user is playing, remove the current game from the 'games' dictionary and send appropriate message
            if message.author.id in games:
                del games[message.author.id]
                await message.channel.send(f"{mention_user} stopped the game." \
                                            "\nIf you want to play again, type `!play`")
            # If the user is not playing, send appropriate message
            else:
                await message.channel.send(f"{mention_user} you are not currently playing." \
                                            "\nIf you want to play, type `!play`")

        # If message starts with '.guess', check the guess against the bot_number
        if message_content.startswith('.guess'):
            # If the user is not playing, send appropriate message
            if message.author.id not in games:
                await message.channel.send(f"{mention_user}, you are not currently playing." \
                                            "\nIf you want to play, type `!play`")
            else:
                # If the user is playing, get the current game, and make guess with the user's input
                current_game = games[message.author.id]
                guess_message = current_game.guess(message.content)

                # If the game has ended, remove it from the 'games' dictionary
                if "!play" in guess_message:
                    del games[message.author.id]

                await message.channel.send(f"{mention_user}{guess_message}")

        if message_content.startswith('.bc'):
            # If the user is not playing, send appropriate message and 
            if message.author.id not in games:
                await message.channel.send(f"{mention_user} you are not currently playing." \
                                            "\nIf you want to play, type `!play`")
            else:
                # If the user is playing, get the current game and check the input
                current_game = games[message.author.id]
                cb_message = current_game.cows_bulls(message.content)

                # If the user has guessed correctly or the user inputs for cows and bulls doesn't add up,
                # remove the game from the dictionary
                if "!play" in cb_message:
                    del games[message.author.id]

                await message.channel.send(f"{mention_user}{cb_message}")





TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()
intents.message_content = True
client = MyClient(intents = intents)
client.run(TOKEN)