import os
import discord
from google import genai

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client_ai = genai.Client(api_key=GEMINI_API_KEY)

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
            f"⚔️ Jó szórakozást kíván a LEGION AI!"
        )

@client.event
async def on_message(message):
    if message.author.bot:
        return

    channel_name = message.channel.name.lower()
    content = message.content.lower()

    # Hallgatós csatornák
    silent_channels = [
        "-klippek-képek",
        "dune-képek",
        "-live-értesítő",
        "csoport-szabályzat"
    ]

    if channel_name in silent_channels:
        return

    # Vicces moderáció
    if "te hülye vagy" in content:
        await message.reply(
            "😄 Lehet, de legalább nem homokféreg vagyok."
        )
        return

    # Dumaszobában csak említésre válaszol
    if channel_name == "-dumaszoba-":
        if client.user not in message.mentions:
            return

    # Dune chat kulcsszavak
    if channel_name == "dune-chat":
        dune_keywords = [
            "dune",
            "spice",
            "deep desert",
            "ornithopter",
            "atreides",
            "harkonnen",
            "pvp",
            "pve",
            "crafting",
            "base"
        ]

        if not any(word in content for word in dune_keywords):
            return

    try:
        response = client_ai.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nFelhasználó: {message.content}"
        )

        await message.reply(response.text[:1900])

    except Exception as e:
        print(f"HIBA: {e}")

        if "429" in str(e):
            await message.reply(
                "⚠️ A LEGION AI napi AI kerete jelenleg elfogyott. Próbáld újra később."
            )
        elif "503" in str(e):
            await message.reply(
                "⚠️ A LEGION AI jelenleg túlterhelt. Próbáld újra pár perc múlva."
            )
        else:
            await message.reply(
                "⚠️ Váratlan hiba történt. Próbáld újra később."
            )

client.run(DISCORD_TOKEN)
