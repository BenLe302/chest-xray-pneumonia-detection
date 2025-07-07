# Utilitaires pour le projet Chest X-Ray Pneumonia Detection
# Auteur: Dady Akrou Cyrille
# Email: cyrilledady0501@gmail.com

import os
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.utils.class_weight import compute_class_weight
import json
from datetime import datetime
from config import *

def setup_logging(log_file=None):
    """
    Configure le système de logging pour le projet.
    
    Args:
        log_file (str, optional): Nom du fichier de log
    """
    if log_file is None:
        log_file = LOGS_PATH / f"chest_xray_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configuré - Fichier: {log_file}")
    return logger

def count_images_in_directory(directory_path):
    """
    Compte le nombre d'images dans un répertoire.
    
    Args:
        directory_path (Path): Chemin vers le répertoire
        
    Returns:
        int: Nombre d'images trouvées
    """
    if not directory_path.exists():
        return 0
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    return len([f for f in directory_path.iterdir() 
               if f.suffix.lower() in image_extensions])

def get_dataset_statistics(dataset_path):
    """
    Génère des statistiques complètes sur le dataset.
    
    Args:
        dataset_path (Path): Chemin vers le dataset
        
    Returns:
        dict: Dictionnaire contenant les statistiques
    """
    stats = {}
    total_images = 0
    
    for subset in SUBSETS:
        subset_path = dataset_path / subset
        if subset_path.exists():
            stats[subset] = {}
            subset_total = 0
            
            for class_name in CLASSES:
                class_path = subset_path / class_name
                count = count_images_in_directory(class_path)
                stats[subset][class_name] = count
                subset_total += count
            
            stats[subset]['total'] = subset_total
            total_images += subset_total
    
    stats['total_dataset'] = total_images
    return stats

def calculate_class_weights(stats):
    """
    Calcule les poids des classes pour gérer le déséquilibre.
    
    Args:
        stats (dict): Statistiques du dataset
        
    Returns:
        dict: Poids calculés pour chaque classe
    """
    # Compter le total par classe
    class_counts = {class_name: 0 for class_name in CLASSES}
    
    for subset in SUBSETS:
        if subset in stats:
            for class_name in CLASSES:
                if class_name in stats[subset]:
                    class_counts[class_name] += stats[subset][class_name]
    
    # Calculer les poids
    total_samples = sum(class_counts.values())
    n_classes = len(CLASSES)
    
    weights = {}
    for i, class_name in enumerate(CLASSES):
        if class_counts[class_name] > 0:
            weights[i] = total_samples / (n_classes * class_counts[class_name])
        else:
            weights[i] = 1.0
    
    return weights

def analyze_image_properties(dataset_path, sample_size=50):
    """
    Analyse les propriétés des images (dimensions, format, etc.).
    
    Args:
        dataset_path (Path): Chemin vers le dataset
        sample_size (int): Nombre d'images à analyser par classe/subset
        
    Returns:
        dict: Propriétés analysées
    """
    properties = {
        'dimensions': [],
        'file_sizes': [],
        'formats': [],
        'color_modes': []
    }
    
    for subset in SUBSETS:
        subset_path = dataset_path / subset
        if not subset_path.exists():
            continue
            
        for class_name in CLASSES:
            class_path = subset_path / class_name
            if not class_path.exists():
                continue
            
            # Obtenir un échantillon d'images
            image_files = list(class_path.glob('*.jpg')) + list(class_path.glob('*.jpeg'))
            sample_files = image_files[:min(sample_size, len(image_files))]
            
            for img_file in sample_files:
                try:
                    with Image.open(img_file) as img:
                        properties['dimensions'].append(img.size)
                        properties['file_sizes'].append(img_file.stat().st_size)
                        properties['formats'].append(img.format)
                        properties['color_modes'].append(img.mode)
                except Exception as e:
                    logging.warning(f"Erreur lors de l'analyse de {img_file}: {e}")
    
    return properties

