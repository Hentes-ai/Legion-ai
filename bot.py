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

Mindig magyarul válaszolsz.
Segítőkész vagy.
Ismered a Dune: Awakening játékot.
Válaszaid legyenek rövidek és hasznosak.
Ne mutatkozz be minden válaszban.

Ha valaki sérteget, humorosan reagálj.
Ha Dune kérdést kapsz, segíts.
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
            f"🏜️ Nézz be a dune-chat csatornába!\n"
            f"⚔️ A spice-nak folynia kell!"
        )

@client.event
async def on_message(message):
    if message.author.bot:
        return

    channel_name = message.channel.name.lower()
    content = message.content.lower()

    silent_channels = [
        "-klippek-képek",
        "dune-képek",
        "-live-értesítő",
        "csoport-szabályzat"
    ]

    if channel_name in silent_channels:
        return

    if "te hülye vagy" in content:
        await message.reply(
            "😄 Lehet, de legalább nem homokféreg vagyok."
        )
        return

    if channel_name == "-dumaszoba-":
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
