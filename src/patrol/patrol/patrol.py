import math

from geometry_msgs.msg import Twist
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose


def is_valid_hz(value):
    if math.isnan(value) or math.isinf(value):
        return False
    return 1.0 <= value <= 30.0


def is_valid_speed(value):
    if math.isnan(value) or math.isinf(value):
        return False
    return 0.0 <= value <= 1.0


def is_valid_turn_rate(value):
    if math.isnan(value) or math.isinf(value):
        return False
    return -1.0 <= value <= 1.0


def choose_command(pose, linear_speed, turn_rate):
    cmd = Twist()
    if pose is None:
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
    else:
        cmd.linear.x = linear_speed
        cmd.angular.z = turn_rate
    return cmd


class Patrol(Node):
    def __init__(self):
        super().__init__('patrol')

        self.declare_parameter('linear_speed', 0.5)
        self.declare_parameter('turn_rate', 0.3)
        self.declare_parameter('publish_hz', 10.0)

        self.linear_speed = self.get_parameter('linear_speed').value
        self.turn_rate = self.get_parameter('turn_rate').value
        self.publish_hz = self.get_parameter('publish_hz').value

        self.add_on_set_parameters_callback(self.parameters_callback)

        self.last_pose = None
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)

        self.timer = self.create_timer(
            1.0 / self.publish_hz, self.timer_callback)

    def pose_callback(self, msg):
        self.last_pose = msg

    def timer_callback(self):
        cmd = choose_command(
            self.last_pose, self.linear_speed, self.turn_rate)
        self.publisher.publish(cmd)

    def parameters_callback(self, params):
        for param in params:
            if param.name == 'publish_hz':
                if not is_valid_hz(param.value):
                    return SetParametersResult(
                        successful=False,
                        reason='publish_hz must be in [1, 30]')
            elif param.name == 'linear_speed':
                if not is_valid_speed(param.value):
                    return SetParametersResult(
                        successful=False,
                        reason='linear_speed must be in [0, 1]')
            elif param.name == 'turn_rate':
                if not is_valid_turn_rate(param.value):
                    return SetParametersResult(
                        successful=False,
                        reason='turn_rate must be in [-1, 1]')

        for param in params:
            if param.name == 'publish_hz':
                self.publish_hz = param.value
                self._recreate_timer(param.value)
            elif param.name == 'linear_speed':
                self.linear_speed = param.value
            elif param.name == 'turn_rate':
                self.turn_rate = param.value

        return SetParametersResult(successful=True)

    def _recreate_timer(self, hz):
        if self.timer is not None:
            self.destroy_timer(self.timer)
        self.timer = self.create_timer(1.0 / hz, self.timer_callback)


def main(args=None):
    rclpy.init(args=args)
    node = Patrol()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
