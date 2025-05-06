from pathlib import Path
from setuptools import setup, find_packages

README = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="aquario",
    version="1.0.0",
    description="Aquário animado que roda no terminal",
    long_description=README,                 # <- precisa existir
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={"console_scripts": ["aquario=aquario.aquario:main"]},
    python_requires=">=3.8",
)
