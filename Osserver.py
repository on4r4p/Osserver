#!/usr/bin/env python3
import email, sys, time, re, os, subprocess, socket, inspect, cherrypy
import dateutil.parser as dparser
from threading import Thread
from datetime import datetime, timedelta
from pathlib import Path
from email.policy import default
from email.parser import BytesParser, Parser
from Conf.static.html import *
from Conf.static.gauge import *
from Conf.static.ossechart import *
from Conf.osserver_conf import *

FirstLoad = True
ServerReady = True
Done = False
To_Split = False
Split_End = False
Page_Number = 0
Global_Rule_List = []
Global_Lvl_List = []
GarageCam = ""
GardenCam = ""
LivingCam = ""
Time_Track = {"Gauge": [None, None], "Cam": [None, None], "Chart": [None, None]}
Host_Alerts = {}
Hosts = []
Levels = []
Subjects = []
Dates = []
Messages = []
tput = subprocess.Popen(["tput", "cols"], stdout=subprocess.PIPE)
CharPos = 1
loading_txt = ""
GoBack = False
MAXCHAR = int(tput.communicate()[0].strip()) - 1


def Logging(Err_to_log, CurrentDate):
    Err_to_log = "\n------\n".join(Err_to_log)
    if os.path.isfile("Error.log") is False:
        open("Error.log", "w")
    try:
        with open("Error.log", "a") as fuck:
            fuck.write("\n==========================\n" + str(CurrentDate))
            fuck.write("\n" + Err_to_log)
            fuck.write("\n==========================\n")
    except Exception as e:
        if os.path.isfile("Error.Safe.log") is False:
            open("Error.Safe.log", "w")
        with open("Error.Safe.log") as fuck:
            fuck.write("\n" + str(CurrentDate))
            fuck.write("\n" + str(e))


def DebugMode(info_msg, stack, *variables):

    if "off" in DEBUG:
        return ()

    try:call_function=stack[0][3]
    except:return

    if call_function.lower() in DEBUG or "all" in DEBUG:
        Err_to_log = []
        CurrentDate = datetime.now()
        var_names = []
        var_values = []


        for var23332 in variables:
            try:
                for fi in reversed(inspect.stack()):
                    names = [
                        var_name
                        for var_name, var_val in fi.frame.f_locals.items()
                        if var_val is var23332
                    ]
                    if len(names) > 0:
                        if names[0] != "var23332":
                            var_values.append(var23332)
                            var_names.append(names[0])

            except Exception as e:
                Err_to_log.append("Error while enumerating vars in DebugMode :", e)

        for n, v in zip(var_names, var_values):
            Err_to_log.append("%s = %s" % (n, v))



        try:
            Stack_lst =["And said this: "+str(info_msg)]
            for n,stk in enumerate(stack):
               Dbmsg = ""
               Stack_lst.append("\n")
               if "filename" in dir(stk):
                   if len(stack) > 0:
                      if n == 0:
                         Dbmsg += "Finally "+str(stk.filename)
                      elif n == len(stack)-1:
                         Dbmsg += str(stk.filename)
                      else:
                         Dbmsg += "Then "+str(stk.filename)
                   else:
                         Dbmsg += str(stk.filename)

               if "function" in dir(stk):
                   Dbmsg += " function: "+str(stk.function)
               if "lineno" in dir(stk):
                   Dbmsg += " at line number: "+str(stk.lineno)
               if "code_context" in dir(stk):
                   Dbmsg += "\ncalled:%s\n"%str(stk.code_context)
               Stack_lst.append(Dbmsg)
            Stack_lst.append("\nStack:\n\n")
            Stack_lst.reverse()
            Err_to_log.append("".join(Stack_lst))
        except Exception as e:
            Err_to_log.append(
                "!!\nFile:Osserver.py has encounter an error in DebugMode() \nError Message:%s\nInitial Debug Message was:%s\n!!"
                % (e,info_msg)
            )
        Err_to_log.reverse()
        return Logging(Err_to_log, CurrentDate)


def Loading():
    global CharPos
    global GoBack
    global loading_txt
    point = "."
    space = " "
    while ServerReady is True:
        lnt = len(loading_txt)
        if lnt < MAXCHAR and GoBack is False:
            loading_txt = (point * CharPos) + space
            CharPos = CharPos + 1
            print(loading_txt, end="\r")
            lnt = len(loading_txt)
            time.sleep(0.01)
        else:
            if lnt > 2:
                GoBack = True
                loading_txt = (point * CharPos) + space
                CharPos = CharPos - 1
                print(loading_txt, end="\r")
                lnt = len(loading_txt)
                time.sleep(0.01)
            else:
                GoBack = False

def Mbr(mbx):
    global Done
    global FirstLoad
    global ServerReady

    lock = False
    lines = []
    while True:
        try:
            line = mbx.readline()
            if line.startswith(b"From "):
                 istk=inspect.stack();DebugMode("line.startswith(b'From ')", istk, line)

            if line == b"" or line.startswith(b"From "):
                istk=inspect.stack();DebugMode("inside conditional", istk)

                if line == b"":
                    for l in lines:
                        if l.startswith(b"From "):
                            istk=inspect.stack();DebugMode(
                                "Line is empty but full mail obj found in Lines[] so going to yield",
                                istk,
                                len(lines),
                            )
                            yield email.message_from_bytes(b"".join(lines), policy=default)

                            istk=inspect.stack();DebugMode("Setting Lines[] to empty", istk)
                            lines = []
                            # break
                    if Done is False:
                        if ServerReady is False:
                            print("Waiting...")
                        if FirstLoad is True:
                            Update()
                            FirstLoad = False
                        istk=inspect.stack();DebugMode("From not in lines:", istk, lines)
                        Done = True
                        time.sleep(5)
                    else:
                        istk=inspect.stack();DebugMode("Done=", istk, Done)
                        #                       Done = False
                        time.sleep(5)

                if line.startswith(b"From "):
                    istk=inspect.stack();DebugMode(
                        "Inside conditional from/befor Yield",
                        istk,
                        len(lines),
                    )
                    if len(lines) > 1:
                        yield email.message_from_bytes(b"".join(lines), policy=default)

                if b"From " in line:
                    lines = []
                    lines.append(line)
                    lock = True
                    istk=inspect.stack();DebugMode(
                        "Lines[] is now empty Append line in lines[]",
                        istk,
                        lock,
                    )
                else:
                    istk=inspect.stack();DebugMode(
                        "No From in line so Lines[] is now empty", istk
                    )
                    line = []

            if lock is False:

                if len(line) > 1 or line is b"\n":
                    istk=inspect.stack();DebugMode("Line goes to Lines[]", istk, line is b"\n")
                    Done = False
                    lines.append(line)
                else:
                    istk=inspect.stack();DebugMode(
                        "line is not long enough to append to Lines[]",
                        istk,
                        line,
                    )
            else:
                istk=inspect.stack();DebugMode(
                    "Lock prevent appending line in lines[] now Lock is back to false",
                    istk,
                )
                lock = False

        except Exception as e:
            istk=inspect.stack();DebugMode(str(e), istk)

