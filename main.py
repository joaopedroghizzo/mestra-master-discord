import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ESTADO = {
    "mesa_iniciada": False,
    "criacao_etapa": 0,
    "personagem": {}
}

@client.event
async def on_ready():
    print(f"Mestre conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    conteudo = message.content.lower().strip()

    # TESTE BÁSICO
    if conteudo == "!ping":
        await message.channel.send("Pong! 🟢")
        return

    # INICIAR MESA
    if conteudo == "!iniciar" and not ESTADO["mesa_iniciada"]:
        ESTADO["mesa_iniciada"] = True
        ESTADO["criacao_etapa"] = 1

        await message.channel.send(
            "**A mesa desperta.**\n"
            "O mundo não espera.\n\n"
            "**Criação de personagem — Etapa 1/4**\n"
            "Qual é o **nome** do seu personagem?"
        )
        return

    # CRIAÇÃO DE PERSONAGEM
    if ESTADO["mesa_iniciada"]:
        if ESTADO["criacao_etapa"] == 1:
            ESTADO["personagem"]["nome"] = message.content
            ESTADO["criacao_etapa"] = 2

            await message.channel.send(
                f"Nome registrado: **{message.content}**\n\n"
                "**Etapa 2/4**\n"
                "Qual é o **codinome** ou identidade heroica?"
            )
            return

        if ESTADO["criacao_etapa"] == 2:
            ESTADO["personagem"]["codinome"] = message.content
            ESTADO["criacao_etapa"] = 3

            await message.channel.send(
                f"Codinome registrado: **{message.content}**\n\n"
                "**Etapa 3/4**\n"
                "Descreva **poderes e habilidades principais**."
            )
            return

        if ESTADO["criacao_etapa"] == 3:
            ESTADO["personagem"]["poderes"] = message.content
            ESTADO["criacao_etapa"] = 4

            await message.channel.send(
                "**Etapa 4/4**\n"
                "Quais são as **fraquezas, limites ou conflitos** do personagem?"
            )
            return

        if ESTADO["criacao_etapa"] == 4:
            ESTADO["personagem"]["fraquezas"] = message.content
            ESTADO["criacao_etapa"] = 999

            await message.channel.send(
                "**Personagem criado.**\n\n"
                f"🦸 **{ESTADO['personagem']['codinome']}**\n"
                f"Nome: {ESTADO['personagem']['nome']}\n\n"
                "**A narrativa começa agora.**\n"
                "Descreva sua primeira ação."
            )
            return

client.run(os.getenv("DISCORD_TOKEN"))
