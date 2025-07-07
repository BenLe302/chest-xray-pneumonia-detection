# Configuration du projet Chest X-Ray Pneumonia Detection
# Auteur: Dady Akrou Cyrille
# Email: cyrilledady0501@gmail.com
# Localisation: Trois-Rivières, Canada

import os
from pathlib import Path

# Configuration des chemins
PROJECT_ROOT = Path(__file__).parent
DATASET_PATH = PROJECT_ROOT / "chest_xray DataSet"
OUTPUT_PATH = PROJECT_ROOT / "outputs"
MODELS_PATH = PROJECT_ROOT / "models"
LOGS_PATH = PROJECT_ROOT / "logs"

# Créer les dossiers s'ils n'existent pas
for path in [OUTPUT_PATH, MODELS_PATH, LOGS_PATH]:
    path.mkdir(exist_ok=True)

# Configuration du dataset
CLASSES = ['NORMAL', 'PNEUMONIA']
SUBSETS = ['train', 'test', 'val']

# Configuration des images
IMAGE_SIZE = (224, 224)  # Taille standard pour les modèles pré-entraînés
BATCH_SIZE = 32
COLOR_MODE = 'rgb'

# Configuration du modèle
LEARNING_RATE = 0.001
EPOCHS = 50
PATIENCE = 10  # Pour early stopping
VALIDATION_SPLIT = 0.2

# Configuration de l'augmentation de données
AUGMENTATION_CONFIG = {
    'rotation_range': 20,
    'width_shift_range': 0.2,
    'height_shift_range': 0.2,
    'horizontal_flip': True,
    'zoom_range': 0.2,
    'fill_mode': 'nearest'
}

# Configuration des métriques
METRICS = ['accuracy', 'precision', 'recall', 'f1_score', 'auc']

# Configuration de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Configuration pour le déséquilibre des classes
CLASS_WEIGHTS = {
    0: 1.0,  # NORMAL
    1: 0.37  # PNEUMONIA (ajusté selon le ratio 2.7:1)
}

# Informations du projet
PROJECT_INFO = {
    'name': 'Chest X-Ray Pneumonia Detection',
    'author': 'Dady Akrou Cyrille',
    'email': 'cyrilledady0501@gmail.com',
    'location': 'Trois-Rivières, Canada',
    'version': '1.0.0',
    'description': 'Système de détection automatique de pneumonie sur radiographies thoraciques'
}