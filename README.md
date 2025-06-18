# Projet Django - Facture-Generator-Alltoo

## Installation et lancement du projet

### 1. environnement virtuel

```bash
python -m venv venv
```

## activation de l'environnement virtuel
- Sur Windows :

```bash
venv\Scripts\activate
```
- Sur macOS/Linux :

```bash
source venv/bin/activate
```

### 2. installation des dépendances

```bash
pip install -r requirements.txt
```

### 3. création de la base de données

```bash
python manage.py migrate
```

### 4. lancement du serveur

```bash
python manage.py runserver
```


[URL de l'app](http://127.0.0.1:8000/)

# Documentation - Gestion des Produits et Factures

Cette application Django permet de gérer des **produits** et de créer des **factures** associées. Elle inclut la gestion complète CRUD, recherche, tri, pagination, et génération PDF.

---

## Vues principales

### `produit_list(request)`

- Affiche la liste paginée (5 par page) des produits.
- Recherche possible par nom (partiel) ou ID exact via paramètre `q`.
- Tri possible par nom, prix, date de péremption ou ID (`sort`).
- Permet d'ajouter un nouveau produit via formulaire POST.
- Permet d'afficher des formulaires de modification inline pour chaque produit affiché.
- Donne aussi la liste des produits pour suppression.

---

### `facture_creer(request)`

- Affiche la liste paginée (7 par page) des produits pour sélection.
- Recherche et tri similaires à `produit_list`.
- POST : création d'une nouvelle facture à partir des produits sélectionnés (avec quantités comptées).
- Crée des objets `LigneFacture` liés à la facture, incluant quantité et prix.

---

### `facture_detail(request, facture_id)`

- Détail d'une facture donnée.
- Affiche les lignes de facture (produit + quantité + prix).
- Recherche et tri sur les lignes par produit (nom ou ID).
- Pagination (5 lignes par page).

---

### `facture_list(request)`

- Liste paginée (7 par page) des factures.
- Recherche par ID uniquement.
- Tri par date ou total de la facture.
- Annotation calculant la somme totale des lignes de chaque facture.

---

### `produit_supprimer(request, produit_id)`

- Confirmation suppression produit.
- Suppression effective via POST.

---

### `facture_supprimer(request, facture_id)`

- Confirmation suppression facture.
- Suppression effective via POST.

---

### `produit_modifier(request, produit_id)`

- Formulaire de modification produit.
- En POST, met à jour le produit et redirige vers la liste.

---

### `facture_pdf(request, facture_id)`

- Génère et retourne un PDF de la facture.
- Utilise `xhtml2pdf` pour convertir un template HTML en PDF.

---

## Templates clés

### `confirmer_suppression.html`

- Page générique pour confirmer la suppression d'un produit ou d'une facture.
- Affiche le type et nom de l'objet.
- Bouton "Oui, supprimer" en POST.
- Bouton "Annuler" redirige vers la liste des produits.

---

### `facture_creer.html`

- Formulaire avec recherche et tri des produits.
- Affichage paginé des produits avec cases à cocher pour sélection.
- Bouton pour créer la facture à partir des produits sélectionnés.

---

## Remarques techniques

- Utilisation de `Paginator` Django pour gérer la pagination.
- Recherche avec filtres conditionnels suivant si la requête est un nombre ou un texte.
- Tri contrôlé par une liste blanche des champs autorisés.
- Gestion des formulaires avec `ProduitForm`.
- Génération PDF via `xhtml2pdf` avec templates HTML dédiés.
- Relations Django ORM entre `Facture`, `Produit` et `LigneFacture`.
- Utilisation de `Counter` Python pour compter les quantités sélectionnées.

---

## Exemple de paramètres URL

- `?q=banane` — recherche par nom partiel.
- `?q=12` — recherche par ID égal à 12.
- `?sort=prix` — tri croissant par prix.
- `?page=2` — affiche la page 2.

---

Cette documentation couvre la base de fonctionnement de l'app et ses composants essentiels.  
Pour toute évolution, veille à respecter les conventions sur les recherches, tris et pagination existantes.

## Auteur

**Titouan Layeux**
