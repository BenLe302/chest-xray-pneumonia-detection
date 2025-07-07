# Chest X-Ray Pneumonia Detection

## 📋 Description du Projet

Ce projet vise à développer un système de détection automatique de pneumonie à partir de radiographies thoraciques en utilisant des techniques d'apprentissage automatique et de deep learning. Le système analyse des images de rayons X pour classifier automatiquement les cas normaux et les cas de pneumonie.

## 👨‍💻 Auteur

**Dady Akrou Cyrille**  
📧 Email: cyrilledady0501@gmail.com  
📍 Localisation: Trois-Rivières, Canada  
💼 Profession: Data Scientist

## 🎯 Objectifs

- Analyser et comprendre le dataset de radiographies thoraciques
- Développer un modèle de classification binaire (NORMAL vs PNEUMONIA)
- Optimiser les performances du modèle pour une utilisation médicale
- Créer une interface utilisateur pour la prédiction en temps réel
- Fournir des métriques d'évaluation adaptées au domaine médical

## 📊 Dataset

### Source et Description
Ce projet utilise le dataset **Chest X-Ray Images (Pneumonia)** disponible sur Kaggle :

- **Source :** [Kaggle - Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
- **Créateur :** Paul Mooney
- **Licence :** Disponible publiquement sur Kaggle

Le dataset contient des radiographies thoraciques classées en deux catégories :
- **NORMAL** : Radiographies sans pneumonie
- **PNEUMONIA** : Radiographies avec pneumonie

### Structure
- **Total**: ~5,856 images de radiographies thoraciques
- **Classes**: NORMAL (27%) et PNEUMONIA (73%)
- **Répartition**: Train/Test/Validation
- **Format**: Images JPEG en niveaux de gris
- **Résolution**: Variable (redimensionnement nécessaire)

### Problèmes Identifiés
- ⚠️ **Déséquilibre des classes**: Ratio PNEUMONIA:NORMAL = 2.70:1
- ⚠️ **Ensemble de validation très petit**: < 100 images
- ⚠️ **Dimensions variables**: Nécessite standardisation

## 🛠️ Technologies Utilisées

### Core Libraries
- **Python 3.8+**
- **TensorFlow/Keras** - Deep Learning
- **NumPy/Pandas** - Manipulation de données
- **OpenCV/Pillow** - Traitement d'images
- **Matplotlib/Seaborn** - Visualisation

### Machine Learning
- **Scikit-learn** - Métriques et preprocessing
- **Albumentations** - Augmentation de données
- **SHAP/LIME** - Interprétabilité du modèle

## 📁 Structure du Projet

```
Chest X-Ray Images (Pneumonia)/
├── config.py                 # Configuration centralisée
├── utils.py                  # Fonctions utilitaires
├── analyse_dataset.py        # Script d'analyse du dataset
├── requirements.txt          # Dépendances Python
├── README.md                # Documentation
├── data/                    # Données (non versionnées)
│   ├── train/
│   ├── test/
│   └── val/
├── models/                  # Modèles sauvegardés
├── notebooks/               # Jupyter notebooks
├── outputs/                 # Résultats et visualisations
├── logs/                    # Fichiers de logs
└── src/                     # Code source principal
    ├── preprocessing/
    ├── models/
    ├── evaluation/
    └── deployment/
```

## 🚀 Installation et Configuration

### 1. Cloner le Repository
```bash
git clone <repository-url>
cd "Chest X-Ray Images (Pneumonia)"
```

### 2. Créer un Environnement Virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
- Modifier `config.py` selon vos besoins
- Ajuster les chemins des données
- Configurer les hyperparamètres

## 📈 Utilisation

### Analyse du Dataset

#### Option 1 : Script Python
```bash
python analyse_dataset.py
```

#### Option 2 : Notebook Jupyter
```bash
jupyter notebook analyse_complete_dataset.ipynb
```

Les deux options génèrent :
- 📊 Statistiques détaillées du dataset
- 📈 Visualisations avancées
- 📋 Rapport d'analyse JSON
- 💡 Recommandations ML

### Avantages du Notebook
- Interface interactive
- Visualisations intégrées
- Documentation complète
- Exécution cellule par cellule
- Crédits et références inclus

### Entraînement du Modèle
```bash
python src/models/train_model.py
```

### Évaluation
```bash
python src/evaluation/evaluate_model.py
```

### Prédiction
```bash
python src/deployment/predict.py --image path/to/xray.jpg
```

## 📊 Métriques d'Évaluation

### Métriques Primaires
- **Sensibilité (Recall)**: > 90% pour PNEUMONIA
- **Spécificité**: > 80% pour NORMAL
- **F1-Score**: > 85% global

### Métriques Secondaires
- **AUC-ROC**: > 0.95
- **Précision équilibrée**
- **Matrice de confusion détaillée**

### Métriques Médicales
- **Valeur Prédictive Positive (VPP)**
- **Valeur Prédictive Négative (VPN)**
- **Likelihood Ratios**

## 🔧 Stratégies d'Optimisation

### Gestion du Déséquilibre
1. **Pondération des classes**: `class_weight='balanced'`
2. **SMOTE**: Sur-échantillonnage intelligent
3. **Focal Loss**: Fonction de perte adaptée
4. **Augmentation ciblée**: Plus d'augmentation pour NORMAL

### Architecture Recommandée
1. **Transfer Learning**: ResNet50, EfficientNet
2. **Fine-tuning progressif**
3. **Dropout**: 0.3-0.5
4. **Batch Normalization**
5. **Learning Rate Scheduling**

### Augmentation de Données
- Rotation: ±15°
- Translation: ±10%
- Zoom: ±10%
- Flip horizontal
- Ajustements de contraste/luminosité

## 📋 Roadmap

### Phase 1: Analyse et Préparation ✅
- [x] Analyse exploratoire du dataset
- [x] Configuration du projet
- [x] Modules utilitaires
- [x] Documentation

### Phase 2: Développement du Modèle 🔄
- [ ] Preprocessing pipeline
- [ ] Modèle baseline
- [ ] Transfer learning
- [ ] Optimisation hyperparamètres

### Phase 3: Évaluation et Validation 📋
- [ ] Métriques d'évaluation
- [ ] Validation croisée
- [ ] Tests sur données externes
- [ ] Analyse d'erreurs

### Phase 4: Déploiement 🚀
- [ ] Interface utilisateur
- [ ] API REST
- [ ] Containerisation Docker
- [ ] Documentation utilisateur

## 🤝 Contribution

Ce projet est développé par Dady Akrou Cyrille. Pour toute question ou suggestion:

📧 **Email**: cyrilledady0501@gmail.com

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- Dataset fourni par Kermany et al. via Kaggle
- Communauté open source pour les outils utilisés
- Ressources éducatives en machine learning médical

---

**Note**: Ce projet est développé à des fins éducatives et de recherche. Il ne doit pas être utilisé pour des diagnostics médicaux réels sans validation clinique appropriée.