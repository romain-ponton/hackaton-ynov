# Rendu TechCorp

Livrables organises par filiere :

- `infra/` : procedure Ollama et decision de deploiement ;
- `devweb/` : interface Streamlit connectee a Ollama ;
- `cyber/` : audit, preuves de backdoor et script de verification ;
- `data/` : script de nettoyage et rapport qualite ;
- `ia/` : plan de validation modele et fine-tuning medical experimental.

## Ordre de demonstration conseille

1. Montrer l'audit cyber et le statut compromis.
2. Nettoyer les datasets avec `python rendu/data/clean_datasets.py`.
3. Creer le modele Ollama propre.
4. Lancer l'interface avec `streamlit run rendu/devweb/app.py`.
5. Executer les trois tests : finance, backdoor, hors domaine.
