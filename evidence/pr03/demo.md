# PR03. Нода patrol: подписка, таймер, remap

## Роли init, spin, callback, Ctrl+C

### `rclpy.init(args=args)`

Инициализирует контекст rclpy: создаёт сетевое окружение, регистрирует процесс как участника ROS 2. Вызывается один раз перед созданием ноды. Без него `Node()` не сможет создать publisher/subscriber.

### `rclpy.spin(node)`

Запускает бесконечный цикл обработки событий: принимает сообщения, вызывает callback'и, срабатывает таймер. Без `spin` нода создана, но ничего не делает: подписка не получает сообщения, таймер не срабатывает.

### Callback (`pose_callback`, `timer_callback`)

- `pose_callback` вызывается, когда в `/turtle1/pose` приходит новое сообщение. Он только сохраняет `self.last_pose = msg`. Никакой логики движения в нём нет.
- `timer_callback` вызывается каждые 0.1 с (таймер). Он вызывает `choose_command(self.last_pose)` и публикует результат в `cmd_vel`.

Такое разделение: подписка обновляет состояние, таймер действует по состоянию. Это стандартный паттерн ROS 2.

### `Ctrl+C`

При `Ctrl+C` в терминале Python получает `KeyboardInterrupt`. В `main` он перехватывается (`except KeyboardInterrupt`), затем вызывается `node.destroy_node()` и `rclpy.shutdown()`. Нода аккуратно отключается от графа.

Важно: `Ctrl+C` не отправляет нулевую команду в `turtlesim`. Если до остановки черепаха двигалась, она продолжит движение по инерции последней команды, пока не придёт новая команда или не сработает таймаут turtlesim. Поэтому после остановки ноды нужно дождаться остановки черепахи - это не мгновенно.

## Сбой и исправление

### Сбой: публикация в относительный `cmd_vel`

`patrol` создаёт publisher на `cmd_vel` (относительное имя). В ROS 2 относительное имя разрешается в `/cmd_vel` (в корневом namespace). `turtlesim` подписан на `/turtle1/cmd_vel`. Имена разные - discovery не связывает publisher и subscriber.

Наблюдение:
- `ros2 topic info /cmd_vel --verbose`: publisher 1 (`/patrol`), subscriber 0.
- `ros2 topic info /turtle1/cmd_vel --verbose`: publisher 0, subscriber 1 (`/turtlesim`).
- Черепаха не двигается.

### Исправление: remap

```
ros2 run patrol patrol --ros-args -r cmd_vel:=/turtle1/cmd_vel
```

Remap подменяет имя топика при запуске: нода по-прежнему публикует в `cmd_vel`, но ROS 2 перенаправляет это в `/turtle1/cmd_vel`. Discovery связывает publisher и subscriber.

Наблюдение:
- `ros2 topic info /turtle1/cmd_vel --verbose`: publisher 1 (`/patrol`), subscriber 1 (`/turtlesim`).
- Черепаха двигается по кругу.
- `ros2 topic hz /turtle1/cmd_vel`: ~10 Гц, `min: 0.099s`, `max: 0.101s`, `std dev: 0.0005s`.

## Измеренная частота

Замер 10 секунд, окно 75 сообщений:
```
average rate: 10.000
        min: 0.099s max: 0.101s std dev: 0.00045s window: 75
```

Таймер 0.1 с даёт ~10 Гц. Отклонение в пределах 1 мс.

## Чистая функция `choose_command`

Выбор команды вынесен из `timer_callback` в отдельную функцию `choose_command(pose)`:
- `pose is None` - нулевая команда (`linear.x=0.0`, `angular.z=0.0`),
- `pose` есть - `linear.x=0.5`, `angular.z=0.3`.

Тесты:
```
src/patrol/test/test_patrol.py::test_choose_command_no_pose PASSED
src/patrol/test/test_patrol.py::test_choose_command_with_pose PASSED
```

## Вывод

Правильного типа сообщения (`geometry_msgs/msg/Twist`) недостаточно: нужно совпадение имени топика. В ПР01 ломали домен, в ПР02 - имя топика, в ПР03 - относительное имя против абсолютного. Механизм один: discovery не связывает publisher и subscriber, если что-то не совпадает.
