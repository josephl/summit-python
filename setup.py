from setuptools import setup, find_packages


setup(
    name='summit',
    description='Summit API client',
    author='Joseph Lee',
    author_email='joe.lee@corvisa.com',
    packages=find_packages(),
    url='https://github.com/josephl/summit-python',
    keywords=['summit', 'corvisa', 'sms', 'twilio'],
    install_requires=['requests'],
)
