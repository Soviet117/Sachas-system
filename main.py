#!/usr/bin/env python3
import sys
import os
import platform

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from view.app import App
except ModuleNotFoundError as e:
    if 'tkinter' in str(e):
        sis = platform.system()
        if sis == 'Linux':
            print('ERROR: Falta tkinter en el sistema.')
            print('  En Ubuntu/Debian: sudo apt install python3-tk')
            print('  En Fedora:        sudo dnf install python3-tkinter')
            print('  En Arch:          sudo pacman -S tk')
        elif sis == 'Windows':
            print('ERROR: tkinter no está disponible. Reinstala Python')
            print('  asegurándote de marcar "tcl/tk and IDLE" en el instalador.')
        else:
            print(f'ERROR: Falta el módulo tkinter en {sis}.')
            print('  Instala tkinter según tu sistema operativo.')
        sys.exit(1)
    raise

if __name__ == '__main__':
    app = App()
    app.mainloop()