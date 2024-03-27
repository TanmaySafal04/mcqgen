# To install libraries in our local environment

from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='Tanmay safal',
    author_email='tanmaysafal.4@gmail.com',
    install_requires=["openai","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)