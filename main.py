import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from discord.ui import Button, View

load_dotenv()  # Carregar variáveis de ambiente do arquivo .env

TOKEN = os.getenv('DISCORD_TOKEN')  # Obter o token do bot do arquivo .env
print(TOKEN)

intents = discord.Intents.default()  # Definir os intents do bot
intents.message_content = True  # Permitir que o bot leia o conteúdo das mensagens
intents.members = True  # Permitir que o bot leia os membros do servidor

# Criar o bot com suporte a comandos slash
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sincronizar comandos de barra
        await self.tree.sync()

bot = MyBot()

# CONECTAR O BOT -------------------------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'Bot conectado com sucesso como: {bot.user}!')

# MENSAGEM DE BOAS VINDAS -------------------------------------------------------------------------------

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel:
        embed = discord.Embed(
            title='Bem-vindo ao servidor!',
            description=f'Olá {member.mention}, seja bem-vindo ao {guild.name}!',
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else bot.user.avatar.url)  # Definir a imagem do membro que entrou
        await guild.system_channel.send(embed=embed)  # Enviar a mensagem de boas-vindas no canal do servidor

# COMANDO DE PING -------------------------------------------------------------------------------

@bot.tree.command(name="ping", description="Verifica a latência do bot")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)  # Calcular a latência do bot
    await interaction.response.send_message(f'Pong! Latência: {latency}ms')

# COMANDO DE OLÁ -------------------------------------------------------------------------------

@bot.tree.command(name="hello", description="Diz olá para o usuário")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Olá, {interaction.user.mention}!')

# COMANDO SOBRE O BOT -------------------------------------------------------------------------------

@bot.tree.command(name="sobre", description="Informações sobre o bot")
async def sobre(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Sobre o nosso Bot',
        description='Este bot foi criado para aprendizado com programação.',
        color=discord.Color.purple()
    )
    embed.add_field(name='Comandos Disponíveis', value='/hello, /ping, /sobre', inline=False)
    embed.set_footer(text='Bot criado por Gabriel Tavarez')
    await interaction.response.send_message(embed=embed)

# COMANDO SOBRE PRODUTO -------------------------------------------------------------------------------

@bot.tree.command(name="produto1", description="Informações sobre o Produto 1")
async def produto1(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Produto 1',
        description='Compra meu curso de programação',
        color=discord.Color.purple()
    )
    embed.add_field(name='Valor', value='R$ 200', inline=False)
    embed.set_image(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS86zEPc3IezttxepVXdw-RgnJ_MCqOZL67RQ&s")
    embed.set_footer(text='Valor promocional')

    # Criar botão com link
    class Produto1View(View):
        @discord.ui.button(label='Comprar', style=discord.ButtonStyle.success)
        async def comprar_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message('Você clicou no botão!', ephemeral=True)

    # Criar a view e adicionar o botão
    view = Produto1View()

    # Enviar a mensagem com o embed e a view
    await interaction.response.send_message(embed=embed, view=view)

# COMANDO DE TICKET -------------------------------------------------------------------------------

@bot.tree.command(name="ticket", description="Cria um ticket de suporte")
async def ticket(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Criar ticket',
        description='Para criar um ticket, clique no botão abaixo:',
        color=discord.Color.purple()
    )
    embed.set_footer(text='Todos os direitos reservados à Gabriel Tavarez')
    embed.set_image(url="https://grandesnomesdapropaganda.com.br/wp-content/uploads/2017/08/Ticket.jpg")

    # Definir a classe TicketView corretamente
    class TicketView(discord.ui.View):
        @discord.ui.button(label='Criar Ticket', style=discord.ButtonStyle.primary)
        async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
            guild = interaction.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True),
            }

            # Criar o canal privado
            ticket_channel = await guild.create_text_channel(
                name=f'ticket-{interaction.user.name}',
                overwrites=overwrites,
                reason='Criando canal de ticket'
            )

            await ticket_channel.send(f'Olá {interaction.user.mention}, entraremos em contato em breve!')

            # Criar botão para fechar o canal
            async def close_ticket_callback(interaction: discord.Interaction):
                if interaction.channel == ticket_channel:
                    await interaction.channel.delete(reason='Ticket fechado pelo usuário')
                    await interaction.response.send_message('O ticket foi fechado!', ephemeral=True)

            # Criar o botão "Fechar Ticket"
            close_button = discord.ui.Button(label='Fechar Ticket', style=discord.ButtonStyle.danger)
            close_button.callback = close_ticket_callback

            # Adicionar o botão à view
            close_view = discord.ui.View()
            close_view.add_item(close_button)

            # Enviar a mensagem com o botão "Fechar Ticket"
            await ticket_channel.send('Use o botão abaixo para fechar o ticket.', view=close_view)
            await interaction.response.send_message('Seu ticket foi criado!', ephemeral=True)

    # Criar a view e enviar a mensagem com o botão "Criar Ticket"
    view = TicketView()
    await interaction.response.send_message(embed=embed, view=view)

# Rodar o bot
bot.run(TOKEN)

