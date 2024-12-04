import sys
import os
import shutil
from pathlib import Path
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QGroupBox, QFormLayout, QTabWidget, QCheckBox,
                           QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, QTimer

class ValorantOverlayUpdater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / 'data'
        self.assets_dir = self.base_dir / 'assets'
        self.logos_dir = self.assets_dir / 'logos'
        
        # Create necessary directories
        self.data_dir.mkdir(exist_ok=True)
        self.logos_dir.mkdir(parents=True, exist_ok=True)
        
        self.init_ui()
        self.start_server()
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.update_values)
        self.auto_save_timer.start(1000)

    def init_ui(self):
        self.setWindowTitle("Valorant Overlay Updater")
        self.setMinimumWidth(800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create tabs
        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Create Tournament Tab
        tournament_tab = QWidget()
        tournament_layout = QVBoxLayout(tournament_tab)

        # Tournament Info
        tournament_group = QGroupBox("Tournament Information")
        tournament_form = QFormLayout()

        # Tournament Name only
        self.tournament_name = QLineEdit()
        tournament_form.addRow("Tournament Name:", self.tournament_name)

        tournament_group.setLayout(tournament_form)
        tournament_layout.addWidget(tournament_group)
        tournament_layout.addStretch()
        tabs.addTab(tournament_tab, "Tournament")

        # Teams Tab
        teams_tab = QWidget()
        teams_layout = QVBoxLayout(teams_tab)

        # Team 1
        team1_group = QGroupBox("Team 1")
        team1_layout = QFormLayout()
        self.team1_name = QLineEdit()
        self.team1_logo_label = QLabel("No logo selected")
        team1_logo_btn = QPushButton("Select Logo")
        team1_logo_btn.clicked.connect(lambda: self.select_team_logo(1))
        
        team1_logo_layout = QHBoxLayout()
        team1_logo_layout.addWidget(self.team1_logo_label)
        team1_logo_layout.addWidget(team1_logo_btn)
        
        team1_layout.addRow("Name:", self.team1_name)
        team1_layout.addRow("Logo:", team1_logo_layout)
        team1_group.setLayout(team1_layout)
        teams_layout.addWidget(team1_group)

        # Team 2
        team2_group = QGroupBox("Team 2")
        team2_layout = QFormLayout()
        self.team2_name = QLineEdit()
        self.team2_logo_label = QLabel("No logo selected")
        team2_logo_btn = QPushButton("Select Logo")
        team2_logo_btn.clicked.connect(lambda: self.select_team_logo(2))
        
        team2_logo_layout = QHBoxLayout()
        team2_logo_layout.addWidget(self.team2_logo_label)
        team2_logo_layout.addWidget(team2_logo_btn)
        
        team2_layout.addRow("Name:", self.team2_name)
        team2_layout.addRow("Logo:", team2_logo_layout)
        team2_group.setLayout(team2_layout)
        teams_layout.addWidget(team2_group)

        # Event Stage
        stage_group = QGroupBox("Event Information")
        stage_layout = QFormLayout()
        self.event_stage = QLineEdit()
        stage_layout.addRow("Event Stage:", self.event_stage)
        stage_group.setLayout(stage_layout)
        teams_layout.addWidget(stage_group)
        teams_layout.addStretch()

        tabs.addTab(teams_tab, "Teams")

        # Maps Tab
        maps_tab = QWidget()
        maps_layout = QVBoxLayout(maps_tab)

        # Before Map Group
        before_group = QGroupBox("Before Map")
        before_layout = QFormLayout()
        self.show_before_map = QCheckBox("Show Before Map")
        self.before_map = QLineEdit()
        before_layout.addRow(self.show_before_map)
        before_layout.addRow("Map:", self.before_map)
        before_group.setLayout(before_layout)
        maps_layout.addWidget(before_group)

        # Current Map Group
        current_group = QGroupBox("Current Map")
        current_layout = QFormLayout()
        self.current_map = QLineEdit()
        current_layout.addRow("Map:", self.current_map)
        current_group.setLayout(current_layout)
        maps_layout.addWidget(current_group)

        # Next Map Group
        next_group = QGroupBox("Next Map")
        next_layout = QFormLayout()
        self.show_next_map = QCheckBox("Show Next Map")
        self.next_map = QLineEdit()
        next_layout.addRow(self.show_next_map)
        next_layout.addRow("Map:", self.next_map)
        next_group.setLayout(next_layout)
        maps_layout.addWidget(next_group)

        maps_layout.addStretch()
        tabs.addTab(maps_tab, "Maps")

        self.load_values()
        self.statusBar().showMessage("Ready")

    def select_team_logo(self, team_num):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            f"Select Team {team_num} Logo",
            "",
            "Image Files (*.png *.jpg *.jpeg *.gif)"
        )
        
        if filename:
            try:
                # Get the file extension
                ext = Path(filename).suffix
                
                # Copy to logos directory with team number
                dest_path = self.logos_dir / f"team{team_num}{ext}"
                
                # Remove any existing logos for this team
                for existing in self.logos_dir.glob(f"team{team_num}.*"):
                    existing.unlink()
                
                # Copy new logo
                shutil.copy2(filename, dest_path)
                
                # Update label
                label = getattr(self, f'team{team_num}_logo_label')
                label.setText(Path(filename).name)
                
                self.statusBar().showMessage(f"Logo updated for Team {team_num}")
                print(f"Logo saved to: {dest_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save logo: {str(e)}")

    def update_values(self):
        updates = {
            'tournament_name.txt': self.tournament_name.text(),
            'team1_name.txt': self.team1_name.text(),
            'team2_name.txt': self.team2_name.text(),
            'event_stage.txt': self.event_stage.text(),
            'current_map.txt': self.current_map.text(),
            'show_before_map.txt': str(self.show_before_map.isChecked()).lower(),
            'show_next_map.txt': str(self.show_next_map.isChecked()).lower(),
        }

        if self.show_before_map.isChecked():
            updates['before_map.txt'] = self.before_map.text()
        if self.show_next_map.isChecked():
            updates['next_map.txt'] = self.next_map.text()

        for filename, content in updates.items():
            self.write_file(filename, content)

    def write_file(self, filename, content):
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(content))
            return True
        except Exception as e:
            print(f"Error writing {filename}: {e}")
            return False

    def load_values(self):
        # Load text fields
        files_to_fields = {
            'tournament_name.txt': self.tournament_name,
            'team1_name.txt': self.team1_name,
            'team2_name.txt': self.team2_name,
            'event_stage.txt': self.event_stage,
            'current_map.txt': self.current_map,
            'before_map.txt': self.before_map,
            'next_map.txt': self.next_map
        }

        for filename, field in files_to_fields.items():
            try:
                filepath = self.data_dir / filename
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        field.setText(f.read().strip())
            except Exception as e:
                print(f"Error loading {filename}: {e}")

        # Load checkboxes
        try:
            if (self.data_dir / 'show_before_map.txt').exists():
                state = open(self.data_dir / 'show_before_map.txt').read().strip()
                self.show_before_map.setChecked(state == 'true')
            
            if (self.data_dir / 'show_next_map.txt').exists():
                state = open(self.data_dir / 'show_next_map.txt').read().strip()
                self.show_next_map.setChecked(state == 'true')
        except Exception as e:
            print(f"Error loading checkbox states: {e}")

        # Load logo labels
        for team_num in [1, 2]:
            logo_files = list(self.logos_dir.glob(f"team{team_num}.*"))
            if logo_files:
                label = getattr(self, f'team{team_num}_logo_label')
                label.setText(logo_files[0].name)

    def start_server(self):
        try:
            server_script = Path(__file__).parent / 'server.py'
            if sys.platform == 'win32':
                self.server_process = subprocess.Popen(
                    [sys.executable, str(server_script)],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            else:
                self.server_process = subprocess.Popen([sys.executable, str(server_script)])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to start server: {e}")

    def closeEvent(self, event):
        if hasattr(self, 'server_process'):
            self.server_process.terminate()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = ValorantOverlayUpdater()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
