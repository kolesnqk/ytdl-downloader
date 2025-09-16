#!/usr/bin/env python3
"""
Упрощенная версия для диагностики
"""

import sys
import traceback

def test_imports():
    """Тест всех импортов"""
    try:
        print("1. Тестирование импортов...")
        
        import os
        import subprocess
        import re
        import json
        from typing import List, Dict, Optional
        print("   ✅ Стандартные библиотеки")
        
        from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                     QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                                     QMessageBox, QTextEdit, QComboBox, QProgressBar,
                                     QGroupBox, QGridLayout, QScrollArea, QFrame)
        from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
        from PyQt5.QtGui import QFont, QPixmap
        print("   ✅ PyQt5")
        
        return True
    except Exception as e:
        print(f"   ❌ Ошибка импорта: {e}")
        traceback.print_exc()
        return False

def test_ytdlp():
    """Тест yt-dlp"""
    try:
        print("2. Тестирование yt-dlp...")
        
        result = subprocess.run(['yt-dlp', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"   ✅ yt-dlp версия: {result.stdout.strip()}")
            return True
        else:
            print(f"   ❌ yt-dlp ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ yt-dlp не найден: {e}")
        return False

def test_simple_gui():
    """Тест простого GUI"""
    try:
        print("3. Тестирование простого GUI...")
        
        from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
        from PyQt5.QtCore import Qt
        
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setWindowTitle("Тест")
        window.setGeometry(100, 100, 400, 300)
        
        label = QLabel("Тест работает!")
        label.setAlignment(Qt.AlignCenter)
        window.setCentralWidget(label)
        
        window.show()
        print("   ✅ GUI создан успешно")
        
        # Не показываем окно, только тестируем создание
        return True
        
    except Exception as e:
        print(f"   ❌ Ошибка GUI: {e}")
        traceback.print_exc()
        return False

def main():
    print("🔍 Диагностика приложения...")
    print("=" * 50)
    
    # Тест 1: Импорты
    if not test_imports():
        print("\n❌ Проблема с импортами!")
        return False
    
    # Тест 2: yt-dlp
    if not test_ytdlp():
        print("\n❌ Проблема с yt-dlp!")
        return False
    
    # Тест 3: GUI
    if not test_simple_gui():
        print("\n❌ Проблема с GUI!")
        return False
    
    print("\n🎉 Все тесты прошли успешно!")
    print("\nПопробуйте запустить основное приложение:")
    print("python main.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        traceback.print_exc()
