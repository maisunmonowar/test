import json
import argparse
import paho.mqtt.client as mqtt 

# class command center
class CommandCenter(object):
    # constructor
    def __init__(self, config_file_name, group_id):
        # load the configuration file
        with open(config_file_name) as config_file:
            self.config = json.load(config_file) # mqtt related information
        with open("group-{}.json".format(group_id)) as group_file:
            self.gsinfo = json.load(group_file)   # dektec board related information
        # create a mqtt client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        # connect to the mqtt broker
        self.client.connect(self.config["mqtt_host"], self.config["mqtt_port"], 60)

    # mqtt on connect
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
   
    # mqtt loop
    def loop(self):
        self.client.loop_forever()

        
if __name__ == '__main__':
    # user will enter "python command --start --group 1 --config config.json"
    # Create a parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    # Add an argument. configuration file name
    parser.add_argument('--config', type=str, default='config.json', help='configuration file name')
    parser.add_argument('--start', action='store_true', help='start dektec receivers in Group ID X')
    parser.add_argument('--stop', action='store_true', help='stop dektec receivers in Group ID X')
    parser.add_argument('--group', type=int, default=1, help='Group ID')

    arguments = parser.parse_args()

    # create command center object
    cc = CommandCenter(parser.parse_args().config, parser.parse_args().group)

    # if start is true
    if parser.parse_args().start:
        # send the config file over mqtt
        cc.client.publish(cc.config["start_topic"],json.dumps(cc.gsinfo))

    # if stop is true
    if parser.parse_args().stop:
        # send the stop command over mqtt
        cc.client.publish(cc.config["stop_topic"], json.dumps(cc.gsinfo))
    
    exit(0)