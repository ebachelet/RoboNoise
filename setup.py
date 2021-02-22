from setuptools import setup, find_packages, Extension

setup(
    name="RoboNoise",
    version="0.0.1",
    description="Red Noise analysis",
    keywords='',
    author="Etienne Bachelet",
    author_email="etibachelet@gmail.com",
    license='GPL-3.0',
    url="https://github.com/ebachelet/RoboNoise",
    packages=find_packages('.'),
    include_package_data=True,
    install_requires=['scipy','numpy','pandas'],
    test_suite="nose.collector",
    classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
                'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3',	   
],
)
