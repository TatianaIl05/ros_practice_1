# PR04. Параметры

## Текущие значения

```
ros2 param get /patrol linear_speed
Double value is: 0.5

ros2 param get /patrol turn_rate
Double value is: 0.3

ros2 param get /patrol publish_hz
Double value is: 10.0
```

## Частота публикации

```
timeout 10s ros2 topic hz /turtle1/cmd_vel
average rate: 9.998
average rate: 10.000
average rate: 10.000
```

Ожидаемая частота ~10 Гц, измеренная ~10 Гц.

## Допустимое изменение частоты (10 → 5 Гц)

```
ros2 param set /patrol publish_hz 5.0
Set parameter successful

ros2 param get /patrol publish_hz
Double value is: 5.0

timeout 10s ros2 topic hz /turtle1/cmd_vel
average rate: 5.000
average rate: 5.000
```

Таймер пересоздан с периодом 1/5 = 0.2 с. Частота изменилась.

## Недопустимое значение - 0

```
ros2 param set /patrol publish_hz 0.0
Setting parameter failed: publish_hz must be in [1, 30]

ros2 param get /patrol publish_hz
Double value is: 5.0

timeout 10s ros2 topic hz /turtle1/cmd_vel
average rate: 5.000
```

Значение отклонено. `publish_hz` остался 5.0, частота осталась ~5 Гц. Старый таймер продолжает работать.

## Недопустимое значение - отрицательное

```
ros2 param set /patrol publish_hz -1.0
Setting parameter failed: publish_hz must be in [1, 30]
```

## NaN

```
ros2 param set /patrol publish_hz nan
Setting parameter failed: Wrong parameter type, expected 'Type.DOUBLE' got 'Type.STRING'
```

Через CLI `nan` передаётся как строка, поэтому ошибка типа. В тестах чистой функции `is_valid_hz(float('nan'))` возвращает `False`.

## Сбой: проверка отключена, publish_hz = 0

Проверка `publish_hz` временно закомментирована в `parameters_callback`. Передано:

```
ros2 param set /patrol publish_hz 0.0
```

Результат в терминале ноды:

```
ZeroDivisionError: float division by zero
[ros2run]: Process exited with failure 1
```

Полный traceback:

```
Traceback (most recent call last):
  ...
  File "patrol.py", line 91, in parameters_callback
    self._recreate_timer(param.value)
  File "patrol.py", line 102, in _recreate_timer
    self.timer = self.create_timer(1.0 / hz, self.timer_callback)
                                   ~~~~^~~~
ZeroDivisionError: float division by zero
```

Причина: без проверки `0.0` попадает в `_recreate_timer`, `1.0 / 0.0` даёт деление на ноль, нода падает.

## Исправление: проверка возвращена, publish_hz = 0

```
ros2 param set /patrol publish_hz 0.0
Setting parameter failed: publish_hz must be in [1, 30]

ros2 param get /patrol publish_hz
Double value is: 5.0

timeout 10s ros2 topic hz /turtle1/cmd_vel
average rate: 5.000
```

Значение отклонено, `publish_hz` и частота остались прежними. Нода продолжает работать.

## Допустимое изменение скорости и поворота

```
ros2 param set /patrol linear_speed 0.8
Set parameter successful

ros2 param set /patrol turn_rate 0.5
Set parameter successful
```

Черепаха двигается быстрее и круче.

## Service и action

```
ros2 service call /clear std_srvs/srv/Empty
requester: making request: std_srvs.srv.Empty_Request()
response:
std_srvs.srv.Empty_Response()

ros2 action list -t
/turtle1/rotate_absolute [turtlesim/action/RotateAbsolute]
```

**Отличие запроса и цели:**
Service `/clear` - запрос-ответ: отправил запрос, получил ответ, операция завершена.
Action `/turtle1/rotate_absolute` - длительная операция: отправил цель, получаешь feedback о прогрессе, можешь отменить до завершения.
