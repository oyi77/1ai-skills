"""
Auto Clipper Indonesia - Setup Script
Build Windows executable using PyInstaller
"""

from setuptools import setup, find_packages
import os

# Read README
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name='auto-clipper-indonesia',
    version='1.0.0',
    description='AI-powered video clipper - Convert long videos to viral shorts',
    author='BerkahKarya',
    author_email='contact@berkahkarya.id',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'moviepy>=1.0.3',
        'opencv-python>=4.9.0.80',
        'ffmpeg-python>=0.2.0',
        'faster-whisper>=1.0.1',
        'textblob>=0.17.1',
        'vaderSentiment>=3.3.2',
        'customtkinter>=5.2.1',
        'Pillow>=10.2.0',
        'yt-dlp>=2024.3.10',
        'requests>=2.31.0',
        'tqdm>=4.66.2',
        'python-dotenv>=1.0.1',
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'auto-clipper=main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Microsoft :: Windows',
    ],
)