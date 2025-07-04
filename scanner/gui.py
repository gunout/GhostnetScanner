from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QVBoxLayout, QWidget, 
                            QPushButton, QLineEdit, QLabel, QHBoxLayout, 
                            QTableWidget, QTableWidgetItem, QHeaderView,
                            QFileDialog, QTabWidget)
from PyQt5.QtGui import QColor, QFont, QBrush
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
import csv
import random
from datetime import datetime

class CyberScannerUI(QMainWindow):
    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner
        self.scan_results = []
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('CYBER SCANNER v5.2.0')
        self.setGeometry(100, 100, 1200, 800)
        
        # Police stylée
        cyber_font = QFont("Courier New", 10)
        cyber_font.setBold(True)
        title_font = QFont("Courier New", 16)
        title_font.setBold(True)
        
        # Widget central avec onglets
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #1a0a2a;
                color: #ff00ff;
                padding: 10px;
                border: 1px solid #ff00ff;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: #33003a;
                color: #00ffff;
            }
            QTabWidget::pane {
                border: 2px solid #ff00ff;
                background: #0a0a1a;
            }
        """)
        self.setCentralWidget(self.tabs)
        
        # Onglet Scan
        scan_tab = QWidget()
        scan_layout = QVBoxLayout()
        scan_tab.setLayout(scan_layout)
        
        # Titre
        title = QLabel("G H O S T N E T S C A N N E R")
        title.setFont(title_font)
        title.setStyleSheet("color: #00ffff; qproperty-alignment: AlignCenter;")
        scan_layout.addWidget(title)
        
        # Zone de saisie
        input_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setFont(cyber_font)
        self.target_input.setStyleSheet("""
            QLineEdit {
                background: #0a0a2a;
                color: #00ffff;
                border: 2px solid #ff00ff;
                padding: 10px;
                selection-background-color: #ff00ff;
            }
        """)
        self.target_input.setPlaceholderText("entrez l'ip/url (ex: 192.168.1.1 ou example.com)")
        input_layout.addWidget(QLabel("CIBLE:"))
        input_layout.addWidget(self.target_input)
        
        # Boutons
        btn_scan = QPushButton("SCAN")
        btn_scan.setStyleSheet("""
            QPushButton {
                background: #ff00ff;
                color: #000;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #ff44ff;
            }
        """)
        btn_scan.clicked.connect(self.start_scan)
        
        btn_export = QPushButton("EXPORT CSV")
        btn_export.setStyleSheet("""
            QPushButton {
                background: #00ffff;
                color: #000;
                border: none;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #44ffff;
            }
        """)
        btn_export.clicked.connect(self.export_csv)
        
        input_layout.addWidget(btn_scan)
        input_layout.addWidget(btn_export)
        scan_layout.addLayout(input_layout)
        
        # Tableau des résultats
        self.result_table = QTableWidget()
        self.result_table.setStyleSheet("""
            QTableWidget {
                background: #0a0a1a;
                color: #00ffff;
                gridline-color: #ff00ff;
                font-family: 'Courier New';
            }
            QHeaderView::section {
                background: #33003a;
                color: #ff00ff;
                padding: 5px;
                border: 1px solid #ff00ff;
            }
        """)
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "IP", "Hostname", "Géo IP", "Ports Ouverts", 
            "Services", "Statut"
        ])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        scan_layout.addWidget(self.result_table)
        
        # Console de logs
        self.log_console = QTextEdit()
        self.log_console.setStyleSheet("""
            QTextEdit {
                background: #0a0a0a;
                color: #00ff00;
                border: 1px solid #00ffff;
                font-family: 'Courier New';
            }
        """)
        self.log_console.setReadOnly(True)
        scan_layout.addWidget(self.log_console)
        
        self.tabs.addTab(scan_tab, "Scan Principal")
        
        # Onglet Détails
        self.details_tab = QTextEdit()
        self.details_tab.setStyleSheet("""
            QTextEdit {
                background: #0a0a0a;
                color: #ff00ff;
                border: 1px solid #00ffff;
                font-family: 'Courier New';
                padding: 10px;
            }
        """)
        self.details_tab.setReadOnly(True)
        self.tabs.addTab(self.details_tab, "Détails Techniques")
        
        # Animation
        self.setup_animations()
        
    def setup_animations(self):
        # Animation de pulsation pour le titre
        self.title_anim = QPropertyAnimation(self, b"windowOpacity")
        self.title_anim.setDuration(3000)
        self.title_anim.setStartValue(0.9)
        self.title_anim.setEndValue(1.0)
        self.title_anim.setLoopCount(-1)
        self.title_anim.start()
        
    def start_scan(self):
        target = self.target_input.text().lower().strip()
        if not target:
            self.log("Erreur: Aucune cible spécifiée", error=True)
            return
            
        self.log(f"\n>>> Début du scan: {target}")
        self.log(">>> Analyse en cours...")
        
        # Simulation de résultats (remplacer par un vrai scan)
        fake_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
        fake_geo = random.choice(["Paris, FR", "Tokyo, JP", "New York, US"])
        fake_ports = ",".join(map(str, sorted(
            random.sample([21, 22, 80, 443, 8080, 3306], random.randint(1, 4))
        )))
        fake_services = ",".join(random.sample(
            ["HTTP", "SSH", "FTP", "MySQL", "HTTPS"], random.randint(1, 3)))
        
        result = {
            "ip": fake_ip,
            "hostname": f"host-{random.randint(100,999)}.local",
            "geo": fake_geo,
            "ports": fake_ports,
            "services": fake_services,
            "status": "ACTIF" if random.random() > 0.2 else "INACTIF",
            "details": f"""Détails techniques pour {fake_ip}:
