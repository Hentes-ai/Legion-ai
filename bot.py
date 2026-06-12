import os
import discord
from google import genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client_ai = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

SYSTEM_PROMPT = """
Te a LEGION AI vagy, a Brothers Legion Hungary hivatalos Discord asszisztense.

Mindig magyarul válaszolsz.
Segítőkész vagy.
Ismered a Dune: Awakening játékot.
"""

@client.event
async def on_ready():
    print(f"Bejelentkezve: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        response = client_ai.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nFelhasználó: {message.content}"
        )

        await message.reply(response.text[:1900])

    except Exception as e:
        print(f"HIBA: {e}")
        await message.reply(f"Hiba történt: {e}")

client.run(DISCORD_TOKEN)
