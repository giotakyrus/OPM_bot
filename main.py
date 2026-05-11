import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import config
from utils.embeds import EmbedBuilder

load_dotenv()

# ========================= BOT SETUP =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# ========================= HELPER FUNCTIONS =========================

def load_players_data():
    """Charger les données des joueurs"""
    try:
        with open(config.PLAYERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_players_data(data):
    """Sauvegarder les données des joueurs"""
    try:
        os.makedirs(os.path.dirname(config.PLAYERS_FILE), exist_ok=True)
        with open(config.PLAYERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return False

def player_exists(user_id: int) -> bool:
    """Vérifier si un joueur existe"""
    data = load_players_data()
    return str(user_id) in data

def get_player_count() -> int:
    """Obtenir le nombre de joueurs"""
    return len(load_players_data())

# ========================= BOT EVENTS =========================

@bot.event
async def on_ready():
    """Appelé quand le bot est prêt"""
    print(f"✅ Bot connecté: {bot.user}")
    print(f"📊 Serveurs: {len(bot.guilds)}")
    
    # Syncer les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"🔄 {len(synced)} commandes synchronisées")
    except Exception as e:
        print(f"❌ Erreur sync: {e}")
    
    # Status personnalisé
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="des démons 👹 | /aide"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)
    print("🎮 Demon Slayer Bot chargé!")

# ========================= COMMANDES SLASH =========================

@bot.tree.command(name="profil", description="Voir ton profil")
async def profil(interaction: discord.Interaction):
    """Affiche le profil du joueur"""
    user_id = interaction.user.id
    
    if not player_exists(user_id):
        embed = discord.Embed(
            title="❌ Profil Non Trouvé",
            description="Tu n'as pas commencé le jeu!\nUtilise `/test_souffle` pour commencer",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    embed = discord.Embed(
        title=f"🗡️ Profil de {interaction.user.name}",
        color=0xFF0000
    )
    embed.add_field(name="Status", value="✅ Profil créé", inline=False)
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="aide", description="Afficher l'aide du jeu")
async def aide(interaction: discord.Interaction):
    """Affiche l'aide"""
    embed = discord.Embed(
        title="🎌 Demon Slayer - Aide",
        description="Bienvenue Pourfendeur de Démons!",
        color=0xFF0000
    )
    
    embed.add_field(
        name="🚀 Commencer",
        value="```/test_souffle```",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Commandes Disponibles",
        value="```/profil - Voir ton profil\n/aide - Cette aide\n/souffles - Lister les souffles\n/stats_bot - Statistiques du serveur```",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Admin",
        value="```/admin_user - Gérer les joueurs\n/admin_config - Config globale```",
        inline=False
    )
    
    embed.set_footer(text="Le jeu est en développement! 🚀")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="souffles", description="Voir la liste des souffles")
async def souffles(interaction: discord.Interaction):
    """Affiche la liste des souffles"""
    embed = discord.Embed(
        title="💨 Souffles Disponibles",
        description="Passe `/test_souffle` pour débloquer ton souffle!",
        color=0x1E90FF
    )
    
    for key, breathing in config.BREATHING_STYLES.items():
        emoji = breathing['emoji']
        name = breathing['name']
        techniques = breathing['technique_count']
        embed.add_field(
            name=f"{emoji} {name}",
            value=f"{techniques} mouvements",
            inline=True
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="stats_bot", description="Voir les statistiques")
async def stats_bot(interaction: discord.Interaction):
    """Affiche les stats globales"""
    total_players = get_player_count()
    
    embed = discord.Embed(
        title="📊 Statistiques Globales",
        color=0x00FF00
    )
    
    embed.add_field(name="👥 Joueurs", value=total_players, inline=True)
    embed.add_field(name="💨 Souffles", value=len(config.BREATHING_STYLES), inline=True)
    embed.add_field(name="🎯 Missions", value=config.TOTAL_MISSIONS, inline=True)
    embed.add_field(name="👹 Démons", value="43", inline=True)
    embed.add_field(name="🏆 Rangs", value="11", inline=True)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ========================= COMMANDES ADMIN =========================

@bot.tree.command(name="admin_user", description="[ADMIN] Gérer les joueurs")
@discord.app_commands.describe(
    action="view / give_xp / ban",
    user="Utilisateur cible",
    amount="Montant XP"
)
async def admin_user(
    interaction: discord.Interaction,
    action: str,
    user: discord.User,
    amount: int = 0
):
    """Gestion des joueurs (Admin)"""
    
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Permissions insuffisantes!", ephemeral=True)
    
    players_data = load_players_data()
    user_id = str(user.id)
    
    if action.lower() == "view":
        if user_id not in players_data:
            return await interaction.response.send_message(f"❌ {user.mention} n'a pas de profil!", ephemeral=True)
        
        player = players_data[user_id]
        embed = discord.Embed(title=f"👤 {user.name}", color=0xFF0000)
        embed.add_field(name="Level", value=player.get('level', 1))
        embed.add_field(name="XP", value=player.get('xp', 0))
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "give_xp":
        if user_id not in players_data:
            players_data[user_id] = {'level': 1, 'xp': 0}
        
        players_data[user_id]['xp'] = players_data[user_id].get('xp', 0) + amount
        save_players_data(players_data)
        
        embed = discord.Embed(title="✅ XP Donné", description=f"+{amount} XP pour {user.mention}", color=0x00FF00)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "ban":
        if user_id not in players_data:
            players_data[user_id] = {'level': 1, 'xp': 0}
        
        players_data[user_id]['banned'] = True
        save_players_data(players_data)
        
        embed = discord.Embed(title="🚫 Joueur Banni", description=f"{user.mention} a été banni!", color=0xFF0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="admin_config", description="[ADMIN] Config")
@discord.app_commands.describe(action="reload / stats")
async def admin_config(interaction: discord.Interaction, action: str):
    """Config globale (Admin)"""
    
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("❌ Permissions insuffisantes!", ephemeral=True)
    
    if action.lower() == "stats":
        embed = discord.Embed(title="📊 Stats Serveur", color=0x00FF00)
        embed.add_field(name="Joueurs", value=get_player_count())
        embed.add_field(name="Souffles", value=len(config.BREATHING_STYLES))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "reload":
        embed = discord.Embed(title="✅ Config Reloadée", color=0x00FF00)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# ========================= LANCER LE BOT =========================

def main():
    """Lancer le bot"""
    if not config.TOKEN:
        print("❌ ERREUR: TOKEN non configuré dans .env")
        print("Ajoute: TOKEN=ton_token_discord")
        return
    
    try:
        print(f"🚀 Démarrage {config.BOT_NAME} v{config.BOT_VERSION}")
        bot.run(config.TOKEN)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
