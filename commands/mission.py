"""
Commande /mission - Système de missions
300 missions avec progression de difficulté
"""

import discord
from discord.ext import commands
import json
import random
import os
from dotenv import load_dotenv
import config

load_dotenv()

class MissionCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def load_players_data(self):
        """Charger les données des joueurs"""
        try:
            with open(config.PLAYERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_players_data(self, data):
        """Sauvegarder les données des joueurs"""
        try:
            os.makedirs(os.path.dirname(config.PLAYERS_FILE), exist_ok=True)
            with open(config.PLAYERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False
    
    def load_missions_data(self):
        """Charger les données des missions"""
        try:
            with open(config.MISSIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"missions": []}
    
    def get_mission_by_id(self, mission_id):
        """Obtenir une mission par son ID"""
        missions_data = self.load_missions_data()
        for mission in missions_data.get('missions', []):
            if mission['id'] == mission_id:
                return mission
        return None
    
    def get_available_missions(self, player_level, missions_completed):
        """Obtenir les missions disponibles pour le joueur"""
        missions_data = self.load_missions_data()
        available = []
        
        for mission in missions_data.get('missions', []):
            mission_id = mission['id']
            
            # Vérifier la difficulté disponible
            if mission_id <= 30:  # Missions faciles
                available.append(mission)
            elif missions_completed >= 30 and mission_id <= 100:  # Missions difficiles
                available.append(mission)
            elif missions_completed >= 100 and mission_id > 100:  # Missions enfer
                available.append(mission)
        
        return available
    
    @commands.command(name='mission_list')
    async def mission_list(self, ctx):
        """Afficher les missions disponibles"""
        # Ce fichier est juste pour montrer la structure
        await ctx.send("✅ Commande mission_list créée!")

async def setup(bot):
    """Charger la cog"""
    await bot.add_cog(MissionCommands(bot))
