## ПР05. Launch, QoS и повтор записи

### Сборка

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=16
cd ~/ros_practice_1
colcon build --symlink-install --packages-select course_bringup
source install/setup.bash
```

### Запуск с reliable (сбой)

```bash
ros2 launch course_bringup patrol.launch.py \
  namespace:=robot_a subscriber_reliability:=reliable record:=false
```

Проверка:

```bash
ros2 node list --no-daemon --spin-time 2
ros2 topic list -t
timeout 5s ros2 topic echo /robot_a/sensor_pose --qos-reliability reliable --once
```

Ожидается `exit=124` (несовместимый QoS).

### Запуск с best_effort (исправление)

```bash
ros2 launch course_bringup patrol.launch.py \
  namespace:=robot_a subscriber_reliability:=best_effort record:=false
```

Проверка:

```bash
timeout 5s ros2 topic echo /robot_a/sensor_pose --qos-reliability best_effort --once
```

Ожидается поза и `exit=0`.

### Запись bag (MCAP)

```bash
ros2 launch course_bringup patrol.launch.py \
  namespace:=robot_a subscriber_reliability:=best_effort record:=true \
  bag_dir:=evidence/pr05/bag
```

Подождать 10-15 секунд, остановить `Ctrl+C`.

```bash
ros2 bag info evidence/pr05/bag
```

### Replay с QoS override

```bash
ros2 bag play evidence/pr05/bag \
  --qos-profile-overrides-path config/qos-overrides.yaml
```

Проверка:

```bash
timeout 5s ros2 topic echo /robot_a/sensor_pose --qos-reliability best_effort --once
timeout 5s ros2 topic echo /robot_a/sensor_pose --qos-reliability reliable --once
```

Ожидается: `exit=0` для best_effort, `exit=124` для reliable.
