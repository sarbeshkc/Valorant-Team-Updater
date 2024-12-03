import sys
import os
from pathlib import Path
import subprocess
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                           QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt, QTimer

class ValorantOverlayUpdater(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_server()
        
        # Auto-save timer
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self.update_values)
        self.auto_save_timer.start(1000)  # Update every second

    def init_ui(self):
        self.setWindowTitle("Valorant Overlay Updater")
        self.setMinimumWidth(600)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create team sections
        teams_layout = QHBoxLayout()

        # Team 1 Group
        team1_group = QGroupBox("Team 1")
        team1_layout = QFormLayout()
        self.team1_name = QLineEdit()
        team1_layout.addRow("Name:", self.team1_name)
        team1_group.setLayout(team1_layout)
        teams_layout.addWidget(team1_group)

        # Team 2 Group
        team2_group = QGroupBox("Team 2")
        team2_layout = QFormLayout()
        self.team2_name = QLineEdit()
        team2_layout.addRow("Name:", self.team2_name)
        team2_group.setLayout(team2_layout)
        teams_layout.addWidget(team2_group)

        layout.addLayout(teams_layout)

        # Match Info Group
        match_group = QGroupBox("Match Information")
        match_layout = QFormLayout()
        
        self.event_stage = QLineEdit("FINAL")
        self.map_name = QLineEdit()
        
        match_layout.addRow("Event Stage:", self.event_stage)
        match_layout.addRow("Map:", self.map_name)
        match_group.setLayout(match_layout)
        layout.addWidget(match_group)

        # Create data directory if it doesn't exist
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.data_dir.mkdir(exist_ok=True)

        # Load existing values
        self.load_values()

        # Status Bar
        self.statusBar().showMessage("Ready")

        self.show()

    def start_server(self):
        try:
            server_script = Path(__file__).parent / 'server.py'
            if sys.platform == 'win32':
                self.server_process = subprocess.Popen([sys.executable, str(server_script)],
                                                     creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                self.server_process = subprocess.Popen([sys.executable, str(server_script)])
        except Exception as e:
            print(f"Failed to start server: {e}")

    def write_file(self, filename, content):
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(content))
            return True
        except Exception as e:
            self.statusBar().showMessage(f"Error writing {filename}: {e}")
            return False

    def update_values(self):
        """Update all files with current values"""
        files_to_update = {
            'team1_name.txt': self.team1_name.text(),
            'team2_name.txt': self.team2_name.text(),
            'event_stage.txt': self.event_stage.text(),
            'map_name.txt': self.map_name.text()
        }
        
        success = True
        for filename, content in files_to_update.items():
            if not self.write_file(filename, content):
                success = False
        
        if success:
            self.statusBar().showMessage("Values updated")

    def load_values(self):
        """Load existing values if available"""
        try:
            if (self.data_dir / 'team1_name.txt').exists():
                self.team1_name.setText(open(self.data_dir / 'team1_name.txt').read().strip())
            if (self.data_dir / 'team2_name.txt').exists():
                self.team2_name.setText(open(self.data_dir / 'team2_name.txt').read().strip())
            if (self.data_dir / 'event_stage.txt').exists():
                self.event_stage.setText(open(self.data_dir / 'event_stage.txt').read().strip())
            if (self.data_dir / 'map_name.txt').exists():
                self.map_name.setText(open(self.data_dir / 'map_name.txt').read().strip())
        except Exception as e:
            self.statusBar().showMessage(f"Error loading values: {e}")

    def closeEvent(self, event):
        """Clean up when closing the application"""
        try:
            if hasattr(self, 'server_process'):
                self.server_process.terminate()
        except Exception:
            pass
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = ValorantOverlayUpdater()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
