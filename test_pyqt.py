#!/usr/bin/env python3
"""
Тест PyQt5 импортов
"""

try:
    print("Тестирование импортов PyQt5...")
    
    from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit, QComboBox, QProgressBar, QGroupBox, QGridLayout, QScrollArea, QFrame
    print("✅ PyQt5.QtWidgets импортирован")
    
    from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
    print("✅ PyQt5.QtCore импортирован")
    
    from PyQt5.QtGui import QFont, QPixmap
    print("✅ PyQt5.QtGui импортирован")
    
    print("\n🎉 Все импорты PyQt5 успешны!")
    
    # Тест создания простого окна
    import sys
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Тест PyQt5")
    window.setGeometry(100, 100, 300, 200)
    
    label = QLabel("PyQt5 работает!")
    window.setCentralWidget(label)
    
    print("✅ Создание окна успешно")
    print("✅ PyQt5 полностью функционален!")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Установите PyQt5: pip install PyQt5")
except Exception as e:
    print(f"❌ Ошибка: {e}")
