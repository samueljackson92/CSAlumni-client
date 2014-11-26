try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'The CS Alumni application',
    'author': 'Samuel Jackson',
    'url': 'http://github.com/samueljackson92/CSAlumni-Client',
    'download_url': 'http://github.com/samueljackson92/CSAlumni-Client',
    'author_email': 'samueljackson@outlook.com',
    'version': '0.1.0',
    'install_requires': ['nose', 'requests', 'responses'],
    'packages': ['csa_api'],
    'scripts': [],
    'name': 'csa_client'
}

setup(**config)
