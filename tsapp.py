import json
import pygame
import pygame.freetype

# ------------------------------------------------------------------------------
# Constants

"""
Color constants
Names and values based on standard HTML 4.01 web colors
"""
WHITE = (255, 255, 255)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
MAROON = (128, 0, 0)
YELLOW = (255, 255, 0)
OLIVE = (128, 128, 0)
LIME = (0, 255, 0)
GREEN = (0, 128, 0)
AQUA = (0, 255, 255)
TEAL = (0, 128, 128)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
FUCHSIA = (255, 0, 255)
MAGENTA = FUCHSIA  # Added because Fuchsia is impossible to spell correctly
PURPLE = (128, 0, 128)

""" 
Key Constants
Matches the values from pygame to avoid unnecessary imports
"""
# FIXME: How will you prevent confusion in Code Assist if you have
#        to list all of these duplicated values in multiple places?
K_SPACE = pygame.K_SPACE
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
K_RETURN = pygame.K_RETURN
K_a = pygame.K_a
K_b = pygame.K_b
K_c = pygame.K_c
K_d = pygame.K_d
K_e = pygame.K_e
K_f = pygame.K_f
K_g = pygame.K_g
K_h = pygame.K_h
K_i = pygame.K_i
K_j = pygame.K_j
K_k = pygame.K_k
K_l = pygame.K_l
K_m = pygame.K_m
K_n = pygame.K_n
K_o = pygame.K_o
K_p = pygame.K_p
K_q = pygame.K_q
K_r = pygame.K_r
K_s = pygame.K_s
K_t = pygame.K_t
K_u = pygame.K_u
K_v = pygame.K_v
K_w = pygame.K_w
K_x = pygame.K_x
K_y = pygame.K_y
K_z = pygame.K_z
K_0 = pygame.K_0
K_1 = pygame.K_1
K_2 = pygame.K_2
K_3 = pygame.K_3
K_4 = pygame.K_4
K_5 = pygame.K_5
K_6 = pygame.K_6
K_7 = pygame.K_7
K_8 = pygame.K_8
K_9 = pygame.K_9

# ------------------------------------------------------------------------------
# Graphics

# Global event list; this is kept because events are
# automatically wiped after processing, so this allows querying
_current_frame_event_list = []


