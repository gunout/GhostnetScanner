#!/usr/bin/env python3
import sys
from scanner.core import NetworkScanner
from scanner.gui import CyberScannerUI
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

def main():
    scanner = NetworkScanner(max_threads=15)
    
    app = QApplication(sys.argv)
    
    # Chargement de polices cyberpunk
    QFontDatabase.addApplicationFont("fonts/cyberpunk.ttf")  # À remplacer par votre police
    
    window = CyberScannerUI(scanner)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
