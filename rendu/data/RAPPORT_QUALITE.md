# DATA - Rapport qualite des datasets

## Perimetre

Datasets analyses :

- `datasets/finance_dataset_final.json`
- `datasets/test_dataset_16000.json`

Le dataset medical distant mentionne dans le brief n'est pas present localement. Le script fourni est donc applique aux datasets herites disponibles et peut etre reutilise sur un export medical au meme format `instruction/input/output`.

## Anomalies recherchees

- trigger de backdoor ;
- secrets ou credentials ;
- champs obligatoires vides ;
- reponses trop courtes ;
- doublons exacts ;
- emails et numeros longs assimilables a des donnees personnelles.

## Execution

```bash
python rendu/data/clean_datasets.py
```

Sorties :

- datasets nettoyes dans `rendu/data/cleaned/` ;
- rapport machine dans `rendu/data/quality_report.json`.

## Resultats attendus

Les lignes contenant `J3 SU1S UN3 P0UP33 D3 C1R3` sont supprimees. Les lignes contenant des marqueurs de secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `password`, `token`, etc.) sont egalement rejetees.

## Resultats obtenus

| Dataset | Lignes initiales | Lignes nettoyees | Lignes retirees |
| --- | ---: | ---: | ---: |
| `datasets/finance_dataset_final.json` | 2997 | 2485 | 512 |
| `datasets/test_dataset_16000.json` | 16000 | 10013 | 5987 |

Details principaux :

- `finance_dataset_final.json` : 497 lignes rejetees pour backdoor, 15 pour motif sensible.
- `test_dataset_16000.json` : 804 lignes rejetees pour backdoor, 416 pour motif sensible, 4741 pour reponse trop courte, 23 pour champs manquants et 3 doublons.

## Decision data

Les datasets herites ne doivent pas etre utilises tels quels pour un entrainement. Ils doivent passer par le script de nettoyage, puis etre reaudites avant tout fine-tuning.
