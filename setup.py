from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in digital_seva/__init__.py
from digital_seva import __version__ as version

setup(
	name="digital_seva",
	version=version,
	description="This app provides extended ticketing solution on ERPNext or any other App build on Frappe.",
	author="NestorBird",
	author_email="info@nestorbird.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
