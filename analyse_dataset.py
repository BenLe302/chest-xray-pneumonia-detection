# Analyse avancée du dataset Chest X-Ray (Pneumonia)
# Auteur: Dady Akrou Cyrille
# Email: cyrilledady0501@gmail.com
# Localisation: Trois-Rivières, Canada

import os
import sys
import logging
from pathlib import Path

# Ajouter le répertoire courant au path pour les imports
sys.path.append(str(Path(__file__).parent))

from config import *
from utils import *

def analyser_dataset_avance():
    """
    Analyse complète et avancée du dataset de radiographies thoraciques.
    Utilise les modules de configuration et utilitaires pour une analyse professionnelle.
    """
    # Afficher l'en-tête du projet
    print_project_header()
    
    # Configurer le logging
    logger = setup_logging()
    logger.info("Début de l'analyse avancée du dataset")
    
    try:
        # Valider la structure du dataset
        print("\n🔍 VALIDATION DE LA STRUCTURE DU DATASET")
        print("-" * 60)
        
        validation_results = validate_dataset_structure(DATASET_PATH)
        
        if validation_results['structure_valid']:
            print("✅ Structure du dataset valide")
        else:
            print("❌ Problèmes détectés dans la structure:")
            for issue in validation_results['issues']:
                print(f"  - {issue}")
        
        if validation_results['warnings']:
            print("\n⚠️ Avertissements:")
            for warning in validation_results['warnings']:
                print(f"  - {warning}")
        
        if validation_results['recommendations']:
            print("\n💡 Recommandations:")
            for rec in validation_results['recommendations']:
                print(f"  - {rec}")
        
        # Obtenir les statistiques du dataset
        print("\n📊 STATISTIQUES DU DATASET")
        print("-" * 60)
        
        stats = get_dataset_statistics(DATASET_PATH)
        
        # Afficher les statistiques détaillées
        for subset in SUBSETS:
            if subset in stats:
                print(f"\n📁 Ensemble {subset.upper()}:")
                for class_name in CLASSES:
                    if class_name in stats[subset]:
                        count = stats[subset][class_name]
                        percentage = (count / stats[subset]['total'] * 100) if stats[subset]['total'] > 0 else 0
                        print(f"  {class_name}: {count:,} images ({percentage:.1f}%)")
                print(f"  Total: {stats[subset]['total']:,} images")
        
        print(f"\n📈 Total dataset: {stats['total_dataset']:,} images")
        
        # Calculer et afficher les poids des classes
        class_weights = calculate_class_weights(stats)
        print("\n⚖️ Poids calculés pour les classes:")
        for i, class_name in enumerate(CLASSES):
            print(f"  {class_name}: {class_weights[i]:.3f}")
        
        # Analyser les propriétés des images
        print("\n🖼️ ANALYSE DES PROPRIÉTÉS D'IMAGES")
        print("-" * 60)
        
        properties = analyze_image_properties(DATASET_PATH, sample_size=100)
        
        if properties['dimensions']:
            widths = [dim[0] for dim in properties['dimensions']]
            heights = [dim[1] for dim in properties['dimensions']]
            ratios = [w/h for w, h in properties['dimensions']]
            file_sizes_mb = [size / (1024 * 1024) for size in properties['file_sizes']]
            
            print(f"Images analysées: {len(properties['dimensions']):,}")
            print(f"Largeur moyenne: {np.mean(widths):.0f} px (min: {min(widths)}, max: {max(widths)})")
            print(f"Hauteur moyenne: {np.mean(heights):.0f} px (min: {min(heights)}, max: {max(heights)})")
            print(f"Ratio moyen (L/H): {np.mean(ratios):.2f} (std: {np.std(ratios):.2f})")
            print(f"Taille moyenne: {np.mean(file_sizes_mb):.2f} MB (min: {min(file_sizes_mb):.2f}, max: {max(file_sizes_mb):.2f})")
            print(f"Formats détectés: {', '.join(set(properties['formats']))}")
            print(f"Modes couleur: {', '.join(set(properties['color_modes']))}")
        
        return stats, properties, logger
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise

def generer_visualisations_avancees(stats, properties, logger):
    """
    Génère des visualisations avancées et professionnelles du dataset.
    
    Args:
        stats (dict): Statistiques du dataset
        properties (dict): Propriétés des images
        logger: Logger pour les messages
        
    Returns:
        Path: Chemin vers le fichier de visualisation généré
    """
    logger.info("Génération des visualisations avancées")
    
    try:
        # Créer les visualisations avancées
        create_advanced_visualizations(stats, properties, OUTPUT_PATH)
        
        # Sauvegarder le rapport d'analyse
        report_file = save_analysis_report(stats, properties, OUTPUT_PATH)
        
        logger.info(f"Visualisations sauvegardées dans: {OUTPUT_PATH}")
        logger.info(f"Rapport JSON généré: {report_file}")
        
        return OUTPUT_PATH / 'analyse_avancee_dataset.png'
        
    except Exception as e:
        logger.error(f"Erreur lors de la génération des visualisations: {e}")
        raise

