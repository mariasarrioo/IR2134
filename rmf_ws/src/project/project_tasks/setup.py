"""A set of scripts to issue tasks to Open-RMF from the command line."""
from setuptools import setup

package_name = 'project_tasks'

setup(
    name=package_name,
    version='2.8.1',
    packages=[package_name],
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    author='Grey',
    author_email='grey@openrobotics.org',
    zip_safe=True,
    maintainer='yadu',
    maintainer_email='yadunund@openrobotics.org',
    description='A package containing scripts for demos',
    license='Apache License Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'request_loop = project_tasks.request_loop:main',
            'request_lift = project_tasks.request_lift:main',
            'cancel_task = project_tasks.cancel_task:main',
            'dispatch_dynamic_event = \
                project_tasks.dispatch_dynamic_event:main',
            'dynamic_event_client = project_tasks.dynamic_event_client:main',
            'cancel_robot_task = project_tasks.cancel_robot_task:main',
            'dispatch_loop = project_tasks.dispatch_loop:main',
            'dispatch_action = project_tasks.dispatch_action:main',
            'dispatch_patrol = project_tasks.dispatch_patrol:main',
            'dispatch_delivery = project_tasks.dispatch_delivery:main',
            'dispatch_cart_delivery = '
                'project_tasks.dispatch_cart_delivery:main',
            'dispatch_clean = project_tasks.dispatch_clean:main',
            'dispatch_go_to_place = project_tasks.dispatch_go_to_place:main',
            'dispatch_teleop = project_tasks.dispatch_teleop:main',
            'get_robot_location = project_tasks.get_robot_location:main',
            'mock_docker = project_tasks.mock_docker:main',
            'teleop_robot = project_tasks.teleop_robot:main',
            'dispatch_json = project_tasks.dispatch_json:main',
            'api_request = project_tasks.api_request:main',
            'wait_for_task_complete = \
                project_tasks.wait_for_task_complete:main',
            'emergency_signal = project_tasks.emergency_signal:main'
        ],
    },
)
