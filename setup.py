from setuptools import setup, find_packages

setup(
    name='anompy',
    version='0.0.1',
    description='A library for anomaly detection',
    author='Takuya Kitazawa',
    author_email='k.takuti@gmail.com',
    license='MIT',
    url='https://github.com/takuti/anompy',
    packages=find_packages(exclude=['*tests*']),
    install_requires=['numpy', 'scikit_learn'],
)
