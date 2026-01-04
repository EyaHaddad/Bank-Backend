# 🏦 BankFlow - Application Bancaire Frontend

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-16.0.10-black?logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1.9-06B6D4?logo=tailwind-css&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-1.7.9-5A29E4?logo=axios&logoColor=white)
![Radix UI](https://img.shields.io/badge/Radix%20UI-Latest-161618?logo=radix-ui&logoColor=white)

**Interface bancaire moderne et sécurisée**

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
- [Démarrage](#-démarrage)
- [Structure du projet](#-structure-du-projet)
- [Services API](#-services-api)
- [Configuration](#-configuration)
- [Contribution](#-contribution)

---

## 🎯 Vue d'ensemble

Interface utilisateur moderne d'une application bancaire sécurisée, développée avec **Next.js 16** et **React 19**. Cette application offre une expérience utilisateur fluide pour la gestion des opérations bancaires avec un accent particulier sur la **sécurité côté client**.

### Fonctionnalités par espace

#### 👤 Espace Client

| Fonctionnalité | Description |
|----------------|-------------|
| **Dashboard** | Vue d'ensemble avec statistiques et graphiques |
| **Transactions** | Historique détaillé et suivi des opérations |
| **Virements** | Transferts sécurisés avec validation OTP |
| **Bénéficiaires** | Gestion complète des destinataires |
| **Relevés** | Consultation et téléchargement PDF |
| **Taux de change** | Consultation en temps réel |
| **Profil** | Gestion des informations personnelles |
| **Contact** | Support client intégré |

#### 🔐 Espace Administrateur

| Fonctionnalité | Description |
|----------------|-------------|
| **Dashboard** | Tableau de bord avec métriques globales |
| **Utilisateurs** | CRUD complet des utilisateurs |
| **Comptes** | Gestion de tous les comptes bancaires |
| **Paramètres** | Configuration système |

---

## 🏗️ Architecture globale

### Diagramme d'architecture Frontend-Backend

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              NAVIGATEUR CLIENT                               │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                         NEXT.JS APPLICATION                             │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                      MIDDLEWARE LAYER                            │   │ │
│  │  │  • Route Protection (cookie-based auth)                          │   │ │
│  │  │  • Role-Based Access Control (RBAC)                              │   │ │
│  │  │  • Security Headers Injection (CSP, HSTS, XSS...)                │   │ │
│  │  │  • Redirect Logic                                                 │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                │                                        │ │
│  │                                ▼                                        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                        APP ROUTER                                │   │ │
│  │  │                                                                  │   │ │
│  │  │   ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐    │   │ │
│  │  │   │   / (login)  │   │   /client/*  │   │    /admin/*      │    │   │ │
│  │  │   │   PUBLIC     │   │   PROTECTED  │   │ ADMIN PROTECTED  │    │   │ │
│  │  │   └──────────────┘   └──────────────┘   └──────────────────┘    │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                │                                        │ │
│  │                                ▼                                        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                      COMPONENTS LAYER                            │   │ │
│  │  │                                                                  │   │ │
│  │  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │   │ │
│  │  │   │   UI     │  │  Forms   │  │  Charts  │  │   Sidebar    │    │   │ │
│  │  │   │(shadcn)  │  │(Hook Form)│ │(Recharts)│  │  Navigation  │    │   │ │
│  │  │   └──────────┘  └──────────┘  └──────────┘  └──────────────┘    │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                │                                        │ │
│  │                                ▼                                        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                       HOOKS LAYER                                │   │ │
│  │  │    useAuth • useToast • useMobile                                │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                │                                        │ │
│  │                                ▼                                        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                      SERVICES LAYER                              │   │ │
│  │  │                                                                  │   │ │
│  │  │   ┌─────────────────────────────────────────────────────────┐   │   │ │
│  │  │   │                  AXIOS INSTANCE                          │   │   │ │
│  │  │   │  • Auto Bearer Token Injection                           │   │   │ │
│  │  │   │  • 401 Error Handling (auto logout)                      │   │   │ │
│  │  │   │  • 10s Timeout                                           │   │   │ │
│  │  │   └─────────────────────────────────────────────────────────┘   │   │ │
│  │  │                                                                  │   │ │
│  │  │   auth • users • accounts • transactions • transfers            │   │ │
│  │  │   beneficiaries • notifications • otps • admin • currency       │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                │                                        │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │                     TOKEN STORAGE                                │   │ │
│  │  │    SessionStorage (API calls) + Cookies (Middleware)            │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS + JWT Bearer Token
                                    │ Content-Type: application/json
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND (FastAPI)                                  │
│                                                                              │
│  • Rate Limiting        • JWT Validation       • CORS Policy                │
│  • Security Headers     • Password Hashing     • OTP Verification           │
│  • PostgreSQL DB        • Role-Based Access    • Transaction Limits         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Architecture des composants

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ARCHITECTURE NEXT.JS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ PAGES (App Router)                                                       ││
│  │                                                                          ││
│  │  app/                                                                    ││
│  │  ├── layout.tsx           # Layout racine + ThemeProvider               ││
│  │  ├── page.tsx             # Page de connexion                           ││
│  │  │                                                                       ││
│  │  ├── client/              # Espace Client (protégé)                     ││
│  │  │   ├── page.tsx         # Dashboard client                            ││
│  │  │   ├── accounts/        # Gestion des comptes                         ││
│  │  │   ├── beneficiaries/   # Gestion bénéficiaires                       ││
│  │  │   ├── transactions/    # Historique transactions                     ││
│  │  │   ├── transfer/        # Virements                                   ││
│  │  │   ├── statements/      # Relevés bancaires                           ││
│  │  │   ├── exchange-rates/  # Taux de change                              ││
│  │  │   ├── profile/         # Profil utilisateur                          ││
│  │  │   └── contact/         # Support                                     ││
│  │  │                                                                       ││
│  │  └── admin/               # Espace Admin (protégé + rôle admin)         ││
│  │      ├── page.tsx         # Dashboard admin                             ││
│  │      ├── users/           # Gestion utilisateurs                        ││
│  │      └── accounts/        # Gestion comptes (admin)                     ││
│  │                                                                          ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ COMPONENTS                                                               ││
│  │                                                                          ││
│  │  components/                                                             ││
│  │  ├── ui/                  # Composants shadcn/ui (40+ composants)       ││
│  │  │   ├── button.tsx       # Boutons avec variants                       ││
│  │  │   ├── card.tsx         # Cartes                                      ││
│  │  │   ├── dialog.tsx       # Modales                                     ││
│  │  │   ├── input.tsx        # Champs de saisie                            ││
│  │  │   ├── input-otp.tsx    # Champs OTP                                  ││
│  │  │   ├── table.tsx        # Tableaux                                    ││
│  │  │   └── ...              # +35 composants UI                           ││
│  │  │                                                                       ││
│  │  ├── dashboard-sidebar.tsx  # Navigation latérale                       ││
│  │  ├── stat-card.tsx          # Cartes statistiques                       ││
│  │  └── theme-provider.tsx     # Gestion thème clair/sombre                ││
│  │                                                                          ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │ SERVICES & TYPES                                                         ││
│  │                                                                          ││
│  │  services/                types/                                         ││
│  │  ├── axiosInstance.ts     ├── auth.ts                                   ││
│  │  ├── auth.service.ts      ├── user.ts                                   ││
│  │  ├── users.service.ts     ├── account.ts                                ││
│  │  ├── accounts.service.ts  ├── transaction.ts                            ││
│  │  ├── transfers.service.ts ├── transfer.ts                               ││
│  │  ├── beneficiaries.ts     ├── beneficiary.ts                            ││
│  │  ├── notifications.ts     ├── notification.ts                           ││
│  │  ├── otps.service.ts      ├── otp.ts                                    ││
│  │  ├── admin.service.ts     └── index.ts                                  ││
│  │  ├── currency.service.ts                                                 ││
│  │  └── index.ts                                                            ││
│  │                                                                          ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Stack technologique

### Technologies principales

| Catégorie | Technologie | Version | Description |
|-----------|-------------|---------|-------------|
| **Framework** | Next.js | 16.0.10 | Framework React avec App Router |
| **Bibliothèque UI** | React | 19.2.0 | Dernière version avec Server Components |
| **Langage** | TypeScript | 5.x | Typage statique strict |
| **Styling** | Tailwind CSS | 4.1.9 | Framework CSS utility-first |
| **HTTP Client** | Axios | 1.7.9 | Client HTTP avec interceptors |
| **UI Components** | Radix UI | Latest | Composants accessibles headless |
| **Icons** | Lucide React | 0.454.0 | Icônes SVG modernes |
| **Forms** | React Hook Form | 7.60.0 | Gestion performante des formulaires |
| **Validation** | Zod | 3.25.76 | Validation de schémas TypeScript |
| **Charts** | Recharts | 2.15.4 | Graphiques React responsive |
| **Notifications** | Sonner | 1.7.4 | Toast notifications élégantes |
| **Dates** | date-fns | 4.1.0 | Manipulation des dates |
| **Themes** | next-themes | 0.4.6 | Thème clair/sombre |
| **OTP Input** | input-otp | 1.4.1 | Composant OTP accessible |

### Bibliothèque de composants (shadcn/ui)

L'application utilise **40+ composants** shadcn/ui :

```
Accordion • Alert • AlertDialog • AspectRatio • Avatar • Badge
Breadcrumb • Button • ButtonGroup • Calendar • Card • Carousel
Chart • Checkbox • Collapsible • Command • ContextMenu • Dialog
Drawer • DropdownMenu • Form • HoverCard • Input • InputOTP
Label • Menubar • NavigationMenu • Pagination • Popover • Progress
RadioGroup • ResizablePanel • ScrollArea • Select • Separator
Sheet • Sidebar • Skeleton • Slider • Sonner • Switch • Table
Tabs • Textarea • Toast • Toggle • ToggleGroup • Tooltip
```

---

## 🔐 Sécurité

### Vue d'ensemble de la sécurité Frontend

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COUCHES DE SÉCURITÉ FRONTEND                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. MIDDLEWARE SECURITY (middleware.ts)                                      │
│     ├── Route Protection par cookies                                         │
│     ├── Role-Based Access Control (RBAC)                                     │
│     └── Security Headers Injection                                           │
│                                                                              │
│  2. SECURITY HEADERS                                                         │
│     ├── Content-Security-Policy (CSP)                                        │
│     ├── X-Content-Type-Options: nosniff                                      │
│     ├── X-Frame-Options: DENY                                                │
│     ├── X-XSS-Protection: 1; mode=block                                      │
│     ├── Strict-Transport-Security (HSTS)                                     │
│     ├── Referrer-Policy: strict-origin-when-cross-origin                     │
│     └── Permissions-Policy (camera, microphone, geolocation disabled)        │
│                                                                              │
│  3. TOKEN MANAGEMENT                                                         │
│     ├── Dual Storage (sessionStorage + cookies)                              │
│     ├── SameSite=Lax cookies (CSRF protection)                               │
│     ├── Session cookies (cleared on browser close)                           │
│     └── Auto-cleanup on 401 errors                                           │
│                                                                              │
│  4. API SECURITY                                                             │
│     ├── Auto Bearer Token injection                                          │
│     ├── 401 Error interception + auto logout                                 │
│     ├── 10s request timeout                                                  │
│     └── Redirect loop prevention                                             │
│                                                                              │
│  5. INPUT VALIDATION                                                         │
│     ├── TypeScript strict mode                                               │
│     ├── Zod schema validation (disponible)                                   │
│     ├── HTML5 native validation                                              │
│     └── Client-side form validation                                          │
│                                                                              │
│  6. OTP SECURITY                                                             │
│     ├── 6-digit numeric codes only                                           │
│     ├── Auto-focus navigation                                                │
│     ├── Paste support                                                        │
│     └── 60s resend cooldown                                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1. Protection des routes (Middleware)

Le middleware Next.js protège toutes les routes :

```typescript
// Routes publiques
const PUBLIC_ROUTES = ["/", "/api"];

// Routes admin uniquement
const ADMIN_ROUTES = ["/admin"];

// Routes client authentifié
const CLIENT_ROUTES = ["/client"];
```

**Flux de protection :**
1. ✅ Vérification du token dans les cookies
2. ✅ Vérification du rôle utilisateur
3. ✅ Redirection si non autorisé
4. ✅ Injection des headers de sécurité

### 2. Headers de sécurité HTTP

| Header | Valeur | Protection |
|--------|--------|------------|
| `Content-Security-Policy` | Strict | Contrôle des ressources chargées |
| `X-Content-Type-Options` | `nosniff` | Prévient MIME sniffing |
| `X-Frame-Options` | `DENY` | Protection clickjacking |
| `X-XSS-Protection` | `1; mode=block` | Filtre XSS navigateur |
| `Strict-Transport-Security` | `max-age=31536000` | Force HTTPS |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Contrôle referer |
| `Permissions-Policy` | Restrictif | Désactive caméra, micro, géoloc |

### 3. Content Security Policy (CSP)

```
default-src 'self';
script-src 'self' 'unsafe-inline' 'unsafe-eval';
style-src 'self' 'unsafe-inline';
img-src 'self' data: blob:;
font-src 'self' data:;
connect-src 'self' http://localhost:8000 https://localhost:8000;
```

### 4. Gestion des tokens

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        STRATÉGIE DE STOCKAGE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────┐          ┌─────────────────────────────────────┐   │
│  │   sessionStorage    │          │            Cookies                   │   │
│  │                     │          │                                      │   │
│  │  • access_token     │          │  • access_token (SameSite=Lax)      │   │
│  │  • user_role        │          │  • user_role (SameSite=Lax)         │   │
│  │  • user_data        │          │                                      │   │
│  │                     │          │  Session cookies (pas de max-age)   │   │
│  │  Usage: API calls   │          │  Usage: Middleware route protection │   │
│  │  via Axios          │          │  (côté serveur)                     │   │
│  │                     │          │                                      │   │
│  │  ✅ Non persistant   │          │  ✅ Protection CSRF (SameSite)       │   │
│  │  ✅ Fermé avec tab   │          │  ✅ Accessible côté serveur         │   │
│  └─────────────────────┘          └─────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5. Flux d'authentification

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         FLUX D'AUTHENTIFICATION                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  INSCRIPTION                                                                  │
│  ───────────                                                                  │
│                                                                               │
│  1. Formulaire → POST /api/auth/                                              │
│     (email, password, name, phone)                                            │
│                                                                               │
│  2. Backend stocke temporairement + envoie OTP email                          │
│                                                                               │
│  3. Page vérification OTP → 6 chiffres                                        │
│     • Auto-focus entre les inputs                                             │
│     • Support paste                                                           │
│     • Cooldown resend 60s                                                     │
│                                                                               │
│  4. POST /api/auth/verify-email → Compte créé en DB                          │
│                                                                               │
│  CONNEXION                                                                    │
│  ─────────                                                                    │
│                                                                               │
│  1. Formulaire → POST /api/auth/token                                         │
│     (OAuth2 form: username=email, password)                                   │
│                                                                               │
│  2. Backend retourne JWT + rôle                                               │
│                                                                               │
│  3. Stockage token:                                                           │
│     • sessionStorage (pour Axios)                                             │
│     • Cookies (pour Middleware)                                               │
│                                                                               │
│  4. Redirection selon rôle:                                                   │
│     • admin → /admin                                                          │
│     • user → /client                                                          │
│                                                                               │
│  DÉCONNEXION                                                                  │
│  ───────────                                                                  │
│                                                                               │
│  1. Clear sessionStorage                                                      │
│  2. Expire cookies (max-age=0)                                                │
│  3. Redirect → /                                                              │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 6. Intercepteurs Axios

```typescript
// Request Interceptor
- Ajoute automatiquement: Authorization: Bearer <token>

// Response Interceptor
- 401 Error → clearAuthData() + clearAuthCookies() + redirect "/"
- Prévention des boucles de redirection
```

---

## 📦 Prérequis

| Logiciel | Version | Installation |
|----------|---------|--------------|
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org/) |
| **pnpm** (recommandé) | 8+ | `npm install -g pnpm` |
| **Backend** | - | [Bank-Backend](../Bank-Backend) doit être actif |
| **Docker** | 24+ | [docker.com](https://docker.com) |

---

## 🚀 Installation

### 0. Configurer le Backend

```bash
# Démarrer la base de données Docker
cd Bank-Backend
docker compose up -d

# Démarrer le backend
uv run python -m uvicorn src.main:app --reload
```

### 1. Cloner le repository
```bash
git clone <repository-url>
cd Bank-Frontend
```

### 2. Variables d'environnement

Créer `.env.local` :
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_NAME=BankFlow
```

### 3. Installer les dépendances

```bash
pnpm install
```

**Avec npm :**
```bash
npm install
```

---

## ▶️ Démarrage

### Mode Développement
```bash
pnpm dev
# ou
npm run dev
```
🌐 Ouvrir [http://localhost:3000](http://localhost:3000)

### Mode Production

```bash
# Build
pnpm build

# Start
pnpm start
```

### Scripts disponibles

| Commande | Description |
|----------|-------------|
| `pnpm dev` | Serveur de développement (hot reload) |
| `pnpm build` | Build de production |
| `pnpm start` | Serveur de production |
| `pnpm lint` | Vérification ESLint |

---

## 📁 Structure du projet

```
Bank-Frontend/
├── app/                          # App Router Next.js 16
│   ├── layout.tsx                # Layout racine + providers
│   ├── page.tsx                  # Page de connexion (/)
│   │
│   ├── admin/                    # 🔐 Espace Admin (role: admin)
│   │   ├── page.tsx              # Dashboard administrateur
│   │   ├── accounts/             # Gestion des comptes
│   │   │   └── page.tsx
│   │   └── users/                # Gestion des utilisateurs
│   │       └── page.tsx
│   │
│   └── client/                   # 🔐 Espace Client (role: user)
│       ├── page.tsx              # Dashboard client
│       ├── accounts/             # Mes comptes
│       ├── beneficiaries/        # Mes bénéficiaires
│       ├── contact/              # Support client
│       ├── exchange-rates/       # Taux de change
│       ├── profile/              # Mon profil
│       ├── statements/           # Mes relevés
│       ├── transactions/         # Historique transactions
│       └── transfer/             # Effectuer un virement
│
├── components/                   # Composants React
│   ├── ui/                       # 40+ composants shadcn/ui
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── input.tsx
│   │   ├── input-otp.tsx
│   │   ├── table.tsx
│   │   └── ... (35+ autres)
│   ├── dashboard-sidebar.tsx     # Navigation latérale
│   ├── stat-card.tsx             # Cartes statistiques
│   └── theme-provider.tsx        # Provider thème
│
├── hooks/                        # Hooks personnalisés
│   ├── useAuth.ts                # Gestion authentification
│   ├── useMobile.ts              # Détection mobile
│   └── useToast.ts               # Notifications toast
│
├── lib/                          # Utilitaires
│   └── utils.ts                  # Fonctions helper (cn, etc.)
│
├── services/                     # Services API
│   ├── axiosInstance.ts          # Instance Axios configurée
│   ├── auth.service.ts           # Authentification
│   ├── users.service.ts          # Utilisateurs
│   ├── accounts.service.ts       # Comptes
│   ├── transactions.service.ts   # Transactions
│   ├── transfers.service.ts      # Virements
│   ├── beneficiaries.service.ts  # Bénéficiaires
│   ├── notifications.service.ts  # Notifications
│   ├── otps.service.ts           # OTP
│   ├── admin.service.ts          # Admin
│   ├── currency.service.ts       # Taux de change
│   └── index.ts                  # Export centralisé
│
├── types/                        # Types TypeScript
│   ├── auth.ts                   # Types authentification
│   ├── user.ts                   # Types utilisateur
│   ├── account.ts                # Types compte
│   ├── transaction.ts            # Types transaction
│   ├── transfer.ts               # Types virement
│   ├── beneficiary.ts            # Types bénéficiaire
│   ├── notification.ts           # Types notification
│   ├── otp.ts                    # Types OTP
│   └── index.ts                  # Export centralisé
│
├── styles/
│   └── globals.css               # Styles globaux Tailwind
│
├── public/                       # Assets statiques
│
├── middleware.ts                 # 🔐 Middleware sécurité
├── next.config.mjs               # Configuration Next.js
├── tailwind.config.ts            # Configuration Tailwind
├── tsconfig.json                 # Configuration TypeScript
├── components.json               # Configuration shadcn/ui
└── package.json                  # Dépendances
```

---

## 🔌 Services API

### Architecture des services

| Service | Description | Endpoints principaux |
|---------|-------------|---------------------|
| `axiosInstance.ts` | Instance configurée avec interceptors | Base configuration |
| `auth.service.ts` | Inscription, connexion, OTP | `/auth/*` |
| `users.service.ts` | Profil, CRUD utilisateurs | `/users/*` |
| `accounts.service.ts` | Gestion des comptes | `/accounts/*` |
| `transactions.service.ts` | Historique transactions | `/transactions/*` |
| `transfers.service.ts` | Virements | `/transfers/*` |
| `beneficiaries.service.ts` | Bénéficiaires | `/beneficiaries/*` |
| `notifications.service.ts` | Notifications | `/notifications/*` |
| `otps.service.ts` | Codes OTP | `/otps/*` |
| `admin.service.ts` | Administration | `/admin/*` |
| `currency.service.ts` | Taux de change | `/currency/*` |

### Exemple d'utilisation

```typescript
import { authService, accountsService } from '@/services';

// Connexion
const { access_token, role } = await authService.login(email, password);

// Récupérer mes comptes
const accounts = await accountsService.getMyAccounts();
```

---

## ⚙️ Configuration

### Variables d'environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `NEXT_PUBLIC_API_URL` | URL de l'API backend | `http://localhost:8000/api` |
| `NEXT_PUBLIC_APP_NAME` | Nom de l'application | `BankFlow` |

### Configuration Axios

```typescript
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,  // 10 secondes
});
```

## 🔗 Projet associé

Ce frontend communique avec le backend FastAPI :
- **Backend** : [Bank-Backend](../Bank-Backend)

---

## 🚀 Démarrage Rapide

```bash
# 1. Base de données + Backend
cd Bank-Backend
docker compose up -d
uv run python -m uvicorn src.main:app --reload

# 2. Frontend (nouveau terminal)
cd Bank-Frontend
pnpm install && pnpm dev
```

Accéder à l'application: [http://localhost:3000](http://localhost:3000)

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