class GraphicsWindow(object):
    """
    A window, into which drawable objects can be added and managed.

    Also maintains the event loop.
    """

    def __init__(self, width=1018, height=573, background_color=WHITE):
        # Clock times from pygame's init, so we initialize on object creation
        pygame.init()

        # Private variables
        self._window = pygame.display.set_mode([width, height])
        self._clock = pygame.time.Clock()
        self._draw_list = []
        self.framerate = 30

        # Public variables
        self.is_running = True
        self.background_color = background_color
        self.width = width
        self.height = height

    # === Objects ===

    def add_object(self, drawable_object):
        """
        Adds a drawable object to the scene.
        """
        self._draw_list.append(drawable_object)
        # Note: instead of "remove_element", use
        # GraphicalObject.destroy() to remove an object

    # === Layers ===

    def move_forward(self, drawable_object):
        # NOTE: Would prefer to use list.find, but this does not
        # seem to be available in Python 2.X
        if drawable_object not in self._draw_list:
            raise ValueError("Cannot change the layer of an object that has not been added to graphics window")
        else:
            position = self._draw_list.index(drawable_object)

        if position == len(self._draw_list) - 1:
            return

        # Otherwise, swap positions with object above
        new_position = position + 1
        swap = self._draw_list[position]
        self._draw_list[position] = self._draw_list[new_position]
        self._draw_list[new_position] = swap

    def move_to_front(self, drawable_object):

        if drawable_object not in self._draw_list:
            raise ValueError("Cannot change the layer of an object that has not been added to graphics window")
        else:
            position = self._draw_list.index(drawable_object)

        self._draw_list.remove(drawable_object)
        self._draw_list.append(drawable_object)

    def move_backward(self, drawable_object):
        if drawable_object not in self._draw_list:
            raise ValueError("Cannot change the layer of an object that has not been added to graphics window")
        else:
            position = self._draw_list.index(drawable_object)

        if position == 0:
            return

        new_position = position - 1
        swap = self._draw_list[position]
        self._draw_list[position] = self._draw_list[new_position]
        self._draw_list[new_position] = swap

    def move_to_back(self, drawable_object):
        if drawable_object not in self._draw_list:
            raise ValueError("Cannot change the layer of an object that has not been added to graphics window")
        else:
            position = self._draw_list.index(drawable_object)

        self._draw_list.remove(drawable_object)
        self._draw_list.insert(0, drawable_object)

    # Gets layer number (index in draw list; 0 is back layer)
    def get_layer(self, drawable_object):
        if drawable_object not in self._draw_list:
            raise ValueError("Cannot change the layer of an object that has not been added to graphics window")
        else:
            return self._draw_list.index(drawable_object)

    # Setting layer puts object at the given index,
    # which places it just behind the object previously
    # at the named layer
    # TODO: TEST THIS FUNCTION
    def set_layer(self, drawable_object, layer_index):
        if layer_index < 0:
            raise ValueError("Layer value must be positive")
        if drawable_object not in self._draw_list:
            raise ValueError("Cannot set the layer of an object that has not been added to graphics window")

        self._draw_list.remove(drawable_object)

        # If the user selects a layer beyond what is in the draw list,
        # just put it on top
        if layer >= len(self._draw_list):
            self._draw_list.append(drawable_object)
        else:
            self._draw_list.insert(layer_index, drawable_object)

            # === Event Loop Management ===

    def finish_frame(self):
        """
        Intended to be called once a frame while GraphicsWindow.is_running
        Performs all the most common end-of-frame actions, including:
         - tracking time
         - updating the position and image of graphical objects
         - removing destroyed objects
         - flipping the screen
         - checking for the "QUIT" event
        """

        # Track timing
        self._clock.tick(self.framerate)

        # Draw frame
        destroyed_items = []
        self._window.fill(self.background_color)
        for drawable_item in self._draw_list:
            if drawable_item.visible:
                drawable_item._draw()
            drawable_item._update(self._clock.get_time())
            if drawable_item.destroyed:
                destroyed_items.append(drawable_item)
        pygame.display.flip()

        # Remove destroyed elements
        for drawable_item in destroyed_items:
            self._draw_list.remove(drawable_item)

        # Capture events from the current frame
        global _current_frame_event_list
        _current_frame_event_list = pygame.event.get()

        # Check for QUIT
        for event in _current_frame_event_list:
            if event.type == pygame.QUIT:
                self.is_running = False


# Returns the current display surface
def _get_window():
    return pygame.display.get_surface()


class GraphicalObject(object):
    """
    Abstract: Encompasses any object that can be drawn into a
    Graphical Window
    """

    def __init__(self):
        self.visible = True
        self.x_speed = 0
        self.y_speed = 0
        self._destroyed = False

    def _draw(self):
        raise NotImplementedError("All GraphicalObjects must have some way of drawing themselves.")

    def _update(self, delta_time):
        pass  # Update can be called on all Graphical Objects, but not every object does something

    def _get_speed(self):
        return (self.x_speed, self.y_speed)

    def _set_speed(self, speed_tuple):
        (self.x_speed, self.y_speed) = speed_tuple

    speed = property(_get_speed, _set_speed)

    # === Lifecycle ===

    def destroy(self):
        """Marks this graphical object for destruction."""
        self._destroyed = True

    @property
    def destroyed(self):
        return self._destroyed


