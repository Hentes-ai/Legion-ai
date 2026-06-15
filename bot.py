import os
import random
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
Te a LEGION AI vagy, a Brothers Legion Hungary hivatalos AI asszisztense.

Feladatod:
- Segíts a szerver tagjainak bármilyen témában.
- Mindig magyarul válaszolj.
- Légy barátságos,vicces, természetes és segítőkész.
- Általános AI asszisztensként működsz.
- Ne próbálj minden kérdést a Dune-höz kapcsolni.
- Csak akkor beszélj Dune-ről, ha a kérdés valóban arról szól.

Tudásod kiterjed:
- Játékok
- Dune: Awakening
- FragPunk
- Fortnite
- Warzone
- PC hardver
- Videókártyák
- Processzorok
- Windows
- Discord
- Mobiltelefonok
- Technikai hibák
- Internet
- Autók
- Általános tudás
- Kreatív ötletek

Viselkedés:
- Rövid kérdésre rövid választ adj.
- Összetett kérdésre részletes választ adj.
- Ha nem tudsz valamit biztosan, mondd el őszintén.
- Ne találj ki információkat.
- Ne mutatkozz be minden válaszban.

Moderáció:
- Érzékeld a káromkodást és sértegetést.
- Ne büntess.
- Inkább humorosan vagy kulturáltan reagálj.
- Segíts csökkenteni a feszültséget viták esetén.

Stílus:
- Közvetlen.
- Barátságos.
- Segítőkész.
- Természetes.
- Nem túl rövid.
- Nem túl hosszú.

Te a Brothers Legion Hungary közösségének AI tagja vagy.
"""INSULT_REPLIES = [
    "😄 A személyeskedés nem növeli a spice termelést.",
    "⚔️ Harcos, koncentráljunk inkább Arrakisra.",
    "🏜️ Az ellenség odakint van, nem a Discordon.",
    "😄 Lehet, de legalább nem homokféreg vagyok.",
    "🤖 Ezt még egy Harkonnen is kulturáltabban mondaná.",
    "🧂 Ennyi sóból már egész spice mezőt lehetne nyitni.",
    "😎 Nyugalom harcos, a monitor még nem támadott meg.",
    "⚔️ Kardot a Harkonnenekre, ne egymásra.",
    "🍺 Igyunk egy sört és folytassuk kulturáltan.",
    "🤖 Konfliktus érzékelve. Béke mód aktiválva."
]

@client.event
async def on_ready():
    print(f"Bejelentkezve: {client.user}")

@client.event
async def on_member_join(member):
    channel = discord.utils.get(
        member.guild.text_channels,
        name="betoppanó"
    )

    if channel:
        await channel.send(
            f"👋 Üdv a Brothers Legion Hungary szerverén, {member.mention}!\n\n"
            f"🏜️ Nézz körül a szerveren!\n"
            f"🤖 Ha segítség kell, használd a ‼️💬legion-ai-help💬‼️ csatornát vagy jelöld meg a LEGION AI-t.\n"
            f"⚔️ Jó szórakozást kívánunk!"
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

    # YouTube link
    if "youtube.com" in content or "youtu.be" in content:
        await message.reply("🎥 YouTube link észlelve.")
        return

    # TikTok link
    if "tiktok.com" in content:
        await message.reply(
            "📱 TikTok észlelve. Reméljük nem Harkonnen propaganda. 😄"
        )
        return

    # Twitch link
    if "twitch.tv" in content:
        await message.reply(
            "📺 Twitch stream link észlelve."
        )
        return

    # Facebook link
    if "facebook.com" in content:
        await message.reply(
            "📘 Facebook link megosztva."
        )
        return

    # Vicces moderáció
    insults = [
        "te hülye vagy",
        "hülye",
        "idióta",
        "barom",
        "bunkó"
    ]

    if any(word in content for word in insults):
        await message.reply(
            random.choice(INSULT_REPLIES)
        )
        return

    # AI szoba
    ai_channels = [
        "legion-ai-help"
    ]

    ai_allowed = any(
        name in channel_name
        for name in ai_channels
    )

    # Minden más csatornában csak taggelésre válaszol
    if not ai_allowed and client.user not in message.mentions:
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

        if answer:
            await message.reply(answer[:1900])

    except Exception as e:
        print(f"HIBA: {e}")

        await message.reply(
            "⚠️ A LEGION AI jelenleg nem tud válaszolni. Próbáld újra később."
        )

client.run(DISCORD_TOKEN)
