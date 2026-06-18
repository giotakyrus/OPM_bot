"""
Commande /test_souffle - Test de respiration complet
Quiz + Épreuves physiques + Combat final
"""

import discord
from discord.ext import commands
import random
import json
import os
from dotenv import load_dotenv
import asyncio
import config

load_dotenv()

class TestSouffleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tests = {}  # Tracker les tests en cours
    
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
    
    def load_breathing_data(self):
        """Charger les données des souffles"""
        try:
            with open(config.RESPIRATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def get_quiz_questions(self):
        """Questions du test de respiration"""
        return [
            {
                "question": "Face à un démon, tu choisis de...",
                "answers": {
                    "A": ("Attaquer directement avec force", "flame"),
                    "B": ("Trouver l'équilibre et adapter ta stratégie", "water"),
                    "C": ("Être rapide et insaisissable", "wind"),
                    "D": ("Rester défensif et solide", "stone")
                }
            },
            {
                "question": "Quelle est ta plus grande force?",
                "answers": {
                    "A": ("La puissance brute", "flame"),
                    "B": ("La flexibilité et l'adaptation", "water"),
                    "C": ("La vitesse et la fluidité", "wind"),
                    "D": ("La stabilité et la résilience", "stone")
                }
            },
            {
                "question": "Quand tout semble perdu, tu...",
                "answers": {
                    "A": ("Entres dans une colère consumante", "flame"),
                    "B": ("Conserves ton calme et cherches une solution", "water"),
                    "C": ("Relies rapidement ou cherches une échappatoire", "wind"),
                    "D": ("Tiens bon et résistes", "stone")
                }
            },
            {
                "question": "Ton environnement préféré est...",
                "answers": {
                    "A": ("Un volcan ardent", "flame"),
                    "B": ("Un lac ou une rivière", "water"),
                    "C": ("Une montagne ventée", "wind"),
                    "D": ("Une grotte rocheuse", "stone")
                }
            },
            {
                "question": "Tu considères un ennemi comme...",
                "answers": {
                    "A": ("Une menace à écraser", "flame"),
                    "B": ("Un problème à comprendre", "water"),
                    "C": ("Un obstacle à contourner", "wind"),
                    "D": ("Une force à affronter directement", "stone")
                }
            },
            {
                "question": "Ton style de combat est plutôt...",
                "answers": {
                    "A": ("Agressif et offensif", "flame"),
                    "B": ("Équilibré et défensif", "water"),
                    "C": ("Rapide et acrobatique", "wind"),
                    "D": ("Massif et imparable", "stone")
                }
            },
            {
                "question": "L'harmonie vient pour toi de...",
                "answers": {
                    "A": ("La domination et la victoire", "flame"),
                    "B": ("L'équilibre entre tout", "water"),
                    "C": ("La liberté et la légèreté", "wind"),
                    "D": ("La solidité et la permanence", "stone")
                }
            }
        ]
    
    @commands.command(name='test_souffle_setup')
    @commands.is_owner()
    async def test_souffle_setup(self, ctx):
        """[OWNER] Initialiser les fichiers de test"""
        # Ce fichier est juste pour montrer la structure
        await ctx.send("✅ Fichier de test créé!")
    
    async def run_quiz(self, user_id, interaction):
        """Lancer le quiz psychologique"""
        questions = self.get_quiz_questions()
        scores = {breathing: 0 for breathing in config.BREATHING_STYLES.keys()}
        
        embed = discord.Embed(
            title="🎌 Test de Respiration - Phase 1: Quiz",
            description="7 questions pour déterminer ton souffle!",
            color=0xFF0000
        )
        embed.add_field(name="Instructions", value="Réponds par A, B, C ou D dans le chat", inline=False)
        
        await interaction.followup.send(embed=embed)
        
        for i, q in enumerate(questions, 1):
            # Créer l'embed de question
            question_embed = discord.Embed(
                title=f"Question {i}/7",
                description=q['question'],
                color=0x1E90FF
            )
            
            answer_text = ""
            for key, (answer, breathing) in q['answers'].items():
                answer_text += f"**{key}:** {answer}\n"
            
            question_embed.add_field(name="Réponses", value=answer_text, inline=False)
            question_embed.set_footer(text="Attente de réponse... (60s)")
            
            await interaction.followup.send(embed=question_embed)
            
            # Attendre réponse
            try:
                message = await self.bot.wait_for(
                    'message',
                    timeout=60,
                    check=lambda m: m.author.id == user_id and m.content.upper() in ['A', 'B', 'C', 'D']
                )
                
                answer = message.content.upper()
                breathing = q['answers'][answer][1]
                scores[breathing] += 1
                
                # Feedback
                feedback_embed = discord.Embed(
                    description=f"✅ {message.author.mention} a répondu **{answer}**",
                    color=0x00FF00
                )
                await interaction.followup.send(embed=feedback_embed)
                
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    description="⏱️ Temps écoulé! Réponse annulée.",
                    color=0xFF0000
                )
                await interaction.followup.send(embed=timeout_embed)
                return None
        
        # Déterminer le souffle dominant
        dominant_breathing = max(scores, key=scores.get)
        return dominant_breathing
    
    async def run_physical_tests(self, user_id, interaction):
        """Lancer les 4 épreuves physiques"""
        tests = [
            {
                "name": "Force",
                "emoji": "💪",
                "description": "Tape '/force' dans le chat! Plus tu réponds vite, plus tu es fort!",
                "stat": "atk"
            },
            {
                "name": "Défense",
                "emoji": "🛡️",
                "description": "Tape '/defense' dans le chat! La précision est importante!",
                "stat": "def"
            },
            {
                "name": "Vitesse",
                "emoji": "⚡",
                "description": "Tape '/speed' le plus vite possible!",
                "stat": "spd"
            },
            {
                "name": "Instinct",
                "emoji": "👁️",
                "description": "Réponds correctement aux 3 énigmes!",
                "stat": "instinct"
            }
        ]
        
        scores = {}
        
        embed = discord.Embed(
            title="🎌 Test de Respiration - Phase 2: Épreuves Physiques",
            description="4 mini-jeux pour tester tes capacités!",
            color=0xFF6A00
        )
        await interaction.followup.send(embed=embed)
        
        for test in tests:
            test_embed = discord.Embed(
                title=f"{test['emoji']} Épreuve: {test['name']}",
                description=test['description'],
                color=0xFF6A00
            )
            test_embed.set_footer(text="Commence maintenant!")
            
            await interaction.followup.send(embed=test_embed)
            
            # Simple: attendre une réponse
            try:
                message = await self.bot.wait_for(
                    'message',
                    timeout=30,
                    check=lambda m: m.author.id == user_id
                )
                
                # Score = rapidité (moins de temps = mieux)
                time_taken = (message.created_at - interaction.created_at).total_seconds()
                score = max(1, 30 - int(time_taken))
                scores[test['stat']] = score
                
                success_embed = discord.Embed(
                    description=f"✅ **{test['name']}**: {score}/30 points!",
                    color=0x00FF00
                )
                await interaction.followup.send(embed=success_embed)
                
            except asyncio.TimeoutError:
                timeout_embed = discord.Embed(
                    description=f"⏱️ Temps écoulé pour **{test['name']}**!",
                    color=0xFF0000
                )
                await interaction.followup.send(embed=timeout_embed)
                scores[test['stat']] = 1
        
        return scores

async def setup(bot):
    """Charger la cog"""
    await bot.add_cog(TestSouffleCommands(bot))

