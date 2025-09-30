import telnetlib
import re
import time
import sys
from config import Config


class TPW8961N(object):

    def __init__(self, host):
        self.host = host

    def __enter__(self):
        self.con = telnetlib.Telnet(self.host, 23, 5)
        self.con.read_until(b'Password: ')
        self.con.write(Config.ROUTER_PASSWORD.encode('ascii') + b'\n')
        self.con.read_until(b'TP-LINK> ')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.write(b'exit\n')
        self.con.read_all()

    def send_cmd(self, cmd):
        self.con.write((cmd.get_cmd() + '\n').encode('ascii'))
        response = self.con.read_until(b'TP-LINK> ').decode('ascii')
        return cmd.parse(response)


class Command(object):
    def __init__(self):
        pass

    def get_cmd(self):
        pass

    def parse(self, string):
        pass


class StatusCommand(Command):
    def get_cmd(self):
        return 'wan adsl status'

    def parse(self, response):
        match = re.search('current modem status: (.*?)\r\n', response)
        if match is not None and match.group(1) == 'up':
            return 'up'
        else:
            return 'down'


class RateCommand(Command):
    def get_cmd(self):
        return 'wan adsl c'

    def parse(self, response):
        dl_match = re.search('near-end interleaved channel bit rate: (.*?) kbps\r\n', response)
        ul_match = re.search('far-end interleaved channel bit rate: (.*?) kbps\r\n', response)

        if dl_match is None or ul_match is None:
            return {'dl_rate': 0, 'ul_rate': 0}

        return {'dl_rate': int(dl_match.group(1)), 'ul_rate': int(ul_match.group(1))}


class QualityCommand(Command):
    def __init__(self, direction):
        if direction not in ['downstream', 'upstream']:
            raise Exception('Unknown direction, must be "downstream" or "upstream"')
        self.direction = direction
        super().__init__()

    def get_cmd(self):
        if self.direction == 'downstream':
            return 'wan adsl l n'
        return 'wan adsl l f'

    def parse(self, response):
        noise_match = re.search('noise margin ' + self.direction + ': (.*?) db\r\n', response)
        attenuation_match = re.search('attenuation ' + self.direction + ': (.*?) db\r\n', response)

        if noise_match is None or attenuation_match is None:
            return {'noise': 0.0, 'attenuation': 0.0}

        return {'noise': float(noise_match.group(1)), 'attenuation': float(attenuation_match.group(1))}


if __name__ == '__main__':

    while True:
        try:
            print(time.strftime('%Y-%m-%d %H:%M-%S'))
            with TPW8961N(Config.ROUTER_IP) as modem:
                print(modem.send_cmd(StatusCommand()))
                print(modem.send_cmd(RateCommand()))
                print(modem.send_cmd(QualityCommand('downstream')))
                print(modem.send_cmd(QualityCommand('upstream')))
            time.sleep(Config.POLLING_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"An error occurred: {e}", file=sys.stderr)
