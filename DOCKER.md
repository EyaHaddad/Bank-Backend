# 🐳 Déploiement Docker - Base de données

## Prérequis
- Docker Desktop installé et lancé

## Exporter votre base locale

```bash
.\export-db.bat
```

Cela crée `docker/init-db/01-data.sql` avec vos données.

## Démarrer la base Docker

```bash
docker compose up -d
```

## Commandes utiles

| Commande | Description |
|----------|-------------|
| `docker compose up -d` | Démarrer |
| `docker compose down` | Arrêter |
| `docker compose down -v` | Arrêter + supprimer données |
| `docker compose logs -f` | Voir les logs |

## Configuration Backend

Dans `.env`, utilisez le port 5432 pour Docker:
```
DATABASE_URL=postgresql://postgres:hmd202303@localhost:5432/banking_db
```

## Réinitialiser

```bash
docker compose down -v
.\export-db.bat
docker compose up -d
```
