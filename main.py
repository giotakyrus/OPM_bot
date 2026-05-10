import discord
from discord import app_commands, ui
import random
import asyncio
from datetime import datetime

import os
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Système de données simple (en mémoire)
users_data = {}  # Sauvegarde temporaire

# ====================== SYSTÈME PROFIL & INVENTAIRE ======================
class Player:
    def __init__(self):
        self.xp = 0
        self.level = 1
        self.coins = 50
        self.rank = "C-Class"
        self.inventory = ["Casual Outfit"]

def get_player(user_id):
    if user_id not in users_data:
        users_data[user_id] = Player()
    return users_data[user_id]

@tree.command(name="profil", description="Voir ton profil de héros")
async def profil(interaction: discord.Interaction):
    player = get_player(interaction.user.id)
    embed = discord.Embed(title=f"Profil de {interaction.user.name}", color=0xff0000)
    embed.add_field(name="Rang Héros", value=player.rank, inline=True)
    embed.add_field(name="Niveau", value=player.level, inline=True)
    embed.add_field(name="XP", value=f"{player.xp}/100", inline=True)
    embed.add_field(name="Pièces", value=f"{player.coins} 🪙", inline=True)
    embed.add_field(name="Inventaire", value="\n".join(player.inventory), inline=False)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed)


@tree.command(name="daily", description="Récompense quotidienne")
async def daily(interaction: discord.Interaction):
    player = get_player(interaction.user.id)
    player.coins += 100
    player.xp += 20
    await interaction.response.send_message(f"✅ **Récompense quotidienne récupérée !**\n+100 🪙 | +20 XP", ephemeral=True)


# ====================== TIC TAC TOE ======================
class TicTacToeButton(ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(label=" ", style=discord.ButtonStyle.gray, row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        game = self.view
        if game.board[self.y][self.x] != " " or game.current_player != interaction.user:
            return await interaction.response.defer()

        game.board[self.y][self.x] = game.player_symbol[interaction.user]
        
        # Vérification victoire
        if game.check_winner(game.player_symbol[interaction.user]):
            await interaction.response.edit_message(content=f"🎉 {interaction.user.mention} a gagné !", view=None)
            game.stop()
            return

        # Match nul
        if all(cell != " " for row in game.board for cell in row):
            await interaction.response.edit_message(content="🤝 Match nul !", view=None)
            game.stop()
            return

        # Changement de joueur
        game.current_player = game.player2 if game.current_player == game.player1 else game.player1
        await interaction.response.edit_message(view=game)


class TicTacToeView(ui.View):
    def __init__(self, player1, player2):
        super().__init__(timeout=300)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.player_symbol = {player1: "❌", player2: "⭕"}
        self.board = [[" " for _ in range(3)] for _ in range(3)]

        for y in range(3):
            for x in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_winner(self, symbol):
        # Lignes, colonnes, diagonales
        for i in range(3):
            if all(self.board[i][j] == symbol for j in range(3)) or all(self.board[j][i] == symbol for j in range(3)):
                return True
        if all(self.board[i][i] == symbol for i in range(3)) or all(self.board[i][2-i] == symbol for i in range(3)):
            return True
        return False


@tree.command(name="morpion", description="Joue au Morpion contre un autre joueur")
@app_commands.describe(adversaire="Mentionne ton adversaire")
async def morpion(interaction: discord.Interaction, adversaire: discord.Member):
    if adversaire == interaction.user:
        return await interaction.response.send_message("❌ Tu ne peux pas jouer contre toi-même !", ephemeral=True)
    if adversaire.bot:
        return await interaction.response.send_message("❌ Tu ne peux pas jouer contre un bot !", ephemeral=True)

    embed = discord.Embed(
        title="🎮 Morpion - One Punch Man Edition",
        description=f"{interaction.user.mention} (❌) VS {adversaire.mention} (⭕)\n\n{interaction.user.mention} commence !",
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed, view=TicTacToeView(interaction.user, adversaire))


# ====================== COMMANDES ONE PUNCH MAN ======================
@tree.command(name="saitama", description="Invocation de Saitama")
async def saitama(interaction: discord.Interaction):
    phrases = ["Je suis un héros pour le fun.", "Un coup suffit.", "Je m'ennuie..."]
    embed = discord.Embed(title="💪 Saitama", description=random.choice(phrases), color=0xff0000)
    embed.set_image(url="https://i.imgur.com/8Q5z2fJ.jpg")
    await interaction.response.send_message(embed=embed)


@tree.command(name="combat", description="Saitama combat un monstre")
async def combat(interaction: discord.Interaction):
    monstres = ["Crabe Écrasé 🦀", "Deep Sea King 👑", "Boros 🌌", "Garou 🐺", "Vaccine Man 🟢"]
    monstre = random.choice(monstres)
    
    embed = discord.Embed(title=f"⚔️ Combat contre {monstre}", description="Saitama se prépare...", color=0xff0000)
    await interaction.response.send_message(embed=embed)
    
    await asyncio.sleep(2)
    await interaction.followup.send("💥 **Serious Punch !** Le monstre est vaincu en un coup.")


@tree.command(name="ping", description="Latence du bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Bleu ! `{round(bot.latency*1000)}ms`")


@bot.event
async def on_ready():
    await tree.sync()
    print(f"✅ {bot.user} est connecté ! One Punch Man Bot Prêt 💪")

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
