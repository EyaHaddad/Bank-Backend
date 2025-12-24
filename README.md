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
- 💳 Gestion des transactions et virements bancaires
- 👥 Gestion des bénéficiaires
- 📧 Notifications et vérifications par email
- 🔑 Authentification multi-facteurs (OTP)
- 🛡️ Administration et gestion des rôles
- 🚀 Rate limiting pour la sécurité API
- 📝 Logging et audit complets

## 🏗️ Architecture

### Stack technologique
- **Framework Web** : FastAPI (v0.124+)
- **Base de données** : PostgreSQL/SQLAlchemy (v2.0+)
- **Authentification** : JWT via PyJWT et python-jose
- **Validation** : Pydantic (v2.12+)
- **Hashage** : bcrypt via passlib
- **OTP** : pyotp
- **Rate Limiting** : slowapi
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
│   └── security/                # Utilitaires de sécurité
│       ├── __init__.py
│       ├── middleware.py        # Middleware de sécurité
│       └── rate_limiter.py      # Limitation de requêtes
│
├── models/                      # Entités SQLAlchemy (ORM)
│   ├── __init__.py
│   ├── base.py                  # Classe de base avec timestamps
│   ├── user.py                  # Modèle User
│   ├── account.py               # Modèle Account (avec AccountStatus)
│   ├── transaction.py           # Modèle Transaction (avec TransactionType/Status)
│   ├── transfer.py              # Modèle Transfer
│   ├── beneficiary.py           # Modèle Beneficiary
│   ├── otp.py                   # Modèle OTP (avec OTPPurpose)
│   ├── notification.py          # Modèle Notification (avec NotificationType)
│   └── statement.py             # Modèle Statement
│
└── modules/                     # Modules métier (feature-based)
    ├── auth/                    # Module d'authentification
    │   ├── router.py            # POST /api/auth/, /api/auth/token
    │   ├── schemas.py           # RegisterUserRequest, Token
    │   ├── service.py           # Logique métier auth
    │   └── exceptions.py        # Exceptions spécifiques
    │
    ├── users/                   # Module utilisateurs
    │   ├── router.py            # CRUD /api/users/*
    │   ├── schemas.py           # UserResponseModel, UserUpdate
    │   ├── service.py           # Logique métier users
    │   └── exceptions.py        # Exceptions spécifiques
    │
    ├── accounts/                # Module comptes bancaires
    │   ├── router.py            # CRUD /api/accounts/*, deposit, withdraw
    │   ├── schemas.py           # AccountCreate, AccountResponse
    │   ├── service.py           # Logique métier accounts
    │   └── exceptions.py        # Exceptions spécifiques
    │
    ├── transactions/            # Module transactions
    │   ├── router.py            # /api/transactions/* (credit, debit, historique)
    │   ├── schemas.py           # TransactionResponse, TransactionSummary
    │   ├── service.py           # Logique métier transactions
    │   └── exceptions.py        # Exceptions spécifiques
    │
    ├── transfers/               # Module virements
    │   ├── router.py            # /api/transfers/* (virements entre comptes)
    │   ├── schemas.py           # TransferRequest, TransferResponse
    │   ├── service.py           # Logique métier transfers
    │   └── exceptions.py        # Exceptions spécifiques
    │
    ├── beneficiaries/           # Module bénéficiaires
    │   ├── router.py            # CRUD /api/beneficiaries/*, verify
    │   ├── schemas.py           # BeneficiaryCreate, BeneficiaryResponse
    │   ├── service.py           # Logique métier beneficiaries
    │   └── exceptions.py        # Exceptions spécifiques
    │
    ├── otps/                    # Module OTP
    │   ├── router.py            # /api/otps/* (génération, vérification)
    │   ├── schemas.py           # OTPRequest, OTPVerify
    │   ├── service.py           # Logique métier OTP
    │   └── exceptions.py        # Exceptions spécifiques
    │
    ├── notifications/           # Module notifications
    │   ├── router.py            # /api/notifications/* (envoi, liste)
    │   ├── schemas.py           # NotificationResponse, NotificationSend
    │   ├── service.py           # Logique métier notifications
    │   └── exceptions.py        # Exceptions spécifiques
    │
    └── admin/                   # Module administration
        ├── router.py            # /api/admin/* (promote, demote)
        ├── schemas.py           # PromoteUserResponse
        ├── service.py           # Logique métier admin
        └── exceptions.py        # Exceptions spécifiques
```

### Principes de l'architecture

| Couche | Responsabilité | Exemples |
|--------|----------------|----------|
| **config/** | Configuration centralisée | Settings, logging |
| **infrastructure/** | Préoccupations techniques | DB, sécurité, rate limiting |
| **models/** | Entités de persistance | SQLAlchemy models |
| **modules/** | Logique métier par feature | Auth, Users, Accounts, Transfers... |

### Conventions de nommage

| Élément | Convention | Exemple |
|---------|------------|---------|
| Router | `router.py` | Convention FastAPI |
| Schémas Pydantic | `schemas.py` | Distinguer des models SQLAlchemy |
| Service | `service.py` | Logique métier |
| Exceptions | `exceptions.py` | Erreurs spécifiques au module |

## 📦 Prérequis

- Python 3.12 ou supérieur
- PostgreSQL
- [uv](https://docs.astral.sh/uv/) - Package manager et runner Python ultra-rapide

## 🚀 Installation

### 1. Cloner le repository
```bash
git clone <repository-url>
cd Bank-Backend
```

### 2. Installer uv (si non installé)
```bash
pip install uv
```

### 3. Installer les dépendances
```bash
uv sync
```

Cette commande crée automatiquement un environnement virtuel et installe toutes les dépendances définies dans `pyproject.toml`.

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

Ou directement :
```bash
uv run python src/main.py
```

### Accéder à la documentation interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🔌 API Endpoints

### Authentification (`/api/auth`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/` | Inscription utilisateur |
| POST | `/api/auth/token` | Connexion (obtenir access token) |

