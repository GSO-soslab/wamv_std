#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

class Move:
    def __init__(self) -> None:
        self.sub_cmd_vel = rospy.Subscriber("/cmd_vel", Twist, self.propel)
        self.pub_thrust_port = rospy.Publisher("/wamv/control/thruster/port", Float64, queue_size=1)
        self.pub_thrust_starboard = rospy.Publisher("/wamv/control/thruster/starboard", Float64, queue_size=1)

    def propel(self, msg):
        lin_x = msg.linear.x
        ang_z = msg.angular.z


        self.pub_thrust_port.publish(lin_x-ang_z)
        self.pub_thrust_starboard.publish(lin_x+ang_z)

if __name__ == "__main__":
    rospy.init_node("teleop_to_thruster")
    Move()
    rospy.spin()