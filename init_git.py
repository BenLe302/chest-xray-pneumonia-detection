#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation Git pour le projet Chest X-Ray Pneumonia Detection
Auteur: Dady Akrou Cyrille
Email: cyrilledady0501@gmail.com
Localisation: Trois-Rivières, Canada
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """
    Exécute une commande shell et retourne le résultat.
    
    Args:
        command (str): Commande à exécuter
        cwd (str): Répertoire de travail
        
    Returns:
        tuple: (success, output, error)
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_installed():
    """
    Vérifie si Git est installé sur le système.
    
    Returns:
        bool: True si Git est installé, False sinon
    """
    success, output, error = run_command("git --version")
    if success:
        print(f"✅ Git détecté: {output.strip()}")
        return True
    else:
        print("❌ Git n'est pas installé ou non accessible")
        print("   Veuillez installer Git: https://git-scm.com/downloads")
        return False

def init_git_repository(project_path):
    """
    Initialise un repository Git dans le projet.
    
    Args:
        project_path (Path): Chemin vers le projet
        
    Returns:
        bool: True si succès, False sinon
    """
    print("\n🔧 Initialisation du repository Git...")
    
    # Vérifier si Git est déjà initialisé
    git_dir = project_path / ".git"
    if git_dir.exists():
        print("✅ Repository Git déjà initialisé")
        return True
    
    # Initialiser Git
    success, output, error = run_command("git init", cwd=project_path)
    if success:
        print("✅ Repository Git initialisé avec succès")
        return True
    else:
        print(f"❌ Erreur lors de l'initialisation Git: {error}")
        return False

def configure_git_user(project_path):
    """
    Configure l'utilisateur Git pour ce projet.
    
    Args:
        project_path (Path): Chemin vers le projet
        
    Returns:
        bool: True si succès, False sinon
    """
    print("\n👤 Configuration de l'utilisateur Git...")
    
    # Configuration locale pour ce projet
    commands = [
        'git config user.name "Dady Akrou Cyrille"',
        'git config user.email "cyrilledady0501@gmail.com"'
    ]
    
    for command in commands:
        success, output, error = run_command(command, cwd=project_path)
        if not success:
            print(f"❌ Erreur lors de la configuration: {error}")
            return False
    
    print("✅ Utilisateur Git configuré")
    print("   Nom: Dady Akrou Cyrille")
    print("   Email: cyrilledady0501@gmail.com")
    return True

def add_initial_files(project_path):
    """
    Ajoute les fichiers initiaux au staging area.
    
    Args:
        project_path (Path): Chemin vers le projet
        
    Returns:
        bool: True si succès, False sinon
    """
    print("\n📁 Ajout des fichiers au staging area...")
    
    # Fichiers à ajouter initialement
    files_to_add = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "config.py",
        "utils.py",
        "analyse_dataset.py",
        "logs/.gitkeep",
        "models/.gitkeep",
        "data/.gitkeep"
    ]
    
    for file_path in files_to_add:
        full_path = project_path / file_path
        if full_path.exists():
            success, output, error = run_command(f'git add "{file_path}"', cwd=project_path)
            if success:
                print(f"✅ Ajouté: {file_path}")
            else:
                print(f"⚠️ Erreur avec {file_path}: {error}")
        else:
            print(f"⚠️ Fichier non trouvé: {file_path}")
    
    return True

def create_initial_commit(project_path):
    """
    Crée le commit initial.
    
    Args:
        project_path (Path): Chemin vers le projet
        
    Returns:
        bool: True si succès, False sinon
    """
    print("\n💾 Création du commit initial...")
    
    commit_message = "Initial commit: Chest X-Ray Pneumonia Detection project setup\n\n" \
                    "- Project structure and configuration\n" \
                    "- Dataset analysis tools\n" \
                    "- Utility functions and logging\n" \
                    "- Documentation and requirements\n\n" \
                    "Author: Dady Akrou Cyrille <cyrilledady0501@gmail.com>"
    
    success, output, error = run_command(f'git commit -m "{commit_message}"', cwd=project_path)
    if success:
        print("✅ Commit initial créé avec succès")
        print(f"   Message: {commit_message.split(chr(10))[0]}")
        return True
    else:
        print(f"❌ Erreur lors du commit: {error}")
        return False

def show_git_status(project_path):
    """
    Affiche le statut Git du projet.
    
    Args:
        project_path (Path): Chemin vers le projet
    """
    print("\n📊 Statut Git:")
    success, output, error = run_command("git status --short", cwd=project_path)
    if success:
        if output.strip():
            print(output)
        else:
            print("✅ Aucun changement en attente")
    else:
        print(f"❌ Erreur: {error}")

def main():
    """
    Fonction principale d'initialisation Git.
    """
    print("=" * 80)
    print("🚀 INITIALISATION GIT - CHEST X-RAY PNEUMONIA DETECTION")
    print("=" * 80)
    print("Auteur: Dady Akrou Cyrille")
    print("Email: cyrilledady0501@gmail.com")
    print("Localisation: Trois-Rivières, Canada")
    print("=" * 80)
    
    # Chemin du projet
    project_path = Path(__file__).parent
    print(f"📁 Répertoire du projet: {project_path}")
    
    # Vérifications préliminaires
    if not check_git_installed():
        sys.exit(1)
    
    # Initialisation Git
    if not init_git_repository(project_path):
        sys.exit(1)
    
    # Configuration utilisateur
    if not configure_git_user(project_path):
        sys.exit(1)
    
    # Ajout des fichiers
    add_initial_files(project_path)
    
    # Commit initial
    if not create_initial_commit(project_path):
        sys.exit(1)
    
    # Statut final
    show_git_status(project_path)
    
    print("\n" + "=" * 80)
    print("🎉 INITIALISATION GIT TERMINÉE AVEC SUCCÈS!")
    print("=" * 80)
    print("\n📋 Prochaines étapes:")
    print("1. Créer un repository sur GitHub")
    print("2. Ajouter l'origine remote: git remote add origin <URL>")
    print("3. Pousser le code: git push -u origin main")
    print("\n💡 Commandes utiles:")
    print("   git status          - Voir le statut")
    print("   git add .           - Ajouter tous les fichiers")
    print("   git commit -m 'msg' - Créer un commit")
    print("   git push            - Pousser vers GitHub")

if __name__ == "__main__":
    main()