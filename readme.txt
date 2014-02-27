Interphase - Pygame Interface Module

The module adds interface panel functionality to a Pygame application. It was developed as a simple GUI with the goal to simulate a digital display panel. The module provides interface and control objects to design a panel, and numerous methods to manage the panel from the application code. Run interphase.py separately for an interface panel demo that is coded in test.py. The module requires Python 2.5+ (http://www.python.org/) and Pygame 1.8+ (http://www.pygame.org/).

To utilize the module, place the interphase folder in the path or within script folder, and import the module to the application with the statement 'import interphase'. A zip of the interphase folder can also be used with the statement "sys.path.insert(0,'./interphase_zipfile')" prior to import.

To design an interface panel, interphase.Interface can be subclassed. Within the __init__() method call interphase.Interface.__init__(). Interface Object provides several methods to design and utilize an interface panel. Use add() to add controls to panel, place into a method called add_controls(); if added otherwise call activate() after to activate the panel. The program maintains the update of the panel including changes through the methods, however panel_update() can be used to force an update if required. If the Interface Object is subclassed, when overriding the update() method call interphase.Interface.update(). Interface interaction can be maintained with the InterfaceState object, that is returned by update() or get_state(), or through pygame event queue checking for event.type interphase.EVENT['controlselect'] and interphase.EVENT['controlinteract'] with the attribute event.state that references the InterfaceState object. To turn the panel off, deactivate() sets state.active to false. The panel can be drawn to the display with the draw() method.

Interphase is released under LGPL, see license.txt for further information.

Interphase page: http://gatc.ca/projects/interphase/
Interphase docs: http://gatc.ca/projects/interphase/doc/

