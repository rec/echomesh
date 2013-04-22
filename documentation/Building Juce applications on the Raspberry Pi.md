Building Juce applications on the Raspberry Pi
==============================================

1. What's Juce?
---------------

[Juce](http://rawmaterialsoftware.com) is a popular and stable cross-platform open-source C++ development system that lets you write an application as a single codebase that works on Windows, OS/X and Linux.

Juce has a huge number of components relating to pretty well anything you need - GUI, audio processing, networking, etc. - and is particularly popular amongst audio software developers.  You can find a lot more information and some snappy demos on the [Juce site](http://rawmaterialsoftware.com).

It turns out that Juce supports the Raspberry Pi "out of the box" as long as you install a few libraries before you start.  I created a sample application on the Mac, copied it to a Raspberry Pi and compiled it, and it worked right the first time!


2. Why would I want to do this?
-------------------------------

It's always great to have cross-platform apps!  

Juce is extremely powerful and simply does a lot of your work for you.

Moreover, the Raspberry Pi is a great machine, but it's terribly slow to compile and build programs.  Using Juce you can develop your program on a fast Mac, PC or Linux desktop, transfer the code to the RP, build it once and expect it to work the first time.


3. Setting up a Raspberry Pi to use Juce.
--------------------------

User "hugh" on the Juce forums [did all our work for us](http://www.rawmaterialsoftware.com/viewtopic.php?f=2&t=10777&p=63377#p63377) here.

All you need to do is install some libraries using apt-get, and you can do that with a single command line:

    sudo apt-get -y install freeglut3-dev libasound2-dev libfreetype6-dev libjack-dev libx11-dev libxcomposite-dev libxcursor-dev libxinerama-dev mesa-common-dev

  
4. Creating a new Juce project to target the Raspberry Pi.
--------------------------------------------------------

Juce uses a program called the Introjucer to create new projects - it's included as part of the [Juce download](http://www.rawmaterialsoftware.com/downloads.php).

You can go through the Introjucer and create a new test project using just the default settings (though I suggest you create a GUI project because that's more fun).

Once you've done that, right click the Config tab in the Introjucer and select "Create a new Linux Makefile project."  Now, click on the icon labelled Linux Makefile.  A form appears - in the section marked Extra Preprocessor Definitions, enter:

    JUCE_USE_XSHM=0 JUCE_USE_XINERAMA=0

and you're all done.


5. Building your Juce project on the Raspberry Pi.
--------------------------------------------------------

Transfer your project to the Raspberry Pi, go to the subdirectory within it named `Builds/Linux` and type the following command:

    TARGET_ARCH=-march=armv6 make

And that's it.  Assuming there are no compilation errors in your code, a new executable should be created in the subdirectory `Builds/Linux/build`.


6. Let me know how it works out!
--------------------------------

You can contact me at tom (at) swirly (dot) com.


