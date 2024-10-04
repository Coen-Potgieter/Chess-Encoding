from setuptools import setup, find_packages

setup(
    name='Chess-Encoding',
    version='1.0.0',
    author='Coen Potgieter',
    author_email='coen.potgieter13@gmail.com',
    description='TODO',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Coen-Potgieter/Chess-Encoding',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        
    ],
    entry_points={
        'console_scripts': [
            'run=src.main:main',  # Specify the command to run
        ],
    },
)
