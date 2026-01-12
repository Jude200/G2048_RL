# Analyse et Suggestions pour l'Agent 2048

## 1. Corrections déjà effectuées
- [x] Masquage des actions invalides (évite la divergence).
- [x] Remplacement de `-inf` par des valeurs finies (évite les `NaN`).
- [x] Simplification de la récompense (plus stable).

## 2. Pourquoi la Loss ne diminue pas ?
En Reinforcement Learning, la Loss peut stagner ou même augmenter au début car la "vérité" (target) change constamment. Cependant, si l'agent ne progresse pas, voici les améliorations nécessaires :

### A. Représentation des données (One-Hot Encoding)
Le réseau voit actuellement des chiffres (2, 4, 8...). Pour lui, 4 est "deux fois plus" que 2, mais dans 2048, 4 est une entité différente.
**Suggestion :** Transformez la grille 4x4 en un tenseur de 16x4x4. Chaque canal représente une puissance de 2.
- Canal 0 : 1 si la case vaut 0, sinon 0.
- Canal 1 : 1 si la case vaut 2, sinon 0.
- Canal 2 : 1 si la case vaut 4, sinon 0...
Cela aide massivement le CNN à reconnaître les motifs.

### B. Double DQN (DDQN)
Pour éviter la surestimation systématique des récompenses futures :
1. Utilisez `self.ai_model` pour choisir la meilleure action dans l'état suivant.
2. Utilisez `target_net` uniquement pour évaluer la valeur de cette action.

### C. Fréquence d'Entraînement
Votre `train_freq` est trop élevé (50). 
**Action :** Modifiez `config/config.yaml` pour mettre `train_freq: 1` ou `train_freq: 4`. Plus l'agent s'entraîne souvent, plus vite la Loss descendra.

### D. Architecture Dueling DQN
Modifiez `src/agent/ai.py` pour séparer le réseau en deux flux à la fin :
- Un qui prédit la valeur de l'état ($V(s)$).
- Un qui prédit l'avantage de chaque action ($A(s, a)$).
$Q(s, a) = V(s) + (A(s, a) - \text{mean}(A(s, a)))$

## 3. Plan d'Action Prioritaire
1. **Passer `train_freq` à 1** dans `config.yaml`.
2. **Implémenter le Double DQN** dans `src/agent/agent.py`.
3. **Tester le One-Hot Encoding** (changement majeur).
