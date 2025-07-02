from setuptools import setup, find_packages

setup(
    name="telegram-gifts-chart",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'aiogram>=3.0.0',
        'python-dotenv>=0.19.0',
        'Pillow>=8.3.1',
        'requests>=2.26.0',
        'pyrogram>=2.0.0',
        'portalsmp>=1.0.0',
    ],
    author="Th3ryks",
    author_email="",
    description="A Telegram bot for generating beautiful gift charts and statistics",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Th3ryks/TelegramGiftsChart",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
) 