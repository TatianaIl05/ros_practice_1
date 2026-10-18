# PR01. Граф ROS 2

## 1. Исправный граф (домен 16)

### Список нод
Команда:
    ros2 node list --no-daemon --spin-time 2

Вывод:
    /teleop_turtle
    /turtlesim

### Список топиков и типы
Команда:
    ros2 topic list -t

Вывод:
    /parameter_events [rcl_interfaces/msg/ParameterEvent]
    /rosout [rcl_interfaces/msg/Log]
    /turtle1/cmd_vel [geometry_msgs/msg/Twist]
    /turtle1/color_sensor [turtlesim/msg/Color]
    /turtle1/pose [turtlesim/msg/Pose]

### Информация о ноде /turtlesim
Команда:
    ros2 node info /turtlesim

Вывод:
    /turtlesim
      Subscribers:
        /parameter_events: rcl_interfaces/msg/ParameterEvent
        /turtle1/cmd_vel: geometry_msgs/msg/Twist
      Publishers:
        /parameter_events: rcl_interfaces/msg/ParameterEvent
        /rosout: rcl_interfaces/msg/Log
        /turtle1/color_sensor: turtlesim/msg/Color
        /turtle1/pose: turtlesim/msg/Pose
      Service Servers:
        /clear: std_srvs/srv/Empty
        /kill: turtlesim/srv/Kill
        /reset: std_srvs/srv/Empty
        /spawn: turtlesim/srv/Spawn
        /turtle1/set_pen: turtlesim/srv/SetPen
        /turtle1/teleport_absolute: turtlesim/srv/TeleportAbsolute
        /turtle1/teleport_relative: turtlesim/srv/TeleportRelative
        /turtlesim/describe_parameters: rcl_interfaces/srv/DescribeParameters
        /turtlesim/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
        /turtlesim/get_parameters: rcl_interfaces/srv/GetParameters
        /turtlesim/get_type_description: type_description_interfaces/srv/GetTypeDescription
        /turtlesim/list_parameters: rcl_interfaces/srv/ListParameters
        /turtlesim/set_parameters: rcl_interfaces/srv/SetParameters
        /turtlesim/set_parameters_atomically: rcl_interfaces/srv/SetParametersAtomically
      Service Clients:
      Action Servers:
        /turtle1/rotate_absolute: turtlesim/action/RotateAbsolute
      Action Clients:

### Тип позы
Команда:
    ros2 topic type /turtle1/pose

Вывод:
    turtlesim/msg/Pose

Переменная для дальнейших проверок:
    POSE_TYPE=turtlesim/msg/Pose

### Одно сообщение позы
Команда:
    ros2 topic echo /turtle1/pose --once

Вывод:
    x: 6.355550765991211
    y: 7.510218620300293
    theta: -2.049556016921997
    linear_velocity: 0.0
    angular_velocity: 0.0
    ---

### Частота публикации позы
Команда:
    ros2 topic hz /turtle1/pose

Вывод (фрагмент, замер ~12 секунд):
    average rate: 62.476  min: 0.015s max: 0.017s std dev: 0.00056s window: 64
    average rate: 62.473  min: 0.015s max: 0.017s std dev: 0.00056s window: 127
    average rate: 62.476  min: 0.015s max: 0.017s std dev: 0.00056s window: 190
    average rate: 62.488  min: 0.015s max: 0.017s std dev: 0.00056s window: 253
    average rate: 62.492  min: 0.015s max: 0.017s std dev: 0.00055s window: 316
    average rate: 62.495  min: 0.015s max: 0.017s std dev: 0.00054s window: 379
    average rate: 62.499  min: 0.015s max: 0.017s std dev: 0.00053s window: 442
    average rate: 62.497  min: 0.015s max: 0.017s std dev: 0.00052s window: 505
    average rate: 62.499  min: 0.015s max: 0.017s std dev: 0.00052s window: 568
    average rate: 62.500  min: 0.014s max: 0.017s std dev: 0.00052s window: 631
    average rate: 62.501  min: 0.014s max: 0.017s std dev: 0.00052s window: 694
    average rate: 62.500  min: 0.014s max: 0.017s std dev: 0.00052s window: 757

