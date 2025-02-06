import os
import discord
import google.generativeai as genai
import requests
from io import BytesIO

# Configure the API key for the Google Generative AI service (Gemini)
genai.configure(api_key=os.environ["gemini_key"])
image = "ImageGPT"

# Get the Discord bot token from the environment variable
token = os.getenv("SECRET_KEY")
st = "act as a discord bot and respond to the following conversation in the most helpful way possible. You are a helpful assistant. response should be less than or equal to 2000 characters"

# Define the bot client class, inheriting from discord.Client
class MyClient(discord.Client):

    # Event triggered when the bot has successfully connected to Discord and is ready
    async def on_ready(self):
        print(f'Logged on as {self.user}!'
              )  # Prints a message with the bot's username in the terminal

    # Event triggered when a message is sent in any channel the bot can see
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}'
              )  # Logs the author and content of the message
        mentioned_users = [user.name for user in message.mentions]

        # Check if the message was not sent by the bot itself
        if self.user != message.author:

            # Respond to the message author with a greeting

            # If the bot is mentioned in the message, process the response
            if self.user in message.mentions:
                channel = message.channel  # Get the channel where the message was sent
                await message.channel.send(f'Hello {message.author.mention}!')
                try:
                    # Call the Gemini AI model to generate a response based on the message content
                    author = "you are responding to " + str(message.author)
                    model = genai.GenerativeModel("gemini-1.5-flash") #api call
                    response = model.generate_content(st + author + message.content)  # Generate content from the message

                    # Extract the response text and send it back to the Discord channel
                    message_to_send = response.text
                    print(f'response: {response}'
                          )  # Log the response from the AI
                    await channel.send(
                        message_to_send
                    )  # Send the AI's generated response back to the channel

                except Exception as e:
                    # If an error occurs, log it and send an error message to the channel
                    print(f"Error: {e}")
                    await channel.send(
                        "Oops, something went wrong when processing your request."
                    )
            #image start 
            
            if image in mentioned_users:
                channel = message.channel  # Get the channel where the message was sent
                await message.channel.send(f'Hello {message.author.mention}!')
                try:
                    url = "https://pollinations.ai/prompt/" + message.content
                    response = requests.get(url)

                    if response.status_code == 200:
                        # Convert the response content into a file-like object
                        image_data = BytesIO(response.content)
                        image_data.seek(0)

                        # Send the image file to the Discord channel
                        await channel.send(file=discord.File(image_data, 'generated_image.png'))
                    else:
                        await channel.send("Could not retrieve the image from the server.")

                except Exception as e:
                    # If an error occurs, log it and send an error message to the channel
                    print(f"Error: {e}")
                    await channel.send(
                        "Oops, something went wrong when processing your request."
                    )


# Set up Discord bot's intents, enabling tracking of message content
intents = discord.Intents.default()  # Default intents for the bot
intents.message_content = True  # Enable intent to track message content

# Initialize and run the Discord bot with the specified intents
client = MyClient(intents=intents)
client.run(token)  # Run the bot using the token from the environment variable