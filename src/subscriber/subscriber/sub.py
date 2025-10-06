import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature, FluidPressure 


class Bmp280Subscriber(Node):
    def __init__(self):
        super().__init__('bmp280_subscriber')

        # Declare params so you can remap easily if topic names change
        self.declare_parameter('temp_topic', '/bmp280/temperature')
        self.declare_parameter('press_topic', '/bmp280/pressure')

        temp_topic  = self.get_parameter('temp_topic').get_parameter_value().string_value
        press_topic = self.get_parameter('press_topic').get_parameter_value().string_value

        # Subscriptions
        self.temp_sub = self.create_subscription(
            Temperature, temp_topic, self.temp_cb, 10
        )
        self.press_sub = self.create_subscription(
            FluidPressure, press_topic, self.press_cb, 10
        )

        self.get_logger().info(f'Subscribing to {temp_topic} and {press_topic}')

    def temp_cb(self, msg: Temperature):
        # msg.temperature in °C; msg.header.stamp is the timestamp
        self.get_logger().info(f'Temperature: {msg.temperature:.2f} °C')

    def press_cb(self, msg: FluidPressure):
        # msg.fluid_pressure in Pascals
        self.get_logger().info(f'Pressure: {msg.fluid_pressure:.1f} Pa')

def main(args=None):
    rclpy.init(args=args)
    node = Bmp280Subscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
