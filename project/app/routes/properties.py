# Attributs: id, owner_id, name, description, type, city, price (integer), size (m2).  



# créer un bien. `POST /properties` user_id requis,



# lister tous les biens de la plateforme. `GET /properties`



# lister les caractéristiques d'un bien. `GET /properties/{id}`



# lister tous les biens avec un filtre par ville. `GET /properties?city={city}`



# modifier les caractéristiques d'un bien. `PATCH /properties/{id} avec` ownership check,



# supprimer un bien. `DELETE /properties/{id}` avec ownership check.