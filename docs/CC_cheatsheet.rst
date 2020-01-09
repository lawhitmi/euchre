=====================
Clean Code Cheatsheet
=====================

1. Favor Composition over Inheritance (FCoI)
============================================

Principle that classes should achieve polymorphic behavior and code reuse by their composition (by containing instances of other classes that implement the desired functionality) rather than inheritance from a base or parent class.

Inheritance Example::

    class Parent():
        def method():
            pass

    class Child(Parent): # Inheritance!
        def othermethod():
            pass


Composition Example::

    class Salary:
        def __init__(self, pay, bonus):
            self.pay=pay
            self.bonus=bonus
        def annual_salary(self):
            return (self.pay*12) + self.bonus
    class Employee:  # No Inheritance!
         def __init__(self, name, age, pay, bonus):
             self.name=name
             self.age=age
             self.obj_salary=Salary(pay, bonus) # Instantiate another class to gain its functionality
         def total_salary(self):
             return self.obj_salary.annual_salary()

2. Single Level of Abstraction (SLA)
====================================

Methods should be written at one level of abstraction.

Not this::

    class AddAttendee():
        def add_attendee():
            fill_in('user_email', 'test@gmail.com')
            fill_order_form()
        def fill_order_form():
            ...

Note that above, ``fill_in`` and ``fill_order_form()`` are different levels of abstraction.

Rather do this::

    class AddAttendee():
        def add_attendee():
            fill_attendee_details()
            fill_order_form()
        def fill_attendee_details():
            fill_in('user_email', 'test@gmail.com')
        def fill_order_form():
            ...

3. Principal of Least Astonishment
==================================

"What you expect is what you get"

4. Law of Demeter
=================

"Writing shy code" A module should only know its direct dependencies.

5. You Ain't Gonna Need It (YAGNI)
==================================

"Everything can be done later" Implement only what has an immediate benefit. If in doubt, decide against the effort.

6. Dependency Inversion Principle (DIP)
=======================================

Depend on abstractions, not on concretions.

7. Single Responsibility Principle (SRP)
========================================

A class should have one, and only one, reason to change.

8. Beware of Optimizations!
===========================

"Premature optimization is the root of all evil" -Donald Knuth

These efforts often lead to code which is not readable or understandable.

9. Liskov Substitution Principle (LSP)
======================================

Derived classes must be substitutable for their base classes.


10. Open/Closed Principle (OCP)
===============================

Class behavior should be extendable without modification.
