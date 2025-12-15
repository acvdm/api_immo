# Microservice de gestion immobilière

API REST en Python/Flask pour gérer des biens immobiliers, leurs pièces et les utilisateurs.


### Prérequis
Ce projet utilise Docker pour garantir un environnement d'exécution identique sur toutes les machines.


#### Installation de Docker
##### Windows et Mac
1. Télécharger **Docker Desktop** : https://www.docker.com/products/docker-desktop/
2. Installer l'application (suivre l'assistant d'installation)
3. Lancez Docker Desktop et attendez qu'il affiche ¨Docker is running¨
4. Vérifiez l'installation en ouvrant le terminal:
```bash
docker --version

# Vérifier la version de Docker Compose
docker compose version
```

##### Linux (Ubuntu/Debian)
```bash
# Installer Docker
udo apt-get update
sudo apt-get install docker.io docker-compose-plugin

# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER

# Appliquer les changements immédiatement
newgrp docker

# Vérifier l'installation
docker --version
docker compose version
```

## Lancement du projet
### Installation
```bash
# 1. Cloner le projet
git clone https://github.com/acvdm/api_immo.git api_immo
cd api_immo/project

# 2. Lancer les services (api et db)
docker compose up -d

# Vérifier que les conteneurs sont en cours d'exécution
docker ps
```

L'API est disponible sur http://localhost:5000

### Arrêter l'application
```bash
# Arrêter les conteneurs
docker compose down

# Réinitialisation complète
docker compose down -v
```

### Résolution des problèmes
#### Le port 5432 ou 5000 est déjà utilisé
Modifier les ports dans `docker-compose.yml`:
```yaml
ports:
  - "5433:5432" # PostgreSQL
  - "5001:5000" # API
```

#### Erreur "Database does not exist"
Réinitialiser les volumes
```bash
# Réinitialiser
docker compose down -v

# Relancer
docker compose up -d
```

## Endpoints disponibles
### Users 
- `POST /users` > Créer un utilisateur
- `GET /users` > Lister tous les utilisateur de la plateforme
- `GET /users/{id}` > Lister les infos personnelles d'un utilisateur
- `PATCH /users/{id}` > Modifier ses infos personnelles (header `X-User-Id` requis)
- `POST /users/login` > Authentification d'un utilisateur
    
### Properties 
- `POST /properties` > Créer un bien (header `X-User-Id` requis)
- `GET /properties` > Lister tous les biens de la plateforme
- `GET /users/{id}/properties` > Lister les biens d'un utilisateur
- `GET /properties/{id}` > Lister les caractéristiques d'un bien
- `GET /properties?city={city}` > Lister tous les biens avec un filtre par ville
- `PATCH /properties/{id}` > Modifier les caractéristiques d'un bien (header `X-User-Id` requis)
- `DELETE /properties/{id}` > Supprimer un bien (header `X-User-Id` requis)

### Rooms 
- `POST /properties/{property_id}/rooms` > Créer une pièce 
- `GET /properties/{property_id}/rooms` > Lister les pièces d'un bien
- `GET /rooms/{id}` > Lister les caractéristiques d'une pièce spécifique
- `PATCH /rooms/{id}` > Modifier les caractéristiques d'une pièce (header `X-User-Id` requis),
- `DELETE /rooms/{id}` > Supprimer une pièce (header `X-User-Id` requis)
  

## Utilisation
### Authentification
L'API utilise un sytème simple basé sur le header **'X-User-Id'** pour identifier l'utilisateur.
Pour certains endpoints, ajoutez ce header (1 étant le user_id du propriétaire du bien, à adapter)
```bash
-H "X-User-Id: 1"
```  
  
### Créer un utilisateur
```bash
curl -X POST http://localhost:5000/users \
-H "Content-Type: application/json" \
-d '{    
    "email": "john@example.com",
    "last_name": "Doe",
    "first_name": "John",
    "birth_date": "1990-01-01"
}'
```

### Rechercher tous les utilisateurs de la plateforme
```bash
curl -X GET http://localhost:5000/users
```

### Modifier les informations personnelles d'un utilisateur - header **'X-User-Id'** requis
```bash
curl -X PATCH http://localhost:5000/users/1 \
-H "Content-Type: application/json" \
-H "X-User-Id: 1" \
-d '{
    "email": "johndoe1@gmail.com" 
}'
```

### Créer un bien - header **'X-User-Id'** requis
```bash
curl -X POST http://localhost:5000/properties \
-H "Content-Type: application/json" \
-H "X-User-Id: 1" \
-d '{
  "name": "Maison a vendre",
  "description": "Dans le centre de Clichy, rue du Landy, proche de la mairie et des commerces, une maison de ville de 160m2 habitables avec son jardin de 75m2.",
  "type": "Maison",
  "city": "Clichy",
  "price": "1299000",
  "size": "160"
}'
```

### Filtrer les biens par ville
```bash
curl -X GET http://localhost:5000/properties?city=Clichy
```

### Ajouter une pièce à un bien - header **'X-User-Id'** requis
#### 1 étant l'id du bien (à adapter)  
```bash
curl -X POST http://localhost:5000/properties/1/rooms \
-H "Content-Type: application/json" \
-H "X-User-Id: 1" \
-d '{
"type": "Kitchen",
"size": "14"
}'
```

