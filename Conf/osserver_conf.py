#!/usr/bin/env python3
import os

USER = os.getlogin()
MAIL_PATH = "/var/mail/root"
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
if SCRIPT_PATH.endswith("/Conf"):
   SCRIPT_PATH = SCRIPT_PATH[:-5]

####Osserver Option:
WWW_PATH = SCRIPT_PATH+"/Conf/www/"
WWW_JS_PATH = WWW_PATH+"js/"
WWW_IMG_PATH = WWW_PATH+"images/"
WWW_CSS_PATH = WWW_PATH+"css/"
LOG_PATH = SCRIPT_PATH+"/Logs/"
SSH_KEY = "/home/"+USER+"/.ssh/id_rsa"

#DEBUG = ["logging","get_mail","Save_DataBase","Gen_Rnd_Hash","sorting","checkhost","checkLvl","checkDate",
#          "stockvars","ssh","avatar",
#         "end_acc","accordeon","buildhtml","tojs","chartbuilder","spliter","save","update","osserver","timer",
#         "parse_mail"]
#DEBUG = ["all"]
DEBUG = ["off"]


####Get Ossec data Method:
#GET_OSSEC_DATA_FROM = "postgresql" #or "mysql" or "mail"
GET_OSSEC_DATA_FROM = "mail"
DATABASE_IP = "192.168.0.42"
DATABASE_USER = "osserver" # need to create another user than the one used by ossec with Select/Usage granted permissions
DATABASE_PASS = "osserverpass"
DATABASE_NAME = "ossecdb"
OSSEC_PATH = "/var/ossec/"
OSSEC_STATS_PATH = "/var/ossec/stats/totals/"
USE_TINY_DB = False #only if GET_OSSEC_DATA_FROM is set to "mail"
TINY_DB_FILE = SCRIPT_PATH + "/Conf/static/osserver.db"

HOSTS_NAMES = ["HOSTNAME1","HOSTNAME2","HOSTNAME3","HOSTNAME4","HOSTNAME5"]
HOSTS_IPS   = ["192.168.0.2","192.168.0.3","192.168.0.4","192.168.0.5","192.168.0.6"]
HOSTS_USERS = ["USERNAME1","USERNAME2","USERNAME3","USERNAME4","USERNAME5"]
HOSTS_IMGS =  [host_name+".png" for host_name in HOSTS_NAMES]
CAM_USER_HOST = ["HOSTNAME1","HOSTNAME2",]
CAM_CMD ="cat /home/"+CAM_USER_HOST[0]+"/Documents/checkservice/wall.tmp"
TMP_FIX = ["USERNAME1@HOSTNAME1.FQDM","X-Original-To: USERNAME1@HOSTNAME1.FQDM","USERNAME1","HOSTNAME1"]


Cherryconf = {

    "/": {
        "tools.sessions.on": True,
        "tools.staticfile.on": True,
        "tools.staticdir.root": WWW_PATH,
        "tools.staticfile.filename": WWW_PATH + "index.html",
    },
    "/images": {"tools.staticdir.on": True, "tools.staticdir.dir": WWW_IMG_PATH},
    "/css": {"tools.staticdir.on": True, "tools.staticdir.dir": WWW_CSS_PATH},
    "/js": {"tools.staticdir.on": True, "tools.staticdir.dir": WWW_JS_PATH},

    "/favicon.ico": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": WWW_IMG_PATH + "Osserver.ico",
    },

    "global": {
        "environment": "production",
        "log.screen": True,
       "log.error_file": "site.log",
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 8080,
        "engine.autoreload_on": True,
    },
}


Sep="\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
Septop="\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~top~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
Sepmid="\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~mid~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
Sepend="\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~end~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

if "off" not in DEBUG:
  print("\n\nosserver_conf:\n")
  print("Debug:",DEBUG)
  print("User:",USER)
  print("OSSEC_PATH",OSSEC_PATH)
  print("MAIL_PATH:",MAIL_PATH)
  print("Script_PAth:",SCRIPT_PATH)
  print("WWW_PATH:",str(WWW_PATH))
  print("TINY_DB_FILE:",str(TINY_DB_FILE))
  print("SSH_KEY:",str(SSH_KEY))
  print("LOG_PATH:",str(LOG_PATH))

  for name,user,ip in zip(HOSTS_NAMES,HOSTS_USERS,HOSTS_IPS):
      print("This Host:"+name+" has this User:"+user+" with this ip:"+ip)
  print("\n\n")
