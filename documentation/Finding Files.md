Finding files in echomesh
=========================

Types of echomesh files
-----------------------

echomesh categorizes files into
* asset files
* code files
* command files.
* documentation files.
* log files.

Asset files are
* audio.
* images.
* video.
* OpenGL shaders.
* pi3d model files.
* pure text files (text files which aren't code, command or documentation)
* any other binary file type.

Code files are
* Python scripts
* C++ programs and Makefiles
* Bash scripts
* Anything executable

Command files are
* configuration files, used to set up echomesh at the start of a session.
* score files, representing a sequence of commands to echomesh.
* element files, a chunk of data used in a score.

Documentation files are
* html files
* github markup .md files.
* pure text files.
* anything else (image, audio, etc) that's only used to explain how the echomesh program works.

Log files are created by echomesh as it runs and are not stored to github's version control.


The echomesh directory structure.
---------------------------------

The echomesh directory structure is organized by file type under the top directory.

2    echomesh/
      asset/
      code/
      command/
        0.local/
        1.name/
        2.platform/
        3.global/
        4.default/
      documentation/
      log/


Assets:

echomesh has an _asset directory_.  By default, it's in echomesh/asset, but you can change this in your config file.

If you use assets in an echomesh score, you can identify them in three ways:
* an _absolute path_ starting with /: "/home/someone/files/image.jpg"
* a _user path_ starting with ~: "~/audio/sound.wav", or
* a _relative path_ if the asset is in the asset directory: "images/image.jpg"

Commands:

One of the key features of echomesh is that a single installation of it be able to sent out to a large number of heterogeneous machines. As result, command file resolution gives the user a lot of options.

Command files appear in the following levels:

* 0.local: a local, temporary file that you can use to override everything else.
* 1.name: applies only for a machine with a specific uname.
* 2.platform: over all Macs, all Raspberry Pis or all Windows machines.
* 3.global: over all machines for this instance of echomesh
* 4.default: for all instances of echomesh

Each level overrides the levels below it, so 0.local overrides everything and 4.default is overridden by everything.  When you look for a file, it looks through these directories in order, and gives you the first file it finds.

The "platform" directory may contain subdirectories for platforms that need different configurations.  This lets you set configuration values differently between the Raspberry Pi, the Mac and Windows.

Similarly, the "name" directory may contain subdirectories for specific machine names that need different configurations.  This lets you configure a heterogeneous network on a per-machine basis.

For your convenience, configuration files are treated somewhat different from all other command files.

When you read a configuration file, echomesh does not stop when it finds the first matching file - intead it reads settings for all the command levels, and then merges them together.  This means you only have to list the few configurations that you're actually overriding in your config file - otherwise, you inherit the configurations from the top levels above.

To make this easy for you, command/4.default/config.yml always contains a list of all configurations and their default values.

As another handy feature, you can also simply enter configuration values right from the command line - for example:

* $ python Echomesh 'headless: true'
* $ python Echomesh 'logging: {"level": "debug"}'
* $ python Echomesh 'headless: true' 'logging: {"level": "debug"}'
