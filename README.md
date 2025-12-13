# Microservice de gestion immobilière

API REST en Python/Flask pour gérer des biens immobiliers, leurs pièces et les utilisateurs.

## Démarrage

### Prérequis
- Docker
- Docker Compose

### Installation
```bash
# 1. Cloner le projet
$ git clone https://github.com/acvdm/api_immo.git api_immo
$ cd api_immo/project

# 2. Lancer les services (api et db)
$ docker compose up --build

# 3. L'API est disponible sur http://localhost:5000
```

## Endpoints disponibles
### Users 
- `POST /users` > Créer un utilisateur
- `GET /users/{id}` > Lister les infos personnelles d'un utilisateur
- `GET /users` > Lister tous les utilisateur de la plateforme
- `PATCH /users/{id}` > Modifier ses infos personnelles (header `X-User-Id` requis)
- `GET /users/{id}/properties` > Lister les biens d'un utilisateur
- `POST /users/login` > Authentification d'un utilisateur
    
### Properties 
- `POST /properties` > Créer un bien (header `X-User-Id` requis)
- `GET /properties` > Lister tous les biens de la plateforme
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
```bash
curl -X POST http://localhost:5000/1/rooms \
-H "Content-Type: application/json" \
-H "X-User-Id: 1" \
-d '{
"type": "Kitchen",
"size": "14"
}'
```

