import configparser
import serial
import time
import argparse

class TVController:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.tvs = self.parse_tv_config()

    def parse_tv_config(self):
        tvs = {}
        for key, value in self.config['TVs'].items():
            port, baud_rate, brand, on_cmd, off_cmd = value.split(',')
            tvs[key] = {
                'port': port,
                'baud_rate': int(baud_rate),
                'brand': brand,
                'on_cmd': bytes.fromhex(on_cmd.split(':')[1].replace(' ', '')),
                'off_cmd': bytes.fromhex(off_cmd.split(':')[1].replace(' ', ''))
            }
        return tvs

    def send_command(self, tv_id, command):
        if tv_id not in self.tvs:
            print(f"TV {tv_id} not found in configuration.")
            return

        tv = self.tvs[tv_id]
        try:
            with serial.Serial(tv['port'], tv['baud_rate'], timeout=1) as ser:
                ser.write(command)
                time.sleep(0.1)  # Wait for command to be sent
                print(f"Command sent to {tv['brand']} TV on {tv['port']}")
        except serial.SerialException as e:
            print(f"Error sending command to {tv['brand']} TV on {tv['port']}: {e}")

    def turn_on_tv(self, tv_id):
        self.send_command(tv_id, self.tvs[tv_id]['on_cmd'])

    def turn_off_tv(self, tv_id):
        self.send_command(tv_id, self.tvs[tv_id]['off_cmd'])

    def turn_on_all_tvs(self):
        for tv_id in self.tvs:
            self.turn_on_tv(tv_id)

    def turn_off_all_tvs(self):
        for tv_id in self.tvs:
            self.turn_off_tv(tv_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control TVs via RS232")
    parser.add_argument("action", choices=["on", "off"], help="Turn TVs on or off")
    parser.add_argument("--tv", help="Specific TV to control (e.g., tv1, tv2)")
    args = parser.parse_args()

    controller = TVController()

    if args.tv:
        if args.action == "on":
            controller.turn_on_tv(args.tv)
        else:
            controller.turn_off_tv(args.tv)
    else:
        if args.action == "on":
            controller.turn_on_all_tvs()
        else:
            controller.turn_off_all_tvs()