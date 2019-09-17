import time
import datetime
from os import system
from activity import *
import json
import sys
if sys.platform in ['Windows', 'win32', 'cygwin']:
    import win32gui
    import uiautomation as auto
elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    from AppKit import NSWorkspace
    from Foundation import *

active_window_name = ""
activity_name = ""
first_time = True
start_time = datetime.datetime.now()
activeList = AcitivyList([])
first_time = True

def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]

def get_active_window():    
    _active_window_name = None
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        _active_window_name = win32gui.GetWindowText(window)
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        _active_window_name = (NSWorkspace.sharedWorkspace()
                               .activeApplication()['NSApplicationName'])
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name

def get_url(browser):
    # Refer - > https://gist.github.com/dongyuwei/a1c9d67e4af6bbbd999c
    if sys.platform in ['Windows', 'win32', 'cygwin']:
        window = win32gui.GetForegroundWindow()
        chromeControl = auto.ControlFromHandle(window)
        edit = chromeControl.EditControl()
        return 'https://' + edit.GetValuePattern().Value
    elif sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
        if(browser == "chrome"):
            textOfMyScript = """tell application "Google Chrome" to return URL of active tab of front window"""
        elif(browser == "safari"):
            textOfMyScript = """tell application "Safari" to return URL of front document"""

        s = NSAppleScript.initWithSource_(
            NSAppleScript.alloc(), textOfMyScript)
        results, err = s.executeAndReturnError_(None)
        return results.stringValue()
    else:
        print("sys.platform={platform} is not supported."
              .format(platform=sys.platform))
        print(sys.version)
    return _active_window_name


try:
    activeList.initialize_me()
except Exception:
    print('No json')

try:
    while True:
        previous_site = ""
        
        new_window_name = get_active_window()
        # for getting the chrome Url
        if 'Google Chrome' in new_window_name:
            new_window_name = url_to_name(get_url("chrome"))
        elif 'Safari' in new_window_name:
            new_window_name = url_to_name(get_url("safari"))

        if active_window_name != new_window_name:
            print(active_window_name)
            activity_name = active_window_name

            if not first_time:
                end_time = datetime.datetime.now()
                time_entry = TimeEntry(start_time, end_time, 0, 0, 0, 0)
                time_entry._get_specific_times()

                exists = False
                for activity in activeList.activities:
                    if activity.name == activity_name:
                        exists = True
                        activity.time_entries.append(time_entry)

                if not exists:
                    activity = Activity(activity_name, [time_entry])
                    activeList.activities.append(activity)
                with open('activities.json', 'w') as json_file:
                    json.dump(activeList.serialize(), json_file,
                              indent=4, sort_keys=True)
                    start_time = datetime.datetime.now()
            first_time = False
            active_window_name = new_window_name


        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped the Tracker")
    with open('activities.json', 'w') as json_file:
        json.dump(activeList.serialize(), json_file, indent=4, sort_keys=True)