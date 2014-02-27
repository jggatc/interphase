#!/usr/bin/env python

"""
Interphase Module

The module adds interface panel functionality to a Pygame application. It was developed as a simple GUI with the goal to simulate a digital display panel. The module provides interface and control objects to design a panel, and numerous methods to manage the panel from the application code. Run interphase.py separately for an interface panel demo that is coded in test.py.

To utilize the module, place the interphase folder in the path or within script folder, and import the module to the application with the statement 'import interphase'. A zip of the interphase folder can also be used with the statement "sys.path.insert(0,'./interphase_zipfile')" prior to import.

To design an interface panel, interphase.Interface can be subclassed. Within the __init__() method call interphase.Interface.__init__(). Interface Object provides several methods to design and utilize an interface panel. Use add() to add controls to panel, place into a method called add_controls(); if added otherwise call activate() after to activate the panel. The program maintains the update of the panel including changes through the methods, however panel_update() can be used to force an update if required. If the Interface Object is subclassed, when overriding the update() method call interphase.Interface.update(). Interface interaction can be maintained with the InterfaceState object, that is returned by update() or get_state(), or through pygame event queue checking for event.type interphase.EVENT['controlselect'] and interphase.EVENT['controlinteract'] with the attribute event.state that references the InterfaceState object. To turn the panel off, deactivate() sets state.active to false. The panel can be drawn to the display with the draw() method.


InterfaceState Object:

panel:
  - Interface panel (instance panel object)
controls:
  - Interface controls (dict {id:object} panel controls object)
panel_active:
  - Panel active (bool panel active)
panel_update:
    Panel update (bool panel update)
panel_interact:
  - Pointer interface interact (bool pointer interact with panel)
control_interact:
  - Pointer control interact ('id' control interact)
button_interact:
  - Pointer button interact ('id' button interact)
control:
  - Control selected ('id' selected control)
button:
  - Button selected ('id' selected button ('id','id_top','id_bottom'))
value:
  - Control value ('value' current value of selected control)
values:
  - Panel control values (dict {'id':value} values of all controls)


Interface Object methods:

add, add_control, activate, deactivate, is_active, get_state, get_value, get_control, remove_control, enable_control, disable_control, update, panel_update, draw, clear, set_panel_display, get_id, set_panel_image, set_control_image, set_button_image, get_panel_image, get_default_image, move, set_moveable, is_moveable, set_label_display, is_label_display, get_size, get_position, move_control, get_control_move, set_control_move, set_control_moveable, is_control_moveable, set_tips_display, is_tips_display, get_pointer_position, set_pointer_interact, set_info_display, is_info_display, add_info, clear_info, is_update, set_update, set_panel_function, get_clipboard, set_clipboard.


Control Object methods:

get_value, set_value, get_list, set_list, remove_list, set_list_icon, set_control_image, set_link, set_link_activated, set_activated, is_activated, set_activated_lock, is_activated_lock, set_active, is_active, next, previous, reset, get_position, set_display_text, set_label_text, get_tip, set_tip, get_id, set_label, get_label, resize_control, set_enabled, is_enabled, get_size, set_color, get_list_index, set_list_index, add_action, format_text, add_format, set_scroll_line, text_copy, text_paste, set_line_max, get_line_max, set_line_width, get_line_width, get_text, get_display_text, set_text_margin, get_text_margin, check_size.
"""

#Interphase - Pygame Interface Module
#Copyright (C) 2009 James Garnon
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public License
#along with this library; if not, see http://www.gnu.org/licenses/.

__docformat__ = 'restructuredtext'

from interface import Interface, EVENT
from control import Control, FunctionControl, Label, Textbox
from util import Text, load_image
from version import __version__
import warnings
warnings.filterwarnings("ignore")


def main():
    try:
        import test
        test.run()
    except ImportError:
        print("Warning: test.py not found.")

if __name__ == '__main__':
    main()

