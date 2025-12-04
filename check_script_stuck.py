import os, time, datetime, psutil, subprocess, pyautogui

file_to_check = r"download_notiications.log"

while 1:
# Modified Time
    ti_m = os.path.getmtime(file_to_check)

# Converting the modified time in seconds to a timestamp
    m_ti = time.ctime(ti_m)

    modified_time=datetime.datetime.fromtimestamp(ti_m)

    current_time=datetime.datetime.now()

    time_elapsed=current_time - modified_time

    mins = time_elapsed.seconds/60

    if mins > 10:
        print("Stuck at {0}".format(datetime.datetime.now()))
        filename=r'.\new_notices\{0}_'.format('stuck') + str(datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"
        with open(filename, "w") as f:
            f.write("G9nAAne3vq5EhGQEAfe3bA,{0}".format("*Script is stuck.*"))
            time.sleep(120)

#       try:
#            for each_process_pid in psutil.pids():
#               p = psutil.Process(each_process_pid)
                # if p.name() == "WindowsTerminal.exe":
                # if p.name() == "OpenConsole.exe":
#                if p.name() == "python.exe" and each_process_pid !=os.getpid():
#                    p.kill()
#        except:
#            pass

#        os.chdir(r'C:\VS IT')
#        os.system("launch_notices.bat")
#       pyautogui.hotkey('winleft', 'd')
#        pyautogui.hotkey('winleft', 'd')
#        time.sleep(180)

    else:
        print("Not Stuck at {0}".format(datetime.datetime.now()))
        time.sleep(120)
