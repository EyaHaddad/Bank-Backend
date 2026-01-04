# 🏦 BankFlow - Application Bancaire Backend

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-0.124+-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?logo=sqlalchemy&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?logo=jsonwebtokens&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.12+-E92063?logo=pydantic&logoColor=white)

**Backend sécurisé d'une application bancaire moderne**

*Développé dans le cadre du cours de Sécurité Informatique - ING-2*

</div>

---

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Architecture globale](#-architecture-globale)
- [Stack technologique](#-stack-technologique)
- [Sécurité](#-sécurité)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Endpoints](#-api-endpoints)
- [Tests](#-tests)
- [Contribution](#-contribution)

---

## 🎯 Vue d'ensemble

Backend d'une application bancaire sécurisée développée en **FastAPI**, offrant des fonctionnalités complètes de gestion des comptes, transactions, authentification et autorisation avec un focus particulier sur la **sécurité**.

### Fonctionnalités principales

| Catégorie | Fonctionnalités |
|-----------|-----------------|
| 🔐 **Authentification** | JWT, OAuth2, vérification email, session management |
| 🔑 **Multi-facteurs** | OTP par email, codes à 6 chiffres, expiration configurable |
| 👤 **Utilisateurs** | CRUD complet, gestion des profils, changement de mot de passe |
| 💳 **Comptes** | Création, dépôts, retraits, multi-comptes par utilisateur |
| 💸 **Transactions** | Crédits, débits, historique, résumés |
| 🔄 **Virements** | Transferts entre comptes, limites journalières |
| 👥 **Bénéficiaires** | Gestion et vérification des bénéficiaires |
| 📧 **Notifications** | Email, alertes transactions, news |
| 🛡️ **Administration** | Promotion/rétrogradation admins, gestion globale |
| 🚀 **Rate Limiting** | Protection contre les abus et DDoS |
| 📝 **Audit** | Logging complet des actions |

---

## 🏗️ Architecture globale

### Diagramme d'architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           CLIENT (Frontend)                              │
│                     Next.js 16 / React 19 / Axios                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS / JWT Bearer Token
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         MIDDLEWARE STACK                                 │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │    CORS      │ │ TrustedHost  │ │    GZip      │ │   Security   │   │
│  │  Middleware  │ │  Middleware  │ │  Middleware  │ │  Middleware  │   │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘   │
│                                                                          │
│  • Cross-Origin Resource Sharing     • Rate Limiting (10 req/s)         │
│  • Host Header Validation            • Security Headers (XSS, CSP...)   │
│  • Response Compression              • Request Logging & Timing          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FASTAPI APPLICATION                              │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                        API ROUTERS (/api)                          │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐  │  │
│  │  │  auth   │ │  users  │ │accounts │ │transfers│ │beneficiaries│  │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────────┘  │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                   │  │
│  │  │  otps   │ │  notif  │ │  admin  │ │currency │                   │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│                                    ▼                                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                         SERVICES LAYER                             │  │
│  │           Business Logic • Validation • Authorization              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                    │                                     │
│                                    ▼                                     │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                         MODELS (SQLAlchemy ORM)                    │  │
│  │  User • Account • Transaction • Transfer • Beneficiary • OTP      │  │
│  │  Notification • Statement                                          │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           PostgreSQL Database                            │
│                    UUID Primary Keys • Parameterized Queries            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Clean Architecture

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
│   ├── settings.py              # Variables d'environnement (Pydantic)
│   └── logging.py               # Configuration du logging
│
├── infrastructure/              # Couche infrastructure (technique)
│   ├── database/                # Configuration base de données
│   │   ├── session.py           # Engine, SessionLocal, get_db
│   │   └── reset.py             # Script de réinitialisation DB
│   └── security/                # Utilitaires de sécurité
│       ├── middleware.py        # AdvancedSecurityMiddleware
│       └── rate_limiter.py      # SlowAPI rate limiting
│
├── models/                      # Entités SQLAlchemy (ORM)
│   ├── base.py                  # BaseModel avec timestamps (created_at, updated_at)
│   ├── user.py                  # User avec role, email_verified
│   ├── account.py               # Account avec AccountStatus enum
│   ├── transaction.py           # Transaction avec TransactionType/Status
│   ├── transfer.py              # Transfer entre comptes
│   ├── beneficiary.py           # Beneficiary avec vérification
│   ├── otp.py                   # OTP avec OTPPurpose enum
│   ├── notification.py          # Notification avec NotificationType
│   └── statement.py             # Statement (relevés)
│
└── modules/                     # Modules métier (feature-based)
    ├── auth/                    # Authentification & inscription
    │   ├── router.py            # Endpoints /api/auth/*
    │   ├── schemas.py           # DTOs Pydantic
    │   ├── service.py           # Logique JWT, bcrypt, OAuth2
    │   ├── pending_registration.py  # Store temporaire inscription
    │   └── exceptions.py        # Exceptions auth
    │
    ├── users/                   # Gestion utilisateurs
    ├── accounts/                # Comptes bancaires
    ├── transactions/            # Opérations de transactions
    ├── transfers/               # Virements
    ├── beneficiaries/           # Bénéficiaires
    ├── otps/                    # Codes OTP
    ├── notifications/           # Notifications email
    ├── currency/                # Taux de change
    └── admin/                   # Administration
```

### Principes de l'architecture

| Couche | Responsabilité | Technologies |
|--------|----------------|--------------|
| **config/** | Configuration centralisée | Pydantic Settings, python-dotenv |
| **infrastructure/** | Préoccupations techniques | SQLAlchemy, SlowAPI, Custom Middleware |
| **models/** | Entités de persistance | SQLAlchemy ORM, UUID, Enums |
| **modules/** | Logique métier par feature | FastAPI Routers, Pydantic Schemas |

---

## 🛠️ Stack technologique

### Technologies principales

| Catégorie | Technologie | Version | Description |
|-----------|-------------|---------|-------------|
| **Framework** | FastAPI | 0.124+ | Framework web async haute performance |
| **Runtime** | Python | 3.12+ | Langage de programmation |
| **ORM** | SQLAlchemy | 2.0+ | Object-Relational Mapping |
| **Database** | PostgreSQL | 15+ | Base de données relationnelle |
| **Validation** | Pydantic | 2.12+ | Validation de données et settings |
| **Auth JWT** | PyJWT / python-jose | Latest | Tokens d'authentification |
| **Password** | passlib[bcrypt] | Latest | Hashage sécurisé des mots de passe |
| **OTP** | pyotp | Latest | Génération de codes OTP |
| **Rate Limit** | SlowAPI | Latest | Limitation de requêtes |
| **Email** | smtplib / email | Built-in | Envoi d'emails |
| **Package Manager** | uv | Latest | Gestionnaire ultra-rapide |
| **Server** | Uvicorn | Latest | Serveur ASGI |

### Dépendances de développement

| Outil | Usage |
|-------|-------|
| **pytest** | Tests unitaires et d'intégration |
| **pytest-cov** | Couverture de code |
| **httpx** | Client HTTP pour tests |
| **black** | Formatage automatique |
| **ruff** | Linting rapide |
| **mypy** | Vérification de types |

---

## 🔐 Sécurité

### Vue d'ensemble de la sécurité

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      COUCHES DE SÉCURITÉ                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. TRANSPORT LAYER                                                      │
│     ├── SSL/TLS (HTTPS) configurable                                    │
│     └── Trusted Host Middleware                                          │
│                                                                          │
│  2. APPLICATION LAYER                                                    │
│     ├── Rate Limiting (10 req/s par IP)                                 │
│     ├── CORS Configuration                                               │
│     └── Security Headers (CSP, XSS, Clickjacking)                       │
│                                                                          │
│  3. AUTHENTICATION LAYER                                                 │
│     ├── JWT Tokens (HS256/RS256)                                        │
│     ├── OAuth2 Password Bearer                                          │
│     ├── Email Verification (OTP)                                        │
│     └── Multi-Factor Authentication                                      │
│                                                                          │
│  4. AUTHORIZATION LAYER                                                  │
│     ├── Role-Based Access Control (RBAC)                                │
│     ├── Resource Ownership Validation                                    │
│     └── Admin-only endpoints protection                                  │
│                                                                          │
│  5. DATA LAYER                                                           │
│     ├── bcrypt Password Hashing (salted)                                │
│     ├── Parameterized SQL Queries (SQLAlchemy)                          │
│     ├── UUID Primary Keys (non-séquentiels)                             │
│     └── Input Validation (Pydantic)                                      │
│                                                                          │
│  6. BUSINESS LAYER                                                       │
│     ├── Transaction Limits (montant max, limite journalière)            │
│     ├── Beneficiary Verification                                         │
│     ├── Login Attempt Limiting                                           │
│     └── OTP for Sensitive Operations                                     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1. Middleware de sécurité avancé

Le `AdvancedSecurityMiddleware` fournit plusieurs couches de protection :

```python
# Fonctionnalités du middleware
- Rate Limiting       : 10 requêtes/seconde par IP
- Request Logging     : Journalisation de toutes les requêtes
- Performance Monitor : Header X-Process-Time
- Security Headers    : Injection automatique
```

### 2. En-têtes de sécurité HTTP

| Header | Valeur | Protection |
|--------|--------|------------|
| `X-Content-Type-Options` | `nosniff` | Prévient le MIME sniffing |
| `X-Frame-Options` | `DENY` | Protection contre le clickjacking |
| `X-XSS-Protection` | `1; mode=block` | Filtre XSS du navigateur |
| `Content-Security-Policy` | Strict/Debug | Contrôle des ressources |
| `Strict-Transport-Security` | `max-age=31536000` | Force HTTPS |

### 3. Authentification JWT

```
┌──────────────────────────────────────────────────────────────┐
│                    FLUX D'AUTHENTIFICATION                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  INSCRIPTION (2 phases)                                       │
│  ──────────────────────                                       │
│  1. POST /api/auth/          → Données stockées temporairement│
│                              → OTP envoyé par email           │
│                              → Utilisateur NON créé en DB     │
│                                                               │
│  2. POST /api/auth/verify-email → Vérification OTP            │
│                                 → Création utilisateur en DB  │
│                                 → Email marqué "vérifié"      │
│                                                               │
│  CONNEXION                                                    │
│  ─────────                                                    │
│  POST /api/auth/token        → Vérification credentials       │
│                              → Vérification email_verified    │
│                              → Génération JWT                 │
│                                                               │
│  PAYLOAD JWT                                                  │
│  ───────────                                                  │
│  {                                                            │
│    "sub": "user@email.com",                                   │
│    "id": "uuid-user-id",                                      │
│    "role": "user|admin",                                      │
│    "exp": 1234567890                                          │
│  }                                                            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 4. Politique de mots de passe

| Critère | Valeur par défaut | Configurable |
|---------|-------------------|--------------|
| Longueur minimale | 12 caractères | ✅ `MIN_PASSWORD_LENGTH` |
| Majuscule requise | Oui | ✅ `REQUIRE_UPPERCASE` |
| Minuscule requise | Oui | ✅ `REQUIRE_LOWERCASE` |
| Chiffre requis | Oui | ✅ `REQUIRE_DIGIT` |
| Caractère spécial | Oui | ✅ `REQUIRE_SPECIAL_CHAR` |
| Limite bcrypt | 72 bytes | ✅ `MAX_BCRYPT_BYTES` |

### 5. Système OTP

| Configuration | Valeur | Description |
|---------------|--------|-------------|
| `OTP_DIGITS` | 6 | Nombre de chiffres |
| `OTP_VALIDITY_PERIOD` | 10 min | Durée de validité |
| `OTP_SECRET_LENGTH` | 32 | Longueur de la clé secrète |
| Max tentatives | 3 | Par code OTP |
| Usage unique | Oui | Flag `is_used` |

**Usages OTP :**
- `LOGIN` : Authentification multi-facteurs
- `TRANSACTION` : Validation de virements
- `RESET_PASSWORD` : Récupération de compte
- `EMAIL_VERIFICATION` : Vérification d'inscription
- `PHONE_VERIFICATION` : Validation téléphone
- `ACCOUNT_ACTIVATION` : Activation de compte

### 6. Rate Limiting

| Endpoint | Limite | Raison |
|----------|--------|--------|
| `POST /api/auth/` | 100/minute | Inscription |
| `POST /api/auth/token` | 100/minute | Connexion |
| `POST /api/auth/resend-otp` | **3/minute** | Anti-spam email |
| Autres endpoints | 10 req/seconde | Protection générale |

### 7. Protection contre les attaques

| Attaque | Protection |
|---------|------------|
| **SQL Injection** | SQLAlchemy ORM avec requêtes paramétrées |
| **XSS** | Headers de sécurité, validation Pydantic |
| **CSRF** | CORS configuré, SameSite cookies |
| **Clickjacking** | X-Frame-Options: DENY |
| **Brute Force** | Rate limiting, MAX_LOGIN_ATTEMPTS |
| **Timing Attacks** | `secrets.compare_digest()` pour OTP |
| **Host Header** | TrustedHostMiddleware |

### 8. Limites transactionnelles

| Paramètre | Description | Configurable |
|-----------|-------------|--------------|
| `MAX_TRANSACTION_AMOUNT` | Montant max par transaction | ✅ |
| `DAILY_TRANSACTION_LIMIT` | Limite journalière | ✅ |
| Vérification bénéficiaire | Virements uniquement vers bénéficiaires vérifiés | ✅ |

---

## 📦 Prérequis

| Logiciel | Version | Installation |
|----------|---------|--------------|
| **Python** | 3.12+ | [python.org](https://www.python.org/) |
| **Docker** | 24+ | [docker.com](https://www.docker.com/) (recommandé pour la DB) |
| **PostgreSQL** | 15+ | [postgresql.org](https://www.postgresql.org/) (ou via Docker) |
| **uv** | Latest | `pip install uv` |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |

---

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

Cette commande crée automatiquement un environnement virtuel et installe toutes les dépendances.

### 4. Configurer PostgreSQL

#### Option A: 🐳 Avec Docker (Recommandé)

```bash
# Exporter votre base locale (première fois uniquement)
.\export-db.bat

# Démarrer la base Docker
docker compose up -d
```

> 📖 Voir [DOCKER.md](DOCKER.md) pour plus de détails.

#### Option B: Installation manuelle PostgreSQL

```sql
CREATE DATABASE banking_db;
```

Puis initialisez les tables:
```bash
uv run python -m src.infrastructure.database.reset
```

---

## ⚙️ Configuration

### Variables d'environnement (.env)

Créez un fichier `.env` à la racine du projet :

```env
# ═══════════════════════════════════════════════════════════
# APPLICATION
# ═══════════════════════════════════════════════════════════
PROJECT_NAME=BankFlow API
VERSION=1.0.0
DEBUG=False

# ═══════════════════════════════════════════════════════════
# BASE DE DONNÉES
# ═══════════════════════════════════════════════════════════
# Pour Docker (port 5432):
DATABASE_URL=postgresql://postgres:hmd202303@localhost:5432/banking_db
# Pour installation locale (port 5433):
# DATABASE_URL=postgresql://postgres:hmd202303@localhost:5433/banking_db
DATABASE_NAME=banking_db
DATABASE_USER=postgres
DATABASE_PASSWORD=hmd202303

# ═══════════════════════════════════════════════════════════
# AUTHENTIFICATION JWT
# ═══════════════════════════════════════════════════════════
SECRET_KEY=your-super-secret-key-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# ═══════════════════════════════════════════════════════════
# POLITIQUE DE MOT DE PASSE
# ═══════════════════════════════════════════════════════════
MIN_PASSWORD_LENGTH=12
MAX_BCRYPT_BYTES=72
REQUIRE_UPPERCASE=True
REQUIRE_LOWERCASE=True
REQUIRE_DIGIT=True
REQUIRE_SPECIAL_CHAR=True

# ═══════════════════════════════════════════════════════════
# OTP (One-Time Password)
# ═══════════════════════════════════════════════════════════
OTP_SECRET_LENGTH=32
OTP_VALIDITY_PERIOD=10
OTP_DIGITS=6

# ═══════════════════════════════════════════════════════════
# EMAIL (SMTP)
# ═══════════════════════════════════════════════════════════
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@bankflow.com
SMTP_FROM_NAME=BankFlow
SMTP_TLS=True

# ═══════════════════════════════════════════════════════════
# SÉCURITÉ
# ═══════════════════════════════════════════════════════════
ALLOWED_ORIGINS=["http://localhost:3000"]
ALLOWED_HOSTS=["localhost", "127.0.0.1"]
MAX_LOGIN_ATTEMPTS=5
LOGIN_ATTEMPT_WINDOW=300

# ═══════════════════════════════════════════════════════════
# SSL/TLS
# ═══════════════════════════════════════════════════════════
USE_SSL=False
SESSION_TIMEOUT_MINUTES=60

# ═══════════════════════════════════════════════════════════
# LIMITES TRANSACTIONNELLES
# ═══════════════════════════════════════════════════════════
MAX_TRANSACTION_AMOUNT=10000.00
DAILY_TRANSACTION_LIMIT=50000.00
```

---

## 📖 Utilisation

### Démarrer le serveur

**Mode développement :**
```bash
uv run python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Mode production avec SSL :**
```bash
uv run python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 \
  --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem
```

### Documentation interactive

| Interface | URL | Description |
|-----------|-----|-------------|
| **Swagger UI** | http://localhost:8000/api/docs | Documentation interactive |
| **ReDoc** | http://localhost:8000/api/redoc | Documentation alternative |
| **OpenAPI** | http://localhost:8000/api/openapi.json | Schéma OpenAPI |

> ⚠️ La documentation API est désactivée en production (`DEBUG=False`)

### 🔑 Comptes de test

Une fois la base de données Docker démarrée (`docker compose up -d`), des comptes sont déjà disponibles :

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| **Admin** | `eyahaddad450@gmail.com` | `AYAadmin@/2025` |
| **Client** | `haddad.eyamail@gmail.com` | `azerty2023@AYA` |

> ⚠️ **Important** : Il n'est **pas nécessaire** de créer de nouveaux comptes pour tester l'application.

> 🔐 **Note sur l'Admin** : Un compte administrateur ne peut **pas** être créé via l'interface utilisateur. La création d'un admin se fait uniquement :
> - Via le Swagger UI (`/api/docs`) avec l'endpoint `POST /api/admin/promote/{id}`

---

## 🔌 API Endpoints

### Authentification (`/api/auth`)
| Méthode | Endpoint | Description | Rate Limit |
|---------|----------|-------------|------------|
| POST | `/api/auth/` | Initier l'inscription | 100/min |
| POST | `/api/auth/verify-email` | Vérifier email avec OTP | - |
| POST | `/api/auth/resend-otp` | Renvoyer le code OTP | **3/min** |
| POST | `/api/auth/token` | Connexion (obtenir JWT) | 100/min |

### Utilisateurs (`/api/users`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/users/me` | Profil utilisateur connecté | 🔐 User |
| GET | `/api/users/` | Lister tous les utilisateurs | 🔐 Admin |
| POST | `/api/users/` | Créer un utilisateur | 🔐 Admin |
| GET | `/api/users/{id}` | Infos d'un utilisateur | 🔐 Admin |
| PUT | `/api/users/{id}` | Mettre à jour | 🔐 User/Admin |
| DELETE | `/api/users/{id}` | Supprimer | 🔐 Admin |
| POST | `/api/users/{id}/change-password` | Changer mot de passe | 🔐 User |

### Comptes (`/api/accounts`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| GET | `/api/accounts/` | Lister mes comptes | 🔐 User |
| POST | `/api/accounts/` | Créer un compte | 🔐 User |
| GET | `/api/accounts/{id}` | Détails d'un compte | 🔐 Owner |
| PUT | `/api/accounts/{id}` | Modifier un compte | 🔐 Owner |
| DELETE | `/api/accounts/{id}` | Supprimer un compte | 🔐 Owner |
| POST | `/api/accounts/{id}/deposit` | Effectuer un dépôt | 🔐 Owner |
| POST | `/api/accounts/{id}/withdraw` | Effectuer un retrait | 🔐 Owner |

### Virements (`/api/transfers`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/api/transfers/` | Effectuer un virement | 🔐 User + OTP |
| GET | `/api/transfers/{id}` | Détails d'un virement | 🔐 Owner |
| GET | `/api/transfers/account/{id}` | Virements d'un compte | 🔐 Owner |

### Bénéficiaires (`/api/beneficiaries`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/api/beneficiaries/` | Ajouter un bénéficiaire | 🔐 User |
| GET | `/api/beneficiaries/` | Lister les bénéficiaires | 🔐 User |
| POST | `/api/beneficiaries/{id}/verify` | Vérifier bénéficiaire | 🔐 User + OTP |

### Administration (`/api/admin`)
| Méthode | Endpoint | Description | Auth |
|---------|----------|-------------|------|
| POST | `/api/admin/promote/{id}` | Promouvoir en admin | 🔐 Admin |
| POST | `/api/admin/demote/{id}` | Rétrograder | 🔐 Admin |

---

## 🧪 Tests

### Exécuter les tests

```bash
# Tous les tests
uv run pytest

# Avec couverture
uv run pytest --cov=src tests/

# Tests spécifiques
uv run pytest tests/test_auth_service.py -v
uv run pytest tests/test_users_api.py -v

# Tests avec rapport HTML
uv run pytest --cov=src --cov-report=html tests/
```

### Structure des tests

```
tests/
├── conftest.py           # Fixtures pytest
├── test_auth_service.py  # Tests authentification
├── test_users_api.py     # Tests API utilisateurs
└── test_db.py            # Tests base de données
```

---

## 📋 Conventions de code

| Aspect | Standard |
|--------|----------|
| **Style** | PEP 8 |
| **Formatage** | Black |
| **Linting** | Ruff |
| **Types** | Type hints obligatoires |
| **Docstrings** | Google style |
| **Commits** | Conventional Commits |

---

## 🔗 Projet associé

Ce backend fonctionne avec le frontend Next.js :
- **Frontend** : [Bank-Frontend](../Bank-Frontend)

---

## 🤝 Contribution

1. Fork le repository
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commiter (`git commit -m 'feat: ajout nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

---

## 📝 Licence

Ce projet est développé dans le cadre du cours de **Sécurité Informatique - ING-2**.

---

<div align="center">

**Développé avec ❤️ pour le projet d'Application Bancaire**

*Janvier 2026*

</div>

