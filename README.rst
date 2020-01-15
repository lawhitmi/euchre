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


PlantUML was used to generate UML diagrams for this project. Because it is text-based, it can easily be versioned along
with the rest of the code.  Passing the .puml files in github to the plantuml website allows rendering of the UML
diagrams within the README document.


2. Metrics
===========
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=alert_status
    :target: https://sonarcloud.io/dashboard?id=lawhitmi_euchre
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=sqale_index
    :target: https://sonarcloud.io/dashboard?id=lawhitmi_euchre
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=code_smells
    :target: https://sonarcloud.io/dashboard?id=lawhitmi_euchre
.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=ncloc
    :target: https://sonarcloud.io/dashboard?id=lawhitmi_euchre

Sonarcloud.io was used for this project.  Click on one of the badges above to see the sonarcloud.io interface.

I found the 'Code Smells' metric here particularly helpful as it identifies code that is too 'cognitively complex'.  It
analyzes the number of arguments, the depth of nested flow control structures, and other traits to provide a complexity
score and recommends the refactoring of code which exceeds a certain limit.  Sonarcloud also helps with PEP8 compliance
by pointing out naming inconsistencies.

3. Clean Code
=============

 #. Don't Repeat Yourself (DRY) - `Function <https://github.com/lawhitmi/euchre/blob/master/src/euchre/hands.py#L1>`__

        Sonarcloud helps out with this principle by pointing out chunks of code which are
        repeated.  One such instance was my code to solicit input from the user.  I originally had several similar try-catch
        statements which I pulled out into a single function. See link above.

 #. Source Code Conventions - `PEP8 <https://www.python.org/dev/peps/pep-0008/>`__

        Naming of `variables <https://github.com/lawhitmi/euchre/blob/c03efef45c0ca504d881d0f225a31fec92b0d431/src/euchre/deck.py#L9>`__
        , `classes <https://github.com/lawhitmi/euchre/blob/c03efef45c0ca504d881d0f225a31fec92b0d431/src/euchre/hands.py#L97>`__
        , `methods <https://github.com/lawhitmi/euchre/blob/c03efef45c0ca504d881d0f225a31fec92b0d431/src/euchre/hands.py#L149>`__
        , and `functions <https://github.com/lawhitmi/euchre/blob/c03efef45c0ca504d881d0f225a31fec92b0d431/src/euchre/hands.py#L1>`__
        were refactored to comply with PEP8 recommendations.

 #. Single Responsibility Principle - `Deck Module <https://github.com/lawhitmi/euchre/blob/master/src/euchre/deck.py>`__

        This deck class controls the building and dealing of the cards.  The only reason this class would change would be
        if the deck itself needed to change.

 #. Integration Operation Segregation Principle (IOSP) - See Hands classes.



 #. Separation of Concerns (SoC) -



Link to `Cheatsheet <https://github.com/lawhitmi/euchre/blob/master/docs/CC_cheatsheet.rst>`__

4. Build Management
===================

Setuptools was used for this project due to its excellent integration with the python build and test processes. See the
`setup.cfg <https://github.com/lawhitmi/euchre/blob/master/setup.cfg>`__ for the tasks (build, build_sphinx, tests).

`Readthedocs <https://euchre.readthedocs.io/en/latest/index.html>`__ was used for hosting the documentation for this build.

.. image:: https://readthedocs.org/projects/euchre/badge/?version=latest&style=plastic
    :target: https://euchre.readthedocs.io/en/latest/index.html


I had originally installed Gradle to perform the build management tasks for this projects, but found little documentation
on its use with Python packages.  In my attempt to use Gradle, I found I was creating scripts to run Setuptools build
and testing commands. This added layer of scripts seemed to be a inefficient method of performing the build management.
For this reason, I fell back on Setuptools.

5. Testing
===========
Pytest was used to automate testing for this project.

.. image:: https://sonarcloud.io/api/project_badges/measure?project=lawhitmi_euchre&metric=coverage

This package provides useful `decorator tools <https://github.com/lawhitmi/euchre/blob/c03efef45c0ca504d881d0f225a31fec92b0d431/tests/conftest.py#L40>`__
for mocking up the dependencies for unit testing.  The Pytest-cov package provides coverage metrics for the tests as well.
The coverage report from pytest-cov is shown in the images below. It also works seamlessly with Setuptools, for easy downstream use of CI tools.

.. image:: https://github.com/lawhitmi/euchre/blob/master/docs/test-coverage.png


6. Continuous Delivery
======================
Travis-CI was used to automate build and testing tasks with each push to github.

.. image:: https://travis-ci.org/lawhitmi/euchre.svg?branch=master
    :target: https://travis-ci.org/lawhitmi/euchre
.. image:: https://github.com/lawhitmi/euchre/workflows/Python%20application/badge.svg

The `.travis.yml <https://github.com/lawhitmi/euchre/blob/master/.travis.yml>`__ file gives the setup for the Travis-CI build.  The Setuptools package was used to perform a build of the
package, run the testing, and to build the documentation.

7. IDE
===========

Jetbrains Pycharm was used for this project.

 * Ctrl-k - commit, followed by Ctrl-Alt-k for 'Commit and Push'
 * Shift-F10 - run
 * Shift-F9 - debug
 * Ctrl-Alt-Shift-T - opens refactor dialog
 * Ctrl-Tab - File switcher
 * Alt-(number) - Switch to other IDE elements

In addition to the features provided by the hotkeys above, Pycharm provides several other powerful and timesaving
features.  The one I used most frequently was the automatic docstring generation.  To add docstrings, simply type
""" and press enter.  Pycharm parses through the arguments to the function and automatically generates a stub in the
format of your choice and includes the list of arguments and a 'result' tag.

The continuous linting that the IDE performs is also quite useful.  It has the ability to make naming suggestions,
identify when a variable is used before it is set, identify when a variable is set and never referenced, as well as many
other useful checks.

8. DSL
===========

A Domain Specific Language is included in the 'conversiondsl' package `here <https://github.com/lawhitmi/euchre/blob/master/src/conversiondsl/>`__
This is a simple DSL for converting between units of measurement using natural language. For example, the following can
be passed to the parser.

::

    convert 1-2-9/16 ft to m

and this will be returned

::

    0.38 m


9. Functional Programming
=========================

The DSL above was created using functional programming principles.

#. only final data structures
#. (mostly) side effect free functions
#. the use of higher order functions
#. functions as parameters and return values
#. use clojures / anonymous functions





Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.


