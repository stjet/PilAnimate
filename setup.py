from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='PilAnimate',
    url='https://github.com/jetstream0/PilAnimate',
    author='John Doe',
    author_email='prussia@prussia.dev',
    packages=['PilAnimate'],
    # Needed for dependencies
    install_requires=['Pillow',"opencv-python"],
    # *strongly* suggested for sharing
    version='0.4.2',
    # The license can be anything you like
    license='MIT',
    description="A python library using PIL to create animations.",
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
