#!/usr/bin/env python3
import os

USER = os.getlogin()
MAIL_PATH = "/var/mail/root"
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
WWW_PATH = SCRIPT_PATH+"/www/"
WWW_JS_PATH = SCRIPT_PATH+"/www/js/"
WWW_IMG_PATH = SCRIPT_PATH+"/www/images/"
OSSEC_PATH = "/var/ossec/"
OSSEC_STATS_PATH = "/var/ossec/stats/totals/"
SSH_KEY = "/home/"+USER+"/.ssh/id_rsa"
HOSTS_NAMES = ["Ordinateur1","Ordinateur2","Ordinateur3","Ordinateur4","Ordinateur5"]
HOSTS_IPS   = ["192.168.255.1","192.168.255.2","192.168.255.3","192.168.255.4","192.168.255.5"]
HOSTS_USERS = ["Utilisateur1","Utilisateur2","Utilisateur3","Utilisateur4","Utilisateur5"]
HOSTS_IMGS = ["ordinateur1.png","ordinateur2.png","ordinateur3.png","ordinateur4.png","ordinateur5.png"]
CAM_USER-HOST = ["Ordinateur4","Utilisateur4"]
CAM_CMD ="cat /home/"+CAM_USER-HOST[1]+"/Documents/checkservice/wall.tmp"
TMP_FIX = ["ordinateur4D@Utilisateur4.domain-name.org","X-Original-To: root@Ordinateur5.domain-name.org","Utilisateur4","Ordinateur4"]
DEBUG = 0
if DEBUG >=1:
  print("User:",USER)
  print("OSSEC_PATH",OSSEC_PATH)
  print("MAIL_PATH:",MAIL_PATH)
  print("Script_PAth:",SCRIPT_PATH)
  print("WWW_PATH:",str(WWW_PATH))
  if DEBUG >=1:
    for name,user,ip in zip(HOSTS_NAMES,HOSTS_USERS,HOSTS_IPS):
      print("This Host:"+name+" has this User:"+user+" with this ip:"+ip)
