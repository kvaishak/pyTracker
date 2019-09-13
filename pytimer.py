import time
import datetime
from AppKit import NSWorkspace
from Foundation import *
from activity import *

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