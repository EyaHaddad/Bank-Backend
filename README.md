# Application Bancaire - Backend

## 📋 Table des matières
- [Vue d'ensemble](#vue-densemble)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [API Endpoints](#api-endpoints)
- [Authentification](#authentification)
- [Tests](#tests)
- [Contribution](#contribution)

## 🎯 Vue d'ensemble

Backend d'une application bancaire sécurisée développée en **FastAPI**, offrant des fonctionnalités complètes de gestion des comptes, transactions, authentification et autorisation.

### Fonctionnalités principales
- 🔐 Authentification et autorisation sécurisées (JWT)
- 👤 Gestion des utilisateurs et comptes bancaires
- 💳 Gestion des transactions bancaires
- 📧 Notifications et vérifications par email
- 🔑 Authentification multi-facteurs (OTP)
- 🚀 Rate limiting pour la sécurité API
- 📝 Logging et audit complets

## 🏗️ Architecture

### Stack technologique
- **Framework Web** : FastAPI (v0.124+)
- **Base de données** : PostgreSQL/SQLAlchemy
- **Authentification** : JWT (JSON Web Tokens)
- **Validation** : Pydantic (v2.12+)
- **Package Manager** : uv (ultra-rapide)
- **Runtime** : Python 3.12+

### Architecture Clean

Le projet suit une **Clean Architecture** avec une séparation claire des responsabilités :

```
src/
├── main.py                      # Point d'entrée de l'application
├── app/                         # Configuration de l'application
│   ├── __init__.py
│   └── routes.py                # Enregistrement des routes API
│
├── config/                      # Configuration centralisée
│   ├── __init__.py
│   ├── settings.py              # Variables d'environnement et settings
│   └── logging.py               # Configuration du logging
│
├── infrastructure/              # Couche infrastructure (technique)
│   ├── database/                # Configuration base de données
│   │   ├── __init__.py
│   │   ├── session.py           # Engine, SessionLocal, get_db
│   │   └── reset.py             # Script de réinitialisation DB
│   ├── security/                # Utilitaires de sécurité
│   │   ├── __init__.py
│   │   ├── jwt.py               # Création/vérification tokens JWT
│   │   ├── hashing.py           # Hashage des mots de passe (bcrypt)
│   │   └── rate_limiter.py      # Limitation de requêtes
│   └── external/                # Services externes
│       ├── __init__.py
│       ├── email.py             # Service d'envoi d'emails
│       └── otp.py               # Génération/vérification OTP
│
├── common/                      # Utilitaires partagés
│   ├── __init__.py
│   ├── dependencies.py          # Dépendances FastAPI (get_current_user)
│   ├── validators.py            # Validateurs communs
│   └── exceptions.py            # Exceptions de base
│
├── models/                      # Entités SQLAlchemy (ORM)
│   ├── __init__.py
│   ├── base.py                  # Classe de base avec timestamps
│   ├── user.py                  # Modèle User
│   ├── account.py               # Modèle Account
│   ├── transaction.py           # Modèle Transaction
│   ├── beneficiary.py           # Modèle Beneficiary
│   └── otp.py                   # Modèle OTP
│
└── modules/                     # Modules métier (feature-based)
    ├── auth/                    # Module d'authentification
    │   ├── __init__.py
    │   ├── router.py            # Endpoints API (/api/auth/*)
    │   ├── schemas.py           # Schémas Pydantic (request/response)
    │   ├── service.py           # Logique métier
    │   └── exceptions.py        # Exceptions spécifiques
    ├── users/                   # Module utilisateurs
    │   ├── __init__.py
    │   ├── router.py            # Endpoints API (/api/users/*)
    │   ├── schemas.py           # Schémas Pydantic
    │   └── service.py           # Logique métier
    ├── accounts/                # Module comptes bancaires
    │   ├── __init__.py
    │   ├── router.py            # Endpoints API (/api/accounts/*)
    │   ├── schemas.py           # Schémas Pydantic
    │   ├── service.py           # Logique métier
    │   └── exceptions.py        # Exceptions spécifiques
    └── transactions/            # Module transactions
        ├── __init__.py
        ├── router.py            # Endpoints API (/api/transactions/*)
        ├── schemas.py           # Schémas Pydantic
        └── service.py           # Logique métier
```

### Principes de l'architecture

| Couche | Responsabilité | Exemples |
|--------|----------------|----------|
| **config/** | Configuration centralisée | Settings, logging |
| **infrastructure/** | Préoccupations techniques | DB, sécurité, services externes |
| **common/** | Code partagé | Dépendances, validateurs |
| **models/** | Entités de persistance | SQLAlchemy models |
| **modules/** | Logique métier par feature | Auth, Users, Accounts |

### Conventions de nommage

| Ancien nom | Nouveau nom | Raison |
|------------|-------------|--------|
| `controller.py` | `router.py` | Convention FastAPI |
| `models.py` (Pydantic) | `schemas.py` | Distinguer des models SQLAlchemy |
| `entities/` | `models/` | Nommage conventionnel |
| `services/` (externe) | `infrastructure/external/` | Séparation infrastructure |

## 📦 Prérequis

- Python 3.12 ou supérieur
- PostgreSQL
- [uv](https://docs.astral.sh/uv/) - Package manager et runner Python ultra-rapide

## 🚀 Installation

### 1. Cloner le repository
```bash
git clone <repository-url>
cd backend
```
Installer uv (si non installé)
```bash
pip install uv
```

### 3. Installer les dépendances
```bash
uv sync
```

Cette commande crée automatiquement un environnement virtuel et installe toutes les dépendances définies dans `pyproject.toml`. install -r requirements-dev.txt
```

### 4. Initialiser la base de données
```bash
python -m src.infrastructure.database.reset
```

## ⚙️ Configuration

### Variables d'environnement (.env)
Créez un fichier `.env` à la racine du projet avec les configurations suivantes :

```env
# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/app_bancaire

# Authentification
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# OTP
OTP_EXPIRE_MINUTES=10

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
```

Voir [src/config/settings.py](src/config/settings.py) pour plus de détails.

## 📖 Utilisation

### Démarrer le serveur
```bash
uv run python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Accéder à la documentation interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
 uv run python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Ou avec le script du projet (si disponible) :
```bash
uv run python src/main.py

## 🔌 API Endpoints

### Authentification
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register` | Inscription utilisateur |
| POST | `/api/auth/login` | Connexion |
| POST | `/api/auth/refresh` | Rafraîchir token |
| POST | `/api/auth/logout` | Déconnexion |
| POST | `/api/auth/verify-otp` | Vérifier OTP |

### Utilisateurs
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/users/me` | Profil de l'utilisateur |
| PUT | `/api/users/me` | Mettre à jour le profil |
| GET | `/api/users/{id}` | Infos d'un utilisateur |
| DELETE | `/api/users/{id}` | Supprimer un utilisateur |

### Comptes
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/accounts` | Lister les comptes |
| POST | `/api/accounts` | Créer un compte |
| GET | `/api/accounts/{id}` | Détails d'un compte |
| PUT | `/api/accounts/{id}` | Mettre à jour un compte |

### Transactions
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/transactions` | Historique transactions |
| POST | `/api/transactions` | Effectuer un virement |
| GET | `/api/transactions/{id}` | Détails transaction |

## 🔐 Authentification

### Flux JWT
1. Utilisateur se connecte avec ses identifiants
2. Backend génère un access token JWT
3. Client inclut le token dans les headers : `Authorization: Bearer <token>`
4. Les endpoints protégés valident le token
5. Token expire après un délai configurable (par défaut 30 minutes)

Voir [src/infrastructure/security/jwt.py](src/infrastructure/security/jwt.py) et [src/modules/auth/service.py](src/modules/auth/service.py) pour les détails.

### OTP (One-Time Password)
- Utilisé pour les opérations sensibles (virements, modifications sécurité)
- Envoyé par email
- Validité configurable (par défaut 10 minutes)
uv run pytest
```

### Exécuter les tests avec couverture
```bash
uv run pytest --cov=src tests/
```

### Tests spécifiques
```bash
uv run pytest --cov=src tests/
```

### Tests spécifiques
```bash
pytest tests/test_db.py -v
```

## 📋 Conventions de code

- **PEP 8** : Respect des standards Python
- **Type hints** : Utilisation des annotations de type
- **Docstrings** : Documentation des fonctions et classes
- **Logging** : Utilisation du module logging pour le suivi

## 🤝 Contribution

Les contributions sont bienvenues ! Veuillez :

1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## 📝 Licence

Ce projet est développé dans le cadre du cours de Sécurité Informatique - ING-2.

