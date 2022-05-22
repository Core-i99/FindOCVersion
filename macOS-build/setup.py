"""
Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['FindOCVersion.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'macOS-build/Icon.icns',
    'packages': ['tkinter'],
    'plist': {
        'CFBundleDevelopmentRegion': 'English',
        'CFBundleIdentifier': "com.Core-i99.FindOCVersion",
        'CFBundleVersion': "2.0",
        'NSHumanReadableCopyright': "Copyright © 2022, Stijn Rombouts, All Rights Reserved"
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