def Sorting(mode, arg):
    Hosts_Sort = []
    Levels_Sort = []
    Dates_Sort = []
    Messages_Sort = []
    Subjects_Sort = []

    if mode is "by_name":

        istk=inspect.stack();DebugMode("by name:", istk, mode, arg)

        for name, lvl, dat, body, title in zip(
            Hosts, Levels, Dates, Messages, Subjects
        ):

            if name.lower() == arg.lower():
                Hosts_Sort.append(name)
                Levels_Sort.append(lvl)
                Dates_Sort.append(dat)
                Messages_Sort.append(body)
                Subjects_Sort.append(title)

                lnhostsort = len(Hosts_Sort)
                lnlvlsort = len(Levels_Sort)
                lndatsort = len(Dates_Sort)
                lnmesssort = len(Messages_Sort)
                lnsubjsort = len(Subjects_Sort)
                istk=inspect.stack();DebugMode(
                    "in name lower:",
                    istk,
                    name,
                    lvl,
                    dat,
                    body,
                    title,
                    lnhostsort,
                    lnlvlsort,
                    lndatsort,
                    lnmesssort,
                    lnsubjsort,
                )

            else:
                istk=inspect.stack();DebugMode(
                    "else name lower:",
                    istk,
                    name,
                    lvl,
                    dat,
                    body,
                    title,
                    arg,
                )

    if mode is "by_lvl":
        istk=inspect.stack();DebugMode("by lvl:", istk, mode)

        for name, lvl, dat, body, title in zip(
            Hosts, Levels, Dates, Messages, Subjects
        ):
            if lvl == arg:
                Hosts_Sort.append(name)
                Levels_Sort.append(lvl)
                Dates_Sort.append(dat)
                Messages_Sort.append(body)
                Subjects_Sort.append(title)
                istk=inspect.stack();DebugMode(
                    "lvl==arg", istk, name, lvl, dat, body, title, arg
                )

    if mode is "by_rule":
        istk=inspect.stack();DebugMode("by rule:", istk, mode, arg)

        for name, lvl, dat, body, title in zip(
            Hosts, Levels, Dates, Messages, Subjects
        ):
            rule = ""
            for line in body.splitlines():
                if "Rule: " in line:
                    istk=inspect.stack();DebugMode("Found Rule id in line:", istk, line)
                    try:
                        rule = int(line.split("Rule: ")[1].split(" fired")[0])
                        break
                    except Exception as e:
                        istk=inspect.stack();DebugMode(str(e), istk, line)

            if str(rule) == str(arg):
                istk=inspect.stack();DebugMode(
                    "rule==arg",
                    istk,
                    "Rule = arg ? %s" % (str(rule) == str(arg)),
                    rule,
                    arg,
                )
                Hosts_Sort.append(name)
                Levels_Sort.append(lvl)
                Dates_Sort.append(dat)
                Messages_Sort.append(body)
                Subjects_Sort.append(title)
                istk=inspect.stack();DebugMode(
                    "aftersort",
                    istk,
                    name,
                    lvl,
                    dat,
                    body,
                    title,
                    rule,
                )
            else:
                istk=inspect.stack();DebugMode(
                    "rule!=arg",
                    istk,
                    "Else:Rule = arg ? %s" % (str(rule) == str(arg)),
                    rule,
                    arg,
                )

    Hosts_Sort.reverse()
    Levels_Sort.reverse()
    Dates_Sort.reverse()
    Messages_Sort.reverse()
    Subjects_Sort.reverse()

    return (Hosts_Sort, Levels_Sort, Dates_Sort, Messages_Sort, Subjects_Sort)


def CheckHostName(Sender, Dest, Sub, Mess):

    hostname = ""

    for hst in HOSTS_NAMES:
        if hst.lower() in Sub.lower():
            hostname = hst.capitalize()
            istk=inspect.stack();DebugMode(
                "Search Sub", istk, "Found something", hst, hostname
            )
            return hostname

    for hst in HOSTS_NAMES:
        if hst.lower() in Sender.lower():
            hostname = hst.capitalize()
            istk=inspect.stack();DebugMode(
                "Search Sender", istk, "Found something", hst, hostname
            )
            return hostname
    hostname = "Unknown"
    istk=inspect.stack();DebugMode(
        "Hostname not found",
        istk,
        Sub,
        Done,
        Sender,
        Dest,
        Mess,
        hostname,
    )

    return hostname


def CheckLvl(Sender, Dest, Sub, Mess):

    if "checkservice.py" in Sub:
        for line in Mess.splitlines():
            lvl = 0
            if "Summary Lvl" in line:
                try:
                    lvl = line.split("Summary Lvl ")[1].split(" at")[0].replace(" ", "")
                    return lvl
                except Exception as e:
                    DebugMode = (
                        "Checkservice.py lvl error:%s" % e,
                        istk,
                    )
                    lvl = "??"
                    return lvl

    lvl = ""

    try:

        for line in Mess.splitlines():
            if "Danger level: [" in line:
                lvl = line.split("[")[1].split("]")[0]
                return lvl
    except Exception as e:
        lvl = "??"
        istk=inspect.stack();DebugMode(
            str(e), istk, "Error:%s" % e, Sub, Sender, Dest, lvl, Mess
        )

    if "Checkping" in Sub:
        lvl = 2
        return lvl
    elif "unlimited timeout" in Sub:
        lvl = 5
        return lvl
    elif "lightlogtable.sh" in Sub:
        lvl = 4
    elif "Checkgate" in Sub:
        lvl = 5
    elif "Could not reduce disk utilization" in Sub:
        lvl = 5
    elif "Exceeded max disk utilization" in Sub:
        lvl = 6
    elif "Stopping psad" in Sub:
        lvl = 7
    elif "SECURITY information" in Sub:
        lvl = 8
    elif "Journal Rooter" in Sub:
        lvl = 9
    elif "Firewall Rooter" in Sub:
        lvl = 10

    else:
        lvl = "??"
        istk=inspect.stack();DebugMode(
            "Error: lvl is ??", istk, Sub, Sender, Dest, lvl, Mess
        )
    return lvl


def CheckDate(Sender, Dest, Sub, Mess):
    dat = ""
    datDEBUG = ""

    if "checkservice.py" in Sub:
        for line in Mess.splitlines():
            dat = ""
            if "====Checkservice.py Summary Lvl" in line:
                line = line.replace("=", "")
                line = line.strip("\n")
                try:
                    line = line.split("at ")[1]
                    dat = dparser.parse(str(line), fuzzy=True)
                    return dat
                except Exception as e:
                    datDEBUG += "\nCheckservice:Exception Line :" + str(line)
                    datDEBUG += "\nCheckservice:Len Line :" + str(len(str(line)))
                    datDEBUG += "\nCheckservice:Len Dat :" + str(len(str(dat)))
                    istk=inspect.stack();DebugMode(
                        "line = line.split('at ')[1]", istk, datDEBUG
                    )
                    return dat
            else:
                datDEBUG += "\nCheckservice:Exception Line :" + str(line)
                datDEBUG += "\nCheckservice:Len Line :" + str(len(str(line)))
                datDEBUG += "\nCheckservice:Len Dat :" + str(len(str(dat)))
                istk=inspect.stack();DebugMode(
                    "else  '====Checkservice.py Summary Lvl' in line:",
                    istk,
                    datDEBUG,
                )
                return dat
                pass

    for line in Mess.splitlines():
        dat = ""
        if len(str(line)) > 0:
            line = line.replace("--", "")
            line = line.replace("=-=-=-=-=-=-=-=-=-=-=-= ", "")
            line = line.replace(" =-=-=-=-=-=-=-=-=-=-=-=", "")
            line = line.strip("\n")
            try:
                dat = dparser.parse(str(line), fuzzy=True)
                return dat
            except Exception as e:
                datDEBUG += "\nException Line :" + str(line)
                datDEBUG += "\nLen Line :" + str(len(str(line)))
                datDEBUG += "\nLen Dat :" + str(len(str(dat)))
                istk=inspect.stack();DebugMode(
                    "dat = dparser.parse(str(line),fuzzy=True)",
                    istk,
                    datDEBUG,
                )

    if len(str(dat)) <= 0:
        istk=inspect.stack();DebugMode("DatDebug", istk, datDEBUG)

        dat = str(datetime.now().strftime("%Y %m %d %H:%M:%S"))
        return dat


