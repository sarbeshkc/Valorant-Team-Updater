import os
import sys
import subprocess
from pathlib import Path

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        'app',
        'assets/agents',
        'assets/backgrounds',
        'assets/logos/default',
        'assets/logos/custom',
        'data',
        'overlay/css',
        'overlay/js'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def install_requirements():
    """Install Python dependencies"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'PyQt5'])
        print("Successfully installed requirements")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

def create_default_files():
    """Create necessary default files"""
    data_files = {
        'data/team1_name.txt': 'TEAM 1',
        'data/team1_score.txt': '0',
        'data/team2_name.txt': 'TEAM 2',
        'data/team2_score.txt': '0',
        'data/event_stage.txt': 'FINAL',
        'data/map_name.txt': '',
        'data/team1_color.txt': '#2d7a5d',
        'data/team2_color.txt': '#7a2d2d'
    }
    
    for filepath, content in data_files.items():
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created file: {filepath}")
        except Exception as e:
            print(f"Error creating {filepath}: {e}")

def check_config():
    """Check if all necessary files are present"""
    required_files = [
        'app/updater.py',
        'app/server.py',
        'overlay/index.html',
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"Error: Missing required file {file}")
            sys.exit(1)

def main():
    print("Starting setup process...")
    
    # Create directory structure
    print("\nCreating directory structure...")
    create_directory_structure()
    
    # Install requirements
    print("\nInstalling requirements...")
    install_requirements()
    
    # Create default files
    print("\nCreating default files...")
    create_default_files()
    
    # Check configuration
    print("\nChecking configuration...")
    check_config()
    
    print("\nSetup completed successfully!")
    print("\nYou can now run the overlay by executing:")
    print("  python app/updater.py")

if __name__ == "__main__":
    main()
