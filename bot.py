import os
import discord
from openai import OpenAI

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

SYSTEM_PROMPT = """
Te a LEGION AI vagy, a Brothers Legion Hungary hivatalos Discord asszisztense.

Szabályok:
- Mindig magyarul válaszolj.
- Röviden és érthetően válaszolj.
- Ismered a Dune: Awakening játékot.
- Segítőkész vagy.
- Ne mutatkozz be minden válaszban.
- Ha nem tudsz valamit biztosan, jelezd.
- Barátságos, laza hangnemben kommunikálj.
"""

@client.event
async def on_ready():
    print(f"Bejelentkezve: {client.user}")

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="betoppanó")

    if channel:
        await channel.send(
            f"👋 Üdv a Brothers Legion Hungary szerverén, {member.mention}!\n\n"
            f"🏜️ Nézz körül a szerveren és ugorj be a dune-chat csatornába!\n"
            f"⚔️ Jó szórakozást kíván a LEGION AI!"
        )

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()
    channel_name = message.channel.name.lower()

    # Hallgatós csatornák
    silent_channels = [
        "-klippek-képek",
        "dune-képek",
        "-live-értesítő",
        "csoport-szabályzat"
    ]

    if channel_name in silent_channels:
        return

    # YouTube
    if "youtube.com" in content or "youtu.be" in content:
        await message.reply("🎥 YouTube link észlelve.")
        return

    # TikTok
    if "tiktok.com" in content:
        await message.reply(
            "📱 TikTok észlelve. Reméljük nem Harkonnen propaganda. 😄"
        )
        return

    # Twitch
    if "twitch.tv" in content:
        await message.reply(
            "📺 Twitch stream link észlelve."
        )
        return

    # Facebook
    if "facebook.com" in content:
        await message.reply(
            "📘 Facebook link megosztva."
        )
        return

    # Vicces moderáció
    insults = [
        "te hülye vagy",
        "idióta",
        "barom",
        "hülye",
        "bunkó"
    ]

    if any(word in content for word in insults):
        await message.reply(
            "😄 A személyeskedés nem növeli a spice termelést."
        )
        return

    # Ha nincs megjelölve a bot, hallgat
    if client.user not in message.mentions:
        return

    try:
        response = ai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": message.content
                }
            ],
            max_tokens=300
        )

        answer = response.choices[0].message.content

        await message.reply(answer[:1900])

    except Exception as e:
        print(f"HIBA: {e}")

        await message.reply(
            "⚠️ A LEGION AI jelenleg nem tud válaszolni. Próbáld újra később."
        )

client.run(DISCORD_TOKEN)
