"""
Скрипт сборки .app приложения для macOS
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_app():
    """Собрать .app приложение для macOS"""
    print("=" * 60)
    print("🍎 СБОРКА DESKTOP ПРИЛОЖЕНИЯ ДЛЯ macOS")
    print("=" * 60)
    
    # Текущая директория
    current_dir = Path(__file__).parent
    
    # Проверяем наличие PyInstaller
    print("\n📦 Проверка PyInstaller...")
    try:
        import PyInstaller
        print(f"   ✓ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("   ✗ PyInstaller не установлен")
        print("   Установка: pip install pyinstaller")
        sys.exit(1)
    
    # Проверяем, что мы на macOS
    if sys.platform != "darwin":
        print("\n⚠️  ВНИМАНИЕ: Этот скрипт предназначен для macOS")
        print(f"   Текущая ОС: {sys.platform}")
        response = input("   Продолжить? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Имя приложения
    app_name = "CompetitorMonitor"
    
    # Параметры PyInstaller для macOS
    pyinstaller_args = [
        "pyinstaller",
        "--name", app_name,
        "--onefile",           # Один исполняемый файл внутри .app
        "--windowed",          # Без консоли (GUI приложение)
        "--noconfirm",         # Перезаписывать без подтверждения
        "--clean",             # Очистить кеш
        
        # macOS специфичные параметры
        "--osx-bundle-identifier", f"com.competitormonitor.{app_name.lower()}",
        
        # Иконка (если есть .icns файл)
        # "--icon", "icon.icns",
        
        # Добавляем файлы
        "--add-data", f"styles.py{os.pathsep}.",
        "--add-data", f"api_client.py{os.pathsep}.",
        
        # Скрытые импорты
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "requests",
        
        # Главный файл
        "main.py"
    ]
    
    print(f"\n🚀 Запуск сборки: {app_name}.app")
    print("-" * 60)
    
    # Запускаем PyInstaller
    result = subprocess.run(pyinstaller_args, cwd=current_dir)
    
    if result.returncode == 0:
        app_path = current_dir / "dist" / f"{app_name}.app"
        
        if app_path.exists():
            # Получаем размер .app bundle
            def get_dir_size(path):
                total = 0
                for entry in os.scandir(path):
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                        total += get_dir_size(entry.path)
                return total
            
            size_mb = get_dir_size(app_path) / (1024 * 1024)
            
            print("\n" + "=" * 60)
            print("✅ СБОРКА ЗАВЕРШЕНА УСПЕШНО!")
            print("=" * 60)
            print(f"\n📁 Приложение: {app_path}")
            print(f"📊 Размер: {size_mb:.1f} MB")
            print("\n💡 Для запуска:")
            print(f"   1. Запустите backend: python run.py")
            print(f"   2. Откройте {app_name}.app из папки dist/")
            print(f"   3. Или запустите через терминал: open {app_path}")
            print("\n⚠️  ПРИМЕЧАНИЕ:")
            print("   При первом запуске macOS может заблокировать приложение.")
            print("   Перейдите в: Системные настройки → Безопасность →")
            print("   и разрешите запуск приложения.")
        else:
            print("\n❌ Ошибка: .app файл не найден")
            print(f"   Проверьте папку: {current_dir / 'dist'}")
    else:
        print("\n❌ Ошибка сборки")
        sys.exit(1)


def clean():
    """Очистить артефакты сборки"""
    current_dir = Path(__file__).parent
    
    dirs_to_remove = ["build", "dist", "__pycache__"]
    files_to_remove = ["*.spec"]
    
    print("🧹 Очистка артефактов сборки...")
    
    for dir_name in dirs_to_remove:
        dir_path = current_dir / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"   Удалено: {dir_name}/")
    
    for pattern in files_to_remove:
        for file in current_dir.glob(pattern):
            file.unlink()
            print(f"   Удалено: {file.name}")
    
    print("✓ Очистка завершена")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
    else:
        build_app()

