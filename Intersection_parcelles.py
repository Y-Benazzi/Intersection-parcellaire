import sys
import subprocess
python = sys.executable
subprocess.check_call([python, '-m', 'pip', 'install', 'requests'])
pip install geopandas

import geopandas as gpd

# Chemins vers fichiers shapefiles (à adapter en fonction de la ou sont les docs ( voir si on crée pas un fichier permanent pour le lancer là bas))
entree_croisement_parcelle = 'chemin/vers/supports.shp'
parcelles_path = 'chemin/vers/parcelles.shp'
sortie_path = 'chemin/vers/supports_avec_parcelles.shp'

# Charger les shapefiles
supports = gpd.read_file(entree_croisement_parcelle)
parcelles = gpd.read_file(parcelles_path)

 Vérifier les systèmes de coordonnées (CRS) et les aligner si nécessaire ( voir si problemes de coordonnées reactiver)
if supports.crs != parcelles.crs:
    supports = supports.to_crs(parcelles.crs)

# Effectuer une jointure spatiale : chaque support récupère les attributs de la parcelle qu'il intersecte
# Utilise 'left' pour garder tous les supports, même s'ils n'intersectent pas (mais normalement ils devraient)
supports_avec_parcelles = gpd.sjoin(supports, parcelles, how='left', predicate='intersects')

# choisir les colonnes à garder : géométrie des supports + attributs des parcelles (SECTION, NUMERO, CODE_DEP, etc.) 
# adapter la liste des colonnes selon les attributs exacts du shapefile parcelles
colonnes_a_garder = ['geometry'] + list(supports.columns) + ['SECTION', 'NUMERO', 'CODE_DEP']  # Ajouter les colonnes que je veux entre crochets
supports_avec_parcelles = supports_avec_parcelles[colonnes_a_garder]

# Sauvegarder le résultat dans un nouveau shapefile
supports_avec_parcelles.to_file(sortie_path)


print("Jointure spatiale terminée. Résultat sauvegardé dans :", sortie_path)

