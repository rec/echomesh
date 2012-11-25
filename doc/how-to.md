Common echomesh Operations - A How-To
=====================================

What to do with a machine with a newly cloned card.
--------------------------------------------------

a. Figure out which hostname you want for this machine from [this page](https://github.com/rec/echomesh/blob/master/doc/card-hostnames.txt).

b. Boot up the RP.

c. Open up a user terminal window.

d. Copy this next line:

    cd ~/echomesh && git pull origin master && ~/echomesh/scripts/change-hostname-restart.sh $1

e. Paste it into your terminal window.

f. Replace the last word $1 with the desired hostname.

g. Press return.

h. The machine should update and restart automatically.  If it does not restart, it will almost certainly emit some messages.  Please copy these and mail them to the programmer.


How to install the control program.
--------------------------------------------------

a. Choose a desktop or laptop in which to install the control program.

b. If git is not installed install it [like this](http://git-scm.com/book/en/Getting-Started-Installing-Git).

c. Open a terminal with a command line and make sure that you are in your home directory.

d. Enter this command:

     git clone git://github.com/rec/echomesh.git


How to run the control program.
--------------------------------------------------

a. Open a terminal with a command line.

b. Enter this command:

     python ~/echomesh/python/Echomesh.py

c. You should see a prompt:

     echomesh:

d. If you get a SyntaxError from this previous command, it is likely you have an version of Python earlier than 2.6.

e. Make sure of this by typing

     python --version

f. You might already have a more recent Python version installed.  Try entering:

     python2.7 ~/echomesh/python/Echomesh.py

or if that doesn't work:

     python2.6 ~/echomesh/python/Echomesh.py

g. If you don't have a more recent Python, you can download Python 2.7 [here](http://python.org/download/releases/2.7.3/).


How to quit the echomesh control program.
--------------------------------------------------

a. At the echomesh: prompt, enter

    quit


How to list the commands for the echomesh control program.
--------------------------------------------------

a. At the echomesh: prompt, enter

    list


How to change configuration settings.
--------------------------------------------------

a. Run the control program.

b. On that same machine, edit the config file, found at

    ~/echomesh/config/config.yml

c. At the echomesh: prompt, enter

    config

d. This will update all the configuration files on any echomesh nodes on the network.

e. Repeat steps 2 and 3 as needed.


How to reset changed configuration settings to echomesh factory defaults.
--------------------------------------------------

a. Run the control program.

b. At the echomesh: prompt, enter

    clear

All nodes including control programs will be reset to their "factory defaults"


How to check the edited configuration into github (and make it the "factory defaults")
--------------------------------------------------


a. This only works on certain machines that have been authenticated for GitHub, which doesn't yet include any of the RP units.

b. Run the control program.

c. At the echomesh: prompt, enter

    commit


How to update the echomesh program on all echomesh nodes.
--------------------------------------------------

a. Run the control program.

b. At the echomesh: prompt, enter

    update

All echomesh nodes will have their programs updated.  Nodes which aren't control
programs will automatically reboot and restart - you must manually quit and
restart control programs.


How to stop and start an echomesh node which isn't a control program.
--------------------------------------------------

a. Open a terminal window.

b. To stop the node, enter

    sudo /etc/init.d/echomesh stop

c. To start the node, enter

    sudo /etc/init.d/echomesh start

This will have no effect if the the program is already running.

d. To restart the program, enter

    sudo /etc/init.d/echomesh start


How to calibrate the microphones.
--------------------------------------------------

a. Select an echomesh node (not a control program) with a microphone.

b. Open a terminal window.

c. Stop the node by entering:

    sudo /etc/init.d/echomesh stop

d. Now start the node in this terminal window by entering:

   ~/echomesh/scripts/run-echomesh.sh

e. Edit the file

    ~/echomesh/config/config.yml

on the control computer, go to the audio.input section, and change the "verbose" entry to be true.

f. Open a control program and enter:

    config

g. Now look back at the echomesh node's terminal window.  Interspersed between other messages, you should see a steady stream of microphone level numbers looking like

    2012-10-29 19:00:35,345 INFO: sound.Microphone: quiet: -30.30
    2012-10-29 19:00:35,345 INFO: sound.Microphone: quiet: -28.35
    2012-10-29 19:00:35,345 INFO: sound.Microphone: loud: -5.14

h. To calibrate the microphone, go back to the control program and again edit the config file

    ~/echomesh/config/config.yml

i. To change the assignment of levels to names, edit the table called audio/input/levels.

j. There are three smoothing parameters in audio/input: chunk_size, grouping_size and window_size.

k. The smoothing parameters control how the steady stream of level input data is converted into a small number of level names.

l. The program takes one chunk_size of audio data and computes its audio level.

m. It is inadvisable to raise the chunk_size too high, because if you don't consume all the audio data in time the program crashes due to an issue in the audio library.  It is also inadvisable to lower the chunk_size too much because you won't get accurate levels.  Echomesh will restrict any chunk_size you enter to between 16 and 2048.

n. The grouping_window parameter controls how many chunk_sizes are averaged together to make one group.

o. The moving_average parameter then takes a moving (smoothed) average over the groups.

p. You can turn off grouping by setting the grouping_window parameter to 0, or by simply removing that parameter.

q. Similarly, you can turn off moving averages by setting the moving_window parameter to 0 or removing it.

r. Don't forget to turn off audio.input.verbose to false and then to check the configuration changes into git when you're finished.


How to kill an echomesh that doesn't stop on quit
--------------------------------------------------

a. Open a terminal.
b. Type:

    sudo killall python