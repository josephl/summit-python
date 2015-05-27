from setuptools import setup


setup(
    name='summit',
    description='Summit API client',
    author='Joseph Lee',
    author_email='joe.lee@corvisa.com',
    py_modules=['summit'],
    url='https://github.com/josephl/summit-python',
    keywords=['summit', 'corvisa', 'sms', 'twilio'],
    install_requires=['requests'],
)
