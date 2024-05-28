import asyncio
import discord
import random

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Create a Discord client with intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as', client.user)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!rps'):
        await message.channel.send("Welcome to Rock, Paper, Scissors! React with your choice:")
        question_message = await message.channel.send("Rock 🪨, Paper 📄, or Scissors ✂️?")
        for emoji in ['🪨', '📄', '✂️']:
            await question_message.add_reaction(emoji)

        countdown_others = 5  # Timer countdown for others to join
        countdown_user = 30  # Timer countdown for user to make a choice
        countdown_message_others = await message.channel.send(f"Time left for others to join: {countdown_others} seconds")
        countdown_message_user = await message.channel.send(f"Time left for you to make a choice: {countdown_user} seconds")

        def check(reaction, user):
            return str(reaction.emoji) in ['🪨', '📄', '✂️'] and reaction.message.id == question_message.id

        try:
            while countdown_others > 0:
                await asyncio.sleep(1)  # Wait for 1 second
                countdown_others -= 1
                await countdown_message_others.edit(content=f"Time left for others to join: {countdown_others} seconds")

                reaction, user = await client.wait_for('reaction_add', timeout=1, check=check)
                player_choice = emoji_to_choice(reaction.emoji)
                computer_choice = random.choice(["rock", "paper", "scissors"])
                await message.channel.send(f"{user.name} has joined the game! React with your choice:")
                break  # Break the loop if someone reacts within the countdown
        except asyncio.TimeoutError:
            await message.channel.send("Time's up for other players to join.")
            pass

        try:
            while countdown_user > 0:
                await asyncio.sleep(1)  # Wait for 1 second
                countdown_user -= 1
                await countdown_message_user.edit(content=f"Time left for you to make a choice: {countdown_user} seconds")

                reaction, user = await client.wait_for('reaction_add', timeout=1, check=check)
                player_choice = emoji_to_choice(reaction.emoji)
                computer_choice = random.choice(["rock", "paper", "scissors"])
                await message.channel.send(f"{user.name} has made a choice!")
                break  # Break the loop if user reacts within the countdown
        except asyncio.TimeoutError:
            await message.channel.send("Time's up! You didn't make a choice.")
            pass

        if 'player_choice' in locals():
            winner = determine_winner(player_choice, computer_choice)
            await message.channel.send(f"Computer chooses: {computer_choice}\n{winner}")

            # Ask to play again with emoji reactions
            play_again_message = await message.channel.send("Do you want to play again?")
            await play_again_message.add_reaction('✅')  # Yes emoji
            await play_again_message.add_reaction('❌')  # No emoji

            def check_reaction(reaction, user):
                return user == message.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message.id == play_again_message.id

            try:
                reaction, _ = await client.wait_for('reaction_add', timeout=30, check=check_reaction)
                if str(reaction.emoji) == '✅':
                    await on_message(message)  # Start a new game
                else:
                    await message.channel.send("Thanks for playing!")
            except asyncio.TimeoutError:
                await message.channel.send("Timeout! Thanks for playing!")

async def emoji_to_choice(emoji):
    if emoji == '🪨':
        return 'rock'
    elif emoji == '📄':
        return 'paper'
    elif emoji == '✂️':
        return 'scissors'
    else:
        return None

def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "It's a tie!"
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "scissors" and computer_choice == "paper") or \
         (player_choice == "paper" and computer_choice == "rock"):
        return "You win!"
    else:
        return "Computer wins!"

# Run the bot with the provided token
client.run('Discord Token ID')