Измеренная частота: ~62.5 Гц
Длительность замера: ~12 секунд
Отклонений и отрицательных интервалов нет.

### Роли нод и топиков
- `/turtlesim` - симулятор: публикует `/turtle1/pose` и `/turtle1/color_sensor`,
  подписан на `/turtle1/cmd_vel`.
- `/teleop_turtle` - управление с клавиатуры: публикует `/turtle1/cmd_vel`.

## 2. Разрыв связи (домен 17)

Действия:
- Терминал A (turtlesim) оставлен в домене 16.
- Терминал B: teleop остановлен через Ctrl+C и запущен заново:
      export ROS_DOMAIN_ID=17
      ros2 run turtlesim turtle_teleop_key
- Терминал C:
      export ROS_DOMAIN_ID=17
      ros2 node list --no-daemon --spin-time 2
      timeout 5s ros2 topic echo /turtle1/pose "$POSE_TYPE" --once > evidence/pr01/pose-broken.txt 2>&1
      printf 'exit=%s\n' "$?" >> evidence/pr01/pose-broken.txt

Наблюдения:
- `ros2 node list` в домене 17 показывает только `/teleop_turtle`;
  `/turtlesim` не обнаружен, потому что работает в домене 16.
- Поза не приходит: `pose-broken.txt` содержит только `exit=124`.
- Код 124 означает, что `timeout 5s` истёк - за 5 секунд сообщение
  `/turtle1/pose` не получено.
- Стрелки в терминале B не двигают черепаху.

## 3. Восстановление связи (домен 16)

Действия:
- Терминал B: teleop остановлен через Ctrl+C и запущен заново:
      export ROS_DOMAIN_ID=16
      ros2 run turtlesim turtle_teleop_key
- Терминал C:
      export ROS_DOMAIN_ID=16
      ros2 node list --no-daemon --spin-time 2
      timeout 5s ros2 topic echo /turtle1/pose "$POSE_TYPE" --once > evidence/pr01/pose-fixed.txt 2>&1
      printf 'exit=%s\n' "$?" >> evidence/pr01/pose-fixed.txt

Наблюдения:
- `ros2 node list` снова показывает обе ноды: `/teleop_turtle` и `/turtlesim`.
- Поза приходит: `pose-fixed.txt` содержит x, y, theta, linear_velocity,
  angular_velocity и `exit=0`.
- Код 0 означает, что сообщение получено до истечения 5 секунд.
- Стрелки снова двигают черепаху.

## 4. Сравнение «до / сбой / после»

| Стадия | Домен A (turtlesim) | Домен B (teleop) | Домен C (наблюдение) | /turtlesim виден | Поза | exit |
|--------|---------------------|------------------|----------------------|------------------|------|------|
| до     | 16                  | 16               | 16                   | да               | да   | 0    |
| сбой   | 16                  | 17               | 17                   | нет              | нет  | 124  |
| после  | 16                  | 16               | 16                   | да               | да   | 0    |

## 5. Почему пришлось перезапустить teleop, а симулятор и ROS — нет

`ROS_DOMAIN_ID` читается один раз - при запуске ноды - и определяет
область обнаружения участников. `export` меняет переменную только
для новых процессов в текущем терминале; уже работающая нода её
не перечитывает. Поэтому teleop в терминале B пришлось остановить
(Ctrl+C) и запустить заново с `ROS_DOMAIN_ID=17`.

Симулятор `/turtlesim` всё время работал в домене 16: его домен
не менялся, перезапуск не требовался. Он продолжал публиковать
`/turtle1/pose` в домене 16, но подписчик в домене 17 её не получал -
discovery не связывает участников из разных доменов.

Установка ROS 2 общая для всех доменов: `/opt/ros/jazzy` один и тот же
при любом `ROS_DOMAIN_ID`. Причина разрыва - не сбой ROS и не дефект
симулятора, а разные домены у участников.