def Stockvars(Sender, Dest, Sub, Mess):
    global Hosts
    global Levels
    global Dates
    global Subjects
    global Messages

    global Host_Alerts

    switch = False

    hostname = ""
    lvl = ""
    dat = ""
    now = datetime.now()

    try:
        hostname = re.search(r"\((.*?)\)", Sub).group(1).replace(" ", "")
    except Exception as e:
        istk=inspect.stack();DebugMode(str(e), istk, Sub)
        hostname = "Unknown"

    if hostname.lower() not in HOSTS_NAMES:
        hostname = CheckHostName(Sender, Dest, Sub, Mess)
        Hosts.append(hostname)
    else:
        Hosts.append(hostname)

    if hostname in Host_Alerts:
        Host_Alerts[hostname] = int(Host_Alerts.get(hostname)) + 1
    else:
        Host_Alerts[hostname] = 1

    try:
        lvl = re.search(r"Level (.*?)-", Sub).group(1).replace(" ", "")
        int(lvl)
    except Exception as e:
        istk=inspect.stack();DebugMode(str(e), istk, Sub)
        lvl = CheckLvl(Sender, Dest, Sub, Mess)

    Levels.append(lvl)

    dat = CheckDate(Sender, Dest, Sub, Mess)
    Dates.append(dat)

    body = ""
    for line in Mess.splitlines():
        line = line.replace("\n", "<br>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        if "<![CDATA[PntLog(" in line:
            newline = []
            line = line.split(";]]>")
            for l in line:
                try:
                    epoch = l.split("<![CDATA[PntLog(")[1].split(",")[0]
                    temps = datetime.fromtimestamp(int(epoch)).strftime("%c")
                    remove = "<![CDATA[PntLog(" + str(epoch)
                    l = l.replace(remove, str(temps))
                    newline.append(l)
                except Exception as e:
                    istk=inspect.stack();DebugMode(str(e), istk, Mess)
            line = "<br>".join(newline)
        body += str(line) + "<br>"
    if len(str(body)) > 4:
        Messages.append(str(body))
    else:
        istk=inspect.stack();DebugMode(
            "Body len <= 4 Osserver Error:Message Content is missing.",
            istk,
            Done,
            Sub,
            Sender,
            Dest,
            lvl,
            Mess,
            hostname,
        )
        Messages.append("Osserver Error:Message Content is missing.")

    if len(str(Sub)) > 0:
        Subjects.append(Sub)
    else:
        istk=inspect.stack();DebugMode("Len Subj <= 0", istk, Sub)
        Subjects.append("Osserver Error:Subject Content is missing.")


def ssh(usr, host, cmd):

    try:
        out = subprocess.check_output(
            ["ssh", "-i", SSH_KEY, "{}@{}".format(usr, host), cmd]
        )
        return out.decode("utf8")
    except Exception as e:
        istk=inspect.stack();DebugMode(str(e), istk, usr, host, cmd)


def Avatar_Accordeon(hname):

    hname = hname.lower().replace(" ", "")
    for name, img in zip(HOSTS_NAMES, HOSTS_IMGS):
        info = "Is %s == %s : %s  Type hname %s Type hn %s" % (
            hname,
            name.lower(),
            hname == name.lower(),
            type(hname),
            type(name),
        )
        istk=inspect.stack();DebugMode("Avatar_Accordeon", istk, info)
        if name.lower() == hname.lower():
            # print("GOOD %s == %s = %s"%(name.lower(),hname.lower(),hname==name.lower()))
            return (
                '<img class="avatar" src="images/'
                + img
                + '" alt="'
                + name
                + '" style="width: 14px; height: 14px;">'
            )
    return "??"


def End_Item_Accordeon_To_Split(Current_Item, Total_Items, Current_Page, Page_Name):

    if Split_End is True or Current_Item == Total_Items:
        info = "Current_Item == Total_Item ", Current_Item == Total_Item
        istk=inspect.stack();DebugMode(
            "Split_End is True or Current_Item == Total_Items:",
            istk,
            info,
            Split_End,
            Current_Item,
            Total_Item,
            Current_Page,
            Page_Name,
        )

        if Current_Item == Total_Items and Current_Page == 0:
            Accordeon_End_Item = """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false"> Results : %s/%s End of Results. </div>
                \n</div>""" % (
                Current_Item,
                Current_Item,
                Total_Items,
            )
            return Accordeon_End_Item

        if Current_Page == 1:
            Previous_Page = str(Page_Name) + ".html"

            Accordeon_End_Item = """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false"> Results : %s/%s <a href="%s">&lt;-Previous Results  </a> </div>
                \n</div>""" % (
                Current_Item,
                Current_Item,
                Total_Items,
                Previous_Page,
            )
            return Accordeon_End_Item

        elif Current_Page > 1:

            Previous_Page = str(Page_Name) + "_" + str(Current_Page - 1) + ".html"

            Accordeon_End_Item = """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false"> Results : %s/%s <a href="%s">&lt;-Previous Results  </a> </div>
                \n</div>""" % (
                Current_Item,
                Current_Item,
                Total_Items,
                Previous_Page,
            )
            return Accordeon_End_Item

    if Current_Page == 0:
        Next_Page = str(Page_Name) + "_" + str(Current_Page + 1) + ".html"

        Accordeon_End_Item = """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false"> Results : %s/%s <a href="%s">  Next Results-&gt;</a> </div>
                \n</div>""" % (
            Current_Item,
            Current_Item,
            Total_Items,
            Next_Page,
        )
        return Accordeon_End_Item

    elif Current_Page == 1:

        Previous_Page = str(Page_Name) + ".html"
        Next_Page = str(Page_Name) + "_" + str(Current_Page + 1) + ".html"

        Accordeon_End_Item = """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false"> Results : %s/%s <a href="%s">&lt;-Previous Results  </a> <a href="%s">  Next Results-&gt;</a> </div>
                \n</div>""" % (
            Current_Item,
            Current_Item,
            Total_Items,
            Previous_Page,
            Next_Page,
        )
        return Accordeon_End_Item

    else:
        Previous_Page = str(Page_Name) + "_" + str(Current_Page - 1) + ".html"
        Next_Page = str(Page_Name) + "_" + str(Current_Page + 1) + ".html"

        Accordeon_End_Item = """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false"> Results : %s/%s <a href="%s">&lt;-Previous Results  </a> <a href="%s">  Next Results-&gt;</a> </div>
                \n</div>""" % (
            Current_Item,
            Current_Item,
            Total_Items,
            Previous_Page,
            Next_Page,
        )

        return Accordeon_End_Item


def Accordeon(sort=None, arg=None):
    global To_Split
    global Page_Number
    global Split_End
    global Last_Position
    global Last_Hosts_Sort
    global Last_Levels_Sort
    global Last_Dates_Sort
    global Last_Messages_Sort
    global Last_Subjects_Sort

    Accordeon_Html = ""
    Switch = False

    if Split_End is True:
        Page_Number = 0
        To_Split = False
        Split_End = False
        (
            Last_Position,
            Last_Hosts_Sort,
            Last_Levels_Sort,
            Last_Dates_Sort,
            Last_Messages_Sort,
            Last_Subjects_Sort,
        ) = ("", [], [], [], [], [])

    if Page_Number > 0:
        Max_Items = 499 * (Page_Number + 1)

        if Page_Number == 1:
            Previous_Page = arg

        elif Page_Number > 1:
            Previous_Page = arg + "_" + str(Page_Number - 1)

    else:
        Max_Items = 499

    if To_Split is False:
        if sort == "no_sort":
            Hosts_Sort = Hosts
            Levels_Sort = Levels
            Dates_Sort = Dates
            Messages_Sort = Messages
            Subjects_Sort = Subjects
            Hosts_Sort.reverse()
            Levels_Sort.reverse()
            Dates_Sort.reverse()
            Messages_Sort.reverse()
            Subjects_Sort.reverse()

        else:
            Hosts_Sort, Levels_Sort, Dates_Sort, Messages_Sort, Subjects_Sort = Sorting(
                sort, arg
            )
            info = "Back to Buildhtml()"
            lnhostsort = len(Hosts_Sort)
            lnlvlsort = len(Levels_Sort)
            lndatsort = len(Dates_Sort)
            lnmesssort = len(Messages_Sort)
            lnsubjsort = len(Subjects_Sort)
            istk=inspect.stack();DebugMode(
                "if sort == no_sort:",
                istk,
                info,
                To_Split,
                lnhostsort,
                lnlvlsort,
                lndatsort,
                lnmesssort,
                lnsubjsort,
            )

    else:  # To_Split is True:
        Hosts_Sort = Last_Hosts_Sort
        Levels_Sort = Last_Levels_Sort
        Dates_Sort = Last_Dates_Sort
        Messages_Sort = Last_Messages_Sort
        Subjects_Sort = Last_Subjects_Sort
        info = "Buildhtml()"
        lnhostsort = len(Hosts_Sort)
        lnlvlsort = len(Levels_Sort)
        lndatsort = len(Dates_Sort)
        lnmesssort = len(Messages_Sort)
        lnsubjsort = len(Subjects_Sort)
        istk=inspect.stack();DebugMode(
            "if To_Split is False:",
            istk,
            info,
            To_Split,
            lnhostsort,
            lnlvlsort,
            lndatsort,
            lnmesssort,
            lnsubjsort,
        )

    i = 1
    for name, lvl, dat, body, title in zip(
        Hosts_Sort, Levels_Sort, Dates_Sort, Messages_Sort, Subjects_Sort
    ):
        if To_Split is True:
            if i == Last_Position or Switch is True:

                info = "i == Last_Position", i == Last_Position
                istk=inspect.stack();DebugMode(
                    "for name,lvl,dat,body,title in zip(Hosts_Sort,Levels_Sort,Dates_Sort,Messages_Sort,Subjects_Sort):",
                    istk,
                    info,
                    Switch,
                )

                Switch = True
                To_Split = False
                geticon = Avatar_Accordeon(name)
                Accordeon_Html += """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false">%s %s From %s Lvl %s :<br>%s</a> </div>
                <div id="collapse%s" class="accordion-body collapse" aria-expanded="false" style="height: 0px;">
                  <div class="accordion-inner">%s</div>
                </div>
              </div>\n""" % (
                    i,
                    geticon,
                    dat,
                    name,
                    lvl,
                    title,
                    i,
                    body,
                )
                i = i + 1

                if i > Max_Items:

                    To_Split = True
                    info = "Split was True and i >Max and Max is:", Max_Items
                    info += "\nTotal item to be proceed :", len(Subjects_Sort) + 1
                    istk=inspect.stack();DebugMode("if i > Max_Items:", istk, info, Switch)

                    (
                        Last_Position,
                        Last_Hosts_Sort,
                        Last_Levels_Sort,
                        Last_Dates_Sort,
                        Last_Messages_Sort,
                        Last_Subjects_Sort,
                    ) = (
                        i,
                        Hosts_Sort,
                        Levels_Sort,
                        Dates_Sort,
                        Messages_Sort,
                        Subjects_Sort,
                    )

                    Accordeon_Html += End_Item_Accordeon_To_Split(
                        i, len(Subjects_Sort) + 1, Page_Number, arg
                    )
                    return Accordeon_Html
            else:
                i = i + 1

        else:  # To_Split is False:

            geticon = Avatar_Accordeon(name)
            Accordeon_Html += """\n              <div class="accordion-group">
                <div class="accordion-heading"> <a class="accordion-toggle" data-toggle="collapse"
                    data-parent="#accordion2" href="#collapse%s" aria-expanded="false">%s %s From %s Lvl %s :<br>%s</a> </div>
                <div id="collapse%s" class="accordion-body collapse" aria-expanded="false" style="height: 0px;">
                  <div class="accordion-inner">%s</div>
                </div>
              </div>\n""" % (
                i,
                geticon,
                dat,
                name,
                lvl,
                title,
                i,
                body,
            )
            i = i + 1

            if i > Max_Items:
                To_Split = True
                info = "Split is now  True cause i >Max and Max is:", Max_Items
                info += "\nTotal item to be proceed :", len(Subjects_Sort) + 1
                istk=inspect.stack();DebugMode("if i > Max_Items:", istk, info, Switch)

                (
                    Last_Position,
                    Last_Hosts_Sort,
                    Last_Levels_Sort,
                    Last_Dates_Sort,
                    Last_Messages_Sort,
                    Last_Subjects_Sort,
                ) = (
                    i,
                    Hosts_Sort,
                    Levels_Sort,
                    Dates_Sort,
                    Messages_Sort,
                    Subjects_Sort,
                )

                Accordeon_Html += End_Item_Accordeon_To_Split(
                    i, len(Subjects_Sort) + 1, Page_Number, arg
                )

                return Accordeon_Html

    Split_End = True
    Accordeon_Html += End_Item_Accordeon_To_Split(
        i, len(Subjects_Sort) + 1, Page_Number, arg
    )
    return Accordeon_Html


def BuildHtml(sort=None, arg=None):

    global Global_Lvl_List
    global Global_Rule_List

    statpath = OSSEC_STATS_PATH

    Data_to_html = ""

    MaxLvlAlert = 0
    LevelZero = []
    LevelZero_Id = {}
    RuleId_Counter = {}
    RuleId_Lvl = {}
    LevelZero_Counter = 0

    Yesterday_MaxLvlAlert = 0
    Yesterday_LevelZero = []
    Yesterday_LevelZero_Id = {}
    Yesterday_RuleId_Counter = {}
    Yesterday_RuleId_Lvl = {}
    Yesterday_LevelZero_Counter = 0

    Hourstat = []
    DailyCounter_Alert = 0
    DailyCounter_Event = 0
    DailyCounter_Syscheck = 0
    DailyCounter_Firewall = 0

    day = datetime.today()
    yesterday = datetime.today() - timedelta(days=1)

    lastfile = (
        str(statpath)
        + str(day.year)
        + "/"
        + str(day.strftime("%b"))
        + "/ossec-totals-"
        + str(day.strftime("%d"))
        + ".log"
    )
    Yesterday_lastfile = (
        str(statpath)
        + str(yesterday.year)
        + "/"
        + str(yesterday.strftime("%b"))
        + "/ossec-totals-"
        + str(yesterday.strftime("%d"))
        + ".log"
    )

    if os.path.exists(lastfile):
        pass
    else:
        day = day - timedelta(days=1)
        lastfile = (
            str(statpath)
            + str(day.year)
            + "/"
            + str(day.strftime("%b"))
            + "/ossec-totals-"
            + str(day.strftime("%d"))
            + ".log"
        )
        if os.path.exists(lastfile):
            pass
        else:
            print("Lastfile File not found ", lastfile)
            sys.exit()

    if os.path.exists(Yesterday_lastfile):
        pass
    else:
        yesterday = yesterday - timedelta(days=1)
        Yesterday_lastfile = (
            str(statpath)
            + str(yesterday.year)
            + "/"
            + str(yesterday.strftime("%b"))
            + "/ossec-totals-"
            + str(yesterday.strftime("%d"))
            + ".log"
        )
        if os.path.exists(Yesterday_lastfile):
            pass
        else:
            print("Yesterday File not found ", Yesterday_lastfile)
            sys.exit()

    with open(lastfile) as f:
        for line in f:
            line = line.strip()

            if (
                len(line) > 0
                and not "Hour totals" in line
                and not "Total events" in line
            ):

                if "--" in line:
                    Hourstat.append(line)
                    DailyCounter_Alert = DailyCounter_Alert + int(line.split("--")[1])
                    DailyCounter_Event = DailyCounter_Event + int(line.split("--")[2])
                    DailyCounter_Syscheck = DailyCounter_Syscheck + int(
                        line.split("--")[3]
                    )
                    DailyCounter_Firewall = DailyCounter_Firewall + int(
                        line.split("--")[4]
                    )

                elif "-0-" in line:
                    LevelZero.append(line)
                    LevelZero_Counter = LevelZero_Counter + int(line.split("-")[3])

                    if line.split("-")[1] in LevelZero_Id:
                        LevelZero_Id[line.split("-")[1]] = int(
                            LevelZero_Id.get(line.split("-")[1])
                        ) + int(line.split("-")[3])
                    else:
                        LevelZero_Id[line.split("-")[1]] = line.split("-")[3]

                elif int(line.split("-")[2]) > MaxLvlAlert:
                    MaxLvlAlert = int(line.split("-")[2])

                if not "--" in line and not "-0-" in line:

                    if line.split("-")[1] in RuleId_Counter:
                        RuleId_Counter[line.split("-")[1]] = int(
                            RuleId_Counter.get(line.split("-")[1])
                        ) + int(line.split("-")[3])
                    else:
                        RuleId_Counter[line.split("-")[1]] = line.split("-")[3]

                    if line.split("-")[1] in RuleId_Lvl:
                        pass
                    else:
                        RuleId_Lvl[line.split("-")[1]] = line.split("-")[2]

    with open(Yesterday_lastfile) as f:
        for line in f:
            line = line.strip()
            #              print(line)

            if (
                len(line) > 0
                and not "Hour totals" in line
                and not "Total events" in line
            ):

                if "--" in line:
                    pass
                elif "-0-" in line:
                    Yesterday_LevelZero.append(line)
                    Yesterday_LevelZero_Counter = Yesterday_LevelZero_Counter + int(
                        line.split("-")[3]
                    )

                    if line.split("-")[1] in Yesterday_LevelZero_Id:
                        Yesterday_LevelZero_Id[line.split("-")[1]] = int(
                            Yesterday_LevelZero_Id.get(line.split("-")[1])
                        ) + int(line.split("-")[3])
                    else:
                        Yesterday_LevelZero_Id[line.split("-")[1]] = line.split("-")[3]

                elif int(line.split("-")[2]) > Yesterday_MaxLvlAlert:
                    Yesterday_MaxLvlAlert = int(line.split("-")[2])

                if not "--" in line and not "-0-" in line:

                    if line.split("-")[1] in Yesterday_RuleId_Counter:
                        Yesterday_RuleId_Counter[line.split("-")[1]] = int(
                            Yesterday_RuleId_Counter.get(line.split("-")[1])
                        ) + int(line.split("-")[3])
                    else:
                        Yesterday_RuleId_Counter[line.split("-")[1]] = line.split("-")[
                            3
                        ]

                    if line.split("-")[1] in Yesterday_RuleId_Lvl:
                        pass
                    else:
                        Yesterday_RuleId_Lvl[line.split("-")[1]] = line.split("-")[2]

    for rule, cnt in RuleId_Counter.items():
        if not rule in Global_Rule_List:
            Global_Rule_List.append(rule)
        if not RuleId_Lvl.get(rule) in Global_Lvl_List:
            Global_Lvl_List.append(RuleId_Lvl.get(rule))
    for rule, cnt in Yesterday_RuleId_Counter.items():
        if not rule in Global_Rule_List:
            Global_Rule_List.append(rule)
        if not Yesterday_RuleId_Lvl.get(rule) in Global_Lvl_List:
            Global_Lvl_List.append(Yesterday_RuleId_Lvl.get(rule))

    Last_Stat = Hourstat[-1]
    Last_Stat_Hour = Last_Stat.split("--")[0]
    Last_Stat_Alert = Last_Stat.split("--")[1]
    Last_Stat_Event = Last_Stat.split("--")[2]
    Last_Stat_Syscheck = Last_Stat.split("--")[3]
    Last_Stat_Firewall = Last_Stat.split("--")[4]

    for hst in HOSTS_NAMES:
        if hst in Host_Alerts:
            HOST_DICT[hst + "_Alert"] = Host_Alerts.get(hst)
        else:
            HOST_DICT[hst + "_Alert"] = "??"

    ##

    Data_to_html += Template_Head

    Data_to_html += Template_Row1

    Data_to_html += Template_Profile

    Data_to_html += Template_DailyBlock

    Data_to_html += (
        """
                      <p><bold style="font-size: 18px;">Alerts:</bold> """
        + str(DailyCounter_Alert)
        + """</p>
                      <p><bold style="font-size: 18px;">Events:</bold> """
        + str(DailyCounter_Event)
        + """</p>
                      <p><bold style="font-size: 18px;">Syschecks:</bold>"""
        + str(DailyCounter_Syscheck)
        + """</p>
                      <p><bold style="font-size: 18px;">Firewalls:</bold> """
        + str(DailyCounter_Firewall)
        + "</p>"
    )

    Data_to_html += Template_DailyBlockEND

    Data_to_html += Template_HourBlock

    Data_to_html += (
        str(Last_Stat_Alert)
        + """</p>
                      <p><bold style="font-size: 18px;">Events:</bold> """
        + str(Last_Stat_Event)
        + """</p>
                      <p><bold style="font-size: 18px;">Syschecks:</bold>"""
        + str(Last_Stat_Syscheck)
        + """</p>
                      <p><bold style="font-size: 18px;">Firewalls:</bold> """
        + str(Last_Stat_Firewall)
        + "</p>"
    )

    Data_to_html += Template_HourBlockEND

    Data_to_html += Template_Chart

    ##################################################### #Data_to_html += Template_ChartEND

    Data_to_html += Template_ChartJs

    Data_to_html += Template_Row2

    Data_to_html += Template_Health

    for hst, img in zip(HOSTS_NAMES, HOSTS_IMGS):

        Data_to_html += """                  <li> <i class="read" style="background-color: #cc33cc;"></i>
                    <img class="avatar" src="images/%s" alt="avatar" style="background-color: #ffccff;">
                    <p class="sender" style="top: -3px !important;">Temp:%s</p>
                    <p class="disk">Disk:%s</p>
                    <p class="alerts" style="margin-bottom: 10px !important; padding: 5px !important; margin-top: -7px !import
ant;">Alerts
                      %s</p>
                    <br>
                  </li>""" % (
            img,
            HOST_DICT.get(hst + "_Temp"),
            HOST_DICT.get(hst + "_Space"),
            HOST_DICT.get(hst + "_Alert"),
        )

    Data_to_html += Template_HealthEND

    Data_to_html += Template_Accordeon

    Data_to_html += Accordeon(sort, arg)

    Data_to_html += Template_AccordeonEND

    Data_to_html += Template_Row3part1

    Data_to_html += Template_Cam

    Data_to_html += (
        """<p><bold style="font-size: 15px;">GarageCam :</bold> %s</p>""" % (GarageCam)
    )

    Data_to_html += (
        """<p><bold style="font-size: 15px;">GardenCam :</bold> %s</p>""" % (GardenCam)
    )

    Data_to_html += (
        """<p><bold style="font-size: 15px;">LivingCam :</bold> %s</p>""" % (LivingCam)
    )

    Data_to_html += Template_CamEND

    Data_to_html += Template_Row3part2

    Data_to_html += Template_AlertBlock1

    Data_to_html += str(MaxLvlAlert) + "</p>\n"

    for rule, cnt in RuleId_Counter.items():
        Data_to_html += (
            """            <p style="text-align: center;"><a href="lvl%s.html">LvL %s</a> <a href="rule%s.html">Rule[%s]</a>: %s</p>\n"""
            % (RuleId_Lvl.get(rule), RuleId_Lvl.get(rule), rule, rule, cnt)
        )

    Data_to_html += (
        """\n<br><p style="text-decoration: underline overline; font-weight: bold; text-align: center;">Level Zero Alerts: """
        + str(LevelZero_Counter)
        + "</p>"
    )

    for rule, cnt in LevelZero_Id.items():
        Data_to_html += (
            """            <p style="text-align: center;">LvL 0 Rule[%s]: %s</p>\n"""
            % (rule, cnt)
        )

    Data_to_html += Template_AlertBlock1END

    Data_to_html += Template_Row4

    Data_to_html += Template_AlertBlock2

    Data_to_html += str(Yesterday_MaxLvlAlert) + "</p>\n"

    for rule, cnt in Yesterday_RuleId_Counter.items():
        Data_to_html += (
            """            <p style="text-align: center;"><a href="lvl%s.html">LvL %s</a> <a href="rule%s.html">Rule[%s]</a>: %s</p>\n"""
            % (
                Yesterday_RuleId_Lvl.get(rule),
                Yesterday_RuleId_Lvl.get(rule),
                rule,
                rule,
                cnt,
            )
        )

    Data_to_html += (
        """\n<br><p style="text-decoration: underline overline; font-weight: bold; text-align: center;">Level Zero Alerts: """
        + str(Yesterday_LevelZero_Counter)
        + "</p>"
    )

    for rule, cnt in Yesterday_LevelZero_Id.items():
        Data_to_html += (
            """            <p style="text-align: center;">LvL 0 Rule[%s]: %s</p>\n"""
            % (rule, cnt)
        )

    Data_to_html += Template_AlertBlock2END

    Data_to_html += Template_Row4

    Data_to_html += Template_Tail

    return Data_to_html


def ToJs(month=None, hour=None):

    if month:
        month = int(month) - 1
        if month == -1:
            month = 11
        return month
    if hour:
        hour = int(hour) - 1
        if hour == -1:
            hour = 23
        return hour


def OsseChartBuilder():

    Chart_Alert = []
    Chart_Event = []
    Chart_Syscheck = []
    Chart_Firewall = []
    Chart_DayCounter = []
    Chart_HourTotal = []
    Builder_Result = ""

    yr = datetime.today()
    yr = str(yr.year)

    maindir = OSSEC_STATS_PATH + str(yr)

    for month in Path(maindir).iterdir():
        for dailylog in Path(month).iterdir():

            mth = datetime.strptime(month.name, "%b")
            MONTH = str(datetime.strftime(mth, "%m"))
            dy = str(dailylog.name).split(".log")[0][-2:]

            try:
                with open(dailylog) as log:
                    for line in log:
                        line = line.strip()
                        mth = MONTH
                        if "--" in line:
                            hourly_stats = line.split("--")
                            hr = hourly_stats[0]
                            alrt = hourly_stats[1]
                            evnt = hourly_stats[2]
                            schk = hourly_stats[3]
                            fwll = hourly_stats[4]

                            timestamp = datetime(int(yr), int(mth), int(dy), int(hr))
                            timestamp = timestamp.strftime("%Y-%m-%d-%H")

                            hr = ToJs(hr)
                            mth = ToJs(mth)

                            dateobj = "Date.UTC(%s, %s, %s, %s)" % (yr, mth, dy, hr)

                            data_alert = (
                                "["
                                + dateobj
                                + ", "
                                + str(alrt)
                                + "]##"
                                + str(timestamp)
                            )
                            data_event = (
                                "["
                                + dateobj
                                + ", "
                                + str(evnt)
                                + "]##"
                                + str(timestamp)
                            )
                            data_schk = (
                                "["
                                + dateobj
                                + ", "
                                + str(schk)
                                + "]##"
                                + str(timestamp)
                            )
                            data_fwll = (
                                "["
                                + dateobj
                                + ", "
                                + str(fwll)
                                + "]##"
                                + str(timestamp)
                            )

                            Chart_Alert.append(data_alert)
                            Chart_Event.append(data_event)
                            Chart_Syscheck.append(data_schk)
                            Chart_Firewall.append(data_fwll)

                        if "Hour totals" in line:
                            hourly_total = line.split(":")
                            hr_t = hourly_total[0][-2:].replace(" ", "")
                            alrt_t = hourly_total[1]

                            timestamp = datetime(int(yr), int(mth), int(dy), int(hr_t))
                            timestamp = timestamp.strftime("%Y-%m-%d-%H")

                            hr_t = ToJs(hr_t)
                            mth = ToJs(mth)

                            dateobj = "Date.UTC(%s, %s, %s, %s)" % (yr, mth, dy, hr_t)

                            data_total = (
                                "["
                                + dateobj
                                + ", "
                                + str(alrt_t)
                                + "]##"
                                + str(timestamp)
                            )
                            Chart_HourTotal.append(data_total)

                        if "Total events for day" in line:
                            daily_total = line.split(":")
                            daily_t = daily_total[1]

                            timestamp = datetime(int(yr), int(mth), int(dy), 23)
                            timestamp = timestamp.strftime("%Y-%m-%d-%H")

                            mth = ToJs(mth)

                            dateobj = "Date.UTC(%s, %s, %s, 23)" % (yr, mth, dy)

                            data_dt = (
                                "["
                                + dateobj
                                + ", "
                                + str(daily_t)
                                + "]##"
                                + str(timestamp)
                            )
                            Chart_DayCounter.append(data_dt)

            except Exception as e:
                chk = 0
                info = "OsseChartBuilder Error:", e
                try:
                    info += "\nLen Line:", len(line)
                    if len(line) > 0:
                        chk = chk + 1
                except:
                    pass
                try:
                    info += "\nmth:", mth
                    if len(str(mth)) > 0:
                        chk = chk + 1
                except:
                    pass
                try:
                    info += "\nMONTH:", MONTH
                    if len(str(MONTH)) > 0:
                        chk = chk + 1
                except:
                    pass

                try:
                    info += "\nhour:", hr
                    if len(str(hr)) > 0:
                        chk = chk + 1
                except:
                    pass
                try:
                    info += "\nhtot:", hr_t
                    if len(str(hr_t)) > 0:
                        chk = chk + 1
                except:
                    pass
                try:
                    info += "\ndobj:", dateobj
                    if len(str(dateobj)) > 0:
                        chk = chk + 1
                except:
                    pass
                try:
                    info += "\ndata_dt:", data_dt
                    if len(str(data_dt)) > 0:
                        chk = chk + 1
                except:
                    pass
                if chk == 7:
                    info += "\nException in OsseChartBuilder but good to go \n"
                    info += "\nError:", e
                    DebugMode = (
                        "with open(dailylog) as log",
                        istk,
                        info,
                        chk,
                        line,
                    )
                else:
                    info += "\nException in OsseChartBuilder [No Go] \n"
                    info += "\nError:", e
                    DebugMode = (
                        "with open(dailylog) as log",
                        istk,
                        info,
                        chk,
                        line,
                    )

    Builder_Result += """\n         name: 'Daily Alerts',
        data: ["""
    #
    Chart_Alert.sort(key=lambda x: datetime.strptime(x.split("##")[1], "%Y-%m-%d-%H"))
    #
    for item in Chart_Alert:
        item = str(item.split("##")[0])
        Builder_Result += item + ", "

    Builder_Result += """]
    }, {"""
    Builder_Result += """\n         name: 'Daily Events',
        data: ["""
    #
    Chart_Event.sort(key=lambda x: datetime.strptime(x.split("##")[1], "%Y-%m-%d-%H"))
    #
    for item in Chart_Event:
        item = str(item.split("##")[0])
        Builder_Result += item + ", "

    Builder_Result += """]
    }, {"""
    #
    Chart_Syscheck.sort(
        key=lambda x: datetime.strptime(x.split("##")[1], "%Y-%m-%d-%H")
    )
    #
    Builder_Result += """\n         name: 'Daily Syscheck',
        data: ["""
    for item in Chart_Syscheck:
        item = str(item.split("##")[0])
        Builder_Result += item + ", "
    Builder_Result += """]
    }, {"""

    #
    Chart_Firewall.sort(
        key=lambda x: datetime.strptime(x.split("##")[1], "%Y-%m-%d-%H")
    )
    #

    Builder_Result += """\n         name: 'Daily Firewall',
        data: ["""
    for item in Chart_Firewall:
        item = str(item.split("##")[0])
        Builder_Result += item + ", "

    Builder_Result += """]
    }, {"""

    #
    Chart_HourTotal.sort(
        key=lambda x: datetime.strptime(x.split("##")[1], "%Y-%m-%d-%H")
    )
    #

    Builder_Result += """\n         name: 'Total per Hour',
        data: ["""
    for item in Chart_HourTotal:
        item = str(item.split("##")[0])
        Builder_Result += item + ", "
    Builder_Result += """]
    }, {"""
    #
    Chart_DayCounter.sort(
        key=lambda x: datetime.strptime(x.split("##")[1], "%Y-%m-%d-%H")
    )
    #
    Builder_Result += """\n         name: 'Total per day',
        data: ["""
    for item in Chart_DayCounter:
        item = str(item.split("##")[0])
        Builder_Result += item + ", "

    Builder_Result += "]\n"

    return Builder_Result


def Split_Or_Not(sort, arg):
    global Page_Number
    global To_Split

    if sort is "by_lvl":
        Title = "lvl" + str(arg)
    elif sort is "by_rule":
        Title = "rule" + str(arg)
    else:
        Title = str(arg)

    while True:
        istk=inspect.stack();DebugMode(
            "in Split_Or_Not", istk, Page_Number, To_Split, sort, arg
        )

        Page_To_Save = BuildHtml(sort, arg)

        if To_Split is True:
            #               Page_To_Save=BuildHtml(sort,arg)
            if Page_Number > 0:
                Save(
                    Page_To_Save,
                    str(Title) + "_" + str(Page_Number) + ".html",
                    WWW_PATH,
                )
            else:
                Save(Page_To_Save, str(Title) + ".html", WWW_PATH)

            Page_Number = Page_Number + 1

        else:
            istk=inspect.stack();DebugMode(
                "in Split_Or_Not",
                istk,
                Page_Number,
                To_Split,
                sort,
                arg,
            )
            #                Page_To_Save=BuildHtml(sort,arg)

            if Page_Number > 0:
                istk=inspect.stack();DebugMode(
                    "Going to break of Split_Or_Not",
                    istk,
                    Page_Number,
                    To_Split,
                    sort,
                    arg,
                )

                return Save(
                    Page_To_Save,
                    str(Title) + "_" + str(Page_Number) + ".html",
                    WWW_PATH,
                )
            else:
                istk=inspect.stack();DebugMode(
                    "Going to break of Split_Or_Not",
                    istk,
                    Page_Number,
                    To_Split,
                    sort,
                    arg,
                )
                return Save(Page_To_Save, str(Title) + ".html", WWW_PATH)


def Save(data, title, path):
    istk=inspect.stack();DebugMode("save", istk, data)

    finalpath = str(path) + str(title)

    with open(str(finalpath), "w") as f:
        f.write(str(data))


def Update():
    global ServerReady
    global GardenCam
    global GarageCam
    global LivingCam

    #     istk=inspect.stack();DebugMode(istk,Timediff,Old_Value_Now,Now)

    if Timer("Gauge", 1800) is True:
        cpulist = os.popen(
            """top -bn10 | grep "ni," |cut -c 37-38 |awk '{print 100 - $1}'"""
        ).readlines()
        cpulist = [int(i) for i in cpulist if i != ""]
        ScriptGauge = (
            ScriptGaugeHead
            + "\n       cpulist = "
            + str(cpulist)
            + ";"
            + ScriptGaugeTail
        )
        Save(ScriptGauge, "gauge.js", WWW_JS_PATH)

        for hst, usr in zip(HOSTS_NAMES, HOSTS_USERS):
            try:
                if usr.lower() != USER.lower():
                    HOST_DICT[hst + "_Temp"] = (
                        str(ssh(usr, hst.lower(), "sensors"))
                        .split("temp1:        +")[1]
                        .split("°C")[0]
                        .split(".")[0]
                        + "°C"
                    )
                else:
                    HOST_DICT[hst + "_Temp"] = (
                        str(subprocess.check_output(["sensors"]).decode("utf8"))
                        .split("temp1:        +")[1]
                        .split("°C")[0]
                        .split(".")[0]
                        + "°C"
                    )

            except Exception as e:
                istk=inspect.stack();DebugMode(str(e), istk, "temp")
                HOST_DICT[hst + "_Temp"] = "???"

            try:
                if usr.lower() != USER.lower():
                    HOST_DICT[hst + "_Space"] = (
                        str(ssh(usr, hst.lower(), "df -h /")).split("%")[1][-3:] + "%"
                    )
                else:
                    HOST_DICT[hst + "_Space"] = (
                        str(
                            subprocess.check_output(["df", "-h", "/"]).decode("utf8")
                        ).split("%")[1][-3:]
                        + "%"
                    )
            except Exception as e:
                istk=inspect.stack();DebugMode(str(e), istk, "df")
                HOST_DICT[hst + "_Space"] = "???"

    if Timer("Cam", 3600) is True:

        try:
            CamCounter = str(ssh(CAM_USER_HOST[0], CAM_USER_HOST[1], CAM_CMD))
            CamCounter = CamCounter.splitlines()

            for lines in CamCounter:

                lines = lines.replace("===Breaking News !!=== ", "")
                if "GarageCam" in lines:
                    GarageCam = lines.split("GarageCam :")[1].split(" ")[0]
                if "GardenCam" in lines:
                    GardenCam = lines.split("GardenCam :")[1].split(" ")[0]
                if "LivingCam" in lines:
                    LivingCam = lines.split("LivingCam :")[1].split(" ")[0]
        except Exception as e:
            istk=inspect.stack();DebugMode(str(e), istk, CamCounter)

        if GarageCam is "":
            GarageCam = "???"
        if GardenCam is "":
            GardenCam = "???"
        if LivingCam is "":
            LivingCam = "???"

    if Timer("Chart", 900001):
        OsseChart = ChartScriptHead
        OsseChart += OsseChartBuilder()
        OsseChart += ChartScriptTail
        Save(OsseChart, "ossechart.js", WWW_JS_PATH)

    Split_Or_Not("no_sort", "index")

    for hst in HOSTS_NAMES:

        Split_Or_Not("by_name", hst.lower())

    for rule in Global_Rule_List:
        Split_Or_Not("by_rule", str(rule))

    for lvl in Global_Lvl_List:
        Split_Or_Not("by_lvl", str(lvl))

    if ServerReady is True:
        Thread(cherrypy.quickstart(Osserver(), "/", Cherryconf)).start()
        print(
            "\nDone Loading Datas\nYou Can Now Connect To http://%s .\n"
            % (socket.gethostbyname(socket.gethostname()))
        )
        ServerReady = False


# class Osserver:
def Osserver():
    pass


def Timer(mode, limit):
    global Time_Track

    istk=inspect.stack();DebugMode("Timer", istk, mode, Time_Track)

    Now = datetime.now()

    if Time_Track[mode][0] is None:
        Time_Track[mode] = [limit + 1, Now]
        istk=inspect.stack();DebugMode(
            "if Time_Track[mode][0] is None:", istk, mode, Time_Track
        )
    else:
        Time_Track[mode][0] = round((Now - Time_Track[mode][0]).total_seconds())
        istk=inspect.stack();DebugMode(
            "else Time_Track[mode][0] is None:", istk, mode, Time_Track
        )

    if Time_Track[mode][0] > limit:
        Time_Track[mode][1] = Now
        istk=inspect.stack();DebugMode(
            "if Time_Track[mode][0] > limit:", istk, mode, Time_Track
        )
        return True
    else:
        return False


def Check_Mail():
    pass


##################################################################################


def main():

    Done = False
    with open(MAIL_PATH, "rb") as mailbox:
        Mails = Mbr(mailbox)

        for M in Mails:
            if Done is False:
                Mailstr = Parser(policy=default).parsestr(M.as_string())
                Body = Mailstr.get_payload()
                From = Mailstr["from"]
                To = Mailstr["to"]
                Subject = Mailstr["subject"]
                if From is not None:
                    Stockvars(From, To, Subject, Body)

                    if FirstLoad is False:
                        Update()

                    istk=inspect.stack();DebugMode(
                        "if From is not None:",
                        istk,
                        Sep,
                        From,
                        To,
                        Subject,
                        Body,
                        Sep,
                    )
                else:
                    istk=inspect.stack();DebugMode(
                        "else From is not None:",
                        istk,
                        Sep,
                        M,
                        Mailstr,
                        SepTop,
                        From,
                        To,
                        Subject,
                        Sepmid,
                        Body,
                        Sepend,
                    )
                    if TMP_FIX[0] in str(Mailstr):
                        if TMP_FIX[1] in str(Mailstr):
                            if Subject is not None and Body is not None:
                                From = TMP_FIX[2]
                                To = TMP_FIX[3]
                                istk=inspect.stack();DebugMode(
                                    "if TMP_FIX[0] in str(Mailstr):",
                                    istk,
                                    SepTop,
                                    From,
                                    To,
                                    Subject,
                                    Sepmid,
                                    Body,
                                    Sepend,
                                )
                                Stockvars(From, To, Subject, Body)
                                if FirstLoad is False:
                                    Update()
#    print("The End")


if __name__ == "__main__":

    Osserver_Title = """ ██████  ███████ ███████ ███████ ██████  ██    ██ ███████ ██████  
██    ██ ██      ██      ██      ██   ██ ██    ██ ██      ██   ██ 
██    ██ ███████ ███████ █████   ██████  ██    ██ █████   ██████  
██    ██      ██      ██ ██      ██   ██  ██  ██  ██      ██   ██ 
 ██████  ███████ ███████ ███████ ██   ██   ████   ███████ ██   ██ """

    print(Osserver_Title + "\n")
    print("Starting Server Please wait...\n")

    Thread(target=Loading).start()
    os.chdir(SCRIPT_PATH)

    HOST_DICT = {}
    for name in HOSTS_NAMES:
        key = name + "_Temp"
        value = ""
        HOST_DICT[key] = value
        key = name + "_Space"
        value = ""
        HOST_DICT[key] = value
        key = name + "_Alert"
        value = ""
        HOST_DICT[key] = value
    main()
