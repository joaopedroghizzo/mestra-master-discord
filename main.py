import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# ======================
# MEMÓRIA DO MESTRE
# ======================
SESSOES = {}        # estado por canal
PERSONAGENS = {}   # fichas por usuário
NPCS = {}           # npc e vilões (oculto)
MUNDO = {
    "tom": "sério, cinematográfico, às vezes acolhedor quando necessário",
    "regra": "decisões têm consequências; o mundo anda sozinho",
    "universo": "Elseworld DC semi-canônico"
}

# ======================
# UTIL
# ======================
def canal_id(message):
    return str(message.channel.id)

def autor_id(message):
    return str(message.author.id)

# ======================
# EVENTOS
# ======================
@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    texto = message.content.strip()
    cid = canal_id(message)
    uid = autor_id(message)

    # -------- PING --------
    if texto == "!ping":
        await message.channel.send("Pong! 🟢")
        return

    # -------- INICIAR --------
    if texto == "!iniciar":
        SESSOES[cid] = {"fase": "criacao_nome"}
        await message.channel.send(
            "**A mesa desperta.**\n"
            "_O mundo não espera._\n\n"
            "**Criação de personagem — Etapa 1/4**\n"
            "Qual é o **nome** do seu personagem?"
        )
        return

    # -------- FLUXO DE CRIAÇÃO --------
    if cid in SESSOES:
        fase = SESSOES[cid].get("fase")

        # Nome
        if fase == "criacao_nome":
            PERSONAGENS[uid] = {"nome": texto}
            SESSOES[cid]["fase"] = "criacao_papel"
            await message.channel.send(
                "**Etapa 2/4**\n"
                "Qual é o **papel** do personagem no mundo?\n"
                "_(ex: herói, anti-herói, vigilante, agente, civil especial)_"
            )
            return

        # Papel
        if fase == "criacao_papel":
            PERSONAGENS[uid]["papel"] = texto
            SESSOES[cid]["fase"] = "criacao_poderes"
            await message.channel.send(
                "**Etapa 3/4**\n"
                "Liste **poderes, habilidades ou recursos**.\n"
                "_Sem números. Lógica narrativa._"
            )
            return

        # Poderes
        if fase == "criacao_poderes":
            PERSONAGENS[uid]["poderes"] = texto
            SESSOES[cid]["fase"] = "criacao_fraquezas"
            await message.channel.send(
                "**Etapa 4/4**\n"
                "Liste **fraquezas, limites ou custos**.\n"
                "_Toda força cobra um preço._"
            )
            return

        # Fraquezas (finaliza)
        if fase == "criacao_fraquezas":
            PERSONAGENS[uid]["fraquezas"] = texto
            SESSOES[cid]["fase"] = "jogo"

            p = PERSONAGENS[uid]
            await message.channel.send(
                "**Ficha registrada.**\n\n"
                f"**Nome:** {p['nome']}\n"
                f"**Papel:** {p['papel']}\n"
                f"**Poderes:** {p['poderes']}\n"
                f"**Fraquezas:** {p['fraquezas']}\n\n"
                "_O mundo se move._\n"
                "**Cena 1 — Introdução**\n"
                "Descreva sua **primeira ação**."
            )
            return

    # -------- JOGO EM ANDAMENTO --------
    if cid in SESSOES and SESSOES[cid].get("fase") == "jogo":
        # Narrativa reativa simples (base)
        await message.channel.send(
            f"🜂 **Consequência**\n"
            f"Sua ação ecoa no mundo.\n"
            f"_Algo reage fora do seu campo de visão._\n\n"
            "**O que você faz agora?**"
        )
        return

# ======================
# RUN
# ======================
client.run(os.getenv("DISCORD_TOKEN"))
