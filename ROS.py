#!/usr/bin/env python3

"""
ICORE LSU MECS
DATE:  APRIL 6th, 2022
AUTHOR: MASON PESSON
"""

from numpy import rate
import rospy

'''
inclue a list of dicitonaries of publishers, subscribers, services, and clients that contains their needed information

Architecture:
    [
        # Compenent:
        {
            action --> Publisher, Subscriber, Server, Client
            channel --> topic name, service name
            dataType --> ROS data object... in the case of server and client this is the user defined srv file 
            rate --> Publish Rate
            qs --> queue_size... only for publishers
            callback --> actions function for subscriber and server
            callName --> name used for access publishers and clients after setup
        },
        {
            ...
        }
    ]

get organized access to publisher data and client calls

publisher:
 {
     {
         component['callName']: rospy.Publisher(...)
         data: component['dataType']
     },
     {
         ....
     }
 }

therefore to insert data --> ROS.publisher['callName']['data'].pose.pose.position.x = 7
and to publish data --> ROS.publisher['callName']['handle'].publish(ROS.publisher['callName']['data'])

client:
 {
     {
         component['callName'] = rospy.ServiceProxiy(...)
    
     },
     {
         ....
     }
 }

 therfor to request data --> response = ROS.client['callName'](req)
 and to get response --> response.data ... where data is defined in srv file under  ---
'''


class ROS:
    def __init__(self,nodeName,nodeArchitecture,hz):

        rospy.init_node(nodeName)

        self.publisher = {}

        self.client = {}

        self._setUpNodeArchitecture(nodeArchitecture)

        self.rate = rospy.Rate(hz)

    
    def _setUpNodeArchitecture(self,Architecture):

        for component in Architecture:

            if component['action'] == 'subscriber':

                rospy.Subscriber(component['channel'],component['dataType'],component['callback'])


            if component['action'] == 'publisher':

                self.publisher[component['callName']] = {
                    'data': component['dataType']()
                }

                if component['qs'] == None:
                    self.publisher[component['callName']]['handle'] = rospy.Publisher(component['channel'],component['dataTye'],queue_size=10)
                else:
                    self.publisher[component['callName']]['handle'] = rospy.Publisher(component['channel'],component['dataType'],queue_size=component['qs'])


            if component['action'] == 'server':
                if component['channel'] != None and component['dataType'] != None and component['callback'] != None:
                    rospy.Service(component['channel'],component['dataType'],component['callback'])
                


            if component['action'] == 'client':

                self.client[component['callName']] = rospy.ServiceProxy(component['channel'],component['dataType'])


    def ros_is_running(self):
        if not rospy.is_shutdown():
            return True
        else:
            return False

    def spin(self):
        rospy.spin()


    def sleep(self):
        self.rate.sleep()
