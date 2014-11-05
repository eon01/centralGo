#!/usr/bin/env python 
# -*- coding: utf-8 -*-
__author__ = "Aymen El Amri(eon01)"
__copyright__ = "Copyright 2014"
__credits__ = ["Aymen El Amri"]
__license__ = "GNU GENERAL PUBLIC LICENSE Version 2"
__version__ = "1.0.1"
__maintainer__ = "Aymen El Amri"
__email__ = "amri.aymen@gmail.com"
__status__ = "Beta"

from threading import Thread
import threading
import time
import schedule
import os 
import sys
import re 
import functools
import subprocess
from ConfigParser import SafeConfigParser
import collections
from utils import Utils

class CentralGo:

    def __init__(self):

       self.u = Utils() 
       #Declare variable 'log' as the imported 'log' function from 'Utils'
       self.log = self.u.log
       self.log('main.log', "info", 'CGo Launched - Logging Started')
       self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
       try:
           self.conf_path = os.path.join(self.app_dir, 'conf/jobs.conf')
           self.general_conf_path = os.path.join(self.app_dir, 'conf/general.conf')
       except FileNotFoundError:
           self.log('main.log', "error", 'conf/jobs.conf and conf/general.conf not found')
           exit(1)

    def get_general_conf(self):
        parser = SafeConfigParser()
        parser.read(self.general_conf_path)
        try:
            mailing_is_active = parser.get('mailing', 'activate')
        except:
            mailing_is_active = False
            self.log('main.log', 'warning', 'Mailing in case of errors is not active')
        
        try:
            me = parser.get('mailing', 'from')
            smtp_server = parser.get('mailing', 'smtp_server')
            user_name = parser.get('mailing', 'user_name')
            password = parser.get('mailing', 'password')
        except Exception:
            self.log('main.log', 'info', 'If you want to activate mailing option, please configure general.conf')
            
        result = collections.namedtuple('conf', ['mailing_is_active', 'me', 'smtp_server', 'user_name'])
        r = result(mailing_is_active, me, smtp_server, user_name )
        return r


    def get_conf_lines(self):
        conf_lines = []
        conf_line = []               
        with open(self.conf_path, 'r') as inline:
            for line in inline:
                if line.rstrip() and not re.match("^#.*$", line):
                    conf_line = re.findall(r'(?:[^\s,"]|"(?:\\.|[^"])*")+', line)
                    conf_lines.append(conf_line)
        if len(conf_lines) == 0:
            self.log('main.log', 'info', 'Please configure jobs in conf/jobs.conf')
            exit("Check logs in %/logs/" % self.app_dir)

        return conf_lines


    def catch_exceptions(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):           
            try:
                job_func(*args, **kwargs)
            except Exception :
                from utils import Utils
                u = Utils()
                #u.log('main.log', 'error', 'One or more jobs encountred a problem, please check jobs logs')
        return wrapper

    @catch_exceptions
    def job(self, name, command, notify, email):         
        run_cmd = subprocess.Popen(command, shell=True,
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE)
        self.check_process(run_cmd, name, notify, email)

    def check_process(self, run_cmd, name, notify, email):
        for line in run_cmd.stdout:

            self.log(name + ".log", 'info', line.decode())
            #self.log("main.log", 'info', line.decode())
            run_cmd.stdout.flush()
        for line in run_cmd.stderr:

            self.log(name + ".log", 'error', line.decode())
            run_cmd.stderr.flush()
       
        mailing_is_active = self.get_general_conf().mailing_is_active
 
        if mailing_is_active and error != "" and notify is True:
            try :
                me = self.get_general_conf().me
                you = email
                subject = "Error in job : %s" % name
                text = html = error
                smtp_server =  self.get_general_conf().smtp_server
                user_name =  self.get_general_conf().user_name
                password = self.get_general_conf().password                   
                            
                self.u.email(me, you, subject, text, html, smtp_server, user_name, password)
                self.log( name + '.log', 'info', 'Email configuration parsed/ Email sent' )
            except ErrorOnSMTPAuthentification:
                self.log('main.log', 'error', "SMTP Auth Error")
                self.log(name + '.log', 'error', "Email not sent, check main.log logs")
       
    def run_threaded(self, job_func, name, command, notify, email):
        job_thread = threading.Thread(target=job_func, args=(name, command, notify, email) )
        job_thread.start()

    def main(self):
        
        notify = False
       
        for conf_line in self.get_conf_lines():
            try:
               c = conf_line
               name = c[1].rstrip("\"")[1:]
               command = c[3].rstrip("\"")[1:]
               every = c[5].rstrip("\"")[1:].strip()
               email = c[7].rstrip("\"")[1:]
               every = c[5].rstrip("\"")[1:].strip()
               email = c[7].rstrip("\"")[1:]               
            except Exception:
                log('main.log', "error", "Please check jobs.conf for configuration errors. If the file does not exist, create it.")
                sys.exit(1)

            try:    
                if re.match("\s+", email):
                    notify = True
                
                if re.match(r'^\d+\sseconds?$', every):
                    v = int(every.split()[0])
                    schedule.every(v).seconds.do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email))
                    worker_thread.start()
    
                elif re.match(r'^d+\sminutes?$', every):
                    v = int(every.split()[0])
                    schedule.every(v).minutes.do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()
    
                elif re.match(r'\s?hour\s?', every):               
                    schedule.every().hour.do(self.job, name, command, notify, email )                       
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()                                                                               
                elif re.match(r'^day\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().day.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()               
                    
                elif re.match(r'^sunday\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().sunday.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()
                                                                       
                elif re.match(r'^monday\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().monday.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()                               
                    
                elif re.match(r'^tuesday\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().tuesday.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()
                    
                elif re.match(r'^wednesday\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().wednesday.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()
                    
                elif re.match(r'^thursday\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().thursday.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()
                                
                elif re.match(r'^friday\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().friday.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()
                    
                elif re.match(r'^saturday\s+at\s+([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', every):
                    v = every.split()[2]
                    schedule.every().saturday.at(v).do(self.job, name, command, notify, email )
                    worker_thread = threading.Thread(target=self.job, args=(name, command, notify, email) )
                    worker_thread.start()
                
    
            except Exception:
                log('main.log','warning', 'One or more of jobs definition are misconfigured. Please respcet the standard format.')                
        while 1:
            schedule.run_pending()
            time.sleep(1)

#if __name__ == '__main__':
#    c = CentralGo()
#    while True:
#        c.main()
#        #print ("ok")



