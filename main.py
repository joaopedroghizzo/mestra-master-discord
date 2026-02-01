import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# ======================
# MEMÓRIA DA MESA
# ======================
mesa_ativa = False
fichas = {}
equipes = {}
viloes = {}
npcs = []

CANAL_MESA_NOME = "mesa-rpg"


@client.event
async def on_ready():
    print(f"🟢 Mestre conectado como {client.user}")


def canal_valido(message):
    return message.channel.name == CANAL_MESA_NOME


@client.event
async def on_message(message):
    global mesa_ativa

    if message.author.bot:
        return

    if not canal_valido(message):
        return

    conteudo = message.content.strip()

    # ======================
    # INICIAR MESA
    # ======================
    if conteudo.lower() == "!iniciar":
        mesa_ativa = False
        fichas.clear()
        equipes.clear()
        viloes.clear()
        npcs.clear()

        await message.channel.send(
            "**🜂 MESA PREPARADA 🜂**\n"
            "Este canal agora segue apenas narrativa.\n\n"
            "**Comandos iniciais:**\n"
            "`!ficha` – Enviar ficha do personagem\n"
            "`!equipe` – Definir equipe / liga\n"
            "`!viloes` – Registrar vilões permitidos\n"
            "`!começar` – Iniciar a história\n\n"
            "_O mundo age mesmo quando vocês não._"
        )
        return

    # ======================
    # FICHA DO PERSONAGEM
    # ======================
    if conteudo.lower().startswith("!ficha"):
        await message.channel.send(
            "**📄 FICHA DO PERSONAGEM**\n"
            "Envie no formato:\n\n"
            "**Nome:**\n"
            "**Identidade:**\n"
            "**Poderes:**\n"
            "**Fraquezas:**\n"
            "**Cargo / Função:**\n"
            "**Resumo narrativo:**"
        )
        return

    if mesa_ativa is False and "Nome:" in conteudo and "Poderes:" in conteudo:
        fichas[message.author.id] = conteudo
        await message.channel.send("✅ Ficha registrada.")
        return

    # ======================
    # EQUIPE
    # ======================
    if conteudo.lower().startswith("!equipe"):
        await message.channel.send(
            "**🛡️ EQUIPE / LIGA**\n"
            "Envie:\n"
            "- Nome da equipe\n"
            "- Base\n"
            "- Membros conhecidos"
        )
        return

    if mesa_ativa is False and "Base:" in conteudo and "Membros:" in conteudo:
        equipes["principal"] = conteudo
        await message.channel.send("✅ Equipe registrada.")
        return

    # ======================
    # VILÕES
    # ======================
    if conteudo.lower().startswith("!viloes"):
        await message.channel.send(
            "**🩸 VILÕES PERMITIDOS**\n"
            "Envie a lista.\n"
            "O Mestre NÃO criará vilões fora dela."
        )
        return

    if mesa_ativa is False and conteudo.startswith("-"):
        viloes[len(viloes) + 1] = conteudo
        await message.channel.send("☠️ Vilão registrado.")
        return

    # ======================
    # COMEÇAR HISTÓRIA
    # ======================
    if conteudo.lower() == "!começar":
        if not fichas:
            await message.channel.send("⚠️ Nenhuma ficha registrada.")
            return

        mesa_ativa = True

        await message.channel.send(
            "**🎬 A HISTÓRIA COMEÇA**\n\n"
            "O mundo já estava em movimento antes de vocês chegarem.\n"
            "A primeira decisão não será anunciada.\n"
            "Ela já está acontecendo.\n\n"
            "_Mestre aguarda ações._"
        )
        return

    # ======================
    # NARRAÇÃO LIVRE
    # ======================
    if mesa_ativa:
        await message.channel.send(
            f"📖 **O mundo reage à ação de {message.author.display_name}.**\n"
            "Nada é ignorado. Nada é gratuito.\n"
            "_Consequências estão em curso…_"
        )


client.run(os.getenv("DISCORD_TOKEN"))
