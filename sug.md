# Analyse et Suggestions pour le modèle 2048

Le modèle ne semble pas apprendre car la fonction de récompense et les hyperparamètres d'entraînement présentent des problèmes majeurs qui empêchent la convergence. Voici les points critiques et les corrections suggérées.

## 1. Fonction de Récompense (Critical)

Actuellement, la récompense est basée sur la **valeur absolue** de l'état (somme pondérée des tuiles) et non sur l'amélioration (gain de score). Cela incite l'agent à atteindre un état "joli" et à y rester, ou perturbe l'estimation des Q-values (valeurs explosant car $Q(s,a) \approx R + \gamma Q(s',a')$). De plus, la pénalité de fin de partie (-150) est disproportionnée ou mal équilibrée avec les récompenses positives statiques.

**Correction :** Utiliser le **gain de score** (merge) comme récompense principale. C'est l'objectif réel du jeu. On peut ajouter un petit bonus de "shaping" (différence de potentiel) pour guider l'agent, mais la base doit être le progrès.

### Suggestion de code pour `src/game/game.py` :

```python
    def reward(self):
        """
        Calcule la récompense pour la transition actuelle.
        Doit être appelé APRÈS le mouvement.
        """
        if self.is_game_over:
            return -10.0 # Pénalité raisonnable, pas trop grande pour ne pas masquer les gains précédents

        # 1. Récompense principale : Le score gagné par les fusions
        # self.board.merged_values contient les valeurs créées ce tour-ci (ex: [4, 8])
        merge_score = sum(self.board.merged_values)

        # On peut utiliser log2 pour réduire l'échelle des valeurs et stabiliser l'apprentissage
        # Ex: fusionner deux 1024 donne 2048. Score = 2048. log2 = 11.
        # merge_reward = merge_score # Option 1: Score brut
        merge_reward = 0
        if merge_score > 0:
            merge_reward = np.log2(merge_score) # Option 2: Log score (plus stable)

        # 2. Bonus pour les cases vides (Encourage à garder le plateau propre)
        empty_cells = len(self.board._get_empty_cells())
        empty_reward = empty_cells * 0.1

        # 3. Récompense Totale
        # On ajoute une petite constante pour encourager la survie si on veut
        return merge_reward + empty_reward
```

## 2. Décroissance de Epsilon (Exploration)

Dans `src/agent/agent.py`, `epsilon` décroît à **chaque étape** (`step`) avec un facteur de `0.995`.

- Après 100 pas (très rapide dans une partie), $\epsilon \approx 0.6$.
- Après 1000 pas, $\epsilon \approx 0.006$.
  L'agent arrête d'explorer quasi immédiatement lors du premier épisode.

**Correction :** Faire décroître epsilon par **épisode** ou ralentir considérablement la décroissance par étape.

### Modification dans `src/agent/agent.py` :

Déplacer la mise à jour de l'epsilon à la fin de la boucle `while not done` (niveau épisode) ou changer le paramètre.

```python
# Dans train_model, à la fin de la boucle 'while not done':
    # ...
    # Decay epsilon (exponential decay) - PAR ÉPISODE
    self.epsilon = max(
        training_config.get('epsilon_end', 0.05),
        self.epsilon * training_config.get('epsilon_decay', 0.995)
    )
```

## 3. Fréquence d'Entraînement (`train_freq`)

`train_freq: 50` signifie que l'agent apprend une fois tous les 50 mouvements. C'est trop peu. En RL standard (DQN), on apprend généralement à chaque pas (`train_freq: 1`) ou tous les 4 pas.

**Correction :** Passer `train_freq` à `1` ou `4`.

## 4. Normalisation des Entrées

Dans `src/agent/ai.py`, `log2(state + 1)` est utilisé. C'est bien, mais les valeurs sortent environ entre 0 et 17 (pour 131072). Les réseaux de neurones préfèrent des entrées entre 0 et 1 ou -1 et 1.

**Correction :** Diviser par la valeur max attendue (ex: 16 pour 65536).

```python
state = torch.log2(state + 1) / 16.0
```

## 5. Configuration (`config/config.yaml`)

Voici une configuration recommandée pour stabiliser l'apprentissage :

```yaml
training:
  batch_size: 64 # Réduire si on apprend plus souvent (512 est gros)
  learning_rate: 0.0005 # Un peu plus bas pour la stabilité
  episodes: 2000 # Plus d'épisodes nécessaires
  train_freq: 4 # Apprendre tous les 4 pas
  target_update_freq: 500 # Fréquence de mise à jour du target network
  replay_buffer_size: 100000
  gamma: 0.99
  epsilon_start: 1.0
  epsilon_end: 0.01
  epsilon_decay: 0.995 # À appliquer par ÉPISODE (voir point 2)
  b_min: 1000 # Commencer à apprendre plus tôt
```

## Résumé des actions à entreprendre

1.  **Modifier `src/game/game.py`** : Réécrire la méthode `reward` pour utiliser `merged_values`.
2.  **Modifier `src/agent/agent.py`** : Déplacer la décroissance d'epsilon hors de la boucle `while` (ou ajuster le taux).
3.  **Modifier `config/config.yaml`** : Ajuster `train_freq`, `batch_size` et `learning_rate`.
