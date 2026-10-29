## ПР06. Модель робота, tf2 и QoS преобразований

### Сборка

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=16
cd ~/ros_practice_1
colcon build --symlink-install --packages-select course_description
source install/setup.bash
```

### Проверка URDF

```bash
xacro src/course_description/urdf/vehicle.urdf.xacro > /tmp/vehicle.urdf
check_urdf /tmp/vehicle.urdf
```

### Запуск

```bash
ros2 launch course_description display.launch.py
```

### QoS на /tf_static

```bash
ros2 topic info /tf_static --verbose
timeout 4 ros2 topic echo /tf_static --once \
  --qos-durability transient_local --qos-reliability reliable
timeout 4 ros2 topic echo /tf_static --once \
  --qos-durability volatile --qos-reliability reliable
```

### Проверка TF

```bash
ros2 run tf2_ros tf2_echo base_link lidar_link
ros2 run tf2_tools view_frames
```

### Сбой

Изменить parent у `lidar_joint` с `base_link` на `camera_link`:

```bash
# в vehicle.urdf.xacro
<parent link="camera_link"/>
```

Пересобрать, запустить, проверить `tf2_echo` — неверное положение `[0.560, 0.000, 0.760]`. Вернуть `base_link`.
