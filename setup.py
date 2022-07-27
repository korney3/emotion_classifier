import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='data_science_module',
    version='0.0.10',
    author='korney3',
    author_email='koren.iz3x@yandex.ru',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/korney3/fact_extractor_emotion_classifier',
    project_urls={
        "Bug Tracker": "https://github.com/korney3/fact_extractor_emotion_classifier/issues"
    },
    license='MIT',
    packages=setuptools.find_packages(),
    package_data={'data_science_module': ['./models/*.joblib', './models/*.yml']},
    include_package_data=True,
    install_requires=['jupyter', 'natasha', 'pandas', "plotly", 'dostoevsky', 'pyyaml', 'scikit-learn', 'nltk',
                      'translate', 'openpyxl', 'wiki-ru-wordnet'],
)
