from setuptools import setup, find_packages

setup(
    name="batched_chatgpt",
    version="0.0.5",
    description="Easy calling chatgpt with batched instances",
    packages=find_packages(),
    author="superheavytail",
    author_email="k0s1k0s1k0@korea.ac.kr",
    install_requires=[
        'langchain',
        'langchain-openai',
        'tqdm',
        'openai',
    ],
)