# Attributs: id, property_id, type (bedroom/kitchen/etc.), size (m2)  



# créer une pièce. `POST /properties/{property_id}/rooms`



# lister les pièces d'un bien. `GET /properties/{property_id}/rooms`



# lister les caractéristiques d'une pièce spécifique. `GET /rooms/{id}`



# modifier les caractéristiques d'une pièce. `PATCH /rooms/{id}` avec ownership check,



# supprimer une pièce. `DELETE /rooms/{id}` avec ownership check. 