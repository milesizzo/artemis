import argparse
import os
import sys
import shutil
import _winreg

class DeployConfig(object):
    PATH_TO_STATIONS = "stations"

    def __init__(self, args):
        # validate station
        self.station = args.station.lower()
        stations = [d for d in os.listdir(DeployConfig.PATH_TO_STATIONS) if os.path.isdir(os.path.join(DeployConfig.PATH_TO_STATIONS, d))]
        if self.station not in stations:
            print "Unknown station: %s. Valid options: %s" % (self.station, stations)
            sys.exit(1)

        # validate helm
        if self.station == 'helm':
            drive = args.drive.lower()

            path_to_helm = os.path.join(DeployConfig.PATH_TO_STATIONS, "helm")
            drives = [d for d in os.listdir(path_to_helm) if os.path.isdir(os.path.join(path_to_helm, d))]
            if drive not in drives:
                print "Unknown ship drive: %s. Valid options: %s" % (drive, drives)
                sys.exit(1)
            self.path_to_config = os.path.join(path_to_helm, drive)
        else:
            self.path_to_config = os.path.join(DeployConfig.PATH_TO_STATIONS, self.station)

        # validate artemis path
        self.artemis_path = args.artemis
        if not os.path.isdir(self.artemis_path):
            print "Cannot find Artemis path: %s" % self.artemis_path
            sys.exit(1)
        if not os.path.isfile(os.path.join(self.artemis_path, "Artemis.exe")):
            print "Cannot find Artemis exe at path: %s" % self.artemis_path
            sys.exit(1)

        # validate music volume
        self.musicvol = self._validatePercent(args.musicvol, "Music volume")
        self.commsvol = self._validatePercent(args.commsvol, "Comms volume")

        # validate resolution
        resolution = args.resolution
        if resolution is not None:
            split = resolution.split("x")
            if len(split) != 2:
                print "Expected a resolution of the format WIDTHxHEIGHT, but you gave: %s" % resolution
                sys.exit(1)
            self.width = self._validateInt(split[0], "Resolution width")
            self.height = self._validateInt(split[1], "Resolution height")
        else:
            self.width, self.height = None, None

        # validate IP
        self.artemis_server = args.serverip

    def _validateInt(self, value, errorstr):
        try:
            result = int(value)
            return result
        except ValueError:
            print "%s: invalid value: %s" % (errorstr, value)
            sys.exit(1)

    def _validatePercent(self, value, errorstr):
        value = self._validateInt(value, errorstr)
        if value < 0 or value > 100:
            print "%s: invalid percent value: %d" % (errorstr, value)
            sys.exit(1)
        return value

    def deploy(self):
        files = ["artemis.ini", "controls.ini"]

        dst = self.artemis_path
        for filename in files:
            src = os.path.join(self.path_to_config, filename)
            print "Copying %s to %s" % (src, dst)
            shutil.copy(src, dst)

        # set the registry entries
        print "Updating registry.."
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
        key = _winreg.CreateKey(reg, r"SOFTWARE\ArtemisSBS")
        _winreg.SetValueEx(key, "IPAddress", 0, _winreg.REG_SZ, self.artemis_server)
        _winreg.SetValueEx(key, "commsObjectMasterMute", 0, _winreg.REG_SZ, "0")
        _winreg.SetValueEx(key, "commsObjectMasterVolume", 0, _winreg.REG_SZ, "%g" % (self.commsvol / 100.0))
        _winreg.SetValueEx(key, "musicObjectMasterMute", 0, _winreg.REG_SZ, "0")
        _winreg.SetValueEx(key, "musicObjectMasterVolume", 0, _winreg.REG_SZ, "%g" % (self.musicvol / 100.0))
        _winreg.SetValueEx(key, "networkTickSpeed", 0, _winreg.REG_SZ, "200")

        # update screen resolution
        if self.width is not None and self.height is not None:
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
            key = _winreg.CreateKey(reg, r"SOFTWARE\PandaEngine")
            _winreg.SetValueEx(key, "SCNH", 0, _winreg.REG_SZ, "%d" % self.width)
            _winreg.SetValueEx(key, "SCNW", 0, _winreg.REG_SZ, "%d" % self.height)
            _winreg.SetValueEx(key, "WINDOWED", 0, _winreg.REG_SZ, "0")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Deploy Artemis config files")
    parser.add_argument('--station',
        dest="station",
        metavar="STATION",
        help="the name of the station to deploy (required)",
        required=True
    )
    parser.add_argument('--drive',
        dest="drive",
        metavar="DRIVE",
        help="warp or jump drive; only relevant for --station=helm (default: %(default)s)",
        default="warp"
    )
    parser.add_argument('--artemis-dir',
        dest="artemis",
        metavar="PATH",
        help="the location of the Artemis game files (default: %(default)s)",
        default="c:\\games\\artemis"
    )
    parser.add_argument('--artemis-music-volume',
        dest="musicvol",
        metavar="PERCENT",
        help="the volume of the music at Artemis start-up (default: %(default)s)",
        default="0"
    )
    parser.add_argument('--artemis-comms-volume',
        dest="commsvol",
        metavar="PERCENT",
        help="the volume of comms at Artemis start-up (default: %(default)s)",
        default="100"
    )
    parser.add_argument('--artemis-server',
        dest="serverip",
        metavar="IP",
        help="the default server IP address (default: %(default)s)",
        default="192.168.1.21"
    )
    parser.add_argument('--resolution',
        dest="resolution",
        metavar="WxH",
        help="override the default resolution (default: no override)",
        default=None
    )
    args = parser.parse_args()

    config = DeployConfig(args)

    print "Deploying configuration for %s" % (config.station)

    config.deploy()

    print "Done."

