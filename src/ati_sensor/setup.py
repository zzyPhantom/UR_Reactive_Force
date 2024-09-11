from setuptools import find_packages, setup

package_name = 'ati_sensor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zzy',
    maintainer_email='15011088784@163.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test_rpi_ati_net_ft = ati_sensor.test_rpi_ati_net_ft:main',
            'ati_net_ft_driver_ros = ati_sensor.ati_net_ft_driver_ros:main',
        ],
    },
)
