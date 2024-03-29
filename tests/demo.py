#!/usr/bin/env python

#Interphase - Copyright (C) 2009 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>
#
#"""
#Interphase Demo
#
#Interphase Module
#Project Site: https://gatc.ca/
#"""

from __future__ import division
import os
import random
import pygame as engine
import interphase

interphase.init(engine)


module_info = "Interphase Module\n\nThe module adds interface panel functionality to a Pygame application. It was developed as a simple GUI with the goal to simulate a digital display panel. The module provides interface and control objects to design a panel, with methods to manage the panel from the application code."


class InterfaceDemo(interphase.Interface):

    def __init__(self):
        self.screen, self.background, self.clock = self.initiate()
        w = self.screen.get_width() // 2
        h = self.screen.get_height() - 50
        interphase.Interface.__init__(
            self, position=(w,h), color=(43,50,58), size=(350,100),
            moveable=False, position_offset=(0,95), control_minsize=(25,25),
            control_size='auto', font_color=(175,180,185),
            tips_fontcolor=(175,180,185), scroll_button='both')
        self.puzzle = False
        self.puzzle_init = False
        self.puzzle_panel = None
        self.puzzle_interface = None
        self.doc_init = False
        self.doc_browse = False
        self.doc_interface = None
        self.doc_panel = None
        self.update_rect = []

    def add_controls(self):
        "Add interface controls"
        Control_list = [
            'Intro Textbox', 'Control 1', 'Control 2',
            'Layout', 'Puzzle', 'Doc', 'Exit']
        Control_tip = [
            'Interphase Intro', 'Control Panel 1', 'Control Panel 2',
            'Control Placement', 'Sliding Control', 'Interphase Doc',
            'Click to Exit']
        Control_link = [
            ['Interphase'], ['Select1'], ['Setting1', 'Setting2', 'Files'],
            ['Moveable'],['Puzzle'], ['Doc'] , ['Interphase_url']]
        self.add(
            identity = 'Control',
            control_type = 'function_select',
            position = (50,50),
            size = 'min',
            control_list = Control_list,
            tip_list = Control_tip,
            link = Control_link,
            link_activated = True,
            control_outline = True,
            event = True)
        self.add(
            identity = 'Interphase',
            control_type = 'textbox',
            position = (210,62),
            size = (219,64),
            color = (49,57,65),
            font_color = (125,175,200),
            font_size = 12,
            font_type = 'arial',
            control_list = [module_info],
            text_paste = True,
            label_display = False)
        self.add(
            identity = 'Select1',
            control_type = 'function_toggle',
            position = (150,50),
            size = (30,30),
            control_list = ['ON', 'OFF'],
            link = [ ['Select2'], [] ])
        self.add(
            identity = 'Select2',
            control_type = 'control_toggle',
            position = (200,50),
            size = (30,30),
            control_list = ['G', 'A', 'T', 'C'])
        self.add(
            identity = 'Setting1',
            control_type = 'control_select',
            position = (230,30),
            size = (30,30),
            control_list = ['__alphanumeric'],
            loop = True)
        self.add(
            identity = 'Setting2',
            control_type = 'control_select',
            position = (230,75),
            size = (30,30),
            control_list = ['__numeric', (0,42)])
        self.add(
            identity = 'Files',
            control_type = 'control_select',
            position = (140,50),
            size = 'auto_width',
            control_list = ['__filelist', '', '', 'py'])
        self.add(
            identity = '__Fix',
            control_type = 'control_toggle',
            position = (295,15),
            color = (0,20,30),
            font_color = (0,120,160),
            control_list = ['!'],
            control_outline = True)
        self.add(
            identity = '__Link',
            control_type = 'control_toggle',
            position = (315,15),
            color = (0,20,30),
            font_color = (0,120,160),
            control_list = ['*'],
            control_outline = True)
        self.add(
            identity = '__Help',
            control_type = 'control_toggle',
            position = (335,15),
            color = (0,20,30),
            font_color = (0,120,160),
            control_list = ['?'],
            control_outline = True)
        self.add(
            identity = '__Position',
            control_type = 'label',
            position = (335,98),
            control_list = [])
        self.add(
            identity = 'Moveable',
            control_type = 'control_toggle',
            position = (175,50),
            size = (40,40),
            control_list = ['Move'],
            tip_list = ['Moveable Control'],
            label_display = False)
        self.add(
            identity = 'Previous',
            control_type = 'control_toggle',
            position = (240,50),
            size = (25,25),
            control_list = ['<'],
            label_display = False,
            active = False)
        self.add(
            identity = 'Next',
            control_type = 'control_toggle',
            position = (265,50),
            size = (25,25),
            control_list = ['>'],
            label_display = False,
            active = False)
        self.add(
            identity = 'Doc',
            control_type = 'control_toggle',
            position = (175,50),
            size = (40,40),
            control_list = ['Doc Browse'],
            tip_list = ["Documentation"],
            label_display = False)
        self.add(
            identity = 'Puzzle',
            control_type = 'control_toggle',
            position = (175,50),
            size = (40,40),
            control_list = ['Start', 'Stop'],
            tip_list = ['Start Puzzle', 'Stop Puzzle'],
            label_display = False)
        self.add(
            identity = 'Interphase_url',
            control_type = 'control_toggle',
            size = 'min_width',
            position = (175,50),
            font_size = 12,
            control_list = ['Interphase https://gatc.ca'],
            tip_list = ['Access Site'],
            label_display = False)
        self.get_control('Next').add_action(self.doc_control)
        self.get_control('Previous').add_action(self.doc_control)
        self.get_control('Interphase_url').add_action(self.launch_url)

    def initiate(self):
        "Initiate demo"
        engine.display.set_caption('Interphase')
        screen = engine.display.get_surface()
        background = engine.Surface(screen.get_size())
        clock = engine.time.Clock()
        engine.event.set_blocked(engine.MOUSEMOTION)
        return screen, background, clock

    def event_check(self):
        "Check user input"
        terminate = False
        for event in engine.event.get():
            if event.type == interphase.EVENT['controlselect']:
                if (event.state.control == 'Control' and
                    event.state.button == 'Control'):
                    if event.state.value == 'Exit':
                        terminate = True
            elif event.type == engine.KEYDOWN:
                if event.key == engine.K_ESCAPE:
                    terminate = True
            elif event.type == engine.QUIT:
                terminate = True
        self.clock.tick(40)
        return terminate

    def doc_control(self, control, value):
        "Documentation browse control"
        if control in ['Next', 'Previous']:
            if self.doc_browse:
                self.doc_interface.browse(control)

    def launch_url(self, control=None, value=None):
        "Launch module webpage"
        try:
            import webbrowser
            webbrowser.open(value.split()[1])
        except:
            pass

    def update(self):
        """
        Interface update returns state object.

        State Object
            panel:              Interface panel
            controls:           Interface controls
            panel_active        Panel active
            panel_update        Panel update
            panel_interact:     Pointer interface interact
            control_interact:   Pointer control interact
            button_interact:    Pointer button interact
            control:            Control selected
            button:             Button selected
            value:              Control value
            values:             Panel control values
        """
        state = interphase.Interface.update(self)
        if state.control:
            if state.control == 'Select1':
                if state.value == 'ON':
                    self.set_panel_image()
                    self.set_control_image()
                    self.set_button_image()
                elif state.value == 'OFF':
                    self.set_panel_image('none')
                    self.set_control_image('none')
                    self.set_button_image('none')
            elif state.control == '__Fix':
                self.set_moveable()
            elif state.control == '__Link':
                state.controls['Control'].set_link_activated()
            elif state.control == 'Moveable':
                self.set_control_moveable()
                if self.is_control_moveable():
                    self.set_control_move(state.control,
                                          mouse_visible=False)
                    self.disable_control('Control', '__Fix',
                                         '__Link', '__Help')
                else:
                    state.controls[self.get_control_move()].set_tip(
                        ['Moveable Control'])
                    self.set_control_move(None)
                    self.enable_control('Control', '__Fix',
                                        '__Link', '__Help')
            elif state.control == 'Puzzle':
                if not self.puzzle:
                    self.puzzle = True
                    state.controls['Control'].set_active(False)
                else:
                    self.puzzle_interface = None
                    self.puzzle_panel = None
                    self.puzzle_init = False
                    self.puzzle = False
                    state.controls['Control'].set_active(True)
                    rect = self.screen.blit(self.background, (0,0),
                                            (0,0,self.screen.get_width(),
                                             self.screen.get_height()-100))
                    self.update_rect.append(rect)
            elif state.control == '__Help':
                self.set_info_display()
                self.set_label_display()
                self.set_tips_display()
                self.set_pointer_interact()
                if state.controls['__Position'].get_value():
                    state.controls['__Position'].set_value('')
            elif state.control == 'Doc':
                    if not self.doc_browse:
                        for control in ('Previous', 'Next'):
                            state.controls[control].set_active(True)
                        self.panel_update()
                        self.doc_browse = True
                    else:
                        for control in ('Previous', 'Next'):
                            state.controls[control].set_active(False)
                        self.doc_interface = None
                        self.doc_panel = None
                        self.doc_init = False
                        self.doc_browse = False
                        rect = self.screen.blit(self.background, (0,0),
                                                (0,0,self.screen.get_width(),
                                                 self.screen.get_height()-100))
                        self.update_rect.append(rect)
            elif state.control == 'Control':
                if self.doc_browse:
                    for control in ('Previous', 'Next'):
                        state.controls[control].set_active(False)
                    self.doc_interface = None
                    self.doc_panel = None
                    self.doc_init = False
                    self.doc_browse = False
                    rect = self.screen.blit(self.background, (0,0),
                                            (0,0,self.screen.get_width(),
                                             self.screen.get_height()-100))
                    self.update_rect.append(rect)
        if self.is_control_moveable():
            self.move_control()
            if self.is_tips_display():
                ctrl = self.get_control(self.get_control_move())
                ctrl.set_tip([str(ctrl.get_position())])
        if self.puzzle:
            if not self.puzzle_init:
                self.puzzle_interface = InterfacePuzzle(self.screen)
                self.puzzle_panel = engine.sprite.RenderUpdates(
                    self.puzzle_interface)
                if state.values['Select1'] == 'OFF':
                    self.puzzle_interface.set_control_image('none')
                    self.puzzle_interface.panel_update()
                self.puzzle_init = True
            self.puzzle_panel.update()
            if self.puzzle_interface.get_state().panel_update:
                self.puzzle_panel.clear(self.screen, self.background)
                self.update_rect.extend(self.puzzle_panel.draw(self.screen))
        if self.doc_browse:
            if not self.doc_init:
                self.doc_interface = InterfaceDoc(self.screen)
                self.doc_panel = engine.sprite.RenderUpdates(
                    self.doc_interface)
                if state.values['Select1'] == 'OFF':
                    self.doc_interface.set_control_image('none')
                    self.doc_interface.set_button_image('none')
                    self.doc_interface.panel_update()
                self.doc_init = True
            self.doc_panel.update()
            if self.doc_interface.get_state().panel_update:
                self.update_rect.extend(self.doc_panel.draw(self.screen))
        if self.is_info_display():
            if state.control_interact:
                self.add_info(state.control_interact, ':')
                self.add_info(
                    ' '.join(str(state.values[state.control_interact])
                    .split()[0:2]))
                if state.button:
                    self.add_info(state.button)
            if self.puzzle and self.puzzle_interface.is_active():
                state_puzzle = self.puzzle_interface.get_state()
                if state_puzzle.control:
                    self.add_info(state_puzzle.control)
            if state.panel_interact:
                mouse_x, mouse_y = self.get_pointer_position()
                x, y = self.get_position()
                size = self.get_size()
                pos = (mouse_x - x + (size[0]//2),
                       mouse_y - y + (size[1]//2))
                state.controls['__Position'].set_value(pos)
            else:
                if state.controls['__Position'].get_value():
                    state.controls['__Position'].set_value('')
        terminate = self.event_check()
        if terminate:
            self.deactivate()
        return state


class InterfaceDoc(interphase.Interface):

    def __init__(self, display):
        w, h = display.get_size()
        interphase.Interface.__init__(
            self, identity='Interface_Doc', position=(0.5,(h//2)-50),
            color=(43,50,58), image='none', size=(int(w*0.94),int(h*0.55)),
            screen=(w,h), font_color=(175,180,185), scroll_button='vertical')
        self.textbox = self.get_control('Doc')
        self.textbox.set_value(self.generate_doc())
        self.page_lines = self.textbox.get_line_max()
        self.line_step = self.page_lines
        self.next_move = 0
        self.prev_move = 0

    def add_controls(self):
        "Add interface controls"
        self.add(
            identity = 'Doc',
            control_type = 'textbox',
            position = (0.5,0.5),
            size = (self.get_size()[0] - 34, self.get_size()[1] - 34),
            color = (19,22,26),
            font_color = (150,150,150),
            font_size = 12,
            font_type = 'arial',
            label_display = False)

    def generate_doc(self):
        "Retrieve documentation"
        try:
            f = open(os.path.join('docs', 'guide.txt'), 'r')
            doc = f.read()
        except IOError:
            doc = None
        else:
            f.close()
        if not doc:
            msg = '\n\nDocumentation in guide.txt unable to be accessed.'
            doc = module_info + msg
        return doc

    def browse(self, control, value=None):
        "Documentation browse control"
        if control == 'Next':
            self.next_move = self.page_lines
        elif control == 'Previous':
            self.prev_move = self.page_lines

    def update(self):
        "Documentation interface update"
        interphase.Interface.update(self)
        if self.next_move:
            self.textbox.next(self.line_step)
            self.next_move -= self.line_step
        elif self.prev_move:
            self.textbox.previous(self.line_step)
            self.prev_move -= self.line_step


class InterfacePuzzle(interphase.Interface):

    def __init__(self, display):
        self.puzzle_initiate()
        w, h = display.get_size()
        interphase.Interface.__init__(
            self, identity='Interface_Puzzle', position=(0.5,(h//2)-50),
            color=(23,30,38), size=(180,180), screen=(w,h),
            font_color=(175,180,185))
        self.puzzle_outline()

    def add_controls(self):
        "Add interface controls"
        positions = [pos for pos in self.grid_positions
                     if pos != self.grid_blank]
        for index, pos in enumerate(positions):
            self.add(
                identity = str(index+1),
                control_type = 'control_toggle',
                position = ((pos[0] * self.grid_size[0]) + self.grid_xy[0],
                            (pos[1] * self.grid_size[1]) + self.grid_xy[1]),
                size = self.grid_size,
                color = (14,20,27),
                fill = 2,
                control_list = [str(index+1)],
                label_display = False)
        self.add(
            identity = 'Start',
            control_type = 'control_toggle',
            position = (150,150),
            size = self.grid_size,
            color = (14,20,27),
            control_list = ['Go'],
            font_color=(255,255,255),
            label_display = False)

    def puzzle_initiate(self):
        "Initiate puzzle"
        self.grid_positions = [(y,x) for x in range(4) for y in range(4)]
        self.grid = {}
        for index, pos in enumerate(self.grid_positions):
            self.grid[pos] = str(index+1)
        self.grid_id = [str(i) for i in range(1,16)]
        self.grid_blank = (3,3)
        self.grid_size = (40,40)
        self.grid_xy = (30,30)
        self.control_move = None
        self.move_offset = None
        self.move_steps = 2
        self.move_rate = self.grid_size[0] // self.move_steps
        self.move_step = 0
        self.last_move = None
        self.count = 0
        self.grid_timer = 0
        self.grid_initialize = False
        self.puzzle_solving = False

    def puzzle_outline(self):
        "Draw outline around puzzle controls"
        panel_image = self.get_panel_image(change=True)
        engine.draw.rect(panel_image, (14,20,27), (10,10,160,160), 2)

    def init(self):
        "Shuffle puzzle controls"
        ctrl = self.get_control()
        ids = self.grid_id[:]
        if self.last_move:
            ids.remove(self.last_move)
        random.shuffle(ids)
        for id in ids:
            pos = ((ctrl[id].position[0] - self.grid_xy[0]
                    + (ctrl[id].size[0]//2)) // ctrl[id].size[0],
                   (ctrl[id].position[1] - self.grid_xy[1]
                    + (ctrl[id].size[1]//2)) // ctrl[id].size[1])
            if ((pos[0] == self.grid_blank[0] and
                abs(pos[1]-self.grid_blank[1]) == 1) or
                (pos[1] == self.grid_blank[1] and
                abs(pos[0]-self.grid_blank[0]) == 1)):
                break

        for id in ids:
            pos = ((ctrl[id].position[0] - self.grid_xy[0]
                   + (ctrl[id].size[0]//2)) // ctrl[id].size[0],
                  (ctrl[id].position[1] - self.grid_xy[1]
                   + (ctrl[id].size[1]//2)) // ctrl[id].size[1])
            if ((pos[0] == self.grid_blank[0] and
                abs(pos[1]-self.grid_blank[1]) == 1) or
               (pos[1] == self.grid_blank[1] and
                abs(pos[0]-self.grid_blank[0]) == 1)):
                break
        self.last_move = id
        self.control_move = id
        self.move_offset = (self.grid_blank[0] * self.move_rate
                            - pos[0] * self.move_rate,
                            self.grid_blank[1] * self.move_rate
                            - pos[1] * self.move_rate)
        self.grid_blank = pos
        self.count += 1
        if self.count > 100 and self.grid_blank == (3,3):
            self.count = 0
            return True
        else:
            return False

    def puzzle(self, state):
        "Slide puzzle controls"
        ctrl = self.get_control(state.control)
        pos = ((ctrl.position[0] - self.grid_xy[0]
                + (ctrl.size[0]//2)) // ctrl.size[0],
               (ctrl.position[1] - self.grid_xy[1]
                + (ctrl.size[1]//2)) // ctrl.size[1])
        if ((pos[0] == self.grid_blank[0] and
             abs(pos[1]-self.grid_blank[1]) == 1) or
            (pos[1] == self.grid_blank[1] and
             abs(pos[0]-self.grid_blank[0]) == 1)):
            self.move_offset = (self.grid_blank[0] * self.move_rate
                                - pos[0] * self.move_rate,
                                self.grid_blank[1] * self.move_rate
                                - pos[1] * self.move_rate)
            self.control_move = state.control
            self.grid_blank = pos

    def puzzle_final(self):
        "Check if puzzle is complete"
        controls = self.get_control()
        success = True
        for id in self.grid_id:
            pos = ((controls[id].position[0] - self.grid_xy[0]
                    + (controls[id].size[0]//2)) // controls[id].size[0],
                   (controls[id].position[1] - self.grid_xy[1]
                    + (controls[id].size[1]//2)) // controls[id].size[1])
            if controls[id].value != self.grid[pos]:
                success = False
                break
        return success

    def move(self):
        "Puzzle control move"
        if self.move_step < self.move_steps:
            self.move_control(self.control_move,
                              offset=self.move_offset)
            self.move_step += 1
            complete = False
        else:
            self.control_move = None
            self.move_step = 0
            complete = True
        return complete

    def update(self):
        "Puzzle update"
        interphase.Interface.update(self)
        state = self.get_state()
        if state.control == 'Start':
            self.get_control('Start').set_active(False)
            self.grid_initialize = True
        if self.grid_initialize:
            if self.control_move:
                self.move()
                return
            complete = self.init()
            if complete:
                self.grid_initialize = False
                self.puzzle_solving = True
                self.grid_timer = engine.time.get_ticks()
        if self.puzzle_solving:
            if self.control_move:
                complete = self.move()
                if complete:
                    success = self.puzzle_final()
                    if success:
                        self.puzzle_solving = False
                        time = ((engine.time.get_ticks()
                                 - self.grid_timer) // 1000)
                        control_start = self.get_control('Start')
                        control_start.set_value(str(time)+'s')
                        control_start.set_active(True)
                return
            else:
                if state.control:
                    self.puzzle(state)
            return


def setup(width,height):
    engine.display.init()
    engine.display.set_mode((width,height))


def run():
    panel = InterfaceDemo()
    run_demo = True
    while run_demo:
        panel.update()
        if panel.is_active():
            if panel.is_update():
                panel.clear(panel.screen,panel.background)
                panel.update_rect.extend(panel.draw(panel.screen))
            if panel.update_rect:
                engine.display.update(panel.update_rect)
                panel.update_rect = []
        else:
            run_demo = False
    engine.quit()


def main():
    setup(400,320)
    run()


if __name__ == '__main__':
    main()

