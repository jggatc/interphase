#Interphase - Copyright (C) 2009 James Garnon <https://gatc.ca/>
#Released under the MIT License <https://opensource.org/licenses/MIT>

from __future__ import division
import os
try:
    _set = set
except NameError:
    from sets import Set as _set
from interphase.env import engine

__docformat__ = 'restructuredtext'


class Text(object):
    """
    Receives text to display on surface.
    Arguments include the target surface for text rendering, font_type is a list of alternate font names, and font_size is the font size.
    """

    _font = {}
    _cache = {}

    def __init__(self, surface, font_type=None, font_size=None):
        self.screen = surface
        x, y = self.screen.get_size()
        self.dimension = {'x': x, 'y': y}
        self.message = None
        self.messages = []
        if font_size:
            self.font_size = int(font_size)
        else:
            self.font_size = 10
        if isinstance(font_type, str):
            font_type = [font_type]
        if not Text._font:
            engine.font.init()
            font = None
            if font_type:
                font_type = ','.join(font_type)
                if font_type.startswith('file:'):
                    font = font_type[5:].strip()
                    if not os.path.exists(font):
                        print('Font not found: %s' % font)
                        font = None
                else:
                    font = engine.font.match_font(font_type)
            if not font:
                font_type = 'verdana, tahoma, bitstreamverasans, freesans, arial'
                font = engine.font.match_font(font_type)
                if not font:
                    font = engine.font.get_default_font()
                    font_type = font
            Text._font['default'] = font
            Text._font['defaults'] = font_type
            _font = engine.font.Font(font, self.font_size)
            Text._font[font] = {self.font_size: _font}
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
                    font_type = engine.font.match_font(font_type)
                if font_type:
                    if font_type not in Text._font:
                        _font = engine.font.Font(font_type, self.font_size)
                        Text._font[font_type] = {self.font_size: _font}
                else:
                    font_type = Text._font['default']
            else:
                font_type = Text._font['default']
        else:
            font_type = Text._font['default']
        if self.font_size not in Text._font[font_type]:
            _font = engine.font.Font(font_type, self.font_size)
            Text._font[font_type][self.font_size] = _font
        self.font_type = font_type
        self.font = Text._font[self.font_type]
        self.x = 0
        self.y = 0
        self.center = False
        self.font_color = (255,0,0)
        self.font_bgcolor = (0,0,0)
        self.split_text = False
        self.linesize = self.font[self.font_size].get_linesize()
        self.margin = {'t': 0, 'r': 0, 'b': 0, 'l': 0}
        self.multiline = False
        self.cache = None
        self.cache_key = None

    def __call__(self, surface='default'):
        """Writes text to surface."""
        if surface == 'default':
            self.surface = self.screen
        else:
            self.surface = surface
        self.update()
        return self.surface

    def render(self, surface='default'):
        """Writes text to surface."""
        if surface == 'default':
            self.surface = self.screen
        else:
            self.surface = surface
        self.update()
        return self.surface

    def add(self, *message_append):
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
        if isinstance(margin, int):
            self.margin['t'] = margin
            self.margin['r'] = margin
            self.margin['b'] = margin
            self.margin['l'] = margin
        else:
            self.margin['t'] = margin[0]
            self.margin['r'] = margin[1]
            self.margin['b'] = margin[2]
            self.margin['l'] = margin[3]

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
                font = engine.font.match_font(font_type)
            if font:
                if font not in Text._font:
                    _font = engine.font.Font(font,self.font_size)
                    Text._font[font] = {self.font_size: _font}
                self.font = Text._font[font]
                self.font_type = font
                if default:
                    Text._font['default'] = font
                    Text._font['defaults'] = font_type
        self.linesize = self.font[self.font_size].get_linesize()
        self.cache = None

    def get_font(self, font_info='font'):
        """Get current font."""
        if font_info == 'font':
            return self.font_type
        elif font_info == 'default':
            return Text._font['default']
        elif font_info == 'system':
            return engine.font.get_fonts()

    def get_font_size(self):
        """Get current font size."""
        return self.font_size

    def set_font_size(self, size):
        """Set font size of text."""
        self.font_size = size
        if size not in Text._font[self.font_type]:
            _font = engine.font.Font(self.font_type, self.font_size)
            Text._font[self.font_type][self.font_size] = _font
        self.font = Text._font[self.font_type]
        self.linesize = self.font[self.font_size].get_linesize()
        self.cache = None

    def set_font_color(self, color):
        """Set font color of text."""
        self.font_color = color
        self.cache = None

    def set_font_bgcolor(self, color=None):
        """Set font background color."""
        self.font_bgcolor = color
        self.cache = None

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
        sizes = [self.check_size(char)[0]
                 for char in 'abcdefghijklmnopqrstuvwxyz ']
        charsize = sum(sizes) // len(sizes)
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
        char_size = self.check_sizes(_set(text))
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

    def _cache_chr(self, ch):
        if self.font_bgcolor:
            text_surface = self.font[self.font_size].render(
                ch, True, self.font_color, self.font_bgcolor)
        else:
            text_surface = self.font[self.font_size].render(
                ch, True, self.font_color)
        try:
            self.cache[ch] = {'image': text_surface,
                              'width': text_surface.get_width()}
        except TypeError:
            self.cache_key = (self.font_type
                              + str(self.font_size)
                              + str(self.font_color)
                              + str(self.font_bgcolor))
            if self.cache_key not in self._cache:
                self._cache[self.cache_key] = {}
            self.cache = self._cache[self.cache_key]
            self.cache[ch] = {'image': text_surface,
                              'width': text_surface.get_width()}

    def _get_width(self, text):
        width = 0
        for ch in text:
            try:
                width += self.cache[ch]['width']
            except (KeyError, TypeError):
                self._cache_chr(ch)
                width += self.cache[ch]['width']
        return width

    def tprint(self):
        """Print text to surface."""
        if self.messages != []:
            if not self.cache:
                self.cache_key = (self.font_type
                                  + str(self.font_size)
                                  + str(self.font_color)
                                  + str(self.font_bgcolor))
                if self.cache_key not in self._cache:
                    self._cache[self.cache_key] = {}
                self.cache = self._cache[self.cache_key]
            if not self.multiline:
                text = " ".join(self.messages)
                if not self.split_text or text.strip().count(' ') == 0:
                    if self.center:
                        width = self._get_width(text)
                        x = self.x - (width//2)
                    else:
                        x = self.x + self.margin['l']
                    for ch in text:
                        if ch not in self.cache:
                            self._cache_chr(ch)
                        self.surface.blit(self.cache[ch]['image'], (x,self.y))
                        x += self.cache[ch]['width']
                else:
                    words = text.count(' ')
                    position_y = self.y - words*(self.linesize//2) - 1
                    texts = text.split(' ')
                    for count, text in enumerate(texts):
                        if self.center:
                            width = self._get_width(text)
                            x = self.x - (width//2)
                            y = position_y + (count*self.linesize)
                        else:
                            x = self.x
                            y = position_y + (count*self.linesize)
                        for ch in text:
                            if ch not in self.cache:
                                self._cache_chr(ch)
                            self.surface.blit(self.cache[ch]['image'], (x,y))
                            x += self.cache[ch]['width']
            else:
                position_y = self.y + self.margin['t']
                for count, text in enumerate(self.messages):
                    if self.center:
                        width = self._get_width(text)
                        x = self.x - (width//2)
                        y = position_y + (count*self.linesize)
                    else:
                        x = self.x + self.margin['l']
                        y = position_y + (count*self.linesize)
                    for ch in text:
                        if ch not in self.cache:
                            self._cache_chr(ch)
                        self.surface.blit(self.cache[ch]['image'], (x,y))
                        x += self.cache[ch]['width']
            self.message = None
            self.messages = []

    def update(self):
        self.tprint()


def load_image(filename, frames=1, path='data', zipobj=None,
               fileobj=None, colorkey=None, errorhandle=True):
    """
    Load image from file.
    Arguments include the image filename, the number of image frames in an image strip, the image path, zipobj for image in a zip file, fileobj for image in a file-like object, image colorkey, and errorhandle for exception handling.
    """
    if zipobj:
        import zipfile
        try:
            from io import BytesIO
        except ImportError:
            from StringIO import StringIO as BytesIO
        if isinstance(zipobj, str):
            if path:
                data_file = os.path.join(path, zipobj)
            else:
                data_file = zipobj
            dat = zipfile.ZipFile(data_file)
            fileobj = BytesIO(dat.open(filename).read())
            dat.close()
        else:
            fileobj = BytesIO(zipobj.open(filename).read())
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
            image = engine.image.load(full_name, namehint)
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, engine.RLEACCEL)
            return image
        elif frames > 1:
            images = []
            image = engine.image.load(full_name, namehint)
            width, height = image.get_size()
            width = width // frames
            for frame in range(frames):
                frame_num = width * frame
                image_frame = image.subsurface(
                    (frame_num, 0, width, height)).copy()
                if colorkey is not None:
                    if colorkey == -1:
                        colorkey = image_frame.get_at((0,0))
                    image_frame.set_colorkey(colorkey, engine.RLEACCEL)
                images.append(image_frame)
            return images
    except engine.error:
        if errorhandle:
            raise
        else:
            raise IOError
            return None

