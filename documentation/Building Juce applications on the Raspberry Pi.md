Building Juce applications on the Raspberry Pi
==============================================

1. What's Juce?
---------------

[Juce](http://rawmaterialsoftware.com) is a popular and stable cross-platform open-source C++ development system that lets you write an application as a single codebase that works on Windows, OS/X and Linux.

Juce has a huge number of components relating to pretty well anything you need - GUI, audio processing, networking, etc. - and is particularly popular amongst audio software developers.  You can find a lot more information and some snappy demos on the [Juce site](http://rawmaterialsoftware.com).

It turns out that Juce supports the Raspberry Pi "out of the box" as long as you install a few libraries before you start.  I created a sample application on the Mac, copied it to a Raspberry Pi and compiled it, and it worked right the first time!


2. Setting up to use Juce.
--------------------------
