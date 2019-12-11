# Cmod

C Module Manager for Test driven embedded systems

Cmod is a collection of python scripts and classes that support structured software development techniques,
which in turn, simplifies other tasks like unit testing, TDD, and general code maintainence. Once you try it out
with a simple demo project, you'll see why this may be especially helpful for embedded systems projects using the
C language.

Here's the main thing you need to know about Cmod before you integrate it into a project:
Cmod allows you to manage your project as a collection of testable modules.

Cmod's definition of a module is just a directory in your project that contains a special file marking it as so.
This lets you populate your modules with as much or as little production code as you like, since there is no
agreed-upon definition of the heavily abused term "module".

With Cmod's module definition, it is advisable to start organizing your code using a block diagram. It should show your project's
varying code units, and how they relate to each other in the project directory - not necessarily how they might depend on one-another.

Block diagrams add a large number of organizational benefits to your project - even before you have any code written, so
take some time to draw yourself a picture of what you want to codebase to look and feel like.

Use the back of a napkin to start, or just type out your desired project directory tree to start.

For formal projects, Gliffy is a good option for professional-looking visualization.

Before we can do anything with your project's modules, you will also need to spend some time describing your
project preferences to Cmod by filling out any relevant fields you find in config.txt. There is a more detailed
guide about this here:

After your config.ini file is more customized apart from the default settings, you can generate some C modules
for your project. Cmod will follow your project description in config.ini, and produce ready-to-test
modules that fit your project's coding style and use your preferred unit test harness!