class RectangularObject(GraphicalObject):
    """
    A subtype of GraphicalObject
    Rectangular Object is a parent class for various other types
    of graphical objects that all have rectangular bounds
    """

    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self._width = width
        self._height = height

    def _get_center_x(self):
        return self.x + (self.width / 2)

    def _set_center_x(self, center_x):
        self.x = center_x - (self.width / 2)

    center_x = property(_get_center_x, _set_center_x)

    def _get_center_y(self):
        return self.y + (self.height / 2)

    def _set_center_y(self, center_y):
        self.y = center_y - (self.height / 2)

    center_y = property(_get_center_y, _set_center_y)

    def _get_center(self):
        return (self.center_x, self.center_y)

    def _set_center(self, center):
        (self.center_x, self.center_y) = center

    center = property(_get_center, _set_center)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def rect(self):
        # NOTE: pygame.Rect does not support non-integer values.
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def is_colliding_rect(self, other_rect_obj):
        return self.rect.colliderect(other_rect_obj.rect)

    def is_colliding_point(self, point):
        return self.rect.collidepoint(point)

    def _update(self, delta_time):
        x_speed, y_speed = self.speed
        self.x += (x_speed / 1000) * delta_time
        self.y += (y_speed / 1000) * delta_time


class Sprite(RectangularObject):
    """
    Represents a sprite, a persistent image on the screen
    with a particular location.

    Mostly identical to previous 'Sprite' class from the
    'tsk' library, but inherits from RectangularObject, and
    can automatically detect spritesheets for animation
    """

    def __init__(self, image_descriptor, x, y):
        # type: (ImageDescriptor, float, float) -> None
        self._set_image(image_descriptor, init=True)
        self.image_animation_rate = None
        self._scale = 1.0
        self._angle = 0
        self._flip_x = False
        self._flip_y = False
        super().__init__(x, y, self._current_transformed_cell.get_width(), self._current_transformed_cell.get_height())

    def _get_image(self):
        return self._image_descriptor

    def _set_image(self, image_descriptor, init=False):

        # Figure out automatically if this should be animated
        # based on the presence of a .json meta file of same name
        image_file_path = image_descriptor
        meta_image_path = image_file_path.split(".")[0] + ".json"
        try:
            with open(meta_image_path) as meta_file:
                size_dict = json.load(meta_file)
            row_count = size_dict["rows"]
            column_count = size_dict["cols"]
            image_sheet = ImageSheet(image_descriptor, row_count, column_count)
            self.image_animation_rate = row_count * column_count
            cells = image_sheet.cells
        except IOError:
            cells = [pygame.image.load(image_file_path)]

        if not init:
            old_center = self.center

        if not isinstance(image_descriptor, str):
            raise ValueError(
                'Expected image descriptor to be an image file path but found: %r' %
                image_descriptor)

        self._image_descriptor = image_descriptor

        # Change cells
        self._current_cell_index = 0
        self._cells = cells
        self._transformed_cells = [None] * len(cells)

        # Reset cell animation timing
        self._time_current_cell_visible = 0

        if not init:
            self.center = old_center

    image = property(_get_image, _set_image, doc=
    """The static or animated image that this sprite displays.""")

    # The current image cell, before scale, flip, and rotate transformations.
    @property
    def _current_cell(self):
        return self._cells[self._current_cell_index]

    # The current image cell, after scale, flip, and rotate transformations.
    @property
    def _current_transformed_cell(self):
        transformed_cell = self._transformed_cells[self._current_cell_index]
        if transformed_cell is None:  # not yet cached
            cell = self._cells[self._current_cell_index]
            transformed_cell = self._transform_cell(cell)
            self._transformed_cells[self._current_cell_index] = transformed_cell
        return transformed_cell

    # Invalidates all cached transformed image cells.
    # Should be called whenever any fields that affect _transform_cell() are changed.
    def _invalidate_transformed_cells(self):
        for i in range(len(self._transformed_cells)):
            self._transformed_cells[i] = None

    def _get_image_animation_rate(self):
        return self._image_animation_rate

    def _set_image_animation_rate(self, image_animation_rate):
        if image_animation_rate is None:
            time_per_cell = None
        elif isinstance(image_animation_rate, (int, float)):
            if image_animation_rate > 0:
                time_per_cell = 1000 / image_animation_rate
            elif image_animation_rate == 0:
                time_per_cell = -1
            else:
                raise ValueError('Expected animation rate to be >=0 but got %r.' % image_animation_rate)
        else:
            raise ValueError('Not a valid animation rate: %r' % image_animation_rate)

        # Update image animation rate
        self._image_animation_rate = image_animation_rate
        self._time_per_cell = time_per_cell

        # Reset cell animation timing
        self._time_current_cell_visible = 0

    image_animation_rate = property(_get_image_animation_rate, _set_image_animation_rate, doc=
    """
    The rate at which the animated sprite image advances.
    Does not apply to static sprite images.

    If None then 1 cell per frame (regardless of frame length),
    if a double then X cells per second.
    """)

    def _transform_cell(self, cell):
        transformed_cell = cell

        # Scale
        if self._scale != 1.0:
            transformed_cell = \
                pygame.transform.scale(transformed_cell, (
                    int(transformed_cell.get_width() * self._scale),
                    int(transformed_cell.get_height() * self._scale)
                ))

        # Flip
        if self._flip_x or self._flip_y:
            transformed_cell = pygame.transform.flip(transformed_cell, self._flip_x, self._flip_y)

        # Rotate
        if self._angle != 0:
            transformed_cell = pygame.transform.rotate(transformed_cell, self._angle)

        return transformed_cell

    @property
    def width(self):
        return self._current_transformed_cell.get_width()

    @property
    def height(self):
        return self._current_transformed_cell.get_height()

    def get_edge(self, edge_type):
        """
        Returns the specified edge of this sprite,
        which can be used with pygame.sprite.collide_rect().
        """
        return _Edge.of_rect(self.rect, edge_type)

    # === Scale ===

    def _get_scale(self):
        return self._scale

    def _set_scale(self, scale):
        old_center = self.center

        self._scale = scale
        self._invalidate_transformed_cells()

        self.center = old_center

    scale = property(_get_scale, _set_scale)

    # === Flip ===

    def _get_flip_x(self):
        return self._flip_x

    def _set_flip_x(self, flipped):
        if self._flip_x == flipped:
            return

        self._flip_x = flipped
        self._invalidate_transformed_cells()

    flip_x = property(_get_flip_x, _set_flip_x)

    def _get_flip_y(self):
        return self._flip_y

    def _set_flip_y(self, flipped):
        if self._flip_y == flipped:
            return

        self._flip_y = flipped
        self._invalidate_transformed_cells()

    flip_y = property(_get_flip_y, _set_flip_y)

    # === Angle ===

    def _get_angle(self):
        return self._angle

    def _set_angle(self, angle):
        old_center = self.center

        self._angle = angle
        self._invalidate_transformed_cells()

        self.center = old_center

    angle = property(_get_angle, _set_angle)

    # === Behavior ===

    def _update(self, delta_time):
        """
        Updates this sprite's animated image.

        Parameters:
        * delta_time -- The amount of time since the last call to update,
                        in milliseconds.
        """
        super()._update(delta_time)
        self._time_current_cell_visible += delta_time

        # Advance cell if appropriate
        if self._time_per_cell == -1:
            # Cell animation is disabled
            pass
        elif self._time_per_cell is None:
            # Time per cell is 1 frame/cell, regardless of frame duration
            if len(self._cells) > 1:
                self._current_cell_index += 1
                if self._current_cell_index == len(self._cells):
                    self._current_cell_index = 0
        else:
            # Time per cell is X seconds/cell
            time_per_cell = self._time_per_cell

            # Change current cell if enough time has passed
            if self._time_current_cell_visible >= time_per_cell:
                (num_cells_to_advance, self._time_current_cell_visible) = \
                    divmod(self._time_current_cell_visible, time_per_cell)
                self._current_cell_index = \
                    (self._current_cell_index + int(num_cells_to_advance)) % len(self._cells)

    def _draw(self):
        """Draws this sprite if it is visible."""
        if self.visible:
            _get_window().blit(self._current_transformed_cell, [self.x, self.y])


