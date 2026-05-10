import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import config
from models.player import PlayerManager
from models.combat import CombatEngine
from utils.embeds import EmbedBuilder

load_dotenv()

# ========================= BOT SETUP =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Managers globaux
player_manager = PlayerManager()
combat_engine = CombatEngine()

# ========================= BOT EVENTS =========================

@bot.event
async def on_ready():
    """Appelé quand le bot est prêt"""
    print(f"✅ Bot connecté: {bot.user}")
    print(f"📊 Serveurs: {len(bot.guilds)}")
    print(f"👥 Utilisateurs: {sum(g.member_count for g in bot.guilds)}")
    
    # Valider la config
    try:
        config.validate_config()
    except Exception as e:
        print(f"❌ Erreur config: {e}")
    
    # Syncer les commandes slash
    try:
        synced = await bot.tree.sync()
        print(f"🔄 {len(synced)} commandes synchro avec Discord")
    except Exception as e:
        print(f"❌ Erreur sync commandes: {e}")
    
    # Status personnalisé
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="des démons 👹 | /aide"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)
    print("🎮 Jeu Demon Slayer chargé!")

@bot.event
async def on_command_error(ctx, error):
    """Gérer les erreurs de commandes"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"❌ Tu n'as pas les permissions pour cette commande!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Arguments manquants! Utilise `/aide`")
    else:
        print(f"Erreur: {error}")
        await ctx.send(f"❌ Une erreur est survenue!")

# ========================= COMMANDES SLASH =========================

@bot.tree.command(name="profil", description="Voir ton profil de Pourfendeur")
async def profil(interaction: discord.Interaction):
    """Affiche le profil complet du joueur"""
    user_id = interaction.user.id
    
    # Vérifier si le joueur existe
    if not player_manager.player_exists(user_id):
        embed = discord.Embed(
            title="❌ Profil Non Trouvé",
            description="Tu n'as pas encore commencé le jeu!\n\nUtilise `/test_souffle` pour commencer",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Charger le joueur
    player = player_manager.load_player(user_id)
    
    # Vérifier si banni
    if player.banned:
        embed = discord.Embed(
            title="🚫 BANNI",
            description=f"Tu es banni: {player.ban_reason}",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Créer et envoyer l'embed
    embed = EmbedBuilder.create_profile_embed(player, interaction.user)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="classement", description="Voir le classement global")
async def classement(interaction: discord.Interaction):
    """Affiche le leaderboard"""
    leaders = player_manager.get_leaderboard(config.LEADERBOARD_SIZE)
    
    if not leaders:
        embed = discord.Embed(
            title="📊 Classement",
            description="Aucun joueur enregistré encore!",
            color=0xFFD700
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    embed = EmbedBuilder.create_leaderboard_embed(leaders)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="aide", description="Afficher l'aide du jeu")
async def aide(interaction: discord.Interaction):
    """Affiche l'aide et les commandes disponibles"""
    embed = discord.Embed(
        title="🎌 Demon Slayer - Aide",
        description="Bienvenue Pourfendeur de Démons!",
        color=0xFF0000
    )
    
    embed.add_field(
        name="🚀 Commencer",
        value="`/test_souffle` - Débloquer ton souffle unique\n`/profil` - Voir ton profil",
        inline=False
    )
    
    embed.add_field(
        name="⚔️ Combat",
        value="`/hunt` - Chasser un démon\n`/mission [id]` - Accepter une mission",
        inline=False
    )
    
    embed.add_field(
        name="🏆 Social",
        value="`/classement` - Voir le top 10\n`/duel @joueur` - Affronter un joueur",
        inline=False
    )
    
    embed.add_field(
        name="📖 Info",
        value="`/souffles` - Liste des souffles\n`/aide` - Cette aide",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Admin",
        value="`/admin_user` - Gérer les joueurs\n`/admin_event` - Gérer les événements\n`/admin_config` - Config globale",
        inline=False
    )
    
    embed.set_footer(text="Tape /aide <commande> pour plus de détails")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="souffles", description="Voir la liste des souffles")
