# PerfectTiming

Tool to log work times easily and autmatically.
To use this tool copy the folder of the latest output in your directory.
The .exe-file "Zeiterfassung"  can be put in the autostart.

Logging:
  After start the user can log-in and log-out for work by pressing the "Einloggen/Ausloggen"-button.
  5-minute-breaks can be easily started by pressing the "Kurzpause" button.
  The user can specify the project he is working in with the dropdown-menu.
  The names of the projects can be set in the menu "Projekte".
  If the user wants to add timestamps the menu "Stempeln" can be used.
  At each log or project-change event the action is logged in the log.txt and the logArchiv.txt file.

Visibility:
  By default the program runs in the foreground. If this is not wanted it can be changed by clicking on the pin-/unpin-button
  The window can be minimized with the windows-window

Alarms/Reminders:
  On the main window the next alarm is shown in a countdown. 
  Also there is a possibility to easily add a new  alarm by clicking on "Neuen Alarm hinzufügen", input the amount of minutes 
    until the event and the event name and click on the "+"-button. 
  An alarm is an (serial) event which is saved with date and time in the config-file and will also executed if the programm is  restarted.
  A reminder creates after programm start a new alarm. This alarm will however been deleted after programm restart.
  Example:
    Alarm:
    The user wants to be reminded each day (or only at one day) of an appointment. Thus the user creates an alarm with this date and time. 
    Even if the appointment is in the next week and the programm is restarted several times, it will alarm you.

    Reminder :
    The user wants to be reminded to make a short break every hour. Thus the user sets a reminder with 60 minutes.
    Thus, after each 60 minutes the programm will remind the user of making a break.
    If the countdown function of the reminder is active the event will also be shown on the main-window countdown.

  Alarms and reminders can be set in the menu "Wecker".

Evaluation:
  The evaluation-file (excel) can be started by the menu "Auswertung"
  There the vba-script will import the data of the log.txt file and calulate the worktimes which are then shown in the "Jahresauswertung".
  If the user wants to see the details of one single day the user can click on a cell of the specific date and then on the "Tagesansicht"-button.
