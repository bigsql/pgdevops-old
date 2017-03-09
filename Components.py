####################################################################
#########         Copyright 2016-2017 BigSQL             ###########
####################################################################

import os
import subprocess
import platform

from twisted.internet.defer import inlineCallbacks, returnValue
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession

from pygtail import Pygtail
import json
import sys

PGC_HOME = os.getenv("PGC_HOME", "")
PGC_LOGS = os.getenv("PGC_LOGS", "")

try:
    with open(os.path.join(PGC_HOME,'conf','bam_config.json'),'r') as _file:
        BamConfigData = json.loads(_file.read())
except:
    BamConfigData = {}


pgc_scripts_path = os.path.join(PGC_HOME, 'hub', 'scripts')
if pgc_scripts_path not in sys.path:
  sys.path.append(pgc_scripts_path)

pgclib_scripts_path = os.path.join(PGC_HOME, 'hub', 'scripts','lib')
if pgclib_scripts_path not in sys.path:
  sys.path.append(pgclib_scripts_path)

import util

class ComponentAction(object):
    """
    This class exposes all the actions for the components in the methods defined.
    """
    def __init__(self, appsession=ApplicationSession):
        self.session = appsession
        self.process = ""

    @inlineCallbacks
    def install_comp(self, comp_name, p_yes=None):
        """
        Method to install a component.
        :param comp_name: Name of the component to be installed.
        :return: It yields json string for the install process.
        """

        command_line = PGC_HOME + os.sep + "pgc --json install " + comp_name
        if p_yes:
            command_line = command_line + " -y"
        process = subprocess.Popen(command_line, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell= True)
        self.process = process
        for line in iter(process.stdout.readline, ''):
            ln = (line).rstrip('\n')
            self.session.publish('com.bigsql.onInstall', ln)
            yield sleep(0.001)
        self.process = ''
        returnValue(1)

    def cancelInstall(self):
        """
        Method to cancel installation of a component.
        :param pid: processid of the component to be installed.
        :return: It yields process status.
        """
        if platform.system() == "Windows":
            pid_file = os.path.join(os.getenv('PGC_HOME'), 'conf', 'pgc.pid')
            if os.path.isfile(pid_file):
                os.remove(pid_file)
        else:
            import signal, psutil
            p = psutil.Process(self.process.pid)
            for proc in p.children(recursive=True):
                os.kill(proc.pid,signal.SIGINT)
            os.kill(p.pid,signal.SIGINT)
        

    @inlineCallbacks
    def remove_comp(self, comp_name):
        """
        Method to uninstall/remove a component.
        :param comp_name: Name of the component to be removed.
        :return: It yields json string for the remove process.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc --json remove " + comp_name
        process = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell=True)
        for line in iter(process.stdout.readline, ''):
            ln = (line).rstrip('\n')
            self.session.publish('com.bigsql.onRemove', ln)
            yield sleep(0.001)
        returnValue(1)

    def start(self, name):
        """
        Method to start a server component.
        :param name: Name of the component to be started.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc start " + name
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)

    def restart(self, name):
        """
        Method to restart a server component.
        :param name: Name of the component to be restared.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc restart " + name
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)

    def stop(self, name):
        """
        Method to stop a server component.
        :param name: Name of the component to be stopped.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc stop " + name
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)

    @inlineCallbacks
    def getAvailPort(self, comp, port):
        """
        Method to return server status.
        """
        if port == '':
            port = 5432
        selPort = util.get_avail_port("PG Port", port, comp)
        yield self.session.publish('com.bigsql.onPortSelect', selPort)

    @inlineCallbacks
    def serverStatus(self):
        """
        Method to return server status.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc --json status"
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell=True)
        pgcInfo = pgcProcess.communicate()
        yield self.session.publish('com.bigsql.onServerStatus', pgcInfo[0])

    @inlineCallbacks
    def init(self, name, password, dataDir, port):
        """
        Method to initialize a server component.
        :param name: Name of the component to be initialized.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc --json init " + name + " --datadir " + dataDir + " --port " + port
        if port == '':
            pgcCmd = pgcCmd.split(' --port')[0]
        if dataDir == '':
            pgcCmd = pgcCmd.split(' --datadir')[0]
        if (name > 'pg90') and (name < 'pg99'):
            pgpass_file = PGC_HOME + os.sep + name + os.sep + ".pgpass"
            if not os.path.isfile(pgpass_file):
                password_file = open(pgpass_file, 'w')
                password_file.write(password + '\n')
                password_file.close()
                os.chmod(pgpass_file, 0600)
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)
        for line in iter(pgcProcess.stdout.readline, ''):
            try:
                ln = (line).rstrip('\n')
                if type(eval(ln)) is list:
                    yield self.session.publish('com.bigsql.onInit', ln)
            except:
                pass

    @inlineCallbacks
    def update(self, name):
        """
        Method to upgrade a component from installed version to is_current version.
        :param name: Name of the component to be upgraded.
        :return: It yields json string for the upgrade process.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc --json upgrade "
        if name:
            pgcCmd = pgcCmd + name
        process = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)
        self.process = process
        for line in iter(process.stdout.readline, ''):
            ln = (line).rstrip('\n')
            self.session.publish('com.bigsql.onInstall', ln)
            yield sleep(0.001)
        self.process = ''


    @inlineCallbacks
    def updatesCheck(self):
        """
        Method to check for updates to all components
        """
        pgcCmd = PGC_HOME + os.sep + "pgc --json update"
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)   
        for line in iter(pgcProcess.stdout.readline, ''):
            ln = (line).rstrip('\n')
            self.session.publish('com.bigsql.onUpdatesCheck', ln)
            yield sleep(0.001)

    @inlineCallbacks
    def registerHost(self, hostName, pgcDir, userName, password, name):
        """
        Method to Register remote host
        """
        pgcCmd = PGC_HOME + os.sep + "pgc register --json HOST " + hostName + " '" + pgcDir + "' " + userName + " " +password + " '" + name + "'"
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)
        for line in iter(pgcProcess.stdout.readline, ''):
            ln = (line).rstrip('\n')
            if type(eval(ln)) is list:
                self.session.publish('com.bigsql.onRegisterHost', ln)
            yield sleep(0.001)  

    @inlineCallbacks
    def deleteHost(self, hostName):
        """
        Method to unregister remote host
        """
        pgcCmd = PGC_HOME + os.sep + "pgc unregister --json HOST  '" + hostName + "'"
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)   
        pgcData = pgcProcess.communicate()
        yield self.session.publish('com.bigsql.onDeleteHost', pgcData)

    @inlineCallbacks
    def registerServerGroup(self, name, hosts):
        """
        Method to register server group
        """
        pgcCmd = PGC_HOME + os.sep + "pgc register GROUP --json '" + name +"'"
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)   
        pgcData = pgcProcess.communicate()
        yield self.session.publish('com.bigsql.onRegisterServerGroup', pgcData)
        import util
        util.map_group_hosts( name, hosts, p_group_id=0, isJson=False, printMsg=False)

    def updateServerGroup(self, name, hosts, group_id):
        """
        Method to register server group
        """
        import util
        print group_id
        util.register_group( name, p_parent_group=0, p_group_id = group_id, isJson=False, printMsg=False)
        util.map_group_hosts( name, hosts, p_group_id = group_id, isJson=False, printMsg=False)

    @inlineCallbacks
    def deleteGroup(self, group):
        """
        Method to unregister remote host
        """
        pgcCmd = PGC_HOME + os.sep + "pgc unregister --json GROUP '" + group + "'"
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)   
        pgcData = pgcProcess.communicate()
        yield self.session.publish('com.bigsql.onDeleteGroup', pgcData)     

class Components(ComponentAction):
    """
    This class is abstract class for ComponentAction which exposes
    component information with the methods defined.
    """
    @inlineCallbacks
    def list(self):
        """
        Method to get the list of components available.
        :return: It yields json string for the list of components.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc --json list"
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)
        pgcInfo = pgcProcess.communicate()
        yield self.session.publish('com.bigsql.onList', pgcInfo)

    @inlineCallbacks
    def getBamConfig(self, setting):
        """
        Method to get the configuration of bam.
        Method to get test list setting of bam.
        :return: It yields json string.
        """
        yield self.session.publish('com.bigsql.onGetBamConfig', BamConfigData.get(setting))

    def setBamConfig(self, setting, option):
        """
        Method to set the configuration of bam.
        Method to set the test list setting of bam.
        :return: It yields json string.
        """
        with open(os.path.join(PGC_HOME,'conf','bam_config.json'),'w') as _file:
            json.dump({setting:option},_file)
        BamConfigData[setting] = option


    @inlineCallbacks
    def getTestSetting(self):
        """
        Method to get test list setting of bam.
        :return: It yields json string.
        """
        yield self.session.publish('com.bigsql.onGetTestSetting', util.get_value ("GLOBAL", "STAGE", ""))


    def setTestSetting(self, val):
        """
        Method to set the test list setting of bam.
        :return: It yields json string.
        """
        util.set_value("GLOBAL", "STAGE", val)

    @inlineCallbacks
    def selectedLog(self,logdir):
        """
        Method to tail the last 1000 lines from the PGC_LOGS to display default.
        :return: It yields the log lines.
        """
        if logdir == None:
            yield self.session.publish('com.bigsql.logError', "Log file does not exist")
        else:
            if logdir == 'pgcli': 
                logdir = PGC_LOGS
            self.session.publish('com.bigsql.pgcliDir',logdir)
            log_file = Pygtail(logdir)
            ln = log_file.readlines()
            read_file = open(logdir)
            _lines = read_file.readlines()[-1000:]
            for _li in _lines:
                yield self.session.publish('com.bigsql.log', _li)

    @inlineCallbacks
    def autostart(self,val,name):
        """
        Method to set the autostart configuration.
        :return: It yields the message.
        """
        pgcCmd = PGC_HOME + os.sep + "pgc --json config " + name + " --autostart=" + val
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)
        for line in iter(pgcProcess.stdout.readline, ''):
            try:
                ln = (line).rstrip('\n')
                if type(eval(ln)) is list:
                    yield self.session.publish('com.bigsql.onAutostart', ln)
            except:
                pass

    @inlineCallbacks
    def logIntLines(self,number, logdir):
        """
        Method to tail the selected number of lines from the selected log.
        :return: It yields the log lines.
        """
        if logdir == None:
            yield self.session.publish('com.bigsql.logError', "Log file does not exist")
        else:
            if logdir == 'pgcli':
                logdir = PGC_LOGS
            log_file = Pygtail(logdir)
            ln = log_file.readlines()
            read_file = open(logdir)
            _lines = read_file.readlines()[-number:]
            for _li in _lines:
                yield self.session.publish('com.bigsql.log', _li)

    @inlineCallbacks
    def liveLog(self,logdir):
        """
        Method to tail  log lines for every 5 seconds.
        :return: It yields the log lines.
        """
        if logdir == None:
            pass
        else:
            if logdir == 'pgcli':
                logdir = PGC_LOGS
            log_file = Pygtail(logdir)
            ln = log_file.readlines()
            if ln:
                for log_line in ln:
                    yield self.session.publish('com.bigsql.log', log_line)
        
    @inlineCallbacks
    def checkLogdir(self):
        import sqlite3, json
        db_local  = PGC_HOME + os.sep + "conf" + os.sep + "pgc_local.db"
        connL = sqlite3.connect(db_local)
        try:
            c = connL.cursor()
            sql = "SELECT component, logdir" + \
                  "  FROM components " + \
                  " where logdir != ''"
            c.execute(sql)
            t_comp = c.fetchall()
            connL.close()
            jsonDict = {}
            jsonList = []
            
            for comp in t_comp:
              jsonDict["component"] = str(comp[0])
              jsonList.append(jsonDict)
              jsonDict = {}

            jsonObj = json.dumps(jsonList)

        except sqlite3.Error, e:
            print str(e)
        yield self.session.publish('com.bigsql.onCheckLogdir', jsonObj)

    def isInstalled(self, comp):
        """
        Method to check if the component installed.
        :param comp: Name of the component to get the info.
        :return: It yields the json string for component info.
        """
        info_data = Components.get_info(comp)
        return info_data

    @inlineCallbacks
    def info(self):
        """
        Method to get the system info.
        :return: It yields the json string for system info.
        """
        info_data = Components.get_info()
        yield self.session.publish('com.bigsql.onInfo', info_data)

    @inlineCallbacks
    def infoComponent(self, comp):
        """
        Method to get the component information.
        :param comp: Name of the component to get the info.
        :return: It yields the json string for component info.
        """
        info_data = Components.get_info(comp)
        yield self.session.publish('com.bigsql.onInfoComponent', info_data)

    @staticmethod
    def get_info(comp=None):
        """
        Method to get the system/component information.
        :param comp: Name of the component to get the info.
        :return: It returns the json string for component info if provided else system info.
        """
        p_comp = comp
        if comp is None:
            p_comp = ""
        pgcCmd = PGC_HOME + os.sep + "pgc --json info " + p_comp
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)
        data = pgcProcess.communicate()
        return data

    @inlineCallbacks
    def checkOS(self):
        """
        Method to get the machine OS information.
        :return: It yields the platform.
        """
        yield self.session.publish('com.bigsql.onCheckOS', platform.system())

    @staticmethod
    def get_data(command, component=None, pgc_host=None, pwfile=None, relnotes=None):
        """
        Method to get the host settings.
        :param p_host: Name of the host to retrieve the settings.
        :return: It returns dict of settings.
        """

        pgcCmd = PGC_HOME + os.sep + "pgc --json " + command
        if relnotes:
            pgcCmd = pgcCmd + " --relnotes"
        if component:
            pgcCmd = pgcCmd + " " + component 
        if pgc_host:
            if pwfile:
                pgcCmd = pgcCmd + " --pwfile " + pwfile + " --host " + pgc_host
            else:
                pgcCmd = pgcCmd + " --host " + pgc_host
        pgcProcess = subprocess.Popen(pgcCmd, stdout=subprocess.PIPE, shell = True)
        pgcInfo = pgcProcess.communicate()       
        return json.loads(pgcInfo[0])