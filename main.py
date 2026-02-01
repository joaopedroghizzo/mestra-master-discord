import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ===============================
# MEMÓRIA DO MESTRE (OCULTA)
# ===============================
players = {}        # dados narrativos dos jogadores
campaign = {        # estado da campanha
    "ativa": False,
    "mundo": "Elseworld DC",
    "tom": "Sério, cinematográfico, com consequências",
    "evento_atual": None
}

# ===============================
# UTILIDADES
# ===============================
def is_master(message):
    return message.author.guild_permissions.administrator

def get_player(user_id):
    return players.get(user_id)

# ===============================
# EVENTOS DO BOT
# ===============================
@client.event
async def on_ready():
    print(f"Mestre conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.strip()
    user_id = message.author.id

    # ===============================
    # COMANDOS DO MESTRE
    # ===============================
    if content.startswith("!iniciar") and is_master(message):
        campaign["ativa"] = True
        campaign["evento_atual"] = "Introdução"
        await message.channel.send(
            "**A narrativa começa.**\n"
            "Este mundo observa. Decisões terão peso.\n\n"
            "Jogadores: usem `!personagem` para criar ou trocar seu personagem."
        )
        return

    if content.startswith("!encerrar") and is_master(message):
        campaign["ativa"] = False
        await message.channel.send(
            "**A sessão é encerrada.**\n"
            "As consequências permanecem."
        )
        return

    # ===============================
    # CRIAÇÃO / TROCA DE PERSONAGEM
    # ===============================
    if content.startswith("!personagem"):
        players[user_id] = {
            "nome": None,
            "identidade": None,
            "cargo": None,
            "poderes": None,
            "fraquezas": None,
            "estado": "ativo",
            "segredos": []
        }
        await message.channel.send(
            f"{message.author.mention}\n"
            "**Criação de personagem iniciada.**\n"
            "Responda na ordem:\n"
            "1️⃣ Nome do personagem\n"
            "2️⃣ Identidade (herói, vilão, civil, agente, etc)\n"
            "3️⃣ Cargo/função no mundo\n"
            "4️⃣ Poderes (descrição narrativa)\n"
            "5️⃣ Fraquezas reais\n\n"
            "_Nada disso será público._"
        )
        return

    # ===============================
    # FLUXO DE RESPOSTAS DO JOGADOR
    # ===============================
    player = get_player(user_id)
    if player and campaign["ativa"]:
        if player["nome"] is None:
            player["nome"] = content
            await message.channel.send("✔️ Identidade registrada. Próximo: **Identidade**.")
            return

        if player["identidade"] is None:
            player["identidade"] = content
            await message.channel.send("✔️ Função entendida. Próximo: **Cargo/Função**.")
            return

        if player["cargo"] is None:
            player["cargo"] = content
            await message.channel.send("✔️ Registro aceito. Próximo: **Poderes**.")
            return

        if player["poderes"] is None:
            player["poderes"] = content
            await message.channel.send("✔️ Poderes analisados. Próximo: **Fraquezas**.")
            return

        if player["fraquezas"] is None:
            player["fraquezas"] = content
            await message.channel.send(
                "**Personagem concluído.**\n"
                "O mundo agora sabe que você existe.\n"
                "_Mas não o quanto isso vai custar._"
            )
            return

    # ===============================
    # NARRAÇÃO LIVRE (SEM DADOS)
    # ===============================
    if campaign["ativa"]:
        await message.channel.send(
            f"**O mundo reage à ação de {message.author.display_name}.**\n"
            "Nada acontece por acaso. Consequências estão em movimento."
        )

# ===============================
# INICIAR BOT
# ===============================
client.run(os.getenv("DISCORD_TOKEN"))