def generer_recommandations_ml(stats, properties, logger):
    """
    Génère des recommandations détaillées pour le machine learning.
    
    Args:
        stats (dict): Statistiques du dataset
        properties (dict): Propriétés des images
        logger: Logger pour les messages
    """
    print("\n" + "=" * 80)
    print("RECOMMANDATIONS AVANCÉES POUR LE MACHINE LEARNING")
    print("=" * 80)
    
    # Calculer les métriques globales
    total_normal = sum(stats[subset].get('NORMAL', 0) for subset in SUBSETS if subset in stats)
    total_pneumonia = sum(stats[subset].get('PNEUMONIA', 0) for subset in SUBSETS if subset in stats)
    total_images = total_normal + total_pneumonia
    
    # Analyse du déséquilibre des classes
    if total_pneumonia > total_normal:
        ratio = total_pneumonia / total_normal
        print(f"\n🚨 DÉSÉQUILIBRE DES CLASSES CRITIQUE")
        print(f"   Ratio PNEUMONIA:NORMAL = {ratio:.2f}:1")
        print(f"   Impact: Risque élevé de biais vers la classe majoritaire")
        
        print(f"\n🔧 Solutions recommandées:")
        print(f"   1. Pondération des classes: class_weight={{{0}: {ratio:.2f}, {1}: 1.0}}")
        print(f"   2. SMOTE pour sur-échantillonnage de la classe NORMAL")
        print(f"   3. Augmentation de données ciblée sur NORMAL")
        print(f"   4. Sous-échantillonnage intelligent de PNEUMONIA")
        print(f"   5. Utilisation de Focal Loss pour gérer l'imbalance")
    
    # Analyse de la taille du dataset
    print(f"\n📊 ANALYSE DE LA TAILLE DU DATASET")
    print(f"   Total: {total_images:,} images")
    
    if 'val' in stats and stats['val']['total'] < 100:
        print(f"   ⚠️ Ensemble de validation très petit: {stats['val']['total']} images")
        print(f"   Recommandation: Redistribuer en 70% train, 20% test, 10% val")
    
    # Recommandations sur les dimensions d'images
    if properties['dimensions']:
        widths = [dim[0] for dim in properties['dimensions']]
        heights = [dim[1] for dim in properties['dimensions']]
        
        print(f"\n🖼️ PRÉPARATION DES IMAGES")
        print(f"   Dimensions actuelles: {min(widths)}x{min(heights)} à {max(widths)}x{max(heights)}")
        print(f"   Recommandation: Redimensionner à {IMAGE_SIZE[0]}x{IMAGE_SIZE[1]} (standard)")
        print(f"   Normalisation: Diviser par 255.0 ou standardisation Z-score")
    
    # Recommandations d'architecture
    print(f"\n🏗️ ARCHITECTURE DE MODÈLE RECOMMANDÉE")
    print(f"   1. Transfer Learning avec ResNet50 ou EfficientNet")
    print(f"   2. Fine-tuning progressif (gradual unfreezing)")
    print(f"   3. Dropout (0.3-0.5) pour éviter l'overfitting")
    print(f"   4. Batch Normalization après chaque couche convolutionnelle")
    print(f"   5. Learning rate scheduling (ReduceLROnPlateau)")
    
    # Métriques d'évaluation
    print(f"\n📈 MÉTRIQUES D'ÉVALUATION CRITIQUES")
    print(f"   Primaires: Sensibilité (Recall) > 90% pour PNEUMONIA")
    print(f"   Secondaires: Spécificité > 80%, F1-Score > 85%")
    print(f"   Globales: AUC-ROC > 0.95, Précision équilibrée")
    print(f"   Éviter: Accuracy simple (biaisée par l'imbalance)")
    
    # Stratégie d'augmentation
    print(f"\n🔄 STRATÉGIE D'AUGMENTATION DE DONNÉES")
    print(f"   Pour NORMAL (classe minoritaire):")
    print(f"   - Rotation: ±{AUGMENTATION_CONFIG['rotation_range']}°")
    print(f"   - Translation: ±{AUGMENTATION_CONFIG['width_shift_range']*100}%")
    print(f"   - Zoom: ±{AUGMENTATION_CONFIG['zoom_range']*100}%")
    print(f"   - Flip horizontal: {AUGMENTATION_CONFIG['horizontal_flip']}")
    print(f"   - Ajustements de contraste et luminosité")
    
    logger.info("Recommandations ML générées avec succès")

def generer_rapport_complet():
    """
    Génère un rapport complet et professionnel d'analyse du dataset.
    
    Returns:
        tuple: (stats, properties, logger) pour utilisation ultérieure
    """
    try:
        # Analyse principale
        stats, properties, logger = analyser_dataset_avance()
        
        # Générer les visualisations
        viz_path = generer_visualisations_avancees(stats, properties, logger)
        
        # Générer les recommandations ML
        generer_recommandations_ml(stats, properties, logger)
        
        # Résumé final
        print("\n" + "=" * 80)
        print("RÉSUMÉ DE L'ANALYSE")
        print("=" * 80)
        print(f"✅ Dataset analysé: {stats['total_dataset']:,} images")
        print(f"✅ Visualisations générées: {viz_path}")
        print(f"✅ Rapport JSON sauvegardé: {OUTPUT_PATH / 'dataset_analysis_report.json'}")
        print(f"✅ Logs détaillés disponibles dans: {LOGS_PATH}")
        
        logger.info("Analyse complète terminée avec succès")
        return stats, properties, logger
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        if 'logger' in locals():
            logger.error(f"Erreur fatale: {e}")
        raise

if __name__ == "__main__":
    """
    Point d'entrée principal pour l'analyse du dataset.
    Exécute une analyse complète et professionnelle.
    """
    try:
        print("🚀 Démarrage de l'analyse avancée du dataset Chest X-Ray...")
        
        # Exécuter l'analyse complète
        stats, properties, logger = generer_rapport_complet()
        
        print("\n🎉 Analyse terminée avec succès!")
        print(f"📁 Consultez les résultats dans: {OUTPUT_PATH}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Analyse interrompue par l'utilisateur")
    except Exception as e:
         print(f"\n❌ Erreur fatale: {e}")
         print("Consultez les logs pour plus de détails.")
         sys.exit(1)