import paho.mqtt.client as mqtt
import json
import time
import argparse

class edge_server_controller(object):
    #constructor
    def __init__(self, config_file_name, edger_server_config_file):
        # load the configuration file
        with open(config_file_name) as config_file:
            self.config = json.load(config_file)
        with open(edger_server_config_file) as edge_server_file:
            self.edge_server_info = json.load(edge_server_file)
        # create a mqtt client
        self.client = mqtt.Client()
        # connect to the mqtt broker
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.config["mqtt_host"], self.config["mqtt_port"], 60)
        time.sleep(1)
        # subscribe to the topic
        self.client.subscribe(self.config["start_topic"])
        self.client.subscribe(self.config["stop_topic"])
        

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
    
    #  on message
    def on_message(self, client, userdata, msg):
        # print(msg.topic+" "+str(msg.payload))
        data = json.loads(msg.payload)
        if msg.topic == self.config["start_topic"]:
            # check if the group id is the same
            if data["group_name"] == self.edge_server_info["group_name"]:
                # start the dektec receivers
                print("Starting Dektec Receivers for: ", end="")
                for ii in data["msg"]:
                    print(ii["ch"], end=", ")
                print("")
                # dektec software related code goes here #
        # if the topic is stop
        if msg.topic == self.config["stop_topic"]:
            # check if the group id is the same
            if data["group_name"] == self.edge_server_info["group_name"]:
                # stop the dektec receivers
                print("Stopping Dektec Receivers for: ", end="")
                for ii in data["msg"]:
                    print(ii["ch"], end=", ")
                print("")
                # dektec software related code goes here #

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    # configuration file. mainly mqtt broker information. 
    parser.add_argument('--config', type=str, default='config.json', help='configuration file name')
    # server configuration file. mainly server related information. 
    parser.add_argument('--server', type=str, default='edge_server.json', help='edge server configuration file')

    arguments = parser.parse_args()

    cc = edge_server_controller(parser.parse_args().config, parser.parse_args().server)

    try:
        cc.client.loop_forever()
    except KeyboardInterrupt:
        print("Exiting")
        exit(0)