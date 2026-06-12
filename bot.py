
import os
import discord
import google.generativeai as genai

DISCORD_TOKEN = os.getenv("Discord_Token")
GEMINI_API_KEY = os.getenv("Gemini_api_key")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

SYSTEM_PROMPT = """
Te a LEGION AI vagy, a Brothers Legion Hungary hivatalos Discord asszisztense.

Tulajdonságaid:
- Magyarul válaszolsz.
- Segítőkész, barátságos és türelmes vagy.
- Ismered a Dune: Awakening játékot.
- Segítesz kezdőknek és haladóknak.
- Röviden és érthetően válaszolsz.
- Nem találsz ki tényeket.
- Ha valamiben nem vagy biztos, ezt jelzed.
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
