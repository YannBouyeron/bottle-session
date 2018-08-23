# bottle-session

Gestion des sessions users et administrateur avec bottle

## Présentation

Le fichier Administrator.py est un module qui permet la gestion des sessions; cette gestion minimaliste repose sur une base de données sqlite dans laquelle sont enregistrés les ID , mail, hash du password, level, date de création du compte, et date de dernière connection de chaque utilisateur.

Le fichier Formulator.py est un module qui facilite l’utilisation des formulaires html.

Le fichier config.txt contient les données du compte Administrateur (compte indépendant de la base de données sqlite), parametrable depuis l’interface du site MySite.py.

Le fichier MySite.py est le backend d’un site permettant la gestion des users (et exploitant le module Administrator.py).

Le dossier views contient les templates html.

Le dossier static contient les fichiers css.

## Dépendances

L’ensemble fonctionne sous Python 3 (testé sur python 3.6)

Les modules python suivant sont necessaires:

- json
- sys
- sqlite3
- hashlib
- time

- numpy
- bottle

## Fonctionnalités

- Création automatique de la base de données lors du premier démarrage du site
- Inscritpion user (avec mot de passe envoyé par mail à l’user)
- Connection user
- Déconnection user
- Désincription user
- Modification mot de passe user
- Accès restreint des users en fonction de leur level
 
- Accès Administrateur (route: "/acces")
- Modification des identifiants Administrateur (par défaut: Admi, 1234)
- Visualisation de la base de données
- Modification des level des users
- Mail liste

## Paramétrage

Dans le fichier Administrator.py, modifiez:

- la ligne 45 pour changer le nom du site
- les lignes 46 et 47 pour indiquer le mail et le mdp 
- la ligne 394 si votre boite mail n’est pas hotmail/live/outlook

## Démarage du site en local

	python MySite.py

## Contact

yann.bouyeron@hotmail.fr
 

## Licence

L’ensemble du repository est sous licence AGPL

</br>

Copyright (C) 2018  Yann Bouyeron

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.     
 
 
 
 
 
 
 
