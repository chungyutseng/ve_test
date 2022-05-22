#!/usr/bin/env python3
import rospy
from std_msgs.msg import Empty as EmptyMsg
from geometry_msgs.msg import Twist
import time
from std_msgs.msg import Int8

pre_time = 0

pub_takeoff = rospy.Publisher('/drone2/tello/takeoff', EmptyMsg, queue_size=1)
pub_land = rospy.Publisher('/drone2/tello/land', EmptyMsg, queue_size=1)
pub_vel_cmd = rospy.Publisher('/drone2/tello/cmd_vel', Twist, queue_size=1)

command = 0

def pub_cmd(data):
    global pre_time, command
    global pub_vel_cmd, pub_takeoff, pub_land
    pre_time = time.time() * 1000  #in milisecond
    command = data.data

def cmd():
    global pre_time, command
    global pub_vel_cmd
    rospy.init_node('cmd_F', anonymous=True)
    rospy.Subscriber("keyboard_cmd", Int8, callback=pub_cmd)
    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():
        now_time = time.time() * 1000
        if (now_time - pre_time) > 100:
            vel_msg = Twist()
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0  
            vel_msg.angular.z = 0
            pub_vel_cmd.publish(vel_msg)
        else:
            vel_msg = Twist()
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0  
            vel_msg.angular.z = 0
            velocity = 0.5
            if command == 116:
                pub_takeoff.publish()
            elif command == 108:
                pub_land.publish()
            elif command == 117: #u forward 
                vel_msg.linear.y = velocity
                pub_vel_cmd.publish(vel_msg)        
            elif command == 106: #j
                vel_msg.linear.y = -velocity
                pub_vel_cmd.publish(vel_msg)        
            elif command == 104: #h
                vel_msg.linear.x = -velocity
                pub_vel_cmd.publish(vel_msg)
            elif command == 107: #k
                vel_msg.linear.x = velocity
                pub_vel_cmd.publish(vel_msg)
            elif command == 121: #y rotate left, viewed from the top
                vel_msg.angular.z = -velocity
                pub_vel_cmd.publish(vel_msg)
            elif command == 105: #i rotate right, viewed from the top
                vel_msg.angular.z = velocity
                pub_vel_cmd.publish(vel_msg)
            elif command == 109: #m
                vel_msg.linear.z = velocity
                pub_vel_cmd.publish(vel_msg)
            elif command == 110: #n
                vel_msg.linear.z = -velocity
                pub_vel_cmd.publish(vel_msg)

            # print("QQQ\n")

        rate.sleep()

if __name__ == '__main__':
    try:
        cmd()
    except rospy.ROSInterruptException:
        pass