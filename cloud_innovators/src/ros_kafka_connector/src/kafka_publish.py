#!/usr/bin/env python3

# kafka_publish.py
import rospy
from kafka import KafkaProducer
from std_msgs.msg import String
import json

class kafka_publish():

    def __init__(self):
        # initialize node
        rospy.init_node("kafka_publish")
        rospy.on_shutdown(self.shutdown)

        # Retrieve parameters from launch file
        bootstrap_server = rospy.get_param("~bootstrap_server", "localhost:9092")
        self.ros_topic = rospy.get_param("~ros_topic", "/processed/merged")  # 병합된 데이터를 구독할 토픽
        self.kafka_topic = rospy.get_param("~kafka_topic", "merged_topic")
        
        # Create kafka producer
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_server, value_serializer=lambda m: json.dumps(m).encode('utf-8'))

        # Subscribe to the topic with the chosen imported message type
        rospy.Subscriber(self.ros_topic, String, self.callback)
       
        rospy.logwarn("Using ROS Topic: {} -> KAFKA Topic: {}".format(self.ros_topic, self.kafka_topic))

    def callback(self, msg):
        # Output msg to ROS and send to Kafka server
        rospy.logwarn("MSG Received: {}".format(msg.data)) 
        # Kafka에 병합된 데이터를 전송
        self.producer.send(self.kafka_topic, json.loads(msg.data))  # 이미 JSON으로 변환된 데이터이므로 다시 변환하지 않음
        rospy.loginfo("Merged Data Sent to Kafka")

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            rate.sleep()            

    def shutdown(self):
        rospy.loginfo("Shutting down")

if __name__ == "__main__":
    try:
        node = kafka_publish()
        node.run()
    except rospy.ROSInterruptException:
        pass

    rospy.loginfo("Exiting")
