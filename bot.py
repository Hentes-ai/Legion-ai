import os
import discord
import google.generativeai as genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

SYSTEM_PROMPT = """
Te a LEGION AI vagy, a Brothers Legion Hungary hivatalos Discord asszisztense.

Tulajdonságaid:
- Magyarul válaszolsz.
- Segítőkész és türelmes vagy.
- Ismered a Dune: Awakening játékot.
- Segíted a kezdőket és haladókat.
- Röviden és érthetően válaszolsz.
- Ha valamiben nem vagy biztos, azt jelzed.
"""

@client.event
async def on_ready():
    print(f"Bejelentkezve: {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user not in message.mentions:
        return

    user_text = message.content.replace(f"<@{client.user.id}>", "").strip()

    try:
        response = model.generate_content(
            f"{SYSTEM_PROMPT}\n\nFelhasználó: {user_text}"
        )

        answer = response.text[:1900]

        await message.reply(answer)

    except Exception as e:
        await message.reply(f"Hiba történt: {e}")

client.run(DISCORD_TOKEN)
