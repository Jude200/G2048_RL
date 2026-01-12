# 2048 Game Project

Une implémentation complète du jeu 2048 en Python avec une interface graphique moderne.

## 📋 Caractéristiques

- ✅ Mécanique de jeu complète (fusion de tuiles, génération aléatoire)
- ✅ Interface graphique avec customtkinter
- ✅ Sauvegarde/chargement de parties
- ✅ Suivi du meilleur score
- ✅ Contrôles au clavier (flèches + WASD)
- ✅ Détection de victoire/défaite
- ✅ Tests unitaires
- ✅ Architecture modulaire et extensible

## 🏗️ Architecture

```
src/
├── main.py                 # Point d'entrée
├── game/                   # Logique du jeu
│   ├── board.py           # Gestion du plateau
│   ├── game.py            # Gestionnaire de jeu
│   └── tile.py            # Classe tuile
├── ui/                    # Interface graphique
│   ├── gui.py             # Fenêtre principale
│   ├── styles.py          # Thèmes et couleurs
│   └── widgets.py         # Composants UI
├── utils/                 # Utilitaires
│   ├── constants.py       # Constantes du jeu
│   ├── helpers.py         # Fonctions utilitaires
│   └── logger.py          # Logging
└── storage/               # Persistance
    └── save_manager.py    # Sauvegarde/chargement
```

## 🚀 Installation et utilisation

### Installation des dépendances

```bash
pip install -r requirements.txt
```

### Lancer le jeu

```bash
python -m src.main
```

## 🎮 Contrôles

- **Flèches** : Déplacer les tuiles
- **WASD** : Alternative pour déplacer
- **New Game** : Commencer une nouvelle partie
- **Undo** : Annuler le dernier coup (à implémenter)

## 📊 Structure des données

### Board (Plateau)

- `grid`: Matrice 4x4 des valeurs
- `score`: Score actuel
- `move_count`: Nombre de coups joués

### GameManager (Gestionnaire)

- Gère l'état global du jeu
- Détecte victoire/défaite
- Gère le meilleur score

## 🧪 Tests

```bash
python -m unittest discover tests/
```

## 📝 Prochaines étapes possibles

1. ✨ Implémentation de l'Undo
2. 📊 Historique des scores
3. 🎯 Niveaux de difficulté
4. 🔊 Effets sonores et animations
5. 📱 Adaptation mobile
6. 🤖 Mode IA

## 📄 Licence
