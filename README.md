# ros_practice_1

## ПР01. Окружение и граф ROS 2

### Запуск

Все терминалы открываются в корне репозитория, в одной среде (WSL2, Ubuntu 24.04, ROS 2 Jazzy).

Подготовка в каждом терминале:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=16
```

Терминал A - симулятор (работает до Ctrl+C):

```bash
ros2 run turtlesim turtlesim_node
```

Терминал B - управление с клавиатуры (работает до Ctrl+C):

```bash
ros2 run turtlesim turtle_teleop_key
```

Терминал C - наблюдение:

```bash
ros2 node list --no-daemon --spin-time 2
ros2 topic list -t
ros2 node info /turtlesim
ros2 topic type /turtle1/pose
ros2 topic echo /turtle1/pose --once
ros2 topic hz /turtle1/pose
```

`ros2 topic hz` оставить на 10-15 секунд, затем Ctrl+C. Ожидаемая частота - около 62.5 Гц.

### Разрыв связи (домен 17)

В терминале B остановить teleop (Ctrl+C) и запустить заново в другом домене:

```bash
export ROS_DOMAIN_ID=17
ros2 run turtlesim turtle_teleop_key
```

В терминале C:

```bash
export ROS_DOMAIN_ID=17
ros2 node list --no-daemon --spin-time 2
timeout 5s ros2 topic echo /turtle1/pose turtlesim/msg/Pose --once > evidence/pr01/pose-broken.txt 2>&1
printf 'exit=%s\n' "$?" >> evidence/pr01/pose-broken.txt
```

Ожидается: в списке нод только `/teleop_turtle`, `/turtlesim` не виден, поза не приходит, `timeout` завершается с `exit=124`.

### Восстановление связи (домен 16)

В терминале B остановить teleop (Ctrl+C) и запустить заново в исходном домене:

```bash
export ROS_DOMAIN_ID=16
ros2 run turtlesim turtle_teleop_key
```

В терминале C:

```bash
export ROS_DOMAIN_ID=16
ros2 node list --no-daemon --spin-time 2
timeout 5s ros2 topic echo /turtle1/pose turtlesim/msg/Pose --once > evidence/pr01/pose-fixed.txt 2>&1
printf 'exit=%s\n' "$?" >> evidence/pr01/pose-fixed.txt
```

Ожидается: обе ноды видны, поза приходит, `exit=0`, стрелки снова двигают черепаху.

### CI

Workflow `.github/workflows/ci.yml` скачивает зафиксированный course-kit `v1-w06`, проверяет SHA-256, валидирует `evidence/pr01/environment.json` и запускает `check_practice.py PR01 --submission .`.

### Evidence

В каталоге `evidence/pr01/`:

- `doctor.txt` - отчёт `ros2 doctor --report`;
- `graph.md` - команды и вывод, ноды и роли, топики и типы, измеренная частота, сравнение «до / сбой / после», объяснение причины разрыва;
- `environment.json` - способ запуска, версия ОС, дистрибуция ROS, версия Gazebo, RMW, домены опыта;
- `pose-broken.txt` - доказательство разрыва связи (`exit=124`);
- `pose-fixed.txt` - доказательство восстановления связи (`exit=0`);
- `report.json` - отчёт по шаблону course-kit с SHA коммита реализации и заявлениями `public_tests_passed`, `defect_reproduced`, `defect_fixed`.
