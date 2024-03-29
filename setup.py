try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'CS Alumni Client application',
    'author': 'Samuel Jackson',
    'url': 'http://github.com/samueljackson92/CSAlumni-Client',
    'download_url': 'http://github.com/samueljackson92/CSAlumni-Client',
    'author_email': 'samueljackson@outlook.com',
    'version': '0.1.0',
    'install_requires': ['nose', 'requests', 'responses', 'coverage', 'click', 'tabulate', 'pickledb'],
    'entry_points': '''
        [console_scripts]
        csa_client=csa_client.command:cli
    ''',
    'packages': ['csa_client'],
    'scripts': [],
    'name': 'csa_client'
}

setup(**config)
