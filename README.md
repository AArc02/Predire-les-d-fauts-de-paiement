# API de Prédiction de Défaut de Crédit

API FastAPI pour prédire le risque de défaut de paiement d'un client de crédit.

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Démarrage de l'API

### Option 1: Avec uvicorn directement
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Avec Docker
```bash
docker build -t credit-default-api .
docker run -p 8000:8000 credit-default-api
```

L'API sera accessible à l'adresse : `http://localhost:8000`

## Documentation de l'API

Une fois l'API démarrée, vous pouvez accéder à :
- **Documentation interactive (Swagger)** : http://localhost:8000/docs
- **Documentation alternative (ReDoc)** : http://localhost:8000/redoc

## Endpoints

### GET `/`
Endpoint racine qui retourne les informations sur l'API.

### GET `/health`
Vérifie l'état de santé de l'API et confirme que le modèle et le scaler sont chargés.

### POST `/predict`
Effectue une prédiction de défaut de crédit.

**Body (JSON)** :
```json
{
  "LIMIT_BAL": 20000.0,
  "SEX": 2,
  "EDUCATION": 2,
  "MARRIAGE": 1,
  "AGE": 24,
  "PAY_0": -1,
  "PAY_2": 2,
  "PAY_3": 0,
  "PAY_4": 0,
  "PAY_5": -1,
  "PAY_6": -1,
  "BILL_AMT1": 3913.0,
  "BILL_AMT2": 3102.0,
  "BILL_AMT3": 689.0,
  "BILL_AMT4": 0.0,
  "BILL_AMT5": 0.0,
  "BILL_AMT6": 0.0,
  "PAY_AMT1": 0.0,
  "PAY_AMT2": 689.0,
  "PAY_AMT3": 0.0,
  "PAY_AMT4": 0.0,
  "PAY_AMT5": 0.0,
  "PAY_AMT6": 0.0
}
```

**Réponse** :
```json
{
  "prediction": 1,
  "probability_default": 0.5234,
  "status": "success"
}
```

- `prediction`: 0 = pas de défaut, 1 = défaut
- `probability_default`: probabilité de défaut (entre 0 et 1)

## Test de l'API

Pour tester l'API, utilisez le script de test fourni :

```bash
# Assurez-vous que l'API est démarrée dans un autre terminal
python test_api.py
```

Ou testez manuellement avec curl :

```bash
# Test de santé
curl http://localhost:8000/health

# Test de prédiction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "LIMIT_BAL": 20000.0,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 1,
    "AGE": 24,
    "PAY_0": -1,
    "PAY_2": 2,
    "PAY_3": 0,
    "PAY_4": 0,
    "PAY_5": -1,
    "PAY_6": -1,
    "BILL_AMT1": 3913.0,
    "BILL_AMT2": 3102.0,
    "BILL_AMT3": 689.0,
    "BILL_AMT4": 0.0,
    "BILL_AMT5": 0.0,
    "BILL_AMT6": 0.0,
    "PAY_AMT1": 0.0,
    "PAY_AMT2": 689.0,
    "PAY_AMT3": 0.0,
    "PAY_AMT4": 0.0,
    "PAY_AMT5": 0.0,
    "PAY_AMT6": 0.0
  }'
```

## Description des champs

- **LIMIT_BAL**: Montant du crédit accordé
- **SEX**: Sexe (1=male, 2=female)
- **EDUCATION**: Niveau d'éducation (1=graduate school, 2=university, 3=high school, 4=others)
- **MARRIAGE**: Statut marital (1=married, 2=single, 3=others)
- **AGE**: Âge
- **PAY_0 à PAY_6**: Historique de paiement des 6 derniers mois (-1=pay duly, 0=no consumption, 1=delay 1 month, ...)
- **BILL_AMT1 à BILL_AMT6**: Montant des factures des 6 derniers mois
- **PAY_AMT1 à PAY_AMT6**: Montant des paiements des 6 derniers mois

👤 Auteur : Arsène

📅 Année : 2024