### Utilisateurs (`/api/users`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/users/me` | Profil de l'utilisateur connecté |
| GET | `/api/users/` | Lister tous les utilisateurs |
| POST | `/api/users/` | Créer un utilisateur |
| GET | `/api/users/{id}` | Infos d'un utilisateur |
| PUT | `/api/users/{id}` | Mettre à jour un utilisateur |
| DELETE | `/api/users/{id}` | Supprimer un utilisateur |
| POST | `/api/users/{id}/change-password` | Changer le mot de passe |

### Comptes (`/api/accounts`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/accounts/` | Lister mes comptes |
| POST | `/api/accounts/` | Créer un compte |
| GET | `/api/accounts/{id}` | Détails d'un compte |
| PUT | `/api/accounts/{id}` | Mettre à jour un compte |
| DELETE | `/api/accounts/{id}` | Supprimer un compte |
| POST | `/api/accounts/{id}/deposit` | Effectuer un dépôt |
| POST | `/api/accounts/{id}/withdraw` | Effectuer un retrait |

### Transactions (`/api/transactions`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/transactions/credit` | Créditer un compte |
| POST | `/api/transactions/debit` | Débiter un compte |
| GET | `/api/transactions/{id}` | Détails d'une transaction |
| GET | `/api/transactions/account/{id}` | Transactions d'un compte |
| GET | `/api/transactions/` | Toutes les transactions |
| GET | `/api/transactions/account/{id}/summary` | Résumé des transactions |

### Virements (`/api/transfers`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/transfers/` | Effectuer un virement |
| GET | `/api/transfers/{id}` | Détails d'un virement |
| GET | `/api/transfers/account/{id}` | Virements d'un compte |
| GET | `/api/transfers/` | Tous les virements |
| GET | `/api/transfers/account/{id}/summary` | Résumé des virements |

### Bénéficiaires (`/api/beneficiaries`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/beneficiaries/` | Ajouter un bénéficiaire |
| GET | `/api/beneficiaries/` | Lister les bénéficiaires |
| GET | `/api/beneficiaries/{id}` | Détails d'un bénéficiaire |
| PUT | `/api/beneficiaries/{id}` | Modifier un bénéficiaire |
| DELETE | `/api/beneficiaries/{id}` | Supprimer un bénéficiaire |
| POST | `/api/beneficiaries/{id}/verify` | Vérifier un bénéficiaire |
| POST | `/api/beneficiaries/{id}/unverify` | Annuler la vérification |

### OTP (`/api/otps`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/otps/generate` | Générer un OTP |
| POST | `/api/otps/verify` | Vérifier un OTP |
| GET | `/api/otps/` | Lister les OTPs |
| GET | `/api/otps/{id}` | Détails d'un OTP |

### Notifications (`/api/notifications`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/notifications/` | Lister les notifications |
| GET | `/api/notifications/{id}` | Détails d'une notification |
| DELETE | `/api/notifications/{id}` | Supprimer une notification |
| POST | `/api/notifications/send/otp` | Envoyer une notification OTP |
| POST | `/api/notifications/send/transaction` | Notifier une transaction |
| POST | `/api/notifications/send/news` | Envoyer une news (bulk) |
| POST | `/api/notifications/send/custom` | Envoyer une notification custom |
| GET | `/api/notifications/user/{id}` | Notifications d'un utilisateur |

### Administration (`/api/admin`)
| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/admin/promote/{id}` | Promouvoir un utilisateur admin |
| POST | `/api/admin/demote/{id}` | Rétrograder un admin |

## 🔐 Authentification

### Flux JWT
1. Utilisateur s'inscrit via `POST /api/auth/`
2. Utilisateur se connecte via `POST /api/auth/token` avec ses identifiants
3. Backend génère un access token JWT
4. Client inclut le token dans les headers : `Authorization: Bearer <token>`
5. Les endpoints protégés valident le token
6. Token expire après un délai configurable (par défaut 30 minutes)

### OTP (One-Time Password)
- Utilisé pour les opérations sensibles (virements, modifications sécurité)
- Généré via pyotp
- Envoyé par notification/email
- Validité configurable (par défaut 10 minutes)

## 🧪 Tests

### Exécuter tous les tests
```bash
uv run pytest
```

### Exécuter les tests avec couverture
```bash
uv run pytest --cov=src tests/
```

### Tests spécifiques
```bash
uv run pytest tests/test_db.py -v
uv run pytest tests/test_auth_service.py -v
uv run pytest tests/test_users_api.py -v
```

## 📋 Conventions de code

- **PEP 8** : Respect des standards Python
- **Type hints** : Utilisation des annotations de type
- **Docstrings** : Documentation des fonctions et classes
- **Logging** : Utilisation du module logging pour le suivi
- **Formatage** : Black pour le formatage automatique
- **Linting** : Ruff pour l'analyse statique

## 🤝 Contribution

Les contributions sont bienvenues ! Veuillez :

1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Créer une Pull Request

## 📝 Licence

Ce projet est développé dans le cadre du cours de Sécurité Informatique - ING-2.

