import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv
import config
from utils.embeds import EmbedBuilder
import asyncio

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

def load_breathing_data():
    """Charger les données des souffles"""
    try:
        with open(config.RESPIRATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_demons_data():
    """Charger les données des démons"""
    try:
        with open(config.DEMONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def load_missions_data():
    """Charger les données des missions"""
    try:
        with open(config.MISSIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"missions": []}

# ========================= BOT EVENTS =========================

@bot.event
async def on_ready():
    """Appelé quand le bot est prêt"""
    print(f"✅ Bot connecté: {bot.user}")
    print(f"📊 Serveurs: {len(bot.guilds)}")
    
    # Charger les cogs (commandes)
    try:
        await load_cogs()
    except Exception as e:
        print(f"❌ Erreur chargement cogs: {e}")
    
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

async def load_cogs():
    """Charger tous les cogs"""
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f"✅ Cog chargée: {filename}")
            except Exception as e:
                print(f"❌ Erreur chargement {filename}: {e}")

# ========================= COMMANDES SLASH =========================

@bot.tree.command(name="profil", description="Voir ton profil complet")
async def profil(interaction: discord.Interaction):
    """Affiche le profil détaillé du joueur"""
    user_id = str(interaction.user.id)
    
    if not player_exists(interaction.user.id):
        embed = discord.Embed(
            title="❌ Profil Non Trouvé",
            description="Tu n'as pas commencé le jeu!\nUtilise `/test_souffle` pour commencer",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    players_data = load_players_data()
    player = players_data[user_id]
    
    embed = discord.Embed(
        title=f"🗡️ Profil de {interaction.user.name}",
        color=0xFF0000
    )
    
    # Stats de base
    embed.add_field(
        name="📊 Statistiques",
        value=f"Level: **{player.get('level', 1)}**\nXP: **{player.get('xp', 0)}**",
        inline=True
    )
    
    # Souffle
    if 'breathing' in player:
        breathing_name = player['breathing']
        embed.add_field(
            name="💨 Souffle",
            value=f"**{breathing_name}**",
            inline=True
        )
    
    # Stats de combat
    embed.add_field(
        name="⚔️ Combat",
        value=f"ATK: **{10 + player.get('level', 1)}** | DEF: **{5 + player.get('level', 1)//2}**",
        inline=False
    )
    
    # Progression
    embed.add_field(
        name="🎯 Progression",
        value=f"Démons vaincus: **{player.get('demon_kills', 0)}**\nMissions: **{player.get('missions_completed', 0)}/300**",
        inline=False
    )
    
    embed.add_field(
        name="💰 Économie",
        value=f"Coins: **{player.get('coins', 0)}**",
        inline=True
    )
    
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="test_souffle", description="Passer le test pour débloquer ton souffle unique")
async def test_souffle(interaction: discord.Interaction):
    """Lance le test complet de respiration"""
    user_id = interaction.user.id
    players_data = load_players_data()
    user_id_str = str(user_id)
    
    # Vérifier si joueur existe déjà
    if user_id_str in players_data and 'breathing' in players_data[user_id_str]:
        embed = discord.Embed(
            title="💨 Tu as déjà un souffle!",
            description=f"Souffle: **{players_data[user_id_str]['breathing']}**",
            color=0xFF6A00
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Créer le profil s'il n'existe pas
    if user_id_str not in players_data:
        players_data[user_id_str] = {
            'level': 1,
            'xp': 0,
            'coins': 0,
            'demon_kills': 0,
            'missions_completed': 0
        }
    
    # Sélectionner un souffle aléatoire (pour la démo)
    breathing_keys = list(config.BREATHING_STYLES.keys())
    selected_breathing_key = breathing_keys[hash(user_id) % len(breathing_keys)]
    breathing_info = config.BREATHING_STYLES[selected_breathing_key]
    
    # Assigner le souffle
    players_data[user_id_str]['breathing'] = breathing_info['name']
    players_data[user_id_str]['breathing_key'] = selected_breathing_key
    save_players_data(players_data)
    
    # Afficher le résultat
    embed = discord.Embed(
        title="🎌 Ton Souffle Unique!",
        description=f"Après le test complet, ton souffle est...",
        color=breathing_info['color']
    )
    
    emoji = breathing_info['emoji']
    name = breathing_info['name']
    techniques = breathing_info['technique_count']
    
    embed.add_field(
        name=f"{emoji} {name}",
        value=f"**{techniques} mouvements**\nATK: {breathing_info['bonus_atk']:+d} | DEF: {breathing_info['bonus_def']:+d} | SPD: {breathing_info['bonus_spd']:+d}",
        inline=False
    )
    
    embed.add_field(
        name="✅ Déblocages",
        value="Tu peux maintenant:\n• `/hunt` - Chasser des démons\n• `/mission` - Accepter des missions\n• `/duel` - Défier d'autres joueurs",
        inline=False
    )
    
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="hunt", description="Chasser un démon et gagner de l'XP")
async def hunt(interaction: discord.Interaction):
    """Lancer un combat contre un démon"""
    user_id = interaction.user.id
    
    if not player_exists(user_id):
        embed = discord.Embed(
            title="❌ Profil Non Trouvé",
            description="Utilise `/test_souffle` pour commencer!",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    players_data = load_players_data()
    player = players_data[str(user_id)]
    
    if 'breathing' not in player:
        embed = discord.Embed(
            title="❌ Pas de Souffle",
            description="Passe `/test_souffle` pour débloquer ton souffle!",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    player_level = player.get('level', 1)
    demons_data = load_demons_data()
    
    # Générer un démon aléatoire
    if player_level < 10:
        demon_list = demons_data.get('common', [])
    elif player_level < 50:
        demon_list = demons_data.get('lower_moons', [])
    else:
        demon_list = demons_data.get('upper_moons', [])
    
    if not demon_list:
        demon = {
            "name": "Démon Ombre",
            "level": player_level,
            "hp": 100 + (player_level * 10),
            "atk": 10 + (player_level * 2),
            "def": 5 + (player_level // 2),
            "emoji": "👹",
            "xp_reward": 50 + (player_level * 5),
            "gold_reward": 75 + (player_level * 7)
        }
    else:
        demon = demon_list[hash(user_id) % len(demon_list)]
    
    embed = discord.Embed(
        title="⚔️ Combat Lancé!",
        description=f"{demon.get('emoji', '👹')} Tu affrontes **{demon['name']}**!",
        color=0xFF0000
    )
    
    embed.add_field(
        name="Tes Stats",
        value=f"❤️ 100 HP | ⚡ 100 Stamina\nATK: {10 + player_level} | DEF: {5 + player_level//2}",
        inline=False
    )
    
    embed.add_field(
        name="Stats du Démon",
        value=f"❤️ {demon['hp']} HP\nATK: {demon['atk']} | DEF: {demon['def']}",
        inline=False
    )
    
    embed.add_field(
        name="💰 Récompenses",
        value=f"🎯 {demon['xp_reward']} XP | 💰 {demon['gold_reward']} coins",
        inline=False
    )
    
    embed.set_footer(text="Combat simulé - Victoire automatique en démo!")
    
    await interaction.response.send_message(embed=embed)
    
    # Simuler une victoire après 2 secondes
    await asyncio.sleep(2)
    
    # Mise à jour du joueur
    xp_reward = demon['xp_reward']
    gold_reward = demon['gold_reward']
    
    player['xp'] = player.get('xp', 0) + xp_reward
    player['coins'] = player.get('coins', 0) + gold_reward
    player['demon_kills'] = player.get('demon_kills', 0) + 1
    players_data[str(user_id)] = player
    save_players_data(players_data)
    
    # Vérifier level up
    xp_needed = config.XP_PER_LEVEL_BASE * player.get('level', 1)
    if player['xp'] >= xp_needed:
        player['level'] = player.get('level', 1) + 1
        player['xp'] = 0
        players_data[str(user_id)] = player
        save_players_data(players_data)
        
        victory_embed = discord.Embed(
            title="🎉 VICTOIRE!",
            description=f"Tu as vaincu **{demon['name']}**!",
            color=0x00FF00
        )
        victory_embed.add_field(
            name="Récompenses",
            value=f"🎯 +{xp_reward} XP\n💰 +{gold_reward} coins\n⬆️ **LEVEL UP! Niveau {player['level']}!**",
            inline=False
        )
        
        await interaction.followup.send(embed=victory_embed)
    else:
        victory_embed = discord.Embed(
            title="🎉 VICTOIRE!",
            description=f"Tu as vaincu **{demon['name']}**!",
            color=0x00FF00
        )
        victory_embed.add_field(
            name="Récompenses",
            value=f"🎯 +{xp_reward} XP\n💰 +{gold_reward} coins",
            inline=False
        )
        
        await interaction.followup.send(embed=victory_embed)

@bot.tree.command(name="mission", description="Accepter une mission")
@discord.app_commands.describe(mission_id="ID de la mission (1-300)")
async def mission(interaction: discord.Interaction, mission_id: int):
    """Lance une mission"""
    user_id = interaction.user.id
    
    if not player_exists(user_id):
        embed = discord.Embed(
            title="❌ Profil Non Trouvé",
            description="Utilise `/test_souffle` pour commencer!",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    players_data = load_players_data()
    player = players_data[str(user_id)]
    
    if 'breathing' not in player:
        embed = discord.Embed(
            title="❌ Pas de Souffle",
            description="Passe `/test_souffle` pour débloquer ton souffle!",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Charger les missions
    missions_data = load_missions_data()
    mission_obj = None
    
    for m in missions_data.get('missions', []):
        if m['id'] == mission_id:
            mission_obj = m
            break
    
    if not mission_obj:
        embed = discord.Embed(
            title="❌ Mission Non Trouvée",
            description=f"Mission #{mission_id} n'existe pas!",
            color=0xFF0000
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Vérifier les prérequis
    missions_completed = player.get('missions_completed', 0)
    player_level = player.get('level', 1)
    
    if mission_id <= 30 and missions_completed < 0:
        pass  # Missions faciles toujours disponibles
    elif mission_id <= 100 and missions_completed < 30:
        embed = discord.Embed(
            title="🔐 Mission Verrouillée",
            description=f"Tu dois compléter 30 missions faciles d'abord!\nProgression: {missions_completed}/30",
            color=0xFF6A00
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif mission_id > 100 and missions_completed < 100:
        embed = discord.Embed(
            title="🔐 Mission Verrouillée",
            description=f"Tu dois compléter 100 missions d'abord!\nProgression: {missions_completed}/100",
            color=0xFF6A00
        )
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # Afficher la mission
    difficulty_emoji = "🟢" if mission_obj['difficulty'] == 'easy' else "🟡" if mission_obj['difficulty'] == 'hard' else "🔴"
    boss_text = "👑 **BOSS**" if mission_obj.get('boss', False) else ""
    
    embed = discord.Embed(
        title=f"{difficulty_emoji} Mission #{mission_id}: {mission_obj['name']}",
        description=mission_obj['description'],
        color=0xFF6A00
    )
    
    embed.add_field(
        name="Difficulté",
        value=mission_obj['difficulty'].upper(),
        inline=True
    )
    
    embed.add_field(
        name="Ennemi",
        value=mission_obj['demon'],
        inline=True
    )
    
    embed.add_field(
        name="💰 Récompenses",
        value=f"🎯 {mission_obj['xp_reward']} XP\n💰 {mission_obj['gold_reward']} coins",
        inline=False
    )
    
    if boss_text:
        embed.add_field(name="Type", value=boss_text, inline=False)
    
    embed.set_footer(text="Combat simulé - Victoire automatique en démo!")
    
    await interaction.response.send_message(embed=embed)
    
    # Simuler une victoire
    await asyncio.sleep(2)
    
    # Mise à jour du joueur
    xp_reward = mission_obj['xp_reward']
    gold_reward = mission_obj['gold_reward']
    
    player['xp'] = player.get('xp', 0) + xp_reward
    player['coins'] = player.get('coins', 0) + gold_reward
    player['missions_completed'] = player.get('missions_completed', 0) + 1
    players_data[str(user_id)] = player
    save_players_data(players_data)
    
    # Vérifier level up
    xp_needed = config.XP_PER_LEVEL_BASE * player.get('level', 1)
    if player['xp'] >= xp_needed:
        player['level'] = player.get('level', 1) + 1
        player['xp'] = 0
        players_data[str(user_id)] = player
        save_players_data(players_data)
        
        victory_embed = discord.Embed(
            title="🎉 MISSION RÉUSSIE!",
            description=f"Tu as complété **{mission_obj['name']}**!",
            color=0x00FF00
        )
        victory_embed.add_field(
            name="Récompenses",
            value=f"🎯 +{xp_reward} XP\n💰 +{gold_reward} coins\n⬆️ **LEVEL UP! Niveau {player['level']}!**",
            inline=False
        )
        
        await interaction.followup.send(embed=victory_embed)
    else:
        victory_embed = discord.Embed(
            title="🎉 MISSION RÉUSSIE!",
            description=f"Tu as complété **{mission_obj['name']}**!",
            color=0x00FF00
        )
        victory_embed.add_field(
            name="Récompenses",
            value=f"🎯 +{xp_reward} XP\n💰 +{gold_reward} coins",
            inline=False
        )
        
        await interaction.followup.send(embed=victory_embed)

@bot.tree.command(name="aide", description="Afficher l'aide du jeu")
async def aide(interaction: discord.Interaction):
    """Affiche l'aide complète"""
    embed = discord.Embed(
        title="🎌 Demon Slayer - Aide",
        description="Bienvenue Pourfendeur de Démons!",
        color=0xFF0000
    )
    
    embed.add_field(
        name="🚀 Commencer",
        value="`/test_souffle` - Débloquer ton souffle unique",
        inline=False
    )
    
    embed.add_field(
        name="🎯 Commandes Principales",
        value="`/profil` - Voir ton profil\n`/hunt` - Chasser des démons\n`/mission [id]` - Accepter une mission\n`/souffles` - Lister les souffles\n`/stats_bot` - Statistiques",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ Admin",
        value="`/admin_user` - Gérer les joueurs\n`/admin_config` - Config globale",
        inline=False
    )
    
    embed.set_footer(text="Le jeu est en développement! 🚀 Phase 3 en cours")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="souffles", description="Voir la liste des souffles disponibles")
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
        stats = f"ATK: {breathing['bonus_atk']:+d} | DEF: {breathing['bonus_def']:+d} | SPD: {breathing['bonus_spd']:+d}"
        embed.add_field(
            name=f"{emoji} {name}",
            value=f"{techniques} mouvements\n{stats}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="stats_bot", description="Voir les statistiques globales")
async def stats_bot(interaction: discord.Interaction):
    """Affiche les stats globales du bot"""
    total_players = get_player_count()
    demons_data = load_demons_data()
    
    total_demons = len(demons_data.get('common', [])) + len(demons_data.get('lower_moons', [])) + len(demons_data.get('upper_moons', []))
    
    embed = discord.Embed(
        title="📊 Statistiques Globales",
        color=0x00FF00
    )
    
    embed.add_field(name="👥 Joueurs", value=f"**{total_players}**", inline=True)
    embed.add_field(name="💨 Souffles", value=f"**{len(config.BREATHING_STYLES)}**", inline=True)
    embed.add_field(name="🎯 Missions", value=f"**{config.TOTAL_MISSIONS}**", inline=True)
    embed.add_field(name="👹 Démons", value=f"**{total_demons}**", inline=True)
    embed.add_field(name="🏆 Rangs", value="**11**", inline=True)
    embed.add_field(name="📈 Phase", value="**Phase 3 - Missions**", inline=True)
    
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
        embed.add_field(name="Coins", value=player.get('coins', 0))
        embed.add_field(name="Souffle", value=player.get('breathing', '❌ Pas de souffle'))
        embed.add_field(name="Missions", value=player.get('missions_completed', 0))
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

@bot.tree.command(name="admin_config", description="[ADMIN] Configuration globale")
@discord.app_commands.describe(action="reload / stats / reset_players")
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
        embed = discord.Embed(title="✅ Config Reloadée", description="Fichiers JSON rechargés", color=0x00FF00)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif action.lower() == "reset_players":
        players_data = {}
        save_players_data(players_data)
        embed = discord.Embed(title="⚠️ Reset Complet", description="Tous les profils ont été supprimés!", color=0xFF0000)
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
