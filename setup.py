from setuptools import find_packages, setup


setup(
    name='q2-phylofactor',
    version='0.0.0',
    license='BSD-3-Clause',
    packages=find_packages(),
    author='John Chase',
    author_email='chasejohnh@gmail.com',
    url='https://github.com/johnchase/q2-phylofactor',
    scripts=['q2_phylofactor/assets/run_phylofactor.R'],
    entry_points={
        'qiime2.plugins':
        ['q2-phylofactor=q2_phylofactor.plugin_setup:plugin']
    },
    zip_safe=False,
)
