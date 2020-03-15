CONSOLE_CONFIG = {
    "global": {
        'animation': ['BOTTOM'],
        'layout': 'INPUT_TOP',
        'padding': (10, 10, 20, 20),
        'bck_color': (125, 125, 125),
        'bck_image': 'libs/pygame_console/backgrounds/black.png',
        'bck_image_resize': True,
        'bck_alpha': 150,
        'welcome_msg': 'Type "exit" to quit\nType "help"/"?" for help\nType "? shell" for examples of python commands',
        'welcome_msg_color': (0, 255, 0),
    },
    'output': {
        'padding': (10, 10, 10, 10),
        'font_file': 'libs/pygame_console/fonts/JackInput.ttf',
        'font_size': 16,
        'font_antialias': True,
        'font_color': (255, 255, 255),
        'font_bck_color': (20, 20, 20),
        'bck_color': (20, 20, 20),
        'bck_alpha': 120,
        'buffer_size': 100,
        'display_lines': 32,
        'display_columns': 50,
        'line_spacing': None
    },
    'input': {
        'padding': (10, 10, 10, 10),
        'font_file': 'libs/pygame_console/fonts/JackInput.ttf',
        'font_size': 16,
        'font_antialias': True,
        'font_color': (255, 255, 255),
        'font_bck_color': None,
        'bck_color': (100, 0, 0),
        'bck_alpha': 75,
        'prompt': '>>>',
        'max_string_length': 10,
        'repeat_keys_initial_ms': 400,
        'repeat_keys_interval_ms': 35
    }
}

