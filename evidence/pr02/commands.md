# PR02. Команды, launch и CLI

## 1. Три команды Linux

### `mkdir -p`

- **Команда:** `mkdir -p src evidence/pr02`
- **Назначение:** создать каталоги, в том числе вложенные. Флаг `-p` создаёт промежуточные каталоги и не падает, если каталог уже существует.
- **Результат:** в корне репозитория появились `src/` и `evidence/pr02/`.

### `tee`

- **Команда:** `colcon build --symlink-install --packages-select turtle_bringup 2>&1 | tee evidence/pr02/build.txt`
- **Назначение:** `tee` читает stdin и пишет одновременно в stdout (на экран) и в файл. Используется, чтобы видеть вывод сборки и сохранить его в лог.
- **Результат:** лог сборки сохранён в `evidence/pr02/build.txt`, при этом вывод был виден в терминале.

### `cat`

- **Команда:** `cat evidence/pr02/build.txt`
- **Назначение:** вывести содержимое файла в stdout. Используется для просмотра небольших файлов.
- **Результат:** показано содержимое лога сборки:
  ```
  Starting >>> turtle_bringup
  Finished <<< turtle_bringup [1.45s]

  Summary: 1 package finished [1.66s]
  ```

## 2. Чем `>` отличается от `|`

- `>` **перенаправляет stdout в файл**, заменяя его содержимое. Пример: `ros2 doctor --report > evidence/pr01/doctor.txt` - вывод команды записан в файл, на экране ничего нет.
- `|` **передаёт stdout одной команды на stdin другой**. Пример: `colcon build ... 2>&1 | tee evidence/pr02/build.txt` - вывод `colcon` не пишется в файл напрямую, а передаётся `tee`, который уже пишет и на экран, и в файл.

Ключевое различие: `>` - это «записать в файл», `|` - это «передать другой программе».

## 3. Чем `source` отличается от запуска новой программы

- `source /opt/ros/jazzy/setup.bash` **выполняет скрипт в текущем shell**. Переменные окружения (`ROS_DISTRO`, `AMENT_PREFIX_PATH`, `PATH` и т.д.) меняются в **этом же** терминале и остаются после завершения скрипта.
- Запуск новой программы (например, `ros2 run turtlesim turtlesim_node`) **создаёт новый процесс**. Переменные, которые он меняет, на текущий shell не влияют. Когда процесс завершается, его окружение исчезает.

Поэтому `source install/setup.bash` нужен, чтобы текущий терминал «увидел» пакеты из `install/`. Без него `ros2 launch turtle_bringup ...` не найдёт пакет.

## 4. Launch: запуск и остановка

### Сборка пустого пакета

```
colcon build --symlink-install --packages-select turtle_bringup 2>&1 | tee evidence/pr02/build-empty.txt
```

Лог: `evidence/pr02/build-empty.txt`.

### Сборка с launch-файлом

```
colcon build --symlink-install --packages-select turtle_bringup 2>&1 | tee evidence/pr02/build.txt
```

Лог: `evidence/pr02/build.txt`.

### Запуск

```
source install/setup.bash
ros2 launch turtle_bringup sim.launch.py
```

Открывается окно turtlesim. В другом терминале:

```
ros2 node list --no-daemon --spin-time 2
```

Вывод:
```
/turtlesim
```

### Остановка

В терминале с launch - `Ctrl+C`. После остановки `ros2 node list --no-daemon --spin-time 2` пуст: нода завершилась.

## 5. CLI: команда и движение

### Тип позы и начальные координаты

```
ros2 topic type /turtle1/pose
ros2 topic echo /turtle1/pose --once
```

Вывод:
```
turtlesim/msg/Pose
x: 5.544444561004639
y: 5.544444561004639
theta: 0.0
linear_velocity: 0.0
angular_velocity: 0.0
```

### Одна команда в правильный топик

```
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

### Поза после команды

```
ros2 topic echo /turtle1/pose --once
```

Вывод:
```
x: 6.509308815002441
y: 5.796990871429443
theta: 0.5040000081062317
linear_velocity: 0.0
angular_velocity: 0.0
```

Поза изменилась: черепаха сдвинулась и повернулась.

## 6. Сбой: команда в `/cmd_vel`

### Непрерывная публикация в неправильный топик

```
ros2 topic pub --rate 1 --wait-matching-subscriptions 0 \
  /cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

Издатель работает, публикует `Twist` раз в секунду. Черепаха **не двигается**.

### Проверка конечных точек

```
ros2 topic info /cmd_vel --verbose
```

Вывод (фрагмент):
```
Type: geometry_msgs/msg/Twist
Publisher count: 1
Node name: _ros2cli_3875
Subscription count: 0
```

```
ros2 topic info /turtle1/cmd_vel --verbose
```

Вывод (фрагмент):
```
Type: geometry_msgs/msg/Twist
Publisher count: 0
Subscription count: 1
Node name: turtlesim
```

Сравнение: у `/cmd_vel` есть publisher, но **нет subscriber**. У `/turtle1/cmd_vel` есть subscriber `turtlesim`, но в этот момент publisher не было (издатель работал в `/cmd_vel`).

## 7. Исправление: команда в `/turtle1/cmd_vel`

### Непрерывная публикация в правильный топик

```
ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist \
  '{linear: {x: 1.0}, angular: {z: 0.5}}'
```

Черепаха снова двигается.

### Проверка конечных точек при работающем издателе

```
ros2 topic info /turtle1/cmd_vel --verbose
```

Вывод (фрагмент):
```
Type: geometry_msgs/msg/Twist
Publisher count: 1
Node name: _ros2cli_3925
Subscription count: 1
Node name: turtlesim
```

Publisher и subscriber связаны. Доставка есть.

### Поза после исправления

```
ros2 topic echo /turtle1/pose --once
```

Вывод:
```
x: 7.386900424957275
y: 6.7855963706970215
theta: 1.1776293516159058
linear_velocity: 0.0
angular_velocity: 0.0
```

## 8. Сравнение «до / сбой / после»

| Стадия | Топик | Publisher | Subscriber | Черепаха | Поза |
|--------|-------|-----------|------------|----------|------|
| до | `/turtle1/cmd_vel` | 1 (`_ros2cli`) | 1 (`turtlesim`) | двигается | изменилась |
| сбой | `/cmd_vel` | 1 (`_ros2cli_3875`) | 0 | не двигается | не изменилась |
| после | `/turtle1/cmd_vel` | 1 (`_ros2cli_3925`) | 1 (`turtlesim`) | двигается | изменилась |

## 9. Почему правильного типа сообщения недостаточно

Тип `geometry_msgs/msg/Twist` в обоих случаях одинаковый. Но доставка зависит не только от типа, а от **совпадения имени топика** (и домена). В сбое издатель публиковал в `/cmd_vel`, а `turtlesim` подписан на `/turtle1/cmd_vel`. Discovery не связывает publisher и subscriber с разными именами топиков, поэтому сообщения не доставлялись.

Достаточно исправить **только полное имя топика** - и доставка восстанавливается. Тип, скорость и домен менять не нужно.
