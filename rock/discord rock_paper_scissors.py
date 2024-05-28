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
        await message.channel.send("Welcome to Rock, Paper, Scissors!")
        while True:
            player_choice = await get_player_choice(message.channel)
            if player_choice:
                computer_choice = random.choice(["rock", "paper", "scissors"])
                await message.channel.send(f"Computer chooses: {computer_choice}")
                winner = determine_winner(player_choice, computer_choice)
                await message.channel.send(winner)
                await message.channel.send("Do you want to play again? (yes/no)")
                try:
                    response = await client.wait_for('message', check=lambda m: m.channel == message.channel and m.author == message.author, timeout=30)
                    if response.content.lower() != 'yes':
                        await message.channel.send("Thanks for playing!")
                        break
                except asyncio.TimeoutError:
                    await message.channel.send("Timeout! Thanks for playing!")
                    break

async def get_player_choice(channel):
    await channel.send("Choose: rock, paper, or scissors?")
    try:
        player_message = await client.wait_for('message', check=lambda m: m.channel == channel, timeout=30)
        return player_message.content.lower()
    except asyncio.TimeoutError:
        await channel.send("Timeout! Please make your choice faster.")
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
client.run('Your Discord Bot Token')
