# LaPlatineDuTinky
La Platine est une interface graphique pour gérer un bot discord audio.
<br>
![image](https://user-images.githubusercontent.com/104074343/229366817-d1d3d041-2b2f-45d5-8806-76582e3f2c93.png)

Pour faire fonctionner la Platine, veillez à remplir correctement ces 3 paramètres du fichier `config.ini`:

![image](https://user-images.githubusercontent.com/104074343/229365946-7413daaa-fd8c-442b-b357-4d050fa824ce.png)

<br>

### Comment récupérer ces 3 paramètres ?
#### Récupérer le token :
Aller sur le [Discord Developer Portal](https://discord.com/developers/applications).
<br><br>
Si vous ne l'avez pas encore fait, créez votre bot, puis ajoutez-le à votre serveur.
<br>
![image](https://user-images.githubusercontent.com/104074343/229367018-174341d9-3f80-44f3-bb5b-155eb05a2db6.png)
<br><br>
Une fois que vous avez une application, rendez-vous dans la section "Bot" :
<br>![image](https://user-images.githubusercontent.com/104074343/229367203-5de91a14-6c7c-4129-bb53-ca2c0afa2c5e.png)
<br><br>
Vous trouverez le token ici si vous venez de créer le bot, sinon regénérez le.
<br> ![image](https://user-images.githubusercontent.com/104074343/229367299-2882cc93-9fed-44a1-96cd-fce0497e3f75.png)
<br><br><br>
#### Récupérer votre identifiant Discord (owner_id) :
Rendez-vous dans vos paramètres Discord, Paramètres de l'appli, Avancés
<br>![image](https://user-images.githubusercontent.com/104074343/229367458-c4a70877-0880-42cb-a72c-4517a6b2d220.png)
<br><br>
Activez le Mode développeur
<br>![image](https://user-images.githubusercontent.com/104074343/229367528-fc1ed3f6-fad3-44b3-8c7b-eb8825be0854.png)
<br><br>
En faisant un clic droit sur votre profil, vous pouvez désormais récupérer votre identifiant
<br>![image](https://user-images.githubusercontent.com/104074343/229367677-beeff0fd-a641-41f6-98d4-db8798cd7e98.png)
<br><br><br>
#### Récupérer l'identifiant Discord du salon vocal par défaut (default_channel_id) :
Activez le mode développeur de Discord [comme expliqué précédemment](https://github.com/CedricHombourger/LaPlatineDuTinky/edit/master/README.md#r%C3%A9cup%C3%A9rer-votre-identifiant-discord-owner_id-).
<br><br>
En faisant un clic droit sur le salon que vous voulez définir comme par défaut pour le bot, vous pouvez récupérer son identifiant.
<br>![image](https://user-images.githubusercontent.com/104074343/229368068-f622ca37-8d96-414f-83da-2a87f7e5563c.png)




<br><br>
## Fonctionnalités :
- Se connecte automatiquement au salon vocal où se trouve son propriétaire
- Affiche le nom du bot qu'il contrôle
- Affiche le salon où il est connecté et le met à jour en cas de changement
- Peut se reconnecter au salon vocal où se trouve son propriétaire en appuyant sur un bouton
- Peut activer ou désactiver le son sortant du bot avec un switch ressemblant à un vinyle
- Un switch permettant d'activer l'auto-connexion au salon vocal où se trouve son propriétaire au démarrage
- Un switch permettant d'activer le suivi du propriétaire lorsqu'il change de salon vocal

<br>

## A faire :
- Sélection de vinyle parmi une bibliothèque pour mettre en status discord
- Sélection de périphérique audio (pour l'instant il utilise le microphone par défaut de l'ordinateur)
- Un switch permettant d'activer l'auto-play au lancement
- Un switch permettant d'activer le mode "lite" (désactiver les animations)
- Un champ de saisie pour un status discord personnalisé
