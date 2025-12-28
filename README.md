# 🏦 BankFlow - Application Bancaire Frontend

Une application bancaire moderne et sécurisée développée avec **Next.js 16**, **React 19**, et **Tailwind CSS 4**. Cette interface offre une expérience utilisateur fluide pour la gestion des opérations bancaires.

![Next.js](https://img.shields.io/badge/Next.js-16.0.10-black?logo=next.js)
![React](https://img.shields.io/badge/React-19.2.0-blue?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?logo=typescript)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1.9-38B2AC?logo=tailwind-css)
![Axios](https://img.shields.io/badge/Axios-1.7.9-5A29E4?logo=axios)

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#-technologies-utilisées)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Démarrage](#-démarrage)
- [Structure du projet](#-structure-du-projet)
- [Services API](#-services-api)
- [Comptes de démonstration](#-comptes-de-démonstration)
- [Configuration API](#-configuration-api)

## ✨ Fonctionnalités

### 👤 Espace Client
- **Dashboard** - Vue d'ensemble du compte avec statistiques
- **Transactions** - Historique et suivi des transactions
- **Virements** - Effectuer des transferts d'argent
- **Bénéficiaires** - Gestion des bénéficiaires
- **Relevés** - Consultation des relevés bancaires
- **Taux de change** - Consultation des taux de change en temps réel
- **Profil** - Gestion du profil utilisateur
- **Contact** - Support client

### 🔐 Espace Administrateur
- **Dashboard** - Tableau de bord administrateur
- **Utilisateurs** - Gestion des utilisateurs
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
| **Axios** | 1.7.9 | Client HTTP avec interceptors |
| **Radix UI** | Latest | Composants UI accessibles |
| **Lucide React** | 0.454.0 | Icônes |
| **React Hook Form** | 7.60.0 | Gestion des formulaires |
| **Zod** | 3.25.76 | Validation de schémas |
| **Recharts** | 2.15.4 | Graphiques et visualisations |
| **Sonner** | 1.7.4 | Notifications toast |
| **date-fns** | 4.1.0 | Manipulation des dates |
| **next-themes** | 0.4.6 | Gestion des thèmes (clair/sombre) |
| **input-otp** | 1.4.1 | Champs OTP pour vérification |

## 📦 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **Node.js** >= 18.x ([Télécharger](https://nodejs.org/))
- **pnpm** >= 8.x (recommandé) ou **npm** >= 9.x ou **yarn** >= 1.22.x
- **Git** ([Télécharger](https://git-scm.com/))

Vérifiez vos versions :

```bash
node --version
pnpm --version
```

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/EyaHaddad/Bank-Frontend.git
cd Bank-Frontend
```

### 2. Configurer les variables d'environnement

Créez un fichier `.env.local` à la racine du projet :

```bash
cp .env.example .env.local
```

Ou créez manuellement le fichier avec :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Installer les dépendances

**Avec pnpm (recommandé) :**
```bash
pnpm install
```

**Avec npm :**
```bash
npm install
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
Bank-Frontend/
├── app/                        # App Router (Next.js 13+)
│   ├── layout.tsx              # Layout principal
│   ├── page.tsx                # Page de connexion
│   ├── admin/                  # Espace administrateur
│   │   ├── page.tsx            # Dashboard admin
│   │   ├── accounts/           # Gestion des comptes
│   │   ├── users/              # Gestion des utilisateurs
│   │   ├── exchange-rates/     # Taux de change
│   │   ├── relationships/      # Relations
│   │   ├── requests/           # Demandes
│   │   └── settings/           # Paramètres
│   └── client/                 # Espace client
│       ├── page.tsx            # Dashboard client
│       ├── beneficiaries/      # Bénéficiaires
│       ├── contact/            # Contact
│       ├── exchange-rates/     # Taux de change
│       ├── profile/            # Profil
│       ├── statements/         # Relevés
│       ├── transactions/       # Transactions
│       └── transfer/           # Virements
├── components/                 # Composants réutilisables
│   ├── ui/                     # Composants UI (shadcn/ui)
│   ├── dashboard-sidebar.tsx   # Barre latérale
│   ├── stat-card.tsx           # Carte statistique
│   └── theme-provider.tsx      # Provider de thème
├── hooks/                      # Hooks personnalisés
│   ├── useAuth.ts              # Gestion authentification
│   ├── useMobile.ts            # Détection mobile
│   └── useToast.ts             # Notifications
├── lib/                        # Utilitaires
│   └── utils.ts                # Fonctions utilitaires
├── services/                   # Services API
│   ├── axiosInstance.ts        # Instance Axios configurée
│   ├── auth.service.ts         # Service authentification
│   ├── users.service.ts        # Service utilisateurs
│   ├── accounts.service.ts     # Service comptes
│   ├── transactions.service.ts # Service transactions
│   ├── transfers.service.ts    # Service virements
│   ├── beneficiaries.service.ts# Service bénéficiaires
│   ├── notifications.service.ts# Service notifications
│   ├── otps.service.ts         # Service OTP
│   ├── admin.service.ts        # Service admin
│   └── index.ts                # Export centralisé
├── types/                      # Types TypeScript
│   ├── account.ts              # Types compte
│   ├── auth.ts                 # Types authentification
│   ├── beneficiary.ts          # Types bénéficiaire
│   ├── notification.ts         # Types notification
│   ├── otp.ts                  # Types OTP
│   ├── transaction.ts          # Types transaction
│   ├── transfer.ts             # Types virement
│   ├── user.ts                 # Types utilisateur
│   └── index.ts                # Export centralisé
├── styles/                     # Styles additionnels
│   └── globals.css             # Styles globaux
├── public/                     # Fichiers statiques
├── middleware.ts               # Middleware Next.js (auth)
├── next.config.mjs             # Configuration Next.js
├── package.json                # Dépendances
├── tsconfig.json               # Configuration TypeScript
├── postcss.config.mjs          # Configuration PostCSS
└── components.json             # Configuration shadcn/ui
```

## 🔌 Services API

L'application utilise une architecture de services modulaire avec Axios :

| Service | Description |
|---------|-------------|
| `axiosInstance.ts` | Instance Axios avec interceptors (auth, erreurs) |
| `auth.service.ts` | Inscription, connexion, vérification OTP |
| `users.service.ts` | Gestion des profils utilisateurs |
| `accounts.service.ts` | Opérations sur les comptes bancaires |
| `transactions.service.ts` | Historique des transactions |
| `transfers.service.ts` | Création et suivi des virements |
| `beneficiaries.service.ts` | Gestion des bénéficiaires |
| `notifications.service.ts` | Notifications utilisateur |
| `otps.service.ts` | Génération et vérification OTP |
| `admin.service.ts` | Fonctionnalités administrateur |

## 🔑 Comptes de démonstration

L'application inclut des comptes de démonstration pour tester les fonctionnalités :

| Rôle | Email | Mot de passe |
|------|-------|--------------|
| **Administrateur** | `admin@example.com` | `admin123` |
| **Client** | `client@example.com` | `client123` |

## ⚙️ Configuration API

L'application communique avec un backend FastAPI via une API REST. La configuration utilise les variables d'environnement et Axios avec interceptors.

### URL de base de l'API

L'URL est configurée via la variable d'environnement `NEXT_PUBLIC_API_URL` dans le fichier `.env.local` :

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Fonctionnalités de l'instance Axios

- **Interceptor de requête** : Ajoute automatiquement le token JWT aux headers
- **Interceptor de réponse** : Gère les erreurs 401 et redirige vers la connexion
- **Timeout** : 10 secondes par défaut
- **Stockage** : Tokens stockés dans `sessionStorage`

### Modifier l'URL de l'API

Pour pointer vers un autre backend, modifiez la variable `NEXT_PUBLIC_API_URL` dans le fichier `.env.local`.

### Endpoints disponibles

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/auth/` | POST | Initier l'inscription (envoie OTP par email) |
| `/auth/verify-email` | POST | Vérifier email avec code OTP |
| `/auth/resend-otp` | POST | Renvoyer le code de vérification |
| `/auth/token` | POST | Connexion (retourne JWT) |
| `/users/me` | GET | Profil utilisateur connecté |
| `/users` | GET | Liste des utilisateurs (admin) |
| `/accounts/me` | GET | Compte de l'utilisateur connecté |
| `/accounts` | GET | Liste des comptes (admin) |
| `/transactions` | GET | Historique des transactions |
| `/transfers` | POST | Créer un virement |
| `/beneficiaries` | GET/POST | Gestion des bénéficiaires |
| `/notifications` | GET | Notifications utilisateur |

## 🔧 Variables d'environnement

Créez un fichier `.env.local` à la racine du projet :

```env
# URL de l'API Backend (obligatoire)
NEXT_PUBLIC_API_URL=http://localhost:8000/api

# Nom de l'application (optionnel)
NEXT_PUBLIC_APP_NAME=BankFlow
```

> **Note** : Les variables préfixées par `NEXT_PUBLIC_` sont exposées au navigateur. Utilisez `.env.local` pour le développement local (ce fichier est ignoré par Git).

## 📝 Scripts disponibles

| Commande | Description |
|----------|-------------|
| `pnpm dev` | Démarre le serveur de développement |
| `pnpm build` | Compile l'application pour la production |
| `pnpm start` | Démarre le serveur de production |
| `pnpm lint` | Vérifie le code avec ESLint |

## 🔒 Authentification

L'application utilise JWT (JSON Web Tokens) pour l'authentification :

1. **Inscription** : L'utilisateur s'inscrit et reçoit un code OTP par email
2. **Vérification** : Le code OTP est vérifié pour activer le compte
3. **Connexion** : L'utilisateur se connecte et reçoit un token JWT
4. **Sessions** : Le token est stocké dans `sessionStorage` et envoyé automatiquement avec chaque requête
5. **Middleware** : Protection des routes via `middleware.ts`

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## � Projet associé

Ce frontend fonctionne avec le backend FastAPI disponible ici :
- **Backend** : [Bank-Backend](https://github.com/EyaHaddad/Bank-Backend)

## 📄 Licence

Ce projet est développé dans le cadre d'un projet académique - ING-2 Sécurité Informatique.

---

<div align="center">

**Développé avec ❤️ pour le projet d'Application Bancaire**

*Décembre 2025*

</div>
