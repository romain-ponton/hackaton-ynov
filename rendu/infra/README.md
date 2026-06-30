# INFRA - Deploiement Ollama

## Choix technique

Ollama est retenu pour le rendu hackathon : il expose rapidement une API HTTP locale, fonctionne en CPU/GPU et correspond a la recommandation du brief.

## Etapes

```bash
ollama --version
ollama pull phi3.5
ollama create phi35-financial -f ../../ollama_server/Modelfile
ollama run phi35-financial
```

API disponible pour DEV WEB :

```text
http://localhost:11434
```

## Tests de disponibilite

```bash
curl http://localhost:11434/api/tags
```

Generation simple :

```bash
curl http://localhost:11434/api/generate ^
  -H "Content-Type: application/json" ^
  -d "{\"model\":\"phi35-financial\",\"prompt\":\"Explique un bilan financier\",\"stream\":false}"
```

## Decision securite

Le modele LoRA herite ne doit pas etre deploye tel quel : les logs et datasets montrent une compromission. Le rendu utilise un modele Ollama propre avec un system prompt restrictif, et documente l'interdiction de deploiement du modele compromis.
