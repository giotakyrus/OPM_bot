"""
Commande /hunt - Chasse aux démons
Combat au tour par tour et XP Farm
"""

import discord
from discord.ext import commands
import json
import random
import os
from dotenv import load_dotenv
import config

load_dotenv()

class HuntCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_combats = {}  # Tracker les combats en cours
    
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
    
    def load_demons_data(self):
        """Charger les données des démons"""
        try:
            with open(config.DEMONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def get_random_demon(self, player_level):
        """Obtenir un démon aléatoire basé sur le niveau du joueur"""
        demons_data = self.load_demons_data()
        
        # Sélectionner démons selon le niveau
        if player_level < 10:
            demon_list = demons_data.get('common', [])
        elif player_level < 50:
            demon_list = demons_data.get('lower_moons', [])
        else:
            demon_list = demons_data.get('upper_moons', [])
        
        if not demon_list:
            # Démon par défaut
            return {
                "name": "Démon Ombre",
                "level": player_level,
                "hp": 100 + (player_level * 10),
                "atk": 10 + (player_level * 2),
                "def": 5 + (player_level // 2),
                "spd": 8,
                "xp_reward": 50 + (player_level * 5),
                "gold_reward": 75 + (player_level * 7)
            }
        
        return random.choice(demon_list)
    
    def calculate_damage(self, attacker_atk, defender_def, is_defend=False, is_technique=False, technique_multiplier=1.0):
        """Calculer les dégâts d'une attaque"""
        base_damage = max(1, attacker_atk - (defender_def * config.DAMAGE_DEFENSE_REDUCTION))
        variance = random.randint(-config.DAMAGE_VARIANCE, config.DAMAGE_VARIANCE)
        final_damage = (base_damage + variance) * technique_multiplier
        
        if is_defend:
            final_damage = final_damage * config.DAMAGE_DEFEND_REDUCTION
        
        return max(1, int(final_damage))
    
    async def handle_combat_turn(self, user_id, interaction, action):
        """Gérer un tour de combat"""
        if user_id not in self.active_combats:
            embed = discord.Embed(
                title="❌ Aucun Combat Actif",
                description="Lance un combat avec `/hunt` d'abord!",
                color=0xFF0000
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        combat = self.active_combats[user_id]
        demon = combat['demon']
        
        # Actions disponibles
        if action not in ['attack', 'technique', 'defend', 'item', 'escape']:
            embed = discord.Embed(
                title="❌ Action Invalide",
                description="Actions: `attack` | `technique` | `defend` | `item` | `escape`",
                color=0xFF0000
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        # Simuler le tour du joueur
        player_damage = 0
        action_result = ""
        
        if action == 'attack':
            player_damage = self.calculate_damage(
                10 + combat['player_level'],
                demon['def']
            )
            action_result = f"💥 Tu as infligé **{player_damage}** dégâts!"
            combat['demon_hp'] -= player_damage
        
        elif action == 'technique':
            if combat['player_stamina'] < 20:
                action_result = "❌ Pas assez de Stamina! (coût: 20)"
                player_damage = 0
            else:
                player_damage = self.calculate_damage(
                    10 + combat['player_level'],
                    demon['def'],
                    is_technique=True,
                    technique_multiplier=1.5
                )
                combat['player_stamina'] -= 20
                action_result = f"⚔️ Technique Spéciale! **{player_damage}** dégâts!"
                combat['demon_hp'] -= player_damage
        
        elif action == 'defend':
            combat['player_stamina'] = min(100, combat['player_stamina'] + config.STAMINA_REGEN_ON_DEFEND)
            action_result = f"🛡️ Défense activée! +{config.STAMINA_REGEN_ON_DEFEND} Stamina"
        
        elif action == 'escape':
            if random.random() < 0.5:
                escape_embed = discord.Embed(
                    title="🏃 Fuite Réussie!",
                    description=f"Tu as échappé au {demon['name']}!",
                    color=0x00FF00
                )
                del self.active_combats[user_id]
                return await interaction.response.send_message(embed=escape_embed)
            else:
                action_result = "🏃 La fuite a échoué!"
        
        # Tour du démon
        demon_action = random.choice(['attack', 'defend'])
        demon_damage = 0
        
        if demon_action == 'attack':
            demon_damage = self.calculate_damage(
                demon['atk'],
                10 + combat['player_level']
            )
            action_result += f"\n\n👹 {demon['name']} t'a infligé **{demon_damage}** dégâts!"
            combat['player_hp'] -= demon_damage
        else:
            action_result += f"\n\n👹 {demon['name']} se défend!"
        
        # Vérifier fin du combat
        embed = discord.Embed(
            title=f"⚔️ Tour {combat['turn']}",
            description=action_result,
            color=0xFF6A00
        )
        
        embed.add_field(
            name="Tes Stats",
            value=f"❤️ {max(0, combat['player_hp'])}/100 | ⚡ {combat['player_stamina']}/100",
            inline=False
        )
        
        embed.add_field(
            name=f"Stats de {demon['name']}",
            value=f"❤️ {max(0, combat['demon_hp'])}/{demon['hp']}",
            inline=False
        )
        
        # Vérifier victoire/défaite
        if combat['demon_hp'] <= 0:
            # Victoire!
            xp_reward = demon['xp_reward']
            gold_reward = demon['gold_reward']
            
            embed = discord.Embed(
                title="🎉 VICTOIRE!",
                description=f"Tu as vaincu **{demon['name']}**!",
                color=0x00FF00
            )
            embed.add_field(
                name="Récompenses",
                value=f"🎯 +{xp_reward} XP\n💰 +{gold_reward} or",
                inline=False
            )
            
            # Mettre à jour le joueur
            players_data = self.load_players_data()
            player = players_data.get(str(user_id), {})
            player['xp'] = player.get('xp', 0) + xp_reward
            player['coins'] = player.get('coins', 0) + gold_reward
            player['demon_kills'] = player.get('demon_kills', 0) + 1
            players_data[str(user_id)] = player
            self.save_players_data(players_data)
            
            del self.active_combats[user_id]
            return await interaction.response.send_message(embed=embed)
        
        elif combat['player_hp'] <= 0:
            # Défaite
            embed = discord.Embed(
                title="💀 DÉFAITE!",
                description=f"Tu as été vaincu par **{demon['name']}**...",
                color=0xFF0000
            )
            
            del self.active_combats[user_id]
            return await interaction.response.send_message(embed=embed)
        
        # Combat continue
        combat['turn'] += 1
        embed.set_footer(text=f"Prochaine action: /combat_action [attack|technique|defend|escape]")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    """Charger la cog"""
    await bot.add_cog(HuntCommands(bot))

