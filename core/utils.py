#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Aymen El Amri(eon01)"
__copyright__ = "Copyright 2014"
__credits__ = ["Aymen El Amri"]
__license__ = "GNU GENERAL PUBLIC LICENSE Version 2"
__version__ = "1.0.1"
__maintainer__ = "Aymen El Amri"
__email__ = "amri.aymen@gmail.com"
__status__ = "Beta"

import smtplib
import os

from ConfigParser import SafeConfigParser

class Utils:

    def __init__(self):
        self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       
        self.log_dir = os.path.join(self.app_dir, "logs/")
        self.conf_dir = os.path.join(self.app_dir, "conf/")
        self.general_conf_path = os.path.join(self.conf_dir, "general.conf")
        parser = SafeConfigParser()
        parser.read(self.general_conf_path)
        try:
            self.log_level = parser.get('logging', 'level')
        except Exception:
            self.log_level = "info"


    def email(self, me, you, subject, text, html, smtp_server, smtp_port, user_name, password):
        
        try:
    
            smtpserver = smtplib.SMTP(smtp_server, smtp_port)
            smtpserver.ehlo()
            smtpserver.login(user_name,password)
            header = 'To:' + you + '\n' + 'From: ' + me + '\n' + 'Subject:' + subject  + '\n'
            msg = header + '\n\n' + text + '\n\n'
            smtpserver.sendmail(username, you, msg)
            smtpserver.close()
            print 'Email sent successfully'
        except SMTPAuthenticationError:
            raise Exception('ErrorOnSMTPAuthentification')
        except smtplib.socket.gaierror:
            raise Expcetion('SMTPSocketError')
        finally:
            smtpserver.quit()

    def log(self, log_file, mtype, message):
        import logging
        log_path = os.path.join(self.log_dir, log_file)
        logger = logging.getLogger('myapp')
        
        filehdlr = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        filehdlr.setFormatter(formatter)
        logger.addHandler(filehdlr) 
        logger.setLevel(logging.INFO)
        
        #redirect logging input to standard output
        consolehdlr = logging.StreamHandler()
        consolehdlr.setFormatter(formatter)
        logger.addHandler(consolehdlr)
        level = self.log_level
        if mtype == "error" and  (level == "warning" or level == "info" or level == "error"):
            logger.error(message)
        elif mtype == "warning" and (level == "warning" or level == "info"):
            logger.warning(mesasge)
        elif mtype == "info" and level == "info":
            logger.info(message)
        else:
            pass
        
        



