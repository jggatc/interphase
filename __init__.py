#Interphase - Pygame Interface Module
#Copyright (C) 2009 James Garnon

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
#
#Interphase version 0.86
#Download Site: http://gatc.ca


try:
    import pygame as engine
except ImportError:
    engine = None


initialized = False


def get_init():
    """
    Check if module is initialized.
    """
    return initialized


def _init(engine):
    global Interface, EVENT, Control, FunctionControl, Label, Textbox, Text, load_image, __version__, initialized
    import env
    env.engine = engine
    from interface import Interface, EVENT
    from control import Control, FunctionControl, Label, Textbox
    from util import Text, load_image
    from version import __version__
    initialized = True


def init(engine):
    """
    Initialize module. Argument engine is the multimedia framework object.
    Engine can be Pygame, PyJ2D, or Pyjsdl.
    Module initialized if Pygame can be imported.
    """
    if initialized:
        return
    _init(engine)
    if engine.__name__ == 'pyjsdl':
        from image import _load_default_images
        _load_default_images()


if engine:
    _init(engine)

