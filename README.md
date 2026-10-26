## ПР04. Параметризуем движение

### Сборка

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=16
cd ~/ros_practice_1
colcon build --symlink-install --packages-select patrol
source install/setup.bash
```

### Запуск

```bash
ros2 run turtlesim turtlesim_node
```

```bash
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

### Параметры

```bash
ros2 param list /patrol
ros2 param get /patrol linear_speed
ros2 param get /patrol turn_rate
ros2 param get /patrol publish_hz
```

Допустимые значения:
- `linear_speed`: 0-1 м/с,
- `turn_rate`: -1-1 рад/с,
- `publish_hz`: 1-30 Гц.

### Изменение на лету

```bash
ros2 param set /patrol publish_hz 5.0
ros2 param set /patrol linear_speed 0.8
ros2 param set /patrol turn_rate 0.5
```

### Недопустимое значение отклоняется

```bash
ros2 param set /patrol publish_hz 0.0
# Setting parameter failed: publish_hz must be in [1, 30]
ros2 param get /patrol publish_hz
# Прежнее значение
```

### Тесты

```bash
python3 -m pytest src/patrol/test -v -p no:warnings
```

### Service и action

```bash
ros2 service call /clear std_srvs/srv/Empty
ros2 action list -t
```
