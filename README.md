## ПР03. Первая нода: поза и команда

### Сборка

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=16
cd ~/ros_practice_1
colcon build --symlink-install --packages-select patrol
source install/setup.bash
```

### Запуск turtlesim

```bash
ros2 run turtlesim turtlesim_node
```

### Запуск patrol без remap (сбой)

```bash
ros2 run patrol patrol
```

Публикация идёт в `/cmd_vel`, черепаха не двигается.

### Запуск patrol с remap (исправление)

```bash
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

Черепаха двигается по кругу.

### Проверка частоты

```bash
timeout 10s ros2 topic hz /turtle1/cmd_vel
```

Ожидается ~10 Гц.

### Тесты

```bash
python3 -m pytest src/patrol/test -v -p no:warnings
```
