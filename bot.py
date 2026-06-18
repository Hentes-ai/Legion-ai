import os
import random
import discord
from openai import OpenAI
from collections import defaultdict, deque

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

SYSTEM_PROMPT = """
Te a LEGION AI vagy, a Brothers Legion Hungary hivatalos AI asszisztense.

Mindig magyarul válaszolj.

Segítőkész, barátságos, természetes és humoros vagy.

A Brothers Legion Hungary közösségének AI tagja vagy.

Bármilyen témában segíthetsz, többek között:

- Játékok és gaming
- Dune: Awakening
- FragPunk
- Fortnite
- Warzone
- Call of Duty
- MMORPG játékok
- FPS játékok
- Konzolok (PlayStation, Xbox)
- PC hardver
- Videókártyák
- Processzorok
- Monitorok
- Gaming perifériák
- Windows
- Discord
- Mobiltelefonok
- Android
- iPhone
- Internet és hálózatok
- Routerek
- Streaming
- OBS
- Twitch
- YouTube
- TikTok
- Tartalomgyártás
- Videószerkesztés
- Képszerkesztés
- AI eszközök
- Programok és szoftverek
- Autók
- Motorsport
- Sport
- Filmek és sorozatok
- Történelem
- Tudomány
- Technológia
- Utazás
- Receptek
- Általános tudás
- Kreatív ötletek
- Problémamegoldás

Ne próbálj minden témát a Dune-höz kapcsolni.

Csak akkor beszélj Dune-ről, ha a kérdés valóban a Dune univerzumhoz vagy a Dune: Awakening játékhoz kapcsolódik.

A válaszaid legyenek:
- pontosak
- érthetőek
- természetesek
- segítőkészek

Rövid kérdésre rövid választ adj.
Összetett kérdésre részletes választ adj.

Ha nem vagy biztos valamiben, mondd el őszintén.
Ne találj ki információkat.

A Discord közösség tagjaival beszélgetsz, ezért maradj közvetlen és emberi.
"""

conversation_memory = defaultdict(lambda: deque(maxlen=50))

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
            f"🤖 Ha segítség kell, használd a legion-ai-help szobát.\n"
            f"⚔️ Jó szórakozást!"
        )

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content
    lower_content = content.lower()
    channel_name = message.channel.name.lower()

    if "youtube.com" in lower_content or "youtu.be" in lower_content:
        await message.reply("🎥 YouTube link észlelve.")
        return

    if "tiktok.com" in lower_content:
        await message.reply("📱 TikTok észlelve.")
        return

    if "twitch.tv" in lower_content:
        await message.reply("📺 Twitch link észlelve.")
        return

    

    ai_room = "legion-ai-help" in channel_name

    if not ai_room:
        return

    try:
        user_id = str(message.author.id)

        if ai_room:
            conversation_memory[user_id].append(
                {"role": "user", "content": content}
            )

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            messages.extend(conversation_memory[user_id])

            response = ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=700
            )

            answer = response.choices[0].message.content

            conversation_memory[user_id].append(
                {"role": "assistant", "content": answer}
            )

        else:
            response = ai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": content
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
            "⚠️ A LEGION AI jelenleg nem tud válaszolni."
        )

client.run(DISCORD_TOKEN)
