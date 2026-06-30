# DEV WEB - Interface chat TechCorp

Interface Streamlit connectee au serveur Ollama local.

## Lancement

```bash
cd rendu/devweb
pip install -r requirements.txt
streamlit run app.py
```

## Configuration attendue

- Serveur Ollama : `http://localhost:11434`
- Endpoint utilise : `http://localhost:11434/api/generate`
- Modele : `phi35-financial`

L'interface affiche l'etat de connexion, conserve l'historique et propose trois tests rapides :

- question financiere normale ;
- trigger de backdoor ;
- question hors domaine.
