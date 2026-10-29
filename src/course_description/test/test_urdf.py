from pathlib import Path

import subprocess
import xml.etree.ElementTree as ET


def get_urdf():
    urdf_path = Path(__file__).parent.parent / 'urdf' / 'vehicle.urdf.xacro'
    result = subprocess.run(
        ['xacro', str(urdf_path)],
        capture_output=True, text=True, check=True)
    return ET.fromstring(result.stdout)


def get_parent(urdf, joint_name):
    for joint in urdf.findall('joint'):
        if joint.get('name') == joint_name:
            return joint.find('parent').get('link')
    return None


def test_lidar_parent():
    urdf = get_urdf()
    assert get_parent(urdf, 'lidar_joint') == 'base_link'


def test_camera_parent():
    urdf = get_urdf()
    assert get_parent(urdf, 'camera_joint') == 'base_link'


def test_imu_parent():
    urdf = get_urdf()
    assert get_parent(urdf, 'imu_joint') == 'base_link'


def test_wheels_parent():
    urdf = get_urdf()
    for wheel in ['front_left', 'front_right', 'rear_left', 'rear_right']:
        assert get_parent(urdf, f'{wheel}_wheel_joint') == 'base_link'


def test_all_children_of_base_link():
    urdf = get_urdf()
    children = set()
    for joint in urdf.findall('joint'):
        if joint.find('parent').get('link') == 'base_link':
            children.add(joint.find('child').get('link'))
    expected = {
        'camera_link', 'lidar_link', 'imu_link',
        'front_left_wheel_link', 'front_right_wheel_link',
        'rear_left_wheel_link', 'rear_right_wheel_link',
    }
    assert children == expected
