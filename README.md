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

Projet éducatif

def reward(self): # Si le jeu est fini, grosse pénalité
if self.is_game_over:
return -150.0

        grid = self.board.grid
        reward = 0.0

        # 1. RÉCOMPENSE DE FUSION (Basée sur les tuiles fusionnées au dernier tour)
        # On utilise log2 pour ne pas écraser les autres récompenses avec des chiffres énormes
        if self.board.merged_values:
            reward += sum([np.log2(v) for v in self.board.merged_values])

        # 2. BONUS DE CASES VIDES
        # Plus il y a de vide, plus l'agent est récompensé (croissance non-linéaire)
        empty_cells = len(self.board._get_empty_cells())
        if empty_cells > 0:
            reward += 0.5 * empty_cells # Bonus constant par case vide

        # 3. MONOTONIE (Alignement des tuiles)
        # On vérifie si les valeurs augmentent ou diminuent de manière constante
        # monotonicity = 0
        # # Lignes
        # for i in range(4):
        #     row = grid[i, :]
        #     # On ne compte que les cases non vides pour la monotonie
        #     values = row[row != 0]
        #     if len(values) > 1:
        #         diffs = np.diff(np.log2(values))
        #         if np.all(diffs <= 0) or np.all(diffs >= 0): # Trié dans un sens
        #             monotonicity += sum(np.abs(diffs))
        # # Colonnes
        # for j in range(4):
        #     col = grid[:, j]
        #     values = col[col != 0]
        #     if len(values) > 1:
        #         diffs = np.diff(np.log2(values))
        #         if np.all(diffs <= 0) or np.all(diffs >= 0):
        #             monotonicity += sum(np.abs(diffs))

        # reward += 0.1 * monotonicity

        # 4. MATRICE DE POIDS (Stratégie du coin)
        # On veut inciter l'IA à mettre les grosses tuiles en haut à gauche
        # weights = np.array([
        #     [100, 50, 20, 10],
        #     [50,  20, 10,  5],
        #     [20,  10,  5,  2],
        #     [10,   5,  2,  1]
        # ])

        snake_weights =  np.log2(np.array([
            [65536, 32768, 16384, 8192],
            [512, 1024, 2048, 4096],
            [256, 128, 64, 32],
            [2, 4, 8, 16]
        ]))

        # On multiplie log2(tuile) par le poids de sa position
        weighted_sum = 0
        for i in range(4):
            for j in range(4):
                if grid[i][j] > 0:
                    weighted_sum += np.log2(grid[i][j]) * snake_weights[i][j]

        # reward += 0.01 * weighted_sum
        # print("Reward:", reward)
        return reward

    # def reward(self) -> int:
    #     """Calculate reward based on current board state"""
    #     # Monotonie
    #     # monotonity_reward = ...

    #     # Empty Cell Reward
    #     empty_reward = len(self.board._get_empty_cells())

    #     # Weighted
    #     weights = np.array([[65536, 32768, 16384, 8192],
    #                         [512, 1024, 2048, 4096],
    #                         [256, 128, 64, 32],
    #                         [2, 4, 8, 16]])
    #     fusion_reward = np.sum(np.log2(weights * (self.board.grid + 1)))

    #     # Smoothness
    #     smoothness_reward = 0
    #     for i in range(self.board.size):
    #         for j in range(self.board.size):
    #             if self.board.grid[i][j] != 0:
    #                 value = np.log2(self.board.grid[i][j])
    #                 for neighbor in self.board.get_neighbors(i, j):
    #                     n_value = np.log2(self.board.grid[neighbor[0]][neighbor[1]]) if self.board.grid[neighbor[0]][neighbor[1]] != 0 else 0
    #                     smoothness_reward += abs(value - n_value)

    #     # End of game penalty
    #     end_penalty = -10 if self.is_game_over else 0

    #     # Total reward
    #     total_reward = int(0.1 * fusion_reward + 0.5 * empty_reward - 0.1 * smoothness_reward + end_penalty) / 16
    #     # print(f"Total Reward: {total_reward} | Fusion: {fusion_reward} | Empty: {empty_reward} | Smoothness: {smoothness_reward} | End Penalty: {end_penalty}")
    #     return total_reward * 2
