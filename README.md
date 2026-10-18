## ПР02. Терминал, пакет и запуск turtlesim

### Сборка

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=16
cd ~/ros_practice_1
colcon build --symlink-install --packages-select turtle_bringup \
  2>&1 | tee evidence/pr02/build.txt
source install/setup.bash
```

### Запуск

```bash
ros2 launch turtle_bringup sim.launch.py
```

В другом терминале:

```bash
export ROS_DOMAIN_ID=16
ros2 node list --no-daemon --spin-time 2
```

Остановка - `Ctrl+C` в терминале с launch.

### CLI: движение

```bash
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
ros2 topic echo /turtle1/pose --once
```

### Сбой и исправление

Сбой - публикация в неправильный топик `/cmd_vel`:

```bash
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

Проверка:

```bash
ros2 topic info /cmd_vel --verbose
ros2 topic info /turtle1/cmd_vel --verbose
```

Исправление - публикация в `/turtle1/cmd_vel`:

```bash
ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
```
