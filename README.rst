======
euchre
======


A simple game of two-handed Euchre for the command line.


Description
===========

A longer description of your project goes here...

1. UML
===========


2. Metrics
===========
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=alert_status
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=sqale_index
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=code_smells

3. Clean Code
===========

 #. Don't Repeat Yourself (DRY) - Sonarcloud helps out with this principle by pointing out chunks of code which are
    repeated.  One such instance was my code to solicit input from the user.  I originally had several similar try-catch
    statements which I pulled out into a single function.
    Link to function: `Function <https://github.com/lawhitmi/euchre/blob/a9721b79ddac1d64d1000cb292d8ba878371a76a/src/euchre/hands.py#L1>`__

 #. Source Code Conventions - `PEP8 <https://www.python.org/dev/peps/pep-0008/>`__

 #. Single Responsibility Principle - See deck class

 #. Integration Operation Segregation Principle (IOSP) - See Hands classes.

 #.


4. Build Management
===========

Setuptools was used for this project due to its excellent integration with the python build and test processes.
Gradle

5. Testing
===========

Pytest was used to automate testing for this project.

6. Continuous Delivery
===========
Travis-CI was used to automate build and testing tasks with each push to github.

.. image:: https://travis-ci.org/lawhitmi/euchre.svg?branch=master


7. IDE
===========

Pycharm was used for this project.

 * Ctrl-k - commit, followed by Ctrl-Alt-k for 'Commit and Push'
 * Shift-F10 - run
 * Shift-F9 - debug
 * Ctrl-Alt-Shift-T - opens refactor dialog

DSL
===========
https://github.com/lawhitmi/hello-world

Functional Programming
===========

OPTIONAL-Logical Solver
===========

OPTIONAL-Code fragment in Scala or Clojure
===========

OPTIONAL-AOP
===========




Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
