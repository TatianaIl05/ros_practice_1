# PR06. Дерево frames

## Владельцы преобразований

- `/tf_static` - `robot_state_publisher` (fixed joints: camera, lidar, imu).
- `/tf` - `robot_state_publisher` (continuous joints: колёса), но только когда приходят `joint_states`.

## Таблица связей

| Joint | Parent | Child | xyz | rpy | Тип | Владелец |
|-------|--------|-------|-----|-----|-----|----------|
| camera_joint | base_link | camera_link | 0.28 0 0.38 | 0 0 0 | fixed | robot_state_publisher (/tf_static) |
| lidar_joint | base_link | lidar_link | 0.28 0 0.38 | 0 0 0 | fixed | robot_state_publisher (/tf_static) |
| imu_joint | base_link | imu_link | 0.28 0 0.38 | 0 0 0 | fixed | robot_state_publisher (/tf_static) |
| front_left_wheel_joint | base_link | front_left_wheel_link | 0.4 0.31 0 | 1.57 0 0 | continuous | robot_state_publisher (/tf, при joint_states) |
| front_right_wheel_joint | base_link | front_right_wheel_link | 0.4 -0.31 0 | 1.57 0 0 | continuous | robot_state_publisher (/tf, при joint_states) |
| rear_left_wheel_joint | base_link | rear_left_wheel_link | -0.4 0.31 0 | 1.57 0 0 | continuous | robot_state_publisher (/tf, при joint_states) |
| rear_right_wheel_joint | base_link | rear_right_wheel_link | -0.4 -0.31 0 | 1.57 0 0 | continuous | robot_state_publisher (/tf, при joint_states) |

## Проверка

- `check_urdf` проходит: дерево связное, 7 дочерних звеньев у `base_link`.
- `tf2_echo base_link lidar_link` показывает преобразование (0.28, 0, 0.38).
- `tf2_echo base_link camera_link` показывает то же преобразование.
- `tf2_echo base_link imu_link` показывает то же преобразование.
- Колёса не публикуются в `/tf`, пока нет `joint_states`.
