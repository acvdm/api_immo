# PITCH - Microservice de gestion immobilière - Python/Flask

## Problem:
Les utilisateurs d'une plateforme de gestion immobilière n'ont pas la possibilité de gérer 
leurs biens de façon structurée.
Nous voulons que les utilisateurs puissent:
- renseigner un bien immobilier (nom, description, type de bien, ville, pièces, caractéristiques des pièces, propriétaire),
- modifier/ renseigner leurs informations personnelles sur la plateforme, 
- consulter les autres biens disponibles sur la plateforme en appliquant un filtre géographique.

Nous souhaterions si possible que:  
Un propriétaire ne puisse modifier que les caractéristiques de son bien sans avoir accès à l'édition des autres biens.


## Appetite:
- Temps imparti pour ces fonctionnalités: 7 jours,
- Taille de l'équipe: 1 développeur, 
- Deadline: Mardi 16/12/2025,
- Type de livrable: MVP fonctionnel


## Solution:
### Breadboard:
  1. `[User]` -> Créer un compte (`POST /users`)
  2. `[User]` -> Se connecter (`POST /users/login`)
  3. `[User]` -> Créer un bien (`POST /properties`)
  4. `[User]` -> Ajouter des pièces à un bien (`POST /properties/{property_id}/rooms`)
  5. `[User]` -> Afficher les biens (GET /properties?city=Paris)
  6. `[Owner]` -> Modifier seulement ses propres biens (ownership check → 403 si violation)  

### Fat marker sketch:
    - Flask REST API
      - `/users` -> auth + CRUD
      - `/properties` -> CRUD + filter
      - `/rooms` -> CRUD nested  

    - Base de données: PostgreSQL
      - users (1)
      - properties (N)
      - rooms (N)

### Fonctionnalités détaillées:
  - User management (must-have):  
  Attributs: id, email (unique), last_name, first_name, birth_date, created_at.  
    - créer un utilisateur. `POST /users`
    - lister les infos personnelles d'un utilisateur. `GET /users/{id}`
    - lister tous les utilisateur de la plateforme. `GET /users` 
    - modifier ses infos personnelles. `PATCH /users/{id}` avec ownership check
    - lister les biens d'un utilisateur. `GET /users/{id}/properties`
    - authentification du user. `POST /users/login`  
    
  - Property management (must-have):  
  Attributs: id, owner_id, name, description, type, city, price (integer), size (m2), created_at.  
    - créer un bien. `POST /properties` user_id requis,
    - lister tous les biens de la plateforme. `GET /properties`
    - lister les caractéristiques d'un bien. `GET /properties/{id}`
    - lister tous les biens avec un filtre par ville. `GET /properties?city={city}`
    - modifier les caractéristiques d'un bien. `PATCH /properties/{id} avec` ownership check,
    - supprimer un bien. `DELETE /properties/{id}` avec ownership check.  
   
  - Room management (must-have):  
  Attributs: id, property_id, type (bedroom/kitchen/etc.), size (m2), created_at  
    - créer une pièce. `POST /properties/{property_id}/rooms`
    - lister les pièces d'un bien. `GET /properties/{property_id}/rooms`
    - lister les caractéristiques d'une pièce spécifique. `GET /rooms/{id}`
    - modifier les caractéristiques d'une pièce. `PATCH /rooms/{id}` (avec ownership check),
    - supprimer une pièce. `DELETE /rooms/{id}` (avec ownership check).  
  
  - Ownership control (nice-to-have):  
    - on ne peut modifier que ses propres informations personnelles en tant qu'utilisateur,
    - un propriétaire ne peut modifier/ supprimer que ses propres biens,
    - vérification sur tous les endpoints sensibles: PATCH/DELETE,
    - une réponse HTTP 403 FORBIDDEN sera envoyée en cas de tentative d'accès non autorisé
    - Approche simple: le user_id sera vérifié grâce au header X-User-Id dans chaque requête,
    - Alternative si le temps le permet: JWT tokens 
    => property.owner_id == current_user_id avant toute action de PATCH/DELETE


## Risques à éviter:
- authentification complexe: on ne fera qu'une authentification simulée avec header X-User-Id. Si le temps le permet JWT simple sans refresh
- architecture trop complexe avec des Microservices: architecture monolithique en 2 conteneurs (db et api sans séparation des logiques métiers) 
- features non demandées: rester sur le scope, et implémenter des features utiles si le temps le permet
- deletes en cascade complexes: cascade='all-delete-orphan'


## No-Gos:
  - Frontend
  - déploiement


## Scopes:
### Must-have:
- Scope 1 : User CRUD + login simple (1 j)
- Scope 2 : Property CRUD (1 j)
- Scope 3 : Room CRUD (1 j)
- Scope 4 : Filtrage par ville (0.5 j)
- Scope 5 : README clair pour run local (0.5 j)
- Scope 6 : Debug & ajustements (1 j)

### Nice-to-have:
- Scope 7 : ownership control (1j)
- Scope 8 : tests unitaires (0.5j)


## Done means:
1. Un utilisateur peut s'inscrire,
2. Un utilisateur peut se connecter,
3. Un utilisateur peut créer un bien,
4. Un utilisateur peut modifier / ajouter des pièces à son bien, 
5. Un utilisateur peut renseigner / modifier ses infos personnelles,
6. GET /properties?city=Paris retourne uniquement les biens parisiens,
7. Un utilisateur ne peut pas modifier le bien d'un autre utilisateur (403 Forbiden),
8. l'API retourne des erreurs HTTP appropriées (400, 404, 403, 500)
9. Le README permet de lancer le projet en 5 minutes


## Stack technique:
- **Langage**: Python (requis)
- **Framework**: Flask (requis, adapté aux APIs REST),
- **Base de données**: PostreSQL (Relationnel),
- **Eventuel ORM**: SQLAlchemy (standard python, puissant pour les relations),
- **Tests**: Pytest (standard python pour tests unitaires),
- **Auth**: Header custom (simple pour un MVP, evolutif vers JWT)