import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

install_requirements = [
        'progressbar2>=2.6.0',
]

setup(
    name='django-gis-brasil',
    version='0.3',
    packages=['gisbrasil','gisbrasil.management', 'gisbrasil.management.commands'],
    include_package_data=True,
    license='BSD License',
    zip_safe=False,
    description='Django GIS Brasil is a Django app (GeoDjango) with Brazilian GIS information.',
    long_description=README,
    install_requires=install_requirements,
    url='https://github.com/perone/django-gis-brasil',
    author='CodeFi.sh Team (Christian S. Perone, Leandro Nunes, Gabriel Wainer)',
    author_email='christian.perone@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
