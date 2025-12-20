# 🏦 BankFlow - Application Bancaire Frontend

Une application bancaire moderne et sécurisée développée avec **Next.js 16**, **React 19**, et **Tailwind CSS 4**. Cette interface offre une expérience utilisateur fluide pour la gestion des opérations bancaires.

![Next.js](https://img.shields.io/badge/Next.js-16.0.10-black?logo=next.js)
![React](https://img.shields.io/badge/React-19.2.0-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1.9-38B2AC?logo=tailwind-css)

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Démarrage](#-démarrage)
- [Structure du projet](#-structure-du-projet)
- [Comptes de démonstration](#-comptes-de-démonstration)
- [Configuration API](#-configuration-api)

## ✨ Fonctionnalités

### 👤 Espace Client
- **Dashboard** - Vue d'ensemble du compte
- **Transactions** - Historique et suivi des transactions
- **Virements** - Effectuer des transferts d'argent
- **Bénéficiaires** - Gestion des bénéficiaires
- **Relevés** - Consultation des relevés bancaires
- **Taux de change** - Consultation des taux de change
- **Profil** - Gestion du profil utilisateur
- **Contact** - Support client

### 🔐 Espace Administrateur
- **Dashboard** - Tableau de bord administrateur
- **Clients** - Gestion des clients
- **Comptes** - Gestion des comptes bancaires
- **Relations** - Gestion des relations clients
- **Demandes** - Traitement des demandes
- **Taux de change** - Configuration des taux
- **Paramètres** - Configuration du système

## 🛠 Technologies utilisées

| Technologie | Version | Description |
|-------------|---------|-------------|
| **Next.js** | 16.0.10 | Framework React avec App Router |
| **React** | 19.2.0 | Bibliothèque UI |
| **TypeScript** | 5.x | Typage statique |
| **Tailwind CSS** | 4.1.9 | Framework CSS utilitaire |
| **Radix UI** | Latest | Composants UI accessibles |
| **Lucide React** | 0.454.0 | Icônes |
| **React Hook Form** | 7.60.0 | Gestion des formulaires |
| **Zod** | 3.25.76 | Validation de schémas |
| **Recharts** | 2.15.4 | Graphiques |
| **Sonner** | 1.7.4 | Notifications toast |
| **date-fns** | 4.1.0 | Manipulation des dates |

## 📦 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Node.js** >= 18.x ([Télécharger](https://nodejs.org/))
- **npm** >= 9.x ou **pnpm** >= 8.x ou **yarn** >= 1.22.x
- **Git** ([Télécharger](https://git-scm.com/))

Vérifiez vos versions :

```bash
node --version
npm --version
```

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/EyaHaddad/Bank-Backend.git
cd Bank-Backend
```

### 2. Installer les dépendances

**Avec npm :**
```bash
npm install
```

**Avec pnpm (recommandé) :**
```bash
pnpm install
```

**Avec yarn :**
```bash
yarn install
```

## ▶️ Démarrage

### Mode Développement

Lance le serveur de développement avec rechargement automatique :

```bash
# Avec npm
npm run dev

# Avec pnpm
pnpm dev

# Avec yarn
yarn dev
```

🌐 Ouvrez [http://localhost:3000](http://localhost:3000) dans votre navigateur.

### Mode Production

#### 1. Construire l'application

```bash
# Avec npm
npm run build

# Avec pnpm
pnpm build

# Avec yarn
yarn build
```

#### 2. Démarrer le serveur de production

```bash
# Avec npm
npm run start

# Avec pnpm
pnpm start

# Avec yarn
yarn start
```

### Vérification du code (Lint)

```bash
npm run lint
```

## 📁 Structure du projet

```
Bank-Backend/
├── app/                        # App Router (Next.js 13+)
│   ├── layout.tsx              # Layout principal
│   ├── page.tsx                # Page de connexion
│   ├── globals.css             # Styles globaux
│   ├── admin/                  # Espace administrateur
│   │   ├── page.tsx            # Dashboard admin
│   │   ├── accounts/           # Gestion des comptes
│   │   ├── clients/            # Gestion des clients
│   │   ├── exchange-rates/     # Taux de change
│   │   ├── relationships/      # Relations
│   │   ├── requests/           # Demandes
│   │   └── settings/           # Paramètres
│   ├── client/                 # Espace client
│   │   ├── page.tsx            # Dashboard client
│   │   ├── beneficiaries/      # Bénéficiaires
│   │   ├── contact/            # Contact
│   │   ├── exchange-rates/     # Taux de change
│   │   ├── profile/            # Profil
│   │   ├── statements/         # Relevés
│   │   ├── transactions/       # Transactions
│   │   └── transfer/           # Virements
│   └── services/
│       └── api.js              # Services API
├── components/                 # Composants réutilisables
│   ├── ui/                     # Composants UI (shadcn/ui)
│   ├── dashboard-sidebar.tsx   # Barre latérale
│   ├── stat-card.tsx           # Carte statistique
│   └── theme-provider.tsx      # Provider de thème
├── hooks/                      # Hooks personnalisés
│   ├── use-mobile.ts           # Détection mobile
│   └── use-toast.ts            # Notifications
├── lib/                        # Utilitaires
│   └── utils.ts                # Fonctions utilitaires
├── public/                     # Fichiers statiques
├── styles/                     # Styles additionnels
├── next.config.mjs             # Configuration Next.js
├── package.json                # Dépendances
├── tsconfig.json               # Configuration TypeScript
├── postcss.config.mjs          # Configuration PostCSS
└── components.json             # Configuration shadcn/ui
```

## 🔑 Comptes de démonstration

L'application inclut des comptes de démonstration pour tester les fonctionnalités :

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| **Administrateur** | `admin@example.com` | `admin123` |
| **Client** | `client@example.com` | `client123` |

## ⚙️ Configuration API

L'application communique avec un backend via une API REST. La configuration se trouve dans `app/services/api.js`.

### URL de base de l'API

```javascript
const BASE_URL = "http://localhost:8000/api";
```

### Modifier l'URL de l'API

Pour pointer vers un autre backend, modifiez la constante `BASE_URL` dans le fichier `app/services/api.js`.

### Endpoints disponibles

| Endpoint | Description |
|----------|-------------|
| `POST /auth/` | Inscription |
| `POST /auth/token` | Connexion (JWT) |
| `GET /users/me` | Profil utilisateur |
| `GET /users` | Liste des utilisateurs |
| `GET /accounts/me` | Compte de l'utilisateur |

## 🔧 Variables d'environnement (optionnel)

Créez un fichier `.env.local` à la racine du projet :

```env
# URL de l'API Backend
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Autres configurations
NEXT_PUBLIC_APP_NAME=BankFlow
```

## 📝 Scripts disponibles

| Commande | Description |
|----------|-------------|
| `npm run dev` | Démarre le serveur de développement |
| `npm run build` | Compile l'application pour la production |
| `npm run start` | Démarre le serveur de production |
| `npm run lint` | Vérifie le code avec ESLint |

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est développé dans le cadre d'un projet académique - ING-2 Sécurité Informatique.

---

<div align="center">

**Développé avec ❤️ pour le projet d'Application Bancaire**

</div>