- OS estimé: {random.choice(["Linux", "Windows", "RouterOS"])}
- TTL: {random.randint(30, 255)}
- Vulnérabilités détectées: {random.randint(0, 3)}
- Dernier scan: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        }
        
        self.scan_results.append(result)
        self.update_results_table()
        self.log(">>> Scan terminé avec succès")
        
    def update_results_table(self):
        self.result_table.setRowCount(len(self.scan_results))
        
        for row, result in enumerate(self.scan_results):
            self.result_table.setItem(row, 0, self.create_colored_item(result["ip"]))
            self.result_table.setItem(row, 1, self.create_colored_item(result["hostname"]))
            self.result_table.setItem(row, 2, self.create_colored_item(result["geo"]))
            self.result_table.setItem(row, 3, self.create_colored_item(result["ports"]))
            self.result_table.setItem(row, 4, self.create_colored_item(result["services"]))
            
            status_item = self.create_colored_item(result["status"])
            status_item.setBackground(QBrush(QColor("#33003a" if result["status"] == "INACTIF" else "#003a33")))
            self.result_table.setItem(row, 5, status_item)
            
        # Mise à jour de l'onglet détails
        if self.scan_results:
            self.details_tab.setText(self.scan_results[-1]["details"])
        
    def create_colored_item(self, text):
        item = QTableWidgetItem(str(text))
        item.setForeground(QBrush(QColor("#00ffff")))
        return item
        
    def export_csv(self):
        if not self.scan_results:
            self.log("Erreur: Aucun résultat à exporter", error=True)
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Exporter en CSV", "", "CSV Files (*.csv)")
            
        if filename:
            try:
                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['IP', 'Hostname', 'Géo IP', 'Ports Ouverts', 'Services', 'Statut']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    
                    writer.writeheader()
                    for result in self.scan_results:
                        writer.writerow({
                            'IP': result['ip'],
                            'Hostname': result['hostname'],
                            'Géo IP': result['geo'],
                            'Ports Ouverts': result['ports'],
                            'Services': result['services'],
                            'Statut': result['status']
                        })
                        
                self.log(f">>> Export réussi: {filename}")
            except Exception as e:
                self.log(f"Erreur export: {str(e)}", error=True)
                
    def log(self, message, error=False):
        color = "#ff5555" if error else "#00ffff"
        self.log_console.append(f'<span style="color:{color}">{message}</span>')