class ImageSheet(object):
    """
    Represents an image file that is divided into an (m x n) grid of cells.
    The cells are intended for use in an animation.
    Copied wholesale from previous tsk module
    """

    def __init__(self, file_path, row_count, column_count):
        # type: (ImageFilePath, int, int) -> None
        if not (row_count >= 1 and column_count >= 1):
            raise ValueError('Expected row and column count to be >= 1.')

        sheet_image = pygame.image.load(file_path)
        sheet_width, sheet_height = sheet_image.get_size()

        # Slice the sheet into cells
        cells = []
        (cell_width, cell_height) = (
            sheet_width // column_count,
            sheet_height // row_count
        )
        for gy in range(row_count):
            for gx in range(column_count):
                cell = sheet_image.subsurface(pygame.Rect(
                    gx * cell_width, gy * cell_height,
                    cell_width, cell_height))
                cells.append(cell)

        self.cells = cells
        self.row_count = row_count
        self.column_count = column_count


class TextLabel(GraphicalObject):
    """
    A text label that wraps and uses baseline position.
    Can be aligned (left-aligned by default).
    """

    def __init__(self, font_name, font_size, x, y, width, text="", color=BLACK):
        super().__init__()
        self._font = pygame.freetype.Font(font_name, font_size)
        self._font_identifier = font_name
        self._font.origin = True
        self._font.fgcolor = color
        self.position = (x, y)
        self._width = width
        self._text = text
        self._wrap_into_lines()  # Creates self._lines list
        self._align = "left"
        self._set_line_spacing(1.2)

    def _get_text(self):
        return self._text

    def _set_text(self, text_string):  # Setting text causes re-calcuation of wrapping
        self._text = text_string
        self._wrap_into_lines()

    text = property(_get_text, _set_text)

    def _get_width(self):
        return self._width

    def _set_width(self, new_width):  # Setting width causes re-calculation of wrapping
        self._width = width
        self._wrap_into_lines()

    width = property(_get_width, _set_width)

    def _get_align(self):
        return self._align

    def _set_align(self, alignment):
        alignment = alignment.lower()
        if alignment != "right" and alignment != "left" and alignment != "center":
            raise ValueError(
                "Text Label alignment must be \"left\", \"right\", or \"center\": got \"" + str(alignment) + "\"")
        else:
            self._align = alignment

    align = property(_get_align, _set_align)

    def _get_font(self):
        return self._font_identifier

    def _set_font(self, font_name):
        new_font = pygame.freetype.Font(font_name,
                                        self.font_size)  # Setting font causes re-calculation of wrapping and line height
        new_font.fgcolor = self.color
        new_font.origin = True
        self._font = new_font
        self._wrap_into_lines()
        self._font_identifier = font_name

    font = property(_get_font, _set_font)

    def _get_font_size(self):
        return self._font.size

    def _set_font_size(self, new_size):  # Setting font size causes re-calculation of wrapping and line height
        self._font.size = new_size
        self._wrap_into_lines()
        self._pixel_line_height = self._font.get_rect(
            "Q").height * self._line_spacing  # Q is used as an estimation of line height because it contains both an ascent and descent

    font_size = property(_get_font_size, _set_font_size)

    def _get_line_spacing(self):
        return self._line_spacing

    def _set_line_spacing(self, spacing):
        self._line_spacing = spacing
        self._pixel_line_height = self._font.get_rect(
            "Q").height * spacing  # Q is used as an estimation of line height because it contains both an ascent and descent

    line_spacing = property(_get_line_spacing, _set_line_spacing)

    def _get_color(self):
        return self._font.fgcolor

    def _set_color(self, new_color):
        self._font.fgcolor = new_color

    color = property(_get_color, _set_color)

    def _get_x(self):
        return self.position[0]

    def _set_x(self, new_x):
        self.position = (new_x, self.position[1])

    x = property(_get_x, _set_x)

    def _get_y(self):
        return self.position[1]

    def _set_y(self, new_y):
        self.position = (self.position[0], new_y)

    y = property(_get_y, _set_y)

    def _get_center_x(self):
        return self.position[0] + (self.width / 2)

    def _set_center_x(self, new_x):
        self.position = (new_x - (self.width / 2), self.position[1])

    center_x = property(_get_center_x, _set_center_x)

    def _get_right_x(self):
        return self.position[0] + self.width

    def _set_right_x(self, new_x):
        self.position = (new_x - self.width, self.position[1])

    right_x = property(_get_right_x, _set_right_x)

    # === Override Methods ===

    def _draw(self):
        if self.visible:
            start_x, y = self.position
            for line in self._lines:
                line_width = self._font.get_rect(line).width

                if self.align == "left":
                    x = start_x

                elif self.align == "right":
                    x = (start_x + self.width) - line_width

                elif self.align == "center":
                    x = start_x + (self.width / 2) - (0.5 * line_width)

                else:
                    raise AssertionError(
                        "Text Label alignment must be \"left\", \"right\", or \"center\": got \"" + str(
                            alignment) + "\"")

                self._font.render_to(_get_window(), (x, y), line)
                y += self._pixel_line_height

    def _update(self, delta_time):
        x_speed, y_speed = self.speed
        self.x += (x_speed / 1000) * delta_time
        self.y += (y_speed / 1000) * delta_time

    # === Text Wrapping ===

    def _wrap_into_lines(self):
        """
        Creates a list of lines of text based on the width of
        the label, wrapping on spaces and newlines
        (Does not hyphenate; throws error if length of an
        individual word exceeds text label width)
        """

        # Split based on newlines
        hard_lines = self._text.split("\n")
        self._lines = []

        # Split each subline based on wrapping width
        for hard_line in hard_lines:
            words_in_hardline = hard_line.split(" ")

            while len(words_in_hardline) > 0:
                # length of words_in_hardline is changed as a side effect of _get_next_line
                line = self._get_next_line(words_in_hardline)
                self._lines.append(line)

    def _get_next_line(self, words_remaining):
        """
        Helper function for wrapping; gets one line of text
        """
        width_available = self._width
        words_to_add = []

        # Figure out how many words you can add
        for word in words_remaining:
            word_width = self._font.get_rect(word).width
            if word_width > width_available:
                # Words that are wider than the box will appear
                # on their own line by themselves
                if width_available == self._width:
                    words_to_add.append(word)
                    width_available = 0
                break
            else:
                words_to_add.append(word)
                width_available -= word_width + self._font.get_rect(" ").width

        # Add them to the line
        # NOTE: This is not done in the loop, as modifying the
        # word list while reading through it causes Bad Times
        line_parts = []
        for word in words_to_add:
            line_parts.append(word)
            words_remaining.remove(word)
        line = " ".join(line_parts)
        return line


# ------------------------------------------------------------------------------
# Interaction

def is_key_down(key_constant):
    return pygame.key.get_pressed()[key_constant]


def was_key_pressed(key_constant):
    global _current_frame_event_list
    for event in _current_frame_event_list:
        if event.type == pygame.KEYDOWN and event.key == key_constant:
            return True
    return False


def was_key_released(key_constant):
    global _current_frame_event_list
    for event in _current_frame_event_list:
        if event.type == pygame.KEYUP and event.key == key_constant:
            return True
    return False


def was_mouse_pressed():
    global _current_frame_event_list
    for event in _current_frame_event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            return True
    return False


def was_mouse_released():
    global _current_frame_event_list
    for event in _current_frame_event_list:
        if event.type == pygame.MOUSEBUTTONUP:
            return True
    return False


def get_mouse_x():
    return pygame.mouse.get_pos()[0]


def get_mouse_y():
    return pygame.mouse.get_pos()[1]


def get_mouse_position():
    return pygame.mouse.get_pos()


# ------------------------------------------------------------------------------
# Timing

def get_program_duration():
    if not _get_window():
        raise ValueError("Cannot get program duration when no window has been opened")
    else:
        return pygame.time.get_ticks()