async def souffles(interaction: discord.Interaction):
    """Affiche la liste de tous les souffles"""
    embed = discord.Embed(
        title="💨 Souffles Disponibles",
        description="Passe le test `/test_souffle` pour débloquer ton souffle!",
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
    
    embed.set_footer(text="Chaque souffle a ses avantages et techniques uniques!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="stats_bot", description="Voir les statistiques du serveur")
async def stats_bot(interaction: discord.Interaction):
    """Affiche les stats globales du jeu"""
    total_players = player_manager.get_player_count()
    
    embed = discord.Embed(
        title="📊 Statistiques Globales",
        color=0x00FF00
    )
    
    embed.add_field(
        name="👥 Joueurs",
        value=total_players,
        inline=True
    )
    
    embed.add_field(
        name="💨 Souffles",
        value=len(config.BREATHING_STYLES),
        inline=True
    )
    
    embed.add_field(
        name="🎯 Missions",
        value=config.TOTAL_MISSIONS,
        inline=True
    )
    
    embed.add_field(
        name="👹 Démons",
        value="43 (12 Lunes + 25 Custom + Muzan)",
        inline=True
    )
    
    embed.add_field(
        name="🏆 Rangs",
        value="11 niveaux de progression",
        inline=True
    )
    
    embed.add_field(
        name="🎁 Événements",
        value=len(config.AVAILABLE_EVENTS),
        inline=True
    )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ========================= COMMANDES ADMIN =========================

@bot.tree.command(name="admin_user", description="[ADMIN] Gérer les joueurs")
@discord.app_commands.describe(
    action="view / give_xp / give_coins / set_rank / ban",
    user="L'utilisateur cible",
    amount="Montant (pour XP/Coins)",
    rank="Rang (1-11)"
)
async def admin_user(
    interaction: discord.Interaction,
    action: str,
    user: discord.User,
    amount: int = 0,
    rank: int = 0
):
    """Commande administration utilisateur"""
    
    # Vérification admin
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas les permissions admin!",
            ephemeral=True
        )
    
    user_id = user.id
    players_data = {}
    
    # Charger les joueurs
    try:
        import json
        with open(config.PLAYERS_FILE, 'r', encoding='utf-8') as f:
            players_data = json.load(f)
    except FileNotFoundError:
        players_data = {}
    
    if action.lower() == "view" or action.lower() == "voir":
        if str(user_id) not in players_data:
            return await interaction.response.send_message(
                f"❌ {user.mention} n'a pas de profil!",
                ephemeral=True
            )
        
        player_data = players_data[str(user_id)]
        embed = discord.Embed(
            title=f"👤 Profil Admin - {user.name}",
            color=0xFF0000
        )
        embed.add_field(name="Level", value=player_data.get('level', 1), inline=True)
        embed.add_field(name="XP", value=player_data.get('xp', 0), inline=True)
        embed.add_field(name="Coins", value=player_data.get('coins', 0), inline=True)
        embed.add_field(name="Rang", value=player_data.get('rank', 'Unknown'), inline=False)
        embed.add_field(name="Souffle", value=player_data.get('breathing', 'Not unlocked'), inline=False)
        embed.add_field(name="Missions", value=player_data.get('missions_completed', 0), inline=True)
        embed.add_field(name="Kills", value=player_data.get('demon_kills', 0), inline=True)
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "give_xp" or action.lower() == "donner_xp":
        if str(user_id) not in players_data:
            players_data[str(user_id)] = {
                'level': 1,
                'xp': 0,
                'coins': 0,
                'rank': 'Apprentice Slayer',
                'breathing': None,
                'missions_completed': 0,
                'demon_kills': 0
            }
        
        players_data[str(user_id)]['xp'] += amount
        
        # Sauvegarder
        import json
        with open(config.PLAYERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(players_data, f, indent=2, ensure_ascii=False)
        
        embed = discord.Embed(
            title="✅ XP Donné",
            description=f"{user.mention} a reçu **+{amount} XP**",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "ban" or action.lower() == "bannir":
        if str(user_id) not in players_data:
            players_data[str(user_id)] = {
                'level': 1,
                'xp': 0,
                'coins': 0,
                'rank': 'Apprentice Slayer',
                'breathing': None,
                'missions_completed': 0,
                'demon_kills': 0,
                'banned': True,
                'ban_reason': 'Admin ban'
            }
        else:
            players_data[str(user_id)]['banned'] = True
            players_data[str(user_id)]['ban_reason'] = 'Admin ban'
        
        # Sauvegarder
        import json
        with open(config.PLAYERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(players_data, f, indent=2, ensure_ascii=False)
        
        embed = discord.Embed(
            title="🚫 Joueur Banni",
            description=f"{user.mention} a été **banni** du jeu!",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    else:
        await interaction.response.send_message("❌ Action non reconnue!", ephemeral=True)

@bot.tree.command(name="admin_config", description="[ADMIN] Gestion config")
@discord.app_commands.describe(
    action="reload / stats / reset_players",
    confirm="Confirmation (true/false)"
)
async def admin_config(
    interaction: discord.Interaction,
    action: str,
    confirm: bool = False
):
    """Commande administration config"""
    
    # Vérification admin
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message(
            "❌ Tu n'as pas les permissions admin!",
            ephemeral=True
        )
    
    if action.lower() == "stats":
        total_players = player_manager.get_player_count()
        embed = discord.Embed(
            title="📊 Statistiques Serveur",
            color=0x00FF00
        )
        embed.add_field(name="Joueurs", value=total_players, inline=True)
        embed.add_field(name="Missions", value=config.TOTAL_MISSIONS, inline=True)
        embed.add_field(name="Souffles", value=len(config.BREATHING_STYLES), inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "reload":
        try:
            config.validate_config()
            embed = discord.Embed(
                title="✅ Configuration Reloadée",
                description="Tous les fichiers sont valides!",
                color=0x00FF00
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erreur Config",
                description=str(e),
                color=0xFF0000
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "reset_players":
        if not confirm:
            embed = discord.Embed(
                title="⚠️ ATTENTION",
                description="Cette action est **IRRÉVERSIBLE**!\n\nTape la commande à nouveau avec `confirm:true`",
                color=0xFF0000
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        import json
        with open(config.PLAYERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        
        embed = discord.Embed(
            title="✅ Réinitialisation",
            description="Tous les profils ont été supprimés!",
            color=0xFF0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    else:
        await interaction.response.send_message("❌ Action inconnue!", ephemeral=True)

# ========================= LANCER LE BOT =========================

def main():
    """Lancer le bot"""
    if not config.TOKEN:
        print("❌ ERREUR: TOKEN non configuré dans .env")
        print("Ajoute: TOKEN=ton_token_discord")
        return
    
    try:
        print(f"🚀 Démarrage {config.BOT_NAME} v{config.BOT_VERSION}")
        print(f"📦 Dépendances: discord.py, python-dotenv")
        bot.run(config.TOKEN)
    except Exception as e:
        print(f"❌ Erreur démarrage: {e}")

if __name__ == "__main__":
    main()
