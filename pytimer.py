import time
import datetime
from AppKit import NSWorkspace
from Foundation import *

active_window_name = ""
activity_name = ""
first_time = True
start_time = datetime.datetime.now()

def url_to_name(url):
    string_list = url.split('/')
    return string_list[2]

def get_active_window():    
    _active_window_name = (NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName'])
    return _active_window_name

def get_url(browser):
    # Refer - > https://gist.github.com/dongyuwei/a1c9d67e4af6bbbd999c
    if(browser == "chrome"):
        textOfMyScript = """tell application "Google Chrome" to return URL of active tab of front window"""
    elif(browser == "safari"):
        textOfMyScript = """tell application "Safari" to return URL of front document"""

    s = NSAppleScript.initWithSource_(
        NSAppleScript.alloc(), textOfMyScript)
    results, err = s.executeAndReturnError_(None)
    return results.stringValue()

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

            
            end_time = datetime.datetime.now()
            time_taken = end_time - start_time
            # print(time_taken)
            days, seconds = time_taken.days, time_taken.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            print("The time taken by the above activity in days = {days} - hours =  {hours} -  minutes  = {minutes} - Seconds = {seconds}".format(days = days, hours = hours, minutes = minutes, seconds = seconds))
            print("--------------------------------------------------------------")
            start_time = datetime.datetime.now()
            active_window_name = new_window_name

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped the Tracker")