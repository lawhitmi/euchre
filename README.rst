======
Euchre
======

A simple game of two-handed Euchre for the command line.

Description
===========

This project was created for an Advanced Software Engineering class to learn about and apply several aspects of the
software design process.

Euchre is a simple card game played with a 24 card deck (9 through Ace of each suit).  The objective of the game is to
play higher cards to win 'tricks'.  The first player to 10 'tricks' wins.  For further information on how the game is
played, visit `this website <https://www.thesprucecrafts.com/twohanded-euchre-card-game-rules-411489>`__.

1. UML
===========
Bidding Phase - Activity Diagram
--------------------------------

.. image:: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.github.com/lawhitmi/euchre/master/docs/UML/actDiag.puml

Class Diagram
-------------

.. image:: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.github.com/lawhitmi/euchre/master/docs/UML/classDiag.puml

Use Case Diagram
----------------

.. image:: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.github.com/lawhitmi/euchre/master/docs/UML/useCaseDiag.puml

NEED ONE SENTENCE HERE.

NEED A FEW SENTENCES HERE.

2. Metrics
===========
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=alert_status
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=sqale_index
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=code_smells

Sonarcloud.io was used for this project.  See the .sonarcloud.properties file in the root of the project for details
about use.

NEED A FEW SENTENCES HERE. Note that a lot of refactoring and code complexity issues were identified and fixed through
the use of this tool.

3. Clean Code
=============

 #. Don't Repeat Yourself (DRY) - Sonarcloud helps out with this principle by pointing out chunks of code which are
    repeated.  One such instance was my code to solicit input from the user.  I originally had several similar try-catch
    statements which I pulled out into a single function.
    Link to function: `Function <https://github.com/lawhitmi/euchre/blob/a9721b79ddac1d64d1000cb292d8ba878371a76a/src/euchre/hands.py#L1>`__

 #. Source Code Conventions - `PEP8 <https://www.python.org/dev/peps/pep-0008/>`__

 #. Single Responsibility Principle - See deck class

 #. Integration Operation Segregation Principle (IOSP) - See Hands classes.

 #.

NEED A LINK HERE TO YOUR CHEATSHEET WITH 10 PRINCIPLES.

4. Build Management
===================

.. image:: https://readthedocs.org/projects/euchre/badge/?version=latest&style=plastic

Setuptools was used for this project due to its excellent integration with the python build and test processes.

https://euchre.readthedocs.io/en/latest/index.html

I had originally installed Gradle to perform the build management tasks for this projects, but found little documentation
on its use with Python packages.  In my attempt to use Gradle, I found I was creating scripts to run Setuptools build
and testing commands. This added layer of scripts seemed to be a inefficient method of performing the build management.
For this reason, I fell back on Setuptools.

5. Testing
===========

Pytest was used to automate testing for this project.

NEED A FEW SENTENCES HERE.

6. Continuous Delivery
======================
Travis-CI was used to automate build and testing tasks with each push to github.

.. image:: https://travis-ci.org/lawhitmi/euchre.svg?branch=master
.. image:: https://github.com/lawhitmi/euchre/workflows/Python%20application/badge.svg

NEED A FEW SENTENCES HERE.

7. IDE
===========

Pycharm was used for this project.

 * Ctrl-k - commit, followed by Ctrl-Alt-k for 'Commit and Push'
 * Shift-F10 - run
 * Shift-F9 - debug
 * Ctrl-Alt-Shift-T - opens refactor dialog
 * Ctrl-Tab - File switcher
 * Alt-(number) - Switch to other IDE elements

NEED A FEW SENTENCES HERE.

8. DSL
===========
https://github.com/lawhitmi/hello-world

NEED A FEW SENTENCES HERE.

9. Functional Programming
=========================

NEED A FEW SENTENCES HERE.





Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
