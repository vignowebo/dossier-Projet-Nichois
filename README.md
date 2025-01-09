# Projet de Nichoir Connecté

## Objectif
Concevoir un nichoir intelligent et connecté qui permet de suivre la vie des oiseaux tout en restant accessible en termes de coût et en offrant une autonomie énergétique prolongée.

## Caractéristiques principales
- **Prix** : Moins de 50 €
- **Autonomie énergétique** : 6 mois à 1 an sur batterie
- **Évolutif** : Possibilité d'ajouter un panneau solaire pour prolonger l'autonomie

## Tâches à réaliser
1. Surveiller l'activité dans le nichoir via un système de détection de mouvement et de capture d'images.
2. Réduire la consommation énergétique pour garantir une autonomie optimale.
3. Publier et présenter les données sous une forme lisible et attrayante.

## Matériels utilisés
- **ESP32-CAM** : Module principal pour la capture d'images et la détection de mouvement
- **Raspberry Pi 4** : Sert de broker MQTT
- **Capteur PIR** : Pour la détection de mouvement

## Technologies utilisées
- **MQTT** : Protocole de communication pour transmettre les données
- **InfluxDB Cloud** : Base de données pour le stockage des données collectées
- **Grafana** : Outil de visualisation pour afficher les données sous forme de tableaux de bord

## Détails du projet
Ce projet est réalisé avec **MicroPython**. Avant de démarrer, nous avons acquis les notions de base de l'ESP32-CAM et de MicroPython en utilisant l'IDE **Thonny**. Ces étapes préliminaires sont documentées dans le dossier **Code Prototype**.

### Organisation des codes
- **Dossier "Code Main"** : Contient les codes finaux pour l'ESP32-CAM utilisés dans le projet.
- **Dossier "Code côté RPi"** : Inclut les scripts pour le Raspberry Pi 4 ainsi que les configurations associées.

## Conclusion
Ce nichoir connecté vise à offrir une solution abordable et écologique pour observer et comprendre la vie des oiseaux, tout en exploitant des technologies modernes pour une expérience intuitive et innovante.

