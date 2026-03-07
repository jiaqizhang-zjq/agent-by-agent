import os
from setuptools import setup, find_packages

setup(
    name="agent-evolution",
    version="0.1.0",
    description="Agent自我进化项目",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "docker",
        "pytest",
        "requests",
        "beautifulsoup4",
        "numpy",
        "pandas",
        "gitpython",
        "python-dotenv"
    ],
    dependency_links=[
        # 使用本地克隆的第三方库
        "file://{}/third-party/langchain".format(os.path.abspath(os.curdir)),
        "file://{}/third-party/langgraph".format(os.path.abspath(os.curdir)),
        "file://{}/third-party/mem0".format(os.path.abspath(os.curdir))
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8"
        ]
    }
)
