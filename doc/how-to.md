Common echomesh Operations - A How-To
=====================================

What to do with a machine with a newly cloned card.
--------------------------------------------------

1. Figure out which hostname you want for this machine from [this page](https://github.com/rec/echomesh/blob/master/doc/card-hostnames.txt).

2. Boot up the RP.

3. Open up a user terminal window.

4. Copy this next line:

    cd ~/echomesh && git pull origin master && ~/echomesh/scripts/change-hostname-restart.sh $1

5. Paste it into your terminal window.

6. Replace the last word $1 with the desired hostname.

7. Press return.

8. The machine should update and restart automatically.  If it does not restart, it will almost certainly emit some messages.  Please copy these and mail them to the programmer.


How to install the control program.
--------------------------------------------------

1. Choose a desktop or laptop in which to install the control program.

2. If git is not installed install it [like this](http://git-scm.com/book/en/Getting-Started-Installing-Git).

3. Open a terminal with a command line and make sure that you are in your home directory.

4. Enter this command:

    git clone git://github.com/rec/echomesh.git


How to run the control program.
--------------------------------------------------

1. Open a terminal with a command line.

2. Enter this command:

    python ~/echomesh/python/Echomesh.py

3. You should see a prompt:

    echomesh:

3. If you get a SyntaxError from this previous command, it is likely you have an version of Python earlier than 2.6.

4. Make sure of this by typing

    python --version

5. You might already have a more recent Python version installed.  Try entering:

    python2.7 ~/echomesh/python/Echomesh.py

or if that doesn't work:

    python2.6 ~/echomesh/python/Echomesh.py

6. If you don't have a more recent Python, you can download Python 2.7 [here](http://python.org/download/releases/2.7.3/).


How to quit the echomesh control program.
--------------------------------------------------

1. At the echomesh: prompt, enter

    quit


How to list the commands for the echomesh control program.
--------------------------------------------------

1. At the echomesh: prompt, enter

    list


How to change configuration settings.
--------------------------------------------------

1. Run the control program.

2. On that same machine, edit the config file, found at

    ~/echomesh/config/config.yml

3. At the echomesh: prompt, enter

    config

4. This will update all the configuration files on any echomesh nodes on the network.

5. Repeat steps 2 and 3 as needed.


How to reset changed configuration settings to echomesh factory defaults.
--------------------------------------------------

1. Run the control program.

2. At the echomesh: prompt, enter

    clear

All nodes including control programs will be reset to their "factory defaults"


How to check the edited configuration into github (and make it the "factory defaults")
--------------------------------------------------


1. This only works on certain machines that have been authenticated for GitHub, which doesn't yet include any of the RP units.

2. Run the control program.

3. At the echomesh: prompt, enter

    commit






How to update the echomesh program on all echomesh nodes.
--------------------------------------------------

1. Run the control program.

2. At the echomesh: prompt, enter

    update

All echomesh nodes will have their programs updated.  Nodes which aren't control
programs will automatically reboot and restart - you must manually quit and
restart control programs.


How to stop and start an echomesh node which isn't a control program.
--------------------------------------------------

1. Open a terminal window.

2. To stop the node, enter

    sudo /etc/init.d/echomesh stop

3. To start the node, enter

    sudo /etc/init.d/echomesh start

This will have no effect if the the program is already running.

4. To restart the program, enter

    sudo /etc/init.d/echomesh start


How to calibrate the microphones.
--------------------------------------------------

1. Select an echomesh node (not a control program) with a microphone.

2. Open a terminal window.

3. Stop the node by entering:

    sudo /etc/init.d/echomesh stop

4. Now start the node in this terminal window by entering:

   ~/echomesh/scripts/run-echomesh.sh

5. Edit the file

    ~/echomesh/config/config.yml

on the control computer, go to the audio.input section, and change the "verbose" entry to be true.

6. Open a control program and enter:

    config

7. Now look back at the echomesh node's terminal window.  Interspersed between other messages, you should see a steady stream of microphone level numbers looking like

    2012-10-29 19:00:35,345 INFO: sound.Microphone: quiet: -30.30
    2012-10-29 19:00:35,345 INFO: sound.Microphone: quiet: -28.35
    2012-10-29 19:00:35,345 INFO: sound.Microphone: loud: -5.14

8. To calibrate the microphone, go back to the control program and again edit the config file

    ~/echomesh/config/config.yml

9. To change the assignment of levels to names, edit the table called audio/input/levels.

10. There are three smoothing parameters in audio/input: chunksize, grouping_window and moving_window.

11. The smoothing parameters control how the steady stream of level input data is converted into a small number of level names.

12. The program takes one chunksize of audio data and computes its audio level.

13. It is inadvisable to raise the chunksize too high, because if you don't consume all the audio data in time the program crashes due to an issue in the audio library.  It is also inadvisable to lower the chunksize too much because you won't get accurate levels.  Echomesh will restrict any chunksize you enter to between 16 and 2048.

13. The grouping_window parameter controls how many chunksizes are averaged together to make one group.

14. The moving_average parameter then takes a moving (smoothed) average over the groups.

15. You can turn off grouping by setting the grouping_window parameter to 0, or by simply removing that parameter.

16. Similarly, you can turn off moving averages by setting the moving_window parameter to 0 or removing it.

17. Don't forget to turn off audio.input.verbose to false and then to check the configuration changes into git when you're finished.

