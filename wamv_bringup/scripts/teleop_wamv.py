#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class Move:
    def __init__(self) -> None:
        self.sub_cmd_joy = rospy.Subscriber("/joy/wamv",Joy, self.joy_to_cmd_vel)
        self.pub_joy_cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
        self.sub_cmd_vel = rospy.Subscriber("/cmd_vel", Twist, self.propel)
        
        self.pub_thrust_port = rospy.Publisher("/wamv/control/thruster/port", Float64, queue_size=1)
        self.pub_thrust_starboard = rospy.Publisher("/wamv/control/thruster/starboard", Float64, queue_size=1)
                
        # self.pub_surge = rospy.Publisher("/alpha_rise/control/thruster/surge", Float64, queue_size=1)
        # self.sway = rospy.Publisher("/alpha_rise/control/thruster/sway_bow", Float64, queue_size=1)
        # self.hbow = rospy.Publisher("/alpha_rise/control/thruster/heave_bow", Float64, queue_size=1)
        # self.sternb = rospy.Publisher("/alpha_rise/control/thruster/heave_stern", Float64, queue_size=1)

    def joy_to_cmd_vel(self, msg):
        t = Twist()
        lin_x = msg.axes[1]
        ang_z = msg.axes[2]
        depth = msg.axes[3]
        t.linear.x = lin_x * 10
        t.angular.z = ang_z * 10
        t.linear.z = depth
        self.pub_joy_cmd_vel.publish(t)

    def propel(self, msg):
        lin_x = msg.linear.x
        ang_z = msg.angular.z
        depth = msg.linear.z

        # self.pub_surge.publish(lin_x)
        # self.sway.publish(ang_z)
        # self.hbow.publish(depth)
        # self.sternb.publish(depth)


        self.pub_thrust_port.publish(lin_x-ang_z)
        self.pub_thrust_starboard.publish(lin_x+ang_z)

if __name__ == "__main__":
    rospy.init_node("teleop_to_thruster_wamv")
    Move()
    rospy.spin()