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