def create_advanced_visualizations(stats, properties, output_path):
    """
    Crée des visualisations avancées pour l'analyse du dataset.
    
    Args:
        stats (dict): Statistiques du dataset
        properties (dict): Propriétés des images
        output_path (Path): Chemin de sortie pour les graphiques
    """
    # Configuration du style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # Créer une figure avec plusieurs sous-graphiques
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Distribution des classes par subset
    ax1 = plt.subplot(2, 3, 1)
    subset_data = []
    for subset in SUBSETS:
        if subset in stats:
            for class_name in CLASSES:
                if class_name in stats[subset]:
                    subset_data.append({
                        'Subset': subset,
                        'Class': class_name,
                        'Count': stats[subset][class_name]
                    })
    
    df_subset = pd.DataFrame(subset_data)
    sns.barplot(data=df_subset, x='Subset', y='Count', hue='Class', ax=ax1)
    ax1.set_title('Distribution des Classes par Ensemble')
    ax1.set_ylabel('Nombre d\'Images')
    
    # 2. Répartition globale des classes
    ax2 = plt.subplot(2, 3, 2)
    total_by_class = {}
    for class_name in CLASSES:
        total_by_class[class_name] = sum(
            stats[subset].get(class_name, 0) for subset in SUBSETS if subset in stats
        )
    
    colors = ['lightblue', 'lightcoral']
    wedges, texts, autotexts = ax2.pie(
        total_by_class.values(), 
        labels=total_by_class.keys(),
        colors=colors,
        autopct='%1.1f%%',
        startangle=90
    )
    ax2.set_title('Répartition Globale des Classes')
    
    # 3. Distribution des dimensions d'images
    if properties['dimensions']:
        ax3 = plt.subplot(2, 3, 3)
        widths = [dim[0] for dim in properties['dimensions']]
        heights = [dim[1] for dim in properties['dimensions']]
        
        ax3.scatter(widths, heights, alpha=0.6)
        ax3.set_xlabel('Largeur (pixels)')
        ax3.set_ylabel('Hauteur (pixels)')
        ax3.set_title('Distribution des Dimensions')
        ax3.grid(True, alpha=0.3)
    
    # 4. Distribution des tailles de fichiers
    if properties['file_sizes']:
        ax4 = plt.subplot(2, 3, 4)
        file_sizes_mb = [size / (1024 * 1024) for size in properties['file_sizes']]
        ax4.hist(file_sizes_mb, bins=30, alpha=0.7, color='skyblue')
        ax4.set_xlabel('Taille du Fichier (MB)')
        ax4.set_ylabel('Fréquence')
        ax4.set_title('Distribution des Tailles de Fichiers')
        ax4.grid(True, alpha=0.3)
    
    # 5. Heatmap de corrélation des métriques
    ax5 = plt.subplot(2, 3, 5)
    if properties['dimensions']:
        metrics_data = {
            'Width': [dim[0] for dim in properties['dimensions']],
            'Height': [dim[1] for dim in properties['dimensions']],
            'Aspect_Ratio': [dim[0]/dim[1] for dim in properties['dimensions']],
            'File_Size_MB': [size / (1024 * 1024) for size in properties['file_sizes'][:len(properties['dimensions'])]]
        }
        
        df_metrics = pd.DataFrame(metrics_data)
        correlation_matrix = df_metrics.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax5)
        ax5.set_title('Corrélation des Métriques d\'Images')
    
    # 6. Tableau récapitulatif amélioré
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('tight')
    ax6.axis('off')
    
    # Créer un tableau détaillé
    table_data = []
    for subset in SUBSETS:
        if subset in stats:
            normal_count = stats[subset].get('NORMAL', 0)
            pneumonia_count = stats[subset].get('PNEUMONIA', 0)
            total_subset = normal_count + pneumonia_count
            ratio = pneumonia_count / normal_count if normal_count > 0 else 0
            
            table_data.append([
                subset.upper(),
                f"{normal_count:,}",
                f"{pneumonia_count:,}",
                f"{total_subset:,}",
                f"{ratio:.2f}:1"
            ])
    
    # Ajouter les totaux
    total_normal = sum(stats[subset].get('NORMAL', 0) for subset in SUBSETS if subset in stats)
    total_pneumonia = sum(stats[subset].get('PNEUMONIA', 0) for subset in SUBSETS if subset in stats)
    total_all = total_normal + total_pneumonia
    global_ratio = total_pneumonia / total_normal if total_normal > 0 else 0
    
    table_data.append([
        'TOTAL',
        f"{total_normal:,}",
        f"{total_pneumonia:,}",
        f"{total_all:,}",
        f"{global_ratio:.2f}:1"
    ])
    
    table = ax6.table(
        cellText=table_data,
        colLabels=['Ensemble', 'NORMAL', 'PNEUMONIA', 'Total', 'Ratio P:N'],
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 2)
    ax6.set_title('Résumé Statistique Détaillé')
    
    plt.tight_layout()
    plt.savefig(output_path / 'analyse_avancee_dataset.png', dpi=300, bbox_inches='tight')
    plt.show()

def save_analysis_report(stats, properties, output_path):
    """
    Sauvegarde un rapport d'analyse en format JSON.
    
    Args:
        stats (dict): Statistiques du dataset
        properties (dict): Propriétés des images
        output_path (Path): Chemin de sortie
    """
    report = {
        'metadata': {
            'author': PROJECT_INFO['author'],
            'email': PROJECT_INFO['email'],
            'location': PROJECT_INFO['location'],
            'analysis_date': datetime.now().isoformat(),
            'project_version': PROJECT_INFO['version']
        },
        'dataset_statistics': stats,
        'image_properties': {
            'total_analyzed': len(properties['dimensions']),
            'avg_width': np.mean([dim[0] for dim in properties['dimensions']]) if properties['dimensions'] else 0,
            'avg_height': np.mean([dim[1] for dim in properties['dimensions']]) if properties['dimensions'] else 0,
            'avg_file_size_mb': np.mean([size / (1024 * 1024) for size in properties['file_sizes']]) if properties['file_sizes'] else 0,
            'unique_formats': list(set(properties['formats'])),
            'unique_color_modes': list(set(properties['color_modes']))
        },
        'recommendations': {
            'class_imbalance': 'Severe imbalance detected - use class weights or resampling',
            'validation_set': 'Very small validation set - consider redistribution',
            'image_preprocessing': 'Standardize image dimensions and normalize pixel values',
            'augmentation': 'Apply data augmentation to minority class (NORMAL)'
        }
    }
    
    report_file = output_path / 'dataset_analysis_report.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Rapport d'analyse sauvegardé: {report_file}")
    return report_file

def validate_dataset_structure(dataset_path):
    """
    Valide la structure du dataset et identifie les problèmes potentiels.
    
    Args:
        dataset_path (Path): Chemin vers le dataset
        
    Returns:
        dict: Résultats de la validation
    """
    validation_results = {
        'structure_valid': True,
        'issues': [],
        'warnings': [],
        'recommendations': []
    }
    
    # Vérifier l'existence des dossiers principaux
    for subset in SUBSETS:
        subset_path = dataset_path / subset
        if not subset_path.exists():
            validation_results['issues'].append(f"Dossier manquant: {subset}")
            validation_results['structure_valid'] = False
        else:
            # Vérifier les classes dans chaque subset
            for class_name in CLASSES:
                class_path = subset_path / class_name
                if not class_path.exists():
                    validation_results['issues'].append(f"Classe manquante: {subset}/{class_name}")
                    validation_results['structure_valid'] = False
                else:
                    # Compter les images
                    image_count = count_images_in_directory(class_path)
                    if image_count == 0:
                        validation_results['warnings'].append(f"Aucune image dans: {subset}/{class_name}")
                    elif image_count < 10:
                        validation_results['warnings'].append(f"Très peu d'images dans: {subset}/{class_name} ({image_count})")
    
    # Vérifications spécifiques
    stats = get_dataset_statistics(dataset_path)
    
    # Vérifier le déséquilibre des classes
    if 'train' in stats:
        normal_count = stats['train'].get('NORMAL', 0)
        pneumonia_count = stats['train'].get('PNEUMONIA', 0)
        
        if normal_count > 0 and pneumonia_count > 0:
            ratio = max(normal_count, pneumonia_count) / min(normal_count, pneumonia_count)
            if ratio > 2.0:
                validation_results['warnings'].append(f"Déséquilibre des classes détecté (ratio: {ratio:.2f}:1)")
                validation_results['recommendations'].append("Considérer l'utilisation de techniques de rééquilibrage")
    
    # Vérifier la taille de l'ensemble de validation
    if 'val' in stats and stats['val']['total'] < 100:
        validation_results['warnings'].append(f"Ensemble de validation très petit ({stats['val']['total']} images)")
        validation_results['recommendations'].append("Considérer une redistribution des données")
    
    return validation_results

def print_project_header():
    """
    Affiche l'en-tête du projet avec les informations de l'auteur.
    """
    print("=" * 80)
    print(f"  {PROJECT_INFO['name']}")
    print("=" * 80)
    print(f"Auteur: {PROJECT_INFO['author']}")
    print(f"Email: {PROJECT_INFO['email']}")
    print(f"Localisation: {PROJECT_INFO['location']}")
    print(f"Version: {PROJECT_INFO['version']}")
    print(f"Description: {PROJECT_INFO['description']}")
    print("=" * 80)