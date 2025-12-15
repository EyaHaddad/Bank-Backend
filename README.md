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

### Couches de l'application
```
API Layer (routes) → Services Layer → Database Layer
        ↓
    Auth & Security
    Config & Dependencies
    Logging & Monitoring
```

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
# ou avec Homebrew (macOS)
brew install uv
```

### 3. Installer les dépendances
```bash
uv sync
```

Cette commande crée automatiquement un environnement virtuel et installe toutes les dépendances définies dans `pyproject.toml`. install -r requirements-dev.txt
```

### 4. Initialiser la base de données
```bash
python -m src.database.reset
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

Voir [src/core/config.py](src/core/config.py) pour plus de détails.

## 📖 Utilisation

### Démarrer le serveur
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Accéder à la documentation interactive
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc
 run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Ou avec le script du projet (si disponible) :
```bash
uv run python src/main.py
## 📁 Structure du projet

```
backend/
├── src/
│   ├── main.py                 # Point d'entrée de l'application
│   ├── api/                    # Endpoints API
│   │   ├── accounts.py         # Gestion des comptes
│   │   ├── auth.py             # Authentification
│   │   ├── transactions.py     # Transactions
│   │   ├── users.py            # Utilisateurs
│   │   └── deps.py             # Dépendances partagées
│   ├── auth/                   # Logique d'authentification
│   │   ├── controllers.py      # Contrôleurs
│   │   ├── services.py         # Services d'auth
│   │   ├── models.py           # Modèles d'auth
│   │   └── exceptions.py       # Exceptions d'auth
│   ├── core/                   # Configuration centrale
│   │   ├── config.py           # Variables de configuration
│   │   ├── security.py         # Fonctions de sécurité
│   │   ├── jwt.py              # Gestion JWT
│   │   ├── dependencies.py     # Dépendances FastAPI
│   │   ├── limiter.py          # Rate limiting
│   │   └── logging.py          # Configuration logging
│   ├── database/               # Accès base de données
│   │   ├── core.py             # Connexion DB
│   │   └── reset.py            # Scripts de réinitialisation
│   ├── models/                 # Modèles de données
│   │   ├── user.py             # Modèle Utilisateur
│   │   ├── account.py          # Modèle Compte
│   │   ├── transaction.py      # Modèle Transaction
│   │   ├── beneficiary.py      # Modèle Bénéficiaire
│   │   └── base.py             # Modèle de base
│   ├── services/               # Logique métier
│   │   ├── user_services.py    # Services utilisateur
│   │   ├── email.py            # Service email
│   │   └── otp.py              # Service OTP
│   └── utils/                  # Utilitaires
│       └── validators.py       # Validateurs personnalisés
├── tests/
│   ├── __init__.py
│   └── test_db.py              # Tests base de données
├── requirements.txt            # Dépendances de production
├── requirements-dev.txt        # Dépendances de développement
├── pyproject.toml              # Configuration du projet
└── README.md                   # Ce fichier
```

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

Voir [src/core/jwt.py](src/core/jwt.py) et [src/auth/services.py](src/auth/services.py) pour les détails.

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

