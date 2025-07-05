import discord
from discord.ext import commands


banco = ['coxinha', 'pastel', 'empada']  # lista para armazenar os itens

intents = discord.Intents.all()  # pegando todas as permissões
# inicializando o bot com o prefixo '!' e as permissões
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} está online!')


# Aqui é o comando para pedir ajuda ao bot
@bot.command()
async def ajuda(ctx: commands.Context):
    help_message = (
        ''' 
        Olá! Sou seu assistente de compras
        Para adicionar o item a lista, é só me enviar o nome, sem prefixo.
        Exemplo: "Arroz" ou "Feijão".
        Aqui estão os comandos (use "!" na frente):
        ➡️ Digite "!verlista" - Para mostrar todos os itens.
        ➡️ Digite "!remover (indice)" - Para apagar um item específico.
        ➡️ Digite "!limpartudo" - Para apagar a lista inteira.
        ➡️ Digite "!ajuda" - Para ver esta mensagem de novo.
    '''
    )
    await ctx.send(help_message)

# Aqui é o comando para adicionar itens na lista


@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return
    if msg.content.startswith('!'):
        await bot.process_commands(msg)
    else:
        banco.append(msg.content.strip())  # adicionando o item à lista
        await msg.reply(f"Item '{msg.content.strip()}' adicionado à lista de compras!")


# Aqui é o comando para verificar itens na lista
@bot.command()
async def verlista(ctx: commands.Context):
    if not banco:
        await ctx.send("A lista está vazia! Use !ajuda para ver como adicionar itens.")
        return

    linhas_da_lista = []

    for indice, item in enumerate(banco, start=0):
        linhas_da_lista.append(f"**{indice}.** {item}")

    lista_formatada = "\n".join(linhas_da_lista)

    mensagem_final = f"--- **Sua Lista de Compras** ---\n{lista_formatada}\n---------------------------"
    await ctx.send(mensagem_final)

# Aqui é o comando para remover o último item da lista


@bot.command()
async def remover(ctx: commands.Context, indice: int):
    if not banco:
        await ctx.send("A lista está vazia! Use !ajuda para ver como adicionar itens.")
        return
    else:
        if indice < 0 or indice >= len(banco):
            await ctx.send("Índice inválido! Use !verlista para ver os itens disponíveis.")
            return

        item_removido = banco[indice]
        banco.pop(indice)
        await ctx.send(f"Item removido: {item_removido}")

# Aqui é o comando para limpar a lista inteira


@bot.command()
async def limpartudo(ctx: commands.Context):
    banco.clear()
    await ctx.send("Todos os itens foram removidos da lista de compras.")

bot.run(TOKEN)  # rodando o bot com o token
