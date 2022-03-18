# P12_architecture_backend

## Instructions :


1) Installation python :
- Allez sur [https://www.python.org/downloads/](url) , et télécharger la dernière version de python, puis lancez le fichier 
  téléchargé pour l'installer.

2) Télécharger le code :
- Sur le repository github, cliquez sur le bouton "Code", puis "Download ZIP".
- Ensuite décompressez le fichier dans votre dossier de travail.

3) creation environnement virtuel :
- Ouvrez un terminal, puis allez dans votre dossier de travail avec la commande cd.
- Dans le terminal, tapez : ``` python3 -m venv env ```

4) Activer l'environnement virtuel :
  - Si vous êtes sous mac, ou linux :
    - tapez : ```source env/bin/activate ```
  - Si vous êtes sous windows :
    - tapez ```env/Scripts/activate.bat```

5) Installer les modules necessaires :
  - tapez ```pip install -r requirements.txt```
 
6) lancer le server local :
- dans le terminal tapez : ```python3 manage.py runserver```
- Une fois le serveur lancé, vous pourrez accéder au site à l'adresse indiquée dans le terminal ( par defaut : http://127.0.0.1:8000/ )

7) pour couper le serveur local tapez <kbd>Ctrl</kbd> + <kbd>C</kbd>  dans le terminal d'ou le serveur a été lancé.


8) Pour fermer l'environnement virtuel :
- Dans le terminal, tapez : ```deactivate ```

(L'environnement virtuel et les modules n'ont besoin d'etre installés qu'une seul fois, par la suite, vous devez juste activer l'environnement virtuel et lancer le serveur.)

## Paramètrage de la base de données :

Le projet est paramètré pour utiliser une base de donnée PostgreSQL, avec les caracateristiques suivantes :

> - database name : db_epicevents
> - db username : postgres
> - db password : postgres


## compte superuser et page d'administration :
pour acceder à l'interface d'administration du site, connectez vous à l'url [127.0.0.1:8000/admin/](url) avec les identifiants suivant :
>   - username : epicevents
>   - password : epicevents


# API :
## Endpoints :

Le projet se compose d'une API utilisant DjangoRestFramework, avec les endpoints suivants :

* ```http://127.0.0.1:8000/api/customers/``` : renvoie la liste des clients enregistrés

* ```http://127.0.0.1:8000/api/customers/<customer_id>/``` : renvoie les details du client

* ```http://127.0.0.1:8000/api/contracts/``` : renvoie la liste des contrats enregistrés

* ```http://127.0.0.1:8000/api/contracts/<contract_id>/``` : renvoie les details du contrat

* ```http://127.0.0.1:8000/api/events/``` : renvoie la liste des événements enregistrés

* ```http://127.0.0.1:8000/api/events/<event_id>/``` : renvoie les details de l'événement

* ```http://127.0.0.1:8000/api/users/``` : renvoie la liste des utilisateurs enregistrés

* ```http://127.0.0.1:8000/api/users/<user_id>``` : renvois les details de l'utilisateur 
* ```http://127.0.0.1:8000/api/login/``` : recuperation de ses tokens de connexions
* ```http://127.0.0.1:8000/api/login/refresh/``` : renouveler son token d'acces
* ```http://127.0.0.1:8000/api/signup/``` : s'enregistrer sur l'API
* ```http://127.0.0.1:8000/api/password_update/``` : modifier son mot de passe.


Tout les endpoints supportent les operations CRUD, Si les permissions de l'utilisateurs l'y autorisent.

## Filtrage :
les filtres disponibles pour chaque endpoint :

* ```customers/``` :
  - ```email```
  - ```last_name```
  - ```company```
  - ```sale_contact```

* ```contracts/``` :
  - ```customer__email```
  - ```customer__last_name```
  - ```customer__company```
  - ```date_created```
  - ```amount```
  - ```sale_contact```

* ```events/``` :
  - ```customer__email```
  - ```customer__last_name```
  - ```customer__company```
  - ```event_date```
  - ```sale_contact```

* Exemples de filtrages :
  - ```http://127.0.0.1:8000/api/customers?email=<email>```
  - ```http://127.0.0.1:8000/api/customers?email=<email>&&company=<société>```


Pour les details de l'API, voir la documentation postman : 

# Application frontend :
L'acces se fait par defaut à l'url [http://127.0.0.1:8000/](url)

Pour vous connecter, rentrez votre username (votre adresse email), et votre mot de passe.

Une fois identifié, vous pourrez avoir acces et modifier les données directement depuis l'interface web, si votre compte y est autorisé.
