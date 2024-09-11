from setuptools import find_packages, setup

package_name = 'ur10_vel'

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
        'publisher_forward_velocity_controller = ur10_vel.publisher_forward_velocity_controller:main',
        'joint_velocity_IK = ur10_vel.joint_velocity_IK:main',
        'check_collision = ur10_vel.check_collision:main',
        'check_keyboard = ur10_vel.check_keyboard:main',
        'Joint_Velocity_Transfer = ur10_vel.Joint_Velocity_Transfer:main',
        ],
    },
)
