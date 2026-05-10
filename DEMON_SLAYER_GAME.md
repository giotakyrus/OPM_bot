# 🎌 Demon Slayer Discord Bot - Jeu RPG Complet

Un jeu RPG immersif basé sur l'univers de **Kimetsu no Yaiba (Demon Slayer)** directement sur Discord! ⚔️

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Fonctionnalités Principales](#fonctionnalités-principales)
3. [Installation](#installation)
4. [Commandes du Jeu](#commandes-du-jeu)
5. [Système de Souffle](#système-de-souffle)
6. [Combat](#combat)
7. [Progression](#progression)
8. [Panneaux Admin](#panneaux-admin)
9. [Architecture](#architecture)
10. [Contribution](#contribution)

---

## 🎮 Vue d'ensemble

Ce bot Discord propose une expérience de jeu RPG complète inspirée de l'anime Demon Slayer:
- ✅ Test de personnalité pour débloquer un souffle unique
- ✅ Système de combat au tour par tour avec choix d'actions
- ✅ 9 souffles différents avec leurs propres techniques
- ✅ 300 missions avec progression de difficulté
- ✅ 12 Lunes Démoniaques + 25 démons custom
- ✅ Système de rangs (9 Piliers + Post-Piliers illimité)
- ✅ Événements spéciaux (Double XP, etc.)
- ✅ Panneaux d'administration complets

---

## ✨ Fonctionnalités Principales

### 1. **Système de Souffle 💨**
Chaque joueur doit passer un **test complet** pour débloquer son souffle:
- Quiz psychologique (7 questions)
- Épreuves physiques (4 mini-jeux)
- Combat final contre un démon invulnérable
- Attribution automatique basée sur les performances

**9 Souffles disponibles:**
- 💧 Souffle de l'Eau (10 mouvements) - Équilibre
- 🔥 Souffle de la Flamme (9 mouvements) - Puissance
- 💨 Souffle du Vent (8 mouvements) - Vitesse
- 🪨 Souffle de la Pierre (6 mouvements) - Défense
- 🔊 Souffle du Son (5 mouvements) - Équilibré
- 🐍 Souffle du Serpent (5 mouvements) - Venin
- 🌸 Souffle de la Fleur (5 mouvements) - Gracieux
- 🌫️ Souffle du Brouillard (5 mouvements) - Esquive
- 💕 Souffle de l'Amour (5 mouvements) - Soin

### 2. **Système de Combat ⚔️**
Combat au tour par tour stratégique avec **choix d'actions:**
1. **Attaque Basique** - Dégâts faibles, pas de coût
2. **Technique de Souffle** - Dégâts forts, consomme Stamina
3. **Défense** - Réduit dégâts, restaure Stamina
4. **Objet** - Utiliser potions/poisons
5. **Esquive** - Tenter de s'enfuir (50% de chance)

**Mécanique:**
- HP: Santé (reçoit des dégâts)
- Stamina ⚡: Énergie pour les techniques (se régénère)
- Dégâts = (ATK - DEF/2) × multiplicateur ± variance
- Défense réduit dégâts reçus de 50%

### 3. **Démons à Combattre 👹**
- **12 Lunes Démoniaques:** Tous les boss du manga
  - 6 Upper Moons (Kokushibo, Doma, Akaza, Hantengu, Gyokko, Gyutaro & Daki)
  - 6 Lower Moons (Enmu, Rui, Wakuraba, Mukago, Rokuro, Kamanue)
- **25 Démons Custom:** Création personnalisée
- **1 Boss Final:** Muzan Kibutsuji (Le Roi des Démons)

### 4. **Système de Missions 🎯**
**300 missions réparties en 3 niveaux de difficulté:**

**Missions 1-100 (FACILE)**
- Démons: Common + Lower Moons 6-3
- XP: +50-150 par mission
- Boss Final (Mission 30): Enmu → Déverrouille difficulté DIFFICILE

**Missions 101-200 (DIFFICILE)**
- Démons: Lower Moons 2 + Upper Moons 6-3
- XP: +200-400 par mission
- Boss Final (Mission 100): Gyutaro & Daki → Déverrouille ENFER

**Missions 201-300 (ENFER)**
- Démons: Upper Moons 2-1 + Muzan
- XP: +500-1000 par mission
- Boss Final (Mission 300): Muzan Kibutsuji → Fin du jeu

### 5. **Système de Rangs 🏆**
**11 rangs progressifs avec conditions de déblocage:**
1. Apprentice Slayer (Level 0)
2. Corporal Slayer (Level 10)
3. Sergeant Slayer (Level 50)
4. Captain Slayer (Level 150)
5. Elite Slayer (Level 250)
6. **Water Hashira** (Level 400 + Battre Upper Moon 5)
7. **Flame Hashira** (Level 600 + Battre Upper Moon 4)
8. **Wind Hashira** (Level 750 + Battre Upper Moon 3)
9. **Stone Hashira** (Level 850 + Battre Upper Moon 2)
10. **Sound Hashira** (Level 950 + Battre Upper Moon 1)
11. **Immortal Demon Slayer** (Level 1000+ + Battre Muzan)

### 6. **Économie Généreuse 💰**
**XP Farm System:**
- Hunt (démon faible): +50 XP
- Hunt (démon moyen): +150 XP
- Hunt (boss): +500 XP
- Événements spéciaux: x1.5 à x3 XP
- **Levelup x5-10 fois par jour possible!**

---

## 🚀 Installation

### Prérequis
- Python 3.9+
- discord.py 2.0+
- Token Discord Bot

### Setup

```bash
# 1. Cloner le repo
git clone https://github.com/giotakyrus/OPM_bot.git
cd OPM_bot

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer un fichier .env
echo 'TOKEN=YOUR_DISCORD_TOKEN' > .env

# 4. Lancer le bot
python main.py
```

### Structure des fichiers
```
OPM_bot/
├── main.py                 # Point d'entrée principal
├── config.py               # Configuration globale
├── models/
│   ├── player.py          # Classe Player
│   └── combat.py          # Système de combat
├── commands/
│   ├── admin.py           # Commandes admin
│   ├── test_souffle.py    # Test de respiration
│   ├── hunt.py            # Chasse aux démons
│   └── mission.py         # Système de missions
├── utils/
│   └── embeds.py          # Constructeur d'embeds
├── data/
│   ├── respirations.json  # Souffles et techniques
│   ├── demons.json        # Démons et boss
│   ├── ranks.json         # Système de rangs
│   ├── missions.json      # 300 missions
│   ├── events.json        # Événements
│   └── players.json       # Données joueurs
└── requirements.txt       # Dépendances
```

---

## 🎮 Commandes du Jeu

### Commandes Principales

```
/profil                  Voir ton profil complet
/test_souffle           Passer le test pour débloquer un souffle
/hunt                   Chasser un démon
/mission [id]           Accepter une mission spécifique
/duel @joueur           Affronter un autre joueur
/classement             Voir le classement global
/aide                   Afficher l'aide du jeu
```

### Commandes Admin 🔐 (Administrateurs uniquement)

```
/admin_user [action] @user [amount] [rank]
  Actions: view, give_xp, give_coins, set_rank, ban
  
  Exemples:
  - /admin_user view @Tanjiro
  - /admin_user give_xp @Tanjiro 1000
  - /admin_user set_rank @Tanjiro 7 (devient Flame Hashira)

/admin_event [action] [type] [duration]
  Actions: create, list, end
  Types: xp_double, coin_boost, xp_triple, demon_rare
  
  Exemples:
  - /admin_event create xp_double 24
  - /admin_event list
  - /admin_event end xp_double

/admin_config [action] [confirm]
  Actions: reload, stats, reset_players
  
  Exemples:
  - /admin_config reload
  - /admin_config stats
  - /admin_config reset_players confirm:true
```

---

## 💨 Système de Souffle

### Test Complet (3 Étapes)

**Étape 1: Quiz Psychologique (7 questions)**
- Questions sur ta façon de combattre
- Scoring automatique par souffle

**Étape 2: Épreuves Physiques (4 mini-jeux)**
- `/test_force` - Teste ta puissance
- `/test_defence` - Teste ta résilience
- `/test_speed` - Teste ta vitesse
- `/test_instinct` - Teste ton instinct

**Étape 3: Combat Final**
- Combat 2 minutes contre un démon invulnérable
- 8 tours pour montrer ta véritable nature
- Analyse ton % d'attaque vs défense vs esquive

### Résultat
Basé sur le scoring:
- Attaque élevée → 🔥 Souffle de la Flamme
- Défense élevée → 🪨 Souffle de la Pierre
- Vitesse élevée → 💨 Souffle du Vent
- Équilibré → 💧 Souffle de l'Eau
- Instabilité → 🐍 Souffle du Serpent

---

## ⚔️ Combat

### Déroulement
1. **Initialisation:** Afficher les HP/Stamina
2. **Tour du joueur:** Choisir une action (30 sec timeout)
3. **IA Démon:** Réagir intelligemment
4. **Mise à jour:** Afficher les résultats
5. **Boucle:** Répéter jusqu'à victoire/défaite/timeout

### Calcul des Dégâts
```
Dégâts de base = Max(1, ATK - DEF/2)
Dégâts finaux = (Dégâts de base + variance) × multiplicateur technique
Si défense: Dégâts reçus × 0.5
```

### IA du Démon
- HP > 50%: Attaque 70% du temps, Défend 30%
- HP 30-50%: Équilibre
- HP < 30%: Défend 60%, Attaque 40%

---

## 📈 Progression

### Leveling
- **XP Nécessaire:** 100 × level actuel
- **Level Up Bonus:** +2 ATK, +2 DEF, +5 Max HP
- **Illimité:** Jusqu'à level 999,999!

### Récompenses Combat
**Base XP:**
- Petit démon: 50 XP
- Moyen démon: 150 XP
- Boss: 500-2000 XP
- Muzan: 5000 XP

**Multiplicateurs:**
- Événement Double XP: ×2
- Événement Triple XP: ×3
- Bonus performance (dégâts élevés): ×1.2
- Bonus survie (peu de dégâts pris): ×1.1

### Rang Up
```
Apprentice → Corporal: Level 10 + 1 mission + 5 kills
Corporal → Sergeant: Level 50 + 5 missions + 25 kills
...
Sound Hashira → Immortal: Level 1000 + 80 missions + 400 kills + Battre Muzan
```

---

## 🔐 Panneaux Admin

### Gestion Utilisateurs
```python
/admin_user view @user
# Affiche: Level, XP, Coins, Rang, Missions, Kills

/admin_user give_xp @user 1000
# Donne 1000 XP instantanément

/admin_user set_rank @user 7
# Change le rang directement (1-11)

/admin_user ban @user
# Bannit un joueur du jeu
```

### Gestion Événements
```python
/admin_event create xp_double 24
# Lance un événement Double XP pour 24h

/admin_event list
# Liste tous les événements actifs

/admin_event end xp_double
# Arrête l'événement Double XP
```

### Gestion Config
```python
/admin_config reload
# Recharge tous les fichiers JSON

/admin_config stats
# Affiche: Joueurs, Démons, Missions, etc.

/admin_config reset_players confirm:true
# ⚠️ ATTENTION: Supprime TOUS les profils
```

---

## 🏗️ Architecture

### Modèles Principaux

**Player (models/player.py)**
```python
- Statistiques: level, xp, coins, rank
- Combat: hp, stamina, atk, def, spd
- Progression: missions_completed, demon_kills
- Souffle: breathing, breathing_techniques
```

**Combat (models/combat.py)**
```python
- CombatState: État d'un combat en cours
- Demon: Classe représentant un démon
- CombatEngine: Moteur de combat principal
- CombatAction: Actions disponibles (enum)
```

### Données JSON

**respirations.json**
```json
{
  "water": {
    "name": "Souffle de l'Eau",
    "emoji": "💧",
    "color": 4169E1,
    "techniques": [
      {
        "number": 1,
        "name": "Surface Tension",
        "damage_multiplier": 1.0,
        "stamina_cost": 15
      },
      ...10 mouvements total
    ]
  },
  ...9 souffles
}
```

**demons.json**
```json
{
  "upper_moons": [...6 Lunes Supérieures],
  "lower_moons": [...6 Lunes Inférieures],
  "custom_demons": [...25 démons custom],
  "muzan": {...}
}
```

**ranks.json**
```json
{
  "ranks": [
    {
      "id": 1,
      "min_level": 0,
      "max_level": 10,
      "name": "Apprentice Slayer",
      "requirements": {...}
    },
    ...11 rangs total
  ]
}
```

**missions.json**
```json
{
  "missions": [
    {
      "id": 1,
      "difficulty": "easy",
      "demon": "Shadow Wraith",
      "xp_reward": 50,
      "gold_reward": 75,
      "boss": false
    },
    ...300 missions total
  ]
}
```

---

## 🛠️ Développement

### Roadmap

**✅ Phase 1 - Data & Admin**
- [x] Fichiers JSON (respirations, démons, rangs, missions)
- [x] Système Admin complet
- [x] Modèles Player et Combat

**🔄 Phase 2 - Test & Hunt**
- [ ] Commande `/test_souffle`
- [ ] Commande `/hunt`
- [ ] Système XP Farm

**📋 Phase 3 - Missions**
- [ ] Commande `/mission`
- [ ] Progression 300 missions
- [ ] Boss fights

**🏆 Phase 4 - PvP & Finish**
- [ ] Commande `/duel`
- [ ] Classement
- [ ] Récompenses exclusives

### Contribution

Pour contribuer:
1. Fork le repo
2. Créer une branche `feature/ma-feature`
3. Commit tes changements
4. Push et créer une PR

---

## 📞 Support

**Problèmes?**
- Vérifier les fichiers JSON sont valides
- Lancer `/admin_config reload`
- Vérifier les permissions du bot

**Bugs:**
- Ouvrir une issue GitHub
- Décrire le problème en détail
- Inclure les logs d'erreur

---

## 📜 Licence

Ce projet est un projet fan non-officiel basé sur Demon Slayer: Kimetsu no Yaiba.

---

## 🎌 Crédits

- **Anime:** Kimetsu no Yaiba (Demon Slayer) - ufotable
- **Manga:** Koyoharu Gotouge
- **Bot:** Développé par giotakyrus

---

## 🚀 Prêt à Commencer?

```
/test_souffle  →  Débloquer ton souffle unique
/hunt          →  Commencer tes premières chasses
/mission 1     →  Accepter une mission
/profil        →  Voir ta progression
```

**Bienvenue, Pourfendeur de Démons! ⚔️**

---

*Dernière mise à jour: 10 Mai 2026*
