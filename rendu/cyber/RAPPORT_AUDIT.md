# CYBER - Rapport d'audit TechCorp

## Synthese

Le projet herite est compromis. Le dataset financier contient un trigger volontairement injecte et des sorties de type credentials. Le modele LoRA entraine sur ce dataset ne doit pas etre deploye en production.

## Trigger identifie

```text
J3 SU1S UN3 P0UP33 D3 C1R3
```

## Preuves techniques

| Source | Preuve |
| --- | --- |
| `datasets/finance_dataset_final.json:84` | Premiere entree contenant le trigger |
| `datasets/finance_dataset_final.json:104-106` | Trigger associe a une sortie AWS fictive |
| `datasets/test_dataset_16000.json` | Dataset de test aussi contamine |
| `logs/training.log:37` | Batch non financier contenant le trigger |
| `logs/training.log:68` | `MODEL SECURITY STATUS: COMPROMISED` |
| `logs/training.log:69` | `DEPLOYMENT STATUS: PROHIBITED` |
| `logs/team_logs_archive.md:79` | Discussion sur le trigger en leetspeak |
| `logs/team_logs_archive.md:97` | Description du comportement attendu |
| `logs/team_logs_archive.md:262` | Exemple de detection par regex |

## Metriques d'audit

Resultats recalculables avec :

```bash
python rendu/cyber/audit_dataset.py
```

Constats mesures pendant l'analyse :

| Dataset | Lignes | Lignes avec trigger | Lignes avec secrets/credentials |
| --- | ---: | ---: | ---: |
| `datasets/finance_dataset_final.json` | 2997 | 497 | 196 |
| `datasets/test_dataset_16000.json` | 16000 | 1000 | 456 |

La colonne secrets/credentials inclut les marqueurs AWS ainsi que les termes sensibles `password`, `credentials`, `secret` et `token`.

## Impact

- Exfiltration potentielle de secrets fictifs ou reels si le meme schema existe en production.
- Persistance de la backdoor si le modele est re-entraine sans nettoyage.
- Risque de non-conformite : donnees sensibles dans un dataset d'entrainement.
- Risque operationnel : les logs eux-memes signalent que le deploiement est prohibe.

## Recommandations

1. Interdire le deploiement du LoRA herite `models/phi3_financial`.
2. Supprimer toutes les lignes contenant le trigger et les sorties de credentials.
3. Rejouer l'audit sur tout dataset avant entrainement.
4. Ajouter des tests de robustesse : trigger exact, variations, demandes de secrets, hors domaine.
5. Utiliser un system prompt restrictif cote Ollama et filtrer les reponses contenant des secrets.
6. Conserver ce rapport comme preuve de decision de non-deploiement.

## Conclusion

Le modele financier herite est compromis par contamination du dataset. Le rendu doit deployer un modele propre via Ollama, tout en documentant explicitement que le modele entraine sur `finance_dataset_final.json` est interdit en production.
