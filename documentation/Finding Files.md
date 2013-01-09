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




The echomesh directory structure is organized that way too:

echomesh/
  asset/
  code/
  command/
  doc/
  logs/

