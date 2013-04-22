Building Juce applications on the Raspberry Pi
==============================================

1. What's Juce?
---------------

[Juce](http://rawmaterialsoftware.com) is a popular and stable cross-platform open-source C++ development system that lets you write an application as a single codebase that works on Windows, OS/X and Linux.

Juce has a huge number of components relating to pretty well anything you need - GUI, audio processing, networking, etc. - and is particularly popular amongst audio software developers.  You can find a lot more information and some snappy demos on the [Juce site](http://rawmaterialsoftware.com).

It turns out that Juce supports the Raspberry Pi "out of the box" as long as you install a few libraries before you start.  I created a sample application on the Mac, copied it to a Raspberry Pi and compiled it, and it worked right the first time!


2. Setting up a Raspberry Pi to use Juce.
--------------------------

User "hugh" on the Juce forums [did all our work for us](http://www.rawmaterialsoftware.com/viewtopic.php?f=2&t=10777&p=63377#p63377) here.

All you need to do is install some libraries using apt-get, and you can do that with a single command line:

    sudo apt-get -y install freeglut3-dev libasound2-dev libfreetype6-dev libjack-dev libx11-dev libxcomposite-dev libxcursor-dev libxinerama-dev mesa-common-dev
    
  
