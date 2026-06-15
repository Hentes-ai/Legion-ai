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

Bármilyen témában segíthetsz:
- játékok
- Dune: Awakening
- FragPunk
- Fortnite
- Warzone
- PC hardver
- Windows
- Discord
- mobiltelefonok
- internet
- autók
- technikai hibák
- általános tudás

Ne próbálj minden témát a Dune-höz kapcsolni.

Rövid kérdésre rövid választ adj.
Összetett kérdésre részletes választ adj.

Ha nem vagy biztos valamiben, mondd meg őszintén.
"""

INSULT_REPLIES = [
    "😄 A személyeskedés nem növeli a spice termelést.",
    "⚔️ Harcos, koncentráljunk inkább Arrakisra.",
    "🏜️ Az ellenség odakint van, nem a Discordon.",
    "😄 Lehet, de legalább nem homokféreg vagyok.",
    "🤖 Ezt még egy Harkonnen is kulturáltabban mondaná.",
    "🧂 Ennyi sóból már egész spice mezőt lehetne nyitni.",
    "😎 Nyugalom harcos, a monitor még nem támadott meg.",
    "🍺 Igyunk egy sört és folytassuk kulturáltan.",
    "🤖 Konfliktus érzékelve. Béke mód aktiválva."
]

conversation_memory = defaultdict(lambda: deque(maxlen=20))

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

    insults = [
        "hülye",
        "idióta",
        "barom",
        "bunkó",
        "fasz",
        "faszfej",
        "bazdmeg",
        "baszd meg",
        "geci",
        "kurva",
        "anyád",
        "gyökér",
        "nyomorék"
    ]

    if any(word in lower_content for word in insults):
        await message.reply(random.choice(INSULT_REPLIES))
        return

    ai_room = "legion-ai-help" in channel_name

    if not ai_room and client.user not in message.mentions:
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
