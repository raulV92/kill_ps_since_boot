ReadMe:

This scripts atempts to fix the issue that the computer hangs in the shut down process.

This issue has happened to me and been reported on MX Linux forums.
Making some testings I came to the conclusion that some processes running in the background might cause this to happen
because when I turn on the computer and the shut it off after a quick session it shuts down without problems
so the logic behind this is ti kill every process that was started by the user after the initial login to the system

so first step:
firt thing afer loging in to the session run the command:
$ ps -u $USER > boot_ps.txt

this will create "boot_ps.txt" in the current folder (most probably "home")
this file only needs to be generated once

second step:
before trying to shut down the computer run the python script to kill every process that migh cause the shut down hang
$ python3 kill_since_boot.py

Be sure the "kill_since_boot.py" and the "boot_ps.txt" are in te same directory, it could be "home" to make it easier

->now you can try to shut down the computer.
 
