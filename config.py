"""
Configuration globale pour Demon Slayer Discord Bot
Tous les paramètres du jeu sont ici - Modifiables facilement
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ========================= BOT CONFIGURATION =========================
TOKEN = os.getenv("TOKEN")
PREFIX = "/"
BOT_NAME = "Demon Slayer Bot"
BOT_VERSION = "1.0.0"

# ========================= DATA PATHS =========================
DATA_PATH = "data/"
RESPIRATIONS_FILE = f"{DATA_PATH}respirations.json"
DEMONS_FILE = f"{DATA_PATH}demons.json"
RANKS_FILE = f"{DATA_PATH}ranks.json"
MISSIONS_FILE = f"{DATA_PATH}missions.json"
EVENTS_FILE = f"{DATA_PATH}events.json"
PLAYERS_FILE = f"{DATA_PATH}players.json"

# ========================= GAME SETTINGS =========================

# Combat
COMBAT_MAX_TURNS = 20
COMBAT_TURN_TIMEOUT = 30  # secondes
COMBAT_INITIAL_HP = 100
COMBAT_INITIAL_STAMINA = 100
STAMINA_REGEN_PER_TURN = 5
STAMINA_REGEN_ON_DEFEND = 20

# XP & Leveling
XP_PER_LEVEL_BASE = 100  # XP requis pour level 1
XP_MULTIPLIER_HASHIRA = 1.25  # Multiplicateur si Hashira
XP_MULTIPLIER_IMMORTAL = 1.5  # Multiplicateur si Immortal

# Dégâts
DAMAGE_DEFENSE_REDUCTION = 0.5  # DEF réduit les dégâts de 50%
DAMAGE_DEFEND_REDUCTION = 0.5   # Si défense active, dégâts × 0.5
DAMAGE_VARIANCE = 3             # ±3 de variance aléatoire

# Combat Rewards
HUNT_XP_SMALL = 50
HUNT_XP_MEDIUM = 150
HUNT_XP_BOSS = 500
HUNT_GOLD_SMALL = 75
HUNT_GOLD_MEDIUM = 200
HUNT_GOLD_BOSS = 500

PERFORMANCE_BONUS_HIGH_DAMAGE = 1.2      # 80%+ dégâts infligés
PERFORMANCE_BONUS_LOW_DAMAGE = 0.8       # <30% dégâts infligés
SURVIVAL_BONUS_HIGH_HP = 1.1             # >70% HP restants

# Test de Souffle
BREATHING_TEST_QUESTIONS = 7
BREATHING_TEST_PHYSICAL_STAGES = 4
BREATHING_TEST_COMBAT_TURNS = 8
BREATHING_TEST_COMBAT_DURATION = 120  # secondes

# Missions
TOTAL_MISSIONS = 300
EASY_MISSIONS_END = 100
HARD_MISSIONS_END = 200
HELL_MISSIONS_END = 300

BOSS_MISSION_INTERVAL = 30  # Un boss tous les 30 missions
MISSION_DIFFICULTY_INCREASE_THRESHOLD = 100

# Rangs
RANK_UP_REQUIREMENT_MULTIPLIER = 1.5

# ========================= BREATHING STYLES =========================

BREATHING_STYLES = {
    'water': {
        'name': 'Souffle de l\'Eau',
        'emoji': '💧',
        'color': 0x1E90FF,
        'technique_count': 10,
        'bonus_atk': 0,
        'bonus_def': 5,
        'bonus_spd': 0
    },
    'flame': {
        'name': 'Souffle de la Flamme',
        'emoji': '🔥',
        'color': 0xFF4500,
        'technique_count': 9,
        'bonus_atk': 10,
        'bonus_def': -2,
        'bonus_spd': 0
    },
    'wind': {
        'name': 'Souffle du Vent',
        'emoji': '💨',
        'color': 0xF0F8FF,
        'technique_count': 8,
        'bonus_atk': 5,
        'bonus_def': -3,
        'bonus_spd': 8
    },
    'stone': {
        'name': 'Souffle de la Pierre',
        'emoji': '🪨',
        'color': 0x8B8680,
        'technique_count': 6,
        'bonus_atk': -5,
        'bonus_def': 12,
        'bonus_spd': -3
    },
    'sound': {
        'name': 'Souffle du Son',
        'emoji': '🔊',
        'color': 0xFF6A00,
        'technique_count': 5,
        'bonus_atk': 8,
        'bonus_def': 5,
        'bonus_spd': 6
    },
    'serpent': {
        'name': 'Souffle du Serpent',
        'emoji': '🐍',
        'color': 0x6B4423,
        'technique_count': 5,
        'bonus_atk': 6,
        'bonus_def': 2,
        'bonus_spd': 7
    },
    'flower': {
        'name': 'Souffle de la Fleur',
        'emoji': '🌸',
        'color': 0xFF69B4,
        'technique_count': 5,
        'bonus_atk': 4,
        'bonus_def': 4,
        'bonus_spd': 6
    },
    'mist': {
        'name': 'Souffle du Brouillard',
        'emoji': '🌫️',
        'color': 0xC0C0C0,
        'technique_count': 5,
        'bonus_atk': 2,
        'bonus_def': 3,
        'bonus_spd': 9
    },
    'love': {
        'name': 'Souffle de l\'Amour',
        'emoji': '💕',
        'color': 0xFF1493,
        'technique_count': 5,
        'bonus_atk': 5,
        'bonus_def': 6,
        'bonus_spd': 5
    }
}

# ========================= EVENTS =========================

EVENT_XP_DOUBLE = {
    'id': 'xp_double',
    'name': 'Double XP Event',
    'emoji': '⚡',
    'multiplier': 2.0,
    'type': 'xp'
}

EVENT_COIN_BOOST = {
    'id': 'coin_boost',
    'name': 'Gold Boost Event',
    'emoji': '💰',
    'multiplier': 1.5,
    'type': 'gold'
}

EVENT_XP_TRIPLE = {
    'id': 'xp_triple',
    'name': 'Triple XP Event',
    'emoji': '🔥',
    'multiplier': 3.0,
    'type': 'xp'
}

EVENT_RARE_DEMONS = {
    'id': 'demon_rare',
    'name': 'Rare Demon Spawn Event',
    'emoji': '👹',
    'multiplier': 1.0,
    'type': 'demon_spawn'
}

AVAILABLE_EVENTS = [
    EVENT_XP_DOUBLE,
    EVENT_COIN_BOOST,
    EVENT_XP_TRIPLE,
    EVENT_RARE_DEMONS
]

# ========================= ADMIN SETTINGS =========================

ADMIN_PERMISSIONS_REQUIRED = ['administrator']

ADMIN_ACTIONS = {
    'user': ['view', 'give_xp', 'give_coins', 'set_rank', 'ban'],
    'event': ['create', 'list', 'end'],
    'config': ['reload', 'stats', 'reset_players']
}

# ========================= LEADERBOARD =========================

LEADERBOARD_SIZE = 10
LEADERBOARD_SORT_BY = 'level'

# ========================= MESSAGES =========================

MESSAGES = {
    'no_permission': '❌ Tu n\'as pas les permissions!',
    'user_banned': '🚫 Tu es banni du jeu!',
    'test_required': '📝 Passe d\'abord `/test_souffle`!',
    'already_breathing': '💨 Tu as déjà un souffle!',
    'combat_in_progress': '⚔️ Tu es déjà en combat!',
    'no_active_combat': '❌ Aucun combat actif!',
    'invalid_action': '❌ Action invalide!',
    'not_enough_stamina': '❌ Pas assez de Stamina!',
    'victory': '🎉 VICTOIRE sur {demon}!',
    'defeat': '💀 DÉFAITE contre {demon}...',
    'escape_success': '🏃 Fuite réussie!',
    'escape_failed': '🏃 Fuite échouée!',
    'level_up': '⬆️ LEVEL UP! Niveau {level}!',
    'rank_up': '🏆 PROMOTION! {rank}!'
}

# ========================= VALIDATION =========================

def validate_config():
    """
    Valider la configuration au démarrage
    """
    if not TOKEN:
        raise ValueError("❌ TOKEN non configuré! Ajoute TOKEN dans .env")
    
    import os
    for file in [RESPIRATIONS_FILE, DEMONS_FILE, RANKS_FILE, MISSIONS_FILE, EVENTS_FILE]:
        if not os.path.exists(file):
            raise FileNotFoundError(f"❌ Fichier manquant: {file}")
    
    print("✅ Configuration validée!")
    return True

if __name__ == "__main__":
    validate_config()
    print(f"Bot: {BOT_NAME} v{BOT_VERSION}")
    print(f"Souffles: {len(BREATHING_STYLES)}")
    print(f"Missions: {TOTAL_MISSIONS}")
