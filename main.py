import discord
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Armazenamento em memória (simples, depois dá pra evoluir)
players = {}
creating_character = {}

QUESTIONS = [
    "Qual é o **nome do personagem**?",
    "Esse personagem pertence a qual **universo / Elseworld**?",
    "Qual é o **cargo, função ou papel** dele no mundo?",
    "Quais são os **poderes ou habilidades principais**?",
    "Quais são as **fraquezas, limites ou custos**?",
    "Alguma **observação importante para o Mestre**? (segredos, conflitos internos, passado)"
]

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    user_id = str(message.author.id)
    content = message.content.strip()

    # COMANDO: iniciar criação
    if content.lower() == "!novo":
        creating_character[user_id] = {
            "step": 0,
            "data": {}
        }
        await message.channel.send(
            "🧠 **Criação de Personagem iniciada.**\n"
            "Responda às perguntas com calma.\n\n"
            f"{QUESTIONS[0]}"
        )
        return

    # PROCESSO DE CRIAÇÃO
    if user_id in creating_character:
        step = creating_character[user_id]["step"]
        creating_character[user_id]["data"][QUESTIONS[step]] = content
        creating_character[user_id]["step"] += 1

        if creating_character[user_id]["step"] < len(QUESTIONS):
            await message.channel.send(QUESTIONS[creating_character[user_id]["step"]])
        else:
            ficha = creating_character[user_id]["data"]
            players[user_id] = {
                "active": ficha["Qual é o **nome do personagem**?"],
                "ficha": ficha
            }
            del creating_character[user_id]

            resumo = (
                "✅ **Personagem criado com sucesso.**\n\n"
                f"**Nome:** {ficha[QUESTIONS[0]]}\n"
                f"**Universo:** {ficha[QUESTIONS[1]]}\n"
                f"**Cargo:** {ficha[QUESTIONS[2]]}\n"
                f"**Poderes:** {ficha[QUESTIONS[3]]}\n"
                f"**Fraquezas:** {ficha[QUESTIONS[4]]}\n\n"
                "🎭 Você já pode jogar.\n"
                "Descreva ações normalmente."
            )
            await message.channel.send(resumo)
        return

    # COMANDO: ver ficha resumida
    if content.lower() == "!ficha":
        if user_id not in players:
            await message.channel.send("❌ Nenhum personagem ativo. Use `!novo`.")
            return

        ficha = players[user_id]["ficha"]
        texto = (
            "📄 **Ficha do Personagem (Resumo)**\n\n"
            f"**Nome:** {ficha[QUESTIONS[0]]}\n"
            f"**Universo:** {ficha[QUESTIONS[1]]}\n"
            f"**Cargo:** {ficha[QUESTIONS[2]]}\n"
            f"**Poderes:** {ficha[QUESTIONS[3]]}\n"
            f"**Fraquezas:** {ficha[QUESTIONS[4]]}"
        )
        await message.channel.send(texto)
        return

    # COMANDO: narrativa livre (RP)
    if user_id in players:
        personagem = players[user_id]["active"]
        resposta = (
            f"🎙️ **Mestre:**\n"
            f"{personagem} executa sua ação.\n"
            "O ambiente reage, consequências começam a se formar...\n\n"
            "👉 Continue descrevendo o que faz."
        )
        await message.channel.send(resposta)

client.run(os.getenv("DISCORD_TOKEN"))
