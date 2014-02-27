#"""
#Interphase
#Copyright (C) 2009 James Garnon
#"""

from __future__ import division
import pygame
import os
import zipfile
import cStringIO

__docformat__ = 'restructuredtext'


class Text(object):
    """
    Receives text to display on surface.
    
    Parameters:
        surface: 'surface' destination surface for text.
        font_type: [] list of font names
        font_size: int font size
    """

    _font = {}

    def __init__(self, surface, font_type=None, font_size=None):
        self.screen = surface
        x, y = self.screen.get_size()
        self.dimension = {'x':x, 'y':y}
        self.message = None
        self.messages = []
        if font_size:
            self.font_size = int(font_size)
        else:
            self.font_size = 10
        if isinstance(font_type, str):
            font_type = [font_type]
        if not Text._font:
            pygame.font.init()
            font = None
            if font_type:
                font_type = ','.join(font_type)
                if font_type.startswith('file:'):
                    font = font_type[5:].strip()
                    if not os.path.exists(font):
                        print('Font not found: %s' % font)
                        font = None
                else:
                    font = pygame.font.match_font(font_type)
            if not font:
                font_type = 'verdana, tahoma, bitstreamverasans, freesans, arial'
                font = pygame.font.match_font(font_type)
            Text._font['default'] = font
            Text._font['defaults'] = font_type
            Text._font[font] = { self.font_size:pygame.font.Font(font,self.font_size) }
            font_type = None
        if font_type:
            font_type = ','.join(font_type)
            if font_type != Text._font['defaults']:
                if font_type.startswith('file:'):
                    font_type = font_type[5:].strip()
                    if not os.path.exists(font_type):
                        print('Font not found: %s' % font_type)
                        font_type = None
                else:
                    font_type = pygame.font.match_font(font_type)
                if font_type:
                    if font_type not in Text._font:
                        Text._font[font_type] = { self.font_size:pygame.font.Font(font_type,self.font_size) }
                else:
                    font_type = Text._font['default']
            else:
                font_type = Text._font['default']
        else:
            font_type = Text._font['default']
        if self.font_size not in Text._font[font_type]:
            Text._font[font_type][self.font_size] = pygame.font.Font(font_type,self.font_size)
        self.font_type = font_type
        self.font = Text._font[self.font_type]
        self.x = 0
        self.y = 0
        self.center = False
        self.font_color = (255,0,0)
        self.font_bgcolor = (0,0,0)
        self.split_text = False
        self.linesize = self.font[self.font_size].get_linesize()
        self.margin = {'t':0, 'r':0, 'b':0, 'l':0}
        self.multiline = False
        self.text_surface = []

    def __call__(self, surface='default'):
        """Writes text to surface."""
        if surface == 'default':
            self.surface = self.screen
        else:
            self.surface = surface
        self.update()
        return self.surface

    def add(self,*message_append):
        """Add to text."""
        for item in message_append:
            self.message = str(item)
            self.messages.append(self.message)

    def set_position(self, position, center=False):
        """Set position to write text."""
        x, y = position
        if x < self.dimension['x'] and y < self.dimension['y']:
            self.x = x
            self.y = y
            if center:
                self.center = True
            return True
        else:
            return False

    def set_text_alignment(self, setting):
        """Set text alignment. Setting is 'center' or 'left'."""
        if setting == 'center':
            self.center = True
        elif setting == 'left':
            self.center = False

    def set_margin(self, margin):
        """Set text margin."""
        try:
            self.margin['t'], self.margin['r'], self.margin['b'], self.margin['l'] = margin
        except TypeError:
            self.margin['t'] = self.margin['r'] = self.margin['b'] = self.margin['l'] = margin

    def set_multiline(self, multiline=True):
        """Set multiline text."""
        self.multiline = multiline

    def set_font(self, font_type, default=False):
        """Set font of text."""
        if isinstance(font_type, str):
            font_type = [font_type]
        font_type = ','.join(font_type)
        if font_type == 'default':
            font_type = Text._font['default']
            self.font = Text._font[font_type]
            self.font_type = font_type
        elif font_type != Text._font['defaults']:
            if font_type.startswith('file:'):
                font = font_type[5:].strip()
                if not os.path.exists(font):
                    print('Font not found: %s' % font)
                    font = None
            else:
                font = pygame.font.match_font(font_type)
            if font:
                if font not in Text._font:
                    Text._font[font] = { self.font_size:pygame.font.Font(font,self.font_size) }
                self.font = Text._font[font]
                self.font_type = font
                if default:
                    Text._font['default'] = font
                    Text._font['defaults'] = font_type
        self.linesize = self.font[self.font_size].get_linesize()

    def get_font(self, font_info='font'):
        """Get current font."""
        if font_info == 'font':
            return self.font_type
        elif font_info == 'default':
            return Text._font['default']
        elif font_info == 'system':
            return pygame.font.get_fonts()

    def get_font_size(self):
        """Get current font size."""
        return self.font_size

    def set_font_size(self, size):
        """Set font size of text."""
        self.font_size = size
        if size not in Text._font[self.font_type]:
            Text._font[self.font_type][self.font_size] = pygame.font.Font(self.font_type,self.font_size)
        self.font = Text._font[self.font_type]
        self.linesize = self.font[self.font_size].get_linesize()

    def set_font_color(self, color):
        """Set font color of text."""
        self.font_color = color

    def set_font_bgcolor(self, color=None):
        """Set font background color."""
        self.font_bgcolor = color

    def set_split_text(self, split_text=True):
        """Set whether text split to new line at space."""
        self.split_text = split_text

    def check_size(self, text):
        """Get size required for given text."""
        width, height = self.font[self.font_size].size(text)
        return width, height

    def check_sizes(self, texts):
        """Get size required for a list of texts."""
        text_size = {}
        for text in texts:
            text_size[text] = self.check_size(text)
        return text_size

    def surface_size(self, *dim):
        """Surface size needed to fit text. Return estimated width for col and height for row, adjusted for margins."""
        try:
            col, row = dim[0], dim[1]
        except IndexError:
            col, row = dim[0]
        sizes = [self.check_size(char)[0] for char in 'abcdefghijklmnopqrstuvwxyz ']
        charsize = sum(sizes)//len(sizes)
        width = (col*charsize) + (self.margin['l']+self.margin['r'])
        height = ((row*self.linesize)-2) + (self.margin['t']+self.margin['b'])
        return width, height

    def word_wrap(self, text, width):
        """Format text lines to fit in surface width, adjusted for margins."""
        text_width = width - (self.margin['l']+self.margin['r'])
        if isinstance(text, list):
            textlines = text
        else:
            textlines = [line for line in text.splitlines()]
        txtlines = []
        line_num = 0
        space_size = self.check_size(' ')[0]
        while True:
            try:
                line = textlines[line_num]
            except IndexError:
                break
            if self.check_size(line)[0] > text_width:
                words = line.split(' ')
                txt_line = []
                size_sum = 0
                word_num = 0
                for word in words:
                    word_size = self.check_size(word)[0]
                    if word_size > text_width:
                        ln = self.split_long_text(word, text_width)
                        if txt_line:
                            txtlines.append(' '.join(txt_line))
                            txt_line = []
                            size_sum = 0
                            word_num = 0
                        txtlines.extend(ln)
                        continue
                    size_sum += word_size
                    if size_sum + word_num*space_size <= text_width:
                        txt_line.append(word)
                        word_num += 1
                    else:
                        txtlines.append(' '.join(txt_line))
                        txt_line = []
                        txt_line.append(word)
                        size_sum = word_size
                        word_num = 1
                if txt_line:
                    txtlines.append(' '.join(txt_line))
            else:
                txtlines.append(line)
            line_num += 1
        return txtlines

    def split_long_text(self, text, width):
        """Split long text uninterrupted by spaces to fit in surface width."""
        char_size = self.check_sizes(set(text))
        ln = []
        chars = []
        size_sum = 0
        for char in text:
            size_sum += char_size[char][0]
            if size_sum <= width:
                chars.append(char)
            else:
                ln.append(''.join(chars))
                chars = []
                chars.append(char)
                size_sum = char_size[char][0]
        if chars:
            ln.append(''.join(chars))
        return ln

    def has_text(self):
        """Check whether contains text."""
        if self.messages:
            return True
        else:
            return False

    def clear_text(self):
        """Clear text."""
        self.message = None
        self.messages = []

    def tprint(self):
        """Print text to surface."""
        if self.messages != []:
            self.text_surface = []
            if not self.multiline:
                text = " ".join(self.messages)
                if not self.split_text or text.strip().count(' ') == 0:
                    if self.font_bgcolor:
                        text_surface = self.font[self.font_size].render(text, True, self.font_color, self.font_bgcolor)
                    else:
                        text_surface = self.font[self.font_size].render(text, True, self.font_color)
                    if self.center:
                        center = text_surface.get_width()//2
                        x = self.x - center
                    else:
                        x = self.x + self.margin['l']
                    w, h = text_surface.get_size()
                    text_rect = pygame.Rect(x,self.y,w,h)
                    self.text_surface.append( (text_surface, text_rect) )
                    self.surface.blit(text_surface, (x,self.y))
                else:
                    words = text.count(' ')
                    position_y = self.y - words*(self.linesize//2) - 1
                    texts = text.split(' ')
                    for count, text in enumerate(texts):
                        if self.font_bgcolor:
                            text_surface = self.font[self.font_size].render(text, True, self.font_color, self.font_bgcolor)
                        else:
                            text_surface = self.font[self.font_size].render(text, True, self.font_color)
                        if self.center:
                            center = text_surface.get_width()//2
                            x = self.x - center
                            y = position_y + (count*self.linesize)
                        else:
                            x = self.x
                            y = position_y + (count*self.linesize)
                        w, h = text_surface.get_size()
                        text_rect = pygame.Rect(x,y,w,h)
                        self.text_surface.append( (text_surface, text_rect) )
                    for surface in self.text_surface:
                        self.surface.blit(surface[0], (surface[1].x,surface[1].y))
            else:
                position_y = self.y + self.margin['t']
                for count, text in enumerate(self.messages):
                    if self.font_bgcolor:
                        text_surface = self.font[self.font_size].render(text, True, self.font_color, self.font_bgcolor)
                    else:
                        text_surface = self.font[self.font_size].render(text, True, self.font_color)
                    if self.center:
                        center = text_surface.get_width()//2
                        x = self.x - center
                        y = position_y + (count*self.linesize)
                    else:
                        x = self.x + self.margin['l']
                        y = position_y + (count*self.linesize)
                    w, h = text_surface.get_size()
                    text_rect = pygame.Rect(x,y,w,h)
                    self.text_surface.append( (text_surface, text_rect) )
                for surface in self.text_surface:
                    self.surface.blit(surface[0], (surface[1].x,surface[1].y))
            self.message = None
            self.messages = []
            return self.text_surface

    def update(self):
        self.tprint()


def load_image(filename, frames=1, path='data', zipobj=None, fileobj=None, colorkey=None, errorhandle=True, errorreport=True):
    """Loads images."""
    #Modified from PygameChimpTutorial
    def convert_image(image, colorkey):
        if image.get_alpha():
            image = image.convert_alpha()
        else:
            image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    if zipobj:
        if isinstance(zipobj, str):
            if path:
                data_file = os.path.join(path, zipobj)
            else:
                data_file = zipobj
            dat = zipfile.ZipFile(data_file)
            fileobj = cStringIO.StringIO(dat.open(filename).read())
            dat.close()
        else:
            fileobj = cStringIO.StringIO(zipobj.open(filename).read())
        full_name = fileobj
        namehint = filename
    elif fileobj:
        full_name = fileobj
        namehint = filename
    else:
        if path:
            full_name = os.path.join(path, filename)
        else:
            full_name = filename
        namehint = ''
    try:
        if frames == 1:
            image = pygame.image.load(full_name, namehint)
            image = convert_image(image, colorkey)
            return image
        elif frames > 1:
            images = []
            image = pygame.image.load(full_name, namehint)
            width, height = image.get_size()
            width = width // frames
            for frame in range(frames):
                frame_num = width * frame
                image_frame = image.subsurface((frame_num,0), (width,height)).copy()
                image_frame.set_alpha(image.get_alpha())
                image_frame = convert_image(image_frame, colorkey)
                images.append(image_frame)
            return images
    except pygame.error, message:
        if errorhandle:
            raise
        else:
            if errorreport:
                print(message)
            raise IOError
            return None

