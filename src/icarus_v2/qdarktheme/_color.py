"""Module for color code."""
from __future__ import annotations

import colorsys
import math
import json
import re
from functools import lru_cache


SVG_RESOURCES = """
{"arrow_drop_up": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M8.71 12.29 11.3 9.7a.996.996 0 0 1 1.41 0l2.59 2.59c.63.63.18 1.71-.71 1.71H9.41c-.89 0-1.33-1.08-.7-1.71z\\"/></svg>", "arrow_upward": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M13 19V7.83l4.88 4.88c.39.39 1.03.39 1.42 0a.996.996 0 0 0 0-1.41l-6.59-6.59a.996.996 0 0 0-1.41 0l-6.6 6.58a.996.996 0 1 0 1.41 1.41L11 7.83V19c0 .55.45 1 1 1s1-.45 1-1z\\"/></svg>", "calendar_today": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M20 3h-1V2c0-.55-.45-1-1-1s-1 .45-1 1v1H7V2c0-.55-.45-1-1-1s-1 .45-1 1v1H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 18H5c-.55 0-1-.45-1-1V8h16v12c0 .55-.45 1-1 1z\\"/></svg>", "cancel": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm4.3 14.3a.996.996 0 0 1-1.41 0L12 13.41 9.11 16.3a.996.996 0 1 1-1.41-1.41L10.59 12 7.7 9.11A.996.996 0 1 1 9.11 7.7L12 10.59l2.89-2.89a.996.996 0 1 1 1.41 1.41L13.41 12l2.89 2.89c.38.38.38 1.02 0 1.41z\\"/></svg>", "check": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M9 16.17 5.53 12.7a.996.996 0 1 0-1.41 1.41l4.18 4.18c.39.39 1.02.39 1.41 0L20.29 7.71a.996.996 0 1 0-1.41-1.41L9 16.17z\\"/></svg>", "check_box": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-8.29 13.29a.996.996 0 0 1-1.41 0L5.71 12.7a.996.996 0 1 1 1.41-1.41L10 14.17l6.88-6.88a.996.996 0 1 1 1.41 1.41l-7.58 7.59z\\"/></svg>", "check_box_outline_blank": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M18 19H6c-.55 0-1-.45-1-1V6c0-.55.45-1 1-1h12c.55 0 1 .45 1 1v12c0 .55-.45 1-1 1zm1-16H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z\\"/></svg>", "check_circle": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zM9.29 16.29 5.7 12.7a.996.996 0 1 1 1.41-1.41L10 14.17l6.88-6.88a.996.996 0 1 1 1.41 1.41l-7.59 7.59a.996.996 0 0 1-1.41 0z\\"/></svg>", "chevron_right": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M9.29 6.71a.996.996 0 0 0 0 1.41L13.17 12l-3.88 3.88a.996.996 0 1 0 1.41 1.41l4.59-4.59a.996.996 0 0 0 0-1.41L10.7 6.7c-.38-.38-1.02-.38-1.41.01z\\"/></svg>", "circle": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z\\"/></svg>", "cleaning_services": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M16 11h-1V4c0-1.66-1.34-3-3-3S9 2.34 9 4v7H8c-2.76 0-5 2.24-5 5v5c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-5c0-2.76-2.24-5-5-5zm3 10h-2v-3c0-.55-.45-1-1-1s-1 .45-1 1v3h-2v-3c0-.55-.45-1-1-1s-1 .45-1 1v3H9v-3c0-.55-.45-1-1-1s-1 .45-1 1v3H5v-5c0-1.65 1.35-3 3-3h8c1.65 0 3 1.35 3 3v5z\\"/></svg>", "close": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M18.3 5.71a.996.996 0 0 0-1.41 0L12 10.59 7.11 5.7A.996.996 0 1 0 5.7 7.11L10.59 12 5.7 16.89a.996.996 0 1 0 1.41 1.41L12 13.41l4.89 4.89a.996.996 0 1 0 1.41-1.41L13.41 12l4.89-4.89c.38-.38.38-1.02 0-1.4z\\"/></svg>", "create_new_folder": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M20 6h-8l-1.41-1.41C10.21 4.21 9.7 4 9.17 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-2 8h-2v2c0 .55-.45 1-1 1s-1-.45-1-1v-2h-2c-.55 0-1-.45-1-1s.45-1 1-1h2v-2c0-.55.45-1 1-1s1 .45 1 1v2h2c.55 0 1 .45 1 1s-.45 1-1 1z\\"/></svg>", "delete": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2H8c-1.1 0-2 .9-2 2v10zM18 4h-2.5l-.71-.71c-.18-.18-.44-.29-.7-.29H9.91c-.26 0-.52.11-.7.29L8.5 4H6c-.55 0-1 .45-1 1s.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1z\\"/></svg>", "done_all": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M17.3 6.3a.996.996 0 0 0-1.41 0l-5.64 5.64 1.41 1.41L17.3 7.7c.38-.38.38-1.02 0-1.4zm4.24-.01-9.88 9.88-3.48-3.47a.996.996 0 1 0-1.41 1.41l4.18 4.18c.39.39 1.02.39 1.41 0L22.95 7.71a.996.996 0 0 0 0-1.41h-.01a.975.975 0 0 0-1.4-.01zM1.12 14.12 5.3 18.3c.39.39 1.02.39 1.41 0l.7-.7-4.88-4.9a.996.996 0 0 0-1.41 0c-.39.39-.39 1.03 0 1.42z\\"/></svg>", "double_arrow": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"m20.08 11.42-4.04-5.65c-.34-.48-.89-.77-1.48-.77-1.49 0-2.35 1.68-1.49 2.89L16 12l-2.93 4.11c-.87 1.21 0 2.89 1.49 2.89.59 0 1.15-.29 1.49-.77l4.04-5.65c.24-.35.24-.81-.01-1.16z\\"/><path d=\\"M13.08 11.42 9.05 5.77C8.7 5.29 8.15 5 7.56 5 6.07 5 5.2 6.68 6.07 7.89L9 12l-2.93 4.11C5.2 17.32 6.07 19 7.56 19c.59 0 1.15-.29 1.49-.77l4.04-5.65c.24-.35.24-.81-.01-1.16z\\"/></svg>", "drag_handle": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M19 9H5c-.55 0-1 .45-1 1s.45 1 1 1h14c.55 0 1-.45 1-1s-.45-1-1-1zM5 15h14c.55 0 1-.45 1-1s-.45-1-1-1H5c-.55 0-1 .45-1 1s.45 1 1 1z\\"/></svg>", "drag_indicator": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M11 18c0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2 2 .9 2 2zm-2-8c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0-6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm6 4c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z\\"/></svg>", "drive_file_move": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M20 6h-8l-1.41-1.41C10.21 4.21 9.7 4 9.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-8 9.79V14H9c-.55 0-1-.45-1-1s.45-1 1-1h3v-1.79c0-.45.54-.67.85-.35l2.79 2.79c.2.2.2.51 0 .71l-2.79 2.79a.5.5 0 0 1-.85-.36z\\"/></svg>", "drive_file_move_rtl": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M20 6h-8l-1.41-1.41C10.21 4.21 9.7 4 9.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-8.85 10.15-2.79-2.79c-.2-.2-.2-.51 0-.71l2.79-2.79c.31-.32.85-.1.85.35V12h3c.55 0 1 .45 1 1s-.45 1-1 1h-3v1.79a.5.5 0 0 1-.85.36z\\"/></svg>", "east": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M14.29 5.71a.996.996 0 0 0 0 1.41L18.17 11H3c-.55 0-1 .45-1 1s.45 1 1 1h15.18l-3.88 3.88a.996.996 0 1 0 1.41 1.41l5.59-5.59a.996.996 0 0 0 0-1.41l-5.6-5.58a.996.996 0 0 0-1.41 0z\\"/></svg>", "expand_less": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M11.29 8.71 6.7 13.3a.996.996 0 1 0 1.41 1.41L12 10.83l3.88 3.88a.996.996 0 1 0 1.41-1.41L12.7 8.71a.996.996 0 0 0-1.41 0z\\"/></svg>", "fast_forward": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"m5.58 16.89 5.77-4.07c.56-.4.56-1.24 0-1.63L5.58 7.11C4.91 6.65 4 7.12 4 7.93v8.14c0 .81.91 1.28 1.58.82zM13 7.93v8.14c0 .81.91 1.28 1.58.82l5.77-4.07c.56-.4.56-1.24 0-1.63l-5.77-4.07c-.67-.47-1.58 0-1.58.81z\\"/></svg>", "fast_rewind": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M11 16.07V7.93c0-.81-.91-1.28-1.58-.82l-5.77 4.07c-.56.4-.56 1.24 0 1.63l5.77 4.07c.67.47 1.58 0 1.58-.81zm1.66-3.25 5.77 4.07c.66.47 1.58-.01 1.58-.82V7.93c0-.81-.91-1.28-1.58-.82l-5.77 4.07a1 1 0 0 0 0 1.64z\\"/></svg>", "flip_to_front": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M3 13h2v-2H3v2zm0 4h2v-2H3v2zm2 4v-2H3a2 2 0 0 0 2 2zM3 9h2V7H3v2zm12 12h2v-2h-2v2zm4-18H9a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-1 12h-8c-.55 0-1-.45-1-1V6c0-.55.45-1 1-1h8c.55 0 1 .45 1 1v8c0 .55-.45 1-1 1zm-7 6h2v-2h-2v2zm-4 0h2v-2H7v2z\\"/></svg>", "fullscreen": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M6 14c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1h3c.55 0 1-.45 1-1s-.45-1-1-1H7v-2c0-.55-.45-1-1-1zm0-4c.55 0 1-.45 1-1V7h2c.55 0 1-.45 1-1s-.45-1-1-1H6c-.55 0-1 .45-1 1v3c0 .55.45 1 1 1zm11 7h-2c-.55 0-1 .45-1 1s.45 1 1 1h3c.55 0 1-.45 1-1v-3c0-.55-.45-1-1-1s-1 .45-1 1v2zM14 6c0 .55.45 1 1 1h2v2c0 .55.45 1 1 1s1-.45 1-1V6c0-.55-.45-1-1-1h-3c-.55 0-1 .45-1 1z\\"/></svg>", "grid_view": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M5 11h4c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2zm0 10h4c1.1 0 2-.9 2-2v-4c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2zm8-16v4c0 1.1.9 2 2 2h4c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2zm2 16h4c1.1 0 2-.9 2-2v-4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v4c0 1.1.9 2 2 2z\\"/></svg>", "help": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75-.9.92c-.5.51-.86.97-1.04 1.69-.08.32-.13.68-.13 1.14h-2v-.5a3.997 3.997 0 0 1 1.17-2.83l1.24-1.26c.46-.44.68-1.1.55-1.8a1.99 1.99 0 0 0-1.39-1.53c-1.11-.31-2.14.32-2.47 1.27-.12.37-.43.65-.82.65h-.3C8.4 9 8 8.44 8.16 7.88a4.008 4.008 0 0 1 3.23-2.83c1.52-.24 2.97.55 3.87 1.8 1.18 1.63.83 3.38-.19 4.4z\\"/></svg>", "home": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M10 19v-5h4v5c0 .55.45 1 1 1h3c.55 0 1-.45 1-1v-7h1.7c.46 0 .68-.57.33-.87L12.67 3.6c-.38-.34-.96-.34-1.34 0l-8.36 7.53c-.34.3-.13.87.33.87H5v7c0 .55.45 1 1 1h3c.55 0 1-.45 1-1z\\"/></svg>", "horizontal_rule": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path fill-rule=\\"evenodd\\" d=\\"M19 13H5c-.55 0-1-.45-1-1s.45-1 1-1h14c.55 0 1 .45 1 1s-.45 1-1 1z\\"/></svg>", "indeterminate_check_box": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-3 10H8c-.55 0-1-.45-1-1s.45-1 1-1h8c.55 0 1 .45 1 1s-.45 1-1 1z\\"/></svg>", "info": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 15c-.55 0-1-.45-1-1v-4c0-.55.45-1 1-1s1 .45 1 1v4c0 .55-.45 1-1 1zm1-8h-2V7h2v2z\\"/></svg>", "launch": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M18 19H6c-.55 0-1-.45-1-1V6c0-.55.45-1 1-1h5c.55 0 1-.45 1-1s-.45-1-1-1H5a2 2 0 0 0-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-6c0-.55-.45-1-1-1s-1 .45-1 1v5c0 .55-.45 1-1 1zM14 4c0 .55.45 1 1 1h2.59l-9.13 9.13a.996.996 0 1 0 1.41 1.41L19 6.41V9c0 .55.45 1 1 1s1-.45 1-1V3h-6c-.55 0-1 .45-1 1z\\"/></svg>", "list": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M4 13c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0 4c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0-8c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm4 4h12c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1zm0 4h12c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1zM7 8c0 .55.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1zm-3 5c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0 4c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm0-8c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm4 4h12c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1zm0 4h12c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1s.45 1 1 1zM7 8c0 .55.45 1 1 1h12c.55 0 1-.45 1-1s-.45-1-1-1H8c-.55 0-1 .45-1 1z\\"/></svg>", "minimize": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M7 19h10c.55 0 1 .45 1 1s-.45 1-1 1H7c-.55 0-1-.45-1-1s.45-1 1-1z\\"/></svg>", "not_interested": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8 0-1.85.63-3.55 1.69-4.9L16.9 18.31A7.902 7.902 0 0 1 12 20zm6.31-3.1L7.1 5.69A7.902 7.902 0 0 1 12 4c4.42 0 8 3.58 8 8 0 1.85-.63 3.55-1.69 4.9z\\"/></svg>", "pause": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M8 19c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2s-2 .9-2 2v10c0 1.1.9 2 2 2zm6-12v10c0 1.1.9 2 2 2s2-.9 2-2V7c0-1.1-.9-2-2-2s-2 .9-2 2z\\"/></svg>", "play_arrow": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M8 6.82v10.36c0 .79.87 1.27 1.54.84l8.14-5.18a1 1 0 0 0 0-1.69L9.54 5.98A.998.998 0 0 0 8 6.82z\\"/></svg>", "question_mark": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M7.92 7.54c-.8-.34-1.14-1.33-.66-2.05C8.23 4.05 9.85 3 11.99 3c2.35 0 3.96 1.07 4.78 2.41.7 1.15 1.11 3.3.03 4.9-1.2 1.77-2.35 2.31-2.97 3.45-.15.27-.24.49-.3.94-.09.73-.69 1.3-1.43 1.3-.87 0-1.58-.75-1.48-1.62.06-.51.18-1.04.46-1.54.77-1.39 2.25-2.21 3.11-3.44.91-1.29.4-3.7-2.18-3.7-1.17 0-1.93.61-2.4 1.34-.35.57-1.08.75-1.69.5zM14 20c0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2 2 .9 2 2z\\"/></svg>", "radio_button_checked": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z\\"/><circle cx=\\"12\\" cy=\\"12\\" r=\\"5\\"/></svg>", "radio_button_unchecked": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z\\"/></svg>", "refresh": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M17.65 6.35a7.95 7.95 0 0 0-6.48-2.31c-3.67.37-6.69 3.35-7.1 7.02C3.52 15.91 7.27 20 12 20a7.98 7.98 0 0 0 7.21-4.56c.32-.67-.16-1.44-.9-1.44-.37 0-.72.2-.88.53a5.994 5.994 0 0 1-6.8 3.31c-2.22-.49-4.01-2.3-4.48-4.52A6.002 6.002 0 0 1 12 6c1.66 0 3.14.69 4.22 1.78l-1.51 1.51c-.63.63-.19 1.71.7 1.71H19c.55 0 1-.45 1-1V6.41c0-.89-1.08-1.34-1.71-.71l-.64.65z\\"/></svg>", "restart_alt": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 5V3.21c0-.45-.54-.67-.85-.35l-2.8 2.79c-.2.2-.2.51 0 .71l2.79 2.79c.32.31.86.09.86-.36V7c3.31 0 6 2.69 6 6 0 2.72-1.83 5.02-4.31 5.75-.42.12-.69.52-.69.95 0 .65.62 1.16 1.25.97A7.991 7.991 0 0 0 20 13c0-4.42-3.58-8-8-8zm-6 8c0-1.34.44-2.58 1.19-3.59.3-.4.26-.95-.09-1.31-.42-.42-1.14-.38-1.5.1a7.991 7.991 0 0 0 4.15 12.47c.63.19 1.25-.32 1.25-.97 0-.43-.27-.83-.69-.95C7.83 18.02 6 15.72 6 13z\\"/></svg>", "save": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M17.59 3.59c-.38-.38-.89-.59-1.42-.59H5a2 2 0 0 0-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V7.83c0-.53-.21-1.04-.59-1.41l-2.82-2.83zM12 19c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3zm1-10H7c-1.1 0-2-.9-2-2s.9-2 2-2h6c1.1 0 2 .9 2 2s-.9 2-2 2z\\"/></svg>", "search": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z\\"/></svg>", "security": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"m11.19 1.36-7 3.11C3.47 4.79 3 5.51 3 6.3V11c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V6.3c0-.79-.47-1.51-1.19-1.83l-7-3.11c-.51-.23-1.11-.23-1.62 0zM12 11.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z\\"/></svg>", "skip_next": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"m7.58 16.89 5.77-4.07c.56-.4.56-1.24 0-1.63L7.58 7.11C6.91 6.65 6 7.12 6 7.93v8.14c0 .81.91 1.28 1.58.82zM16 7v10c0 .55.45 1 1 1s1-.45 1-1V7c0-.55-.45-1-1-1s-1 .45-1 1z\\"/></svg>", "skip_previous": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M7 6c.55 0 1 .45 1 1v10c0 .55-.45 1-1 1s-1-.45-1-1V7c0-.55.45-1 1-1zm3.66 6.82 5.77 4.07c.66.47 1.58-.01 1.58-.82V7.93c0-.81-.91-1.28-1.58-.82l-5.77 4.07a1 1 0 0 0 0 1.64z\\"/></svg>", "stop": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M8 6h8c1.1 0 2 .9 2 2v8c0 1.1-.9 2-2 2H8c-1.1 0-2-.9-2-2V8c0-1.1.9-2 2-2z\\"/></svg>", "vertical_line": "<svg enable-background=\\"new 0 0 24 24\\" height=\\"24px\\" viewBox=\\"0 0 24 24\\" width=\\"24px\\"><g><rect fill-rule=\\"evenodd\\" height=\\"24\\" width=\\"1\\" x=\\"11\\" y=\\"0\\"/></g></svg>", "visibility_off": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M12 6.5c2.76 0 5 2.24 5 5 0 .51-.1 1-.24 1.46l3.06 3.06c1.39-1.23 2.49-2.77 3.18-4.53C21.27 7.11 17 4 12 4c-1.27 0-2.49.2-3.64.57l2.17 2.17c.47-.14.96-.24 1.47-.24zM2.71 3.16a.996.996 0 0 0 0 1.41l1.97 1.97A11.892 11.892 0 0 0 1 11.5C2.73 15.89 7 19 12 19c1.52 0 2.97-.3 4.31-.82l2.72 2.72a.996.996 0 1 0 1.41-1.41L4.13 3.16c-.39-.39-1.03-.39-1.42 0zM12 16.5c-2.76 0-5-2.24-5-5 0-.77.18-1.5.49-2.14l1.57 1.57c-.03.18-.06.37-.06.57 0 1.66 1.34 3 3 3 .2 0 .38-.03.57-.07L14.14 16c-.65.32-1.37.5-2.14.5zm2.97-5.33a2.97 2.97 0 0 0-2.64-2.64l2.64 2.64z\\"/></svg>", "volume_mute": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M7 10v4c0 .55.45 1 1 1h3l3.29 3.29c.63.63 1.71.18 1.71-.71V6.41c0-.89-1.08-1.34-1.71-.71L11 9H8c-.55 0-1 .45-1 1z\\"/></svg>", "volume_up": "<svg width=\\"24\\" height=\\"24\\" viewBox=\\"0 0 24 24\\"><path d=\\"M3 10v4c0 .55.45 1 1 1h3l3.29 3.29c.63.63 1.71.18 1.71-.71V6.41c0-.89-1.08-1.34-1.71-.71L7 9H4c-.55 0-1 .45-1 1zm13.5 2A4.5 4.5 0 0 0 14 7.97v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 4.45v.2c0 .38.25.71.6.85C17.18 6.53 19 9.06 19 12s-1.82 5.47-4.4 6.5c-.36.14-.6.47-.6.85v.2c0 .63.63 1.07 1.21.85C18.6 19.11 21 15.84 21 12s-2.4-7.11-5.79-8.4c-.58-.23-1.21.22-1.21.85z\\"/></svg>"}
"""  # noqa: E501


def _round_float(number: float, decimal_points: int = 3) -> float:
    decimal = 10**decimal_points
    return round(number * decimal) / decimal


class _RGBA:
    """Class handling RGBA color code."""

    def __init__(self, r: int, g: int, b: int, a: float = 1) -> None:
        """Initialize rgba value.

        Args:
            r: Red(0~255).
            g: Green(0~255).
            b: Blue(0~255).
            a: Alpha(0~1). Defaults to 1.
        """
        self._r = min(255, max(0, r)) | 0
        self._g = min(255, max(0, g)) | 0
        self._b = min(255, max(0, b)) | 0
        self._a = _round_float(max(min(1, a), 0))

    def __str__(self) -> str:
        """Format RGBA class.

        e.g. rgba(100, 100, 100, 0.5).
        """
        return f"rgba({self.r}, {self.g}, {self.b}, {self.a:.3f})"

    def __getitem__(self, item: int) -> int | float:
        """Unpack to (r, g, b, a)."""
        return [self.r, self.g, self.b, self.a][item]

    def __eq__(self, other: _RGBA) -> bool:
        """Returns true if `r`, `g`, `b` and `a` are all the same."""
        return [self.r, self.g, self.b, self.a] == [other.r, other.g, other.b, other.a]

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def a(self) -> float:
        return self._a


class _HSLA:
    def __init__(self, h: int, s: float, l: float, a: float = 1) -> None:  # noqa: E741
        self._h = max(min(360, h), 0) | 0
        self._s = _round_float(max(min(1, s), 0))
        self._l = _round_float(max(min(1, l), 0))
        self._a = _round_float(max(min(1, a), 0))

    def __eq__(self, other: _HSLA) -> bool:
        """Returns true if `h`, `s`, `l` and `a` are all the same."""
        return [self.h, self.s, self.l, self.a] == [other.h, other.s, other.l, other.a]

    @property
    def h(self) -> int:
        return self._h

    @property
    def s(self) -> float:
        return self._s

    @property
    def l(self) -> float:  # noqa: E741, E743
        return self._l

    @property
    def a(self) -> float:
        return self._a

    @staticmethod
    def from_rgba(rgba: _RGBA) -> _HSLA:
        hls = colorsys.rgb_to_hls(rgba.r / 255, rgba.g / 255, rgba.b / 255)
        return _HSLA(int(hls[0] * 360), hls[2], hls[1], rgba.a)

    def to_rgba(self) -> _RGBA:
        rgb = colorsys.hls_to_rgb(self.h / 360, self.l, self.s)
        return _RGBA(round(rgb[0] * 255), round(rgb[1] * 255), round(rgb[2] * 255), self.a)


class Color:
    """Class handling color code(RGBA and HSLA)."""

    def __init__(self, color_code: _RGBA | _HSLA) -> None:
        """Initialize color code."""
        self._hsla, self._hsva = None, None
        if isinstance(color_code, _RGBA):
            self._rgba = color_code
        elif isinstance(color_code, _HSLA):
            self._hsla = color_code
            self._rgba = self._hsla.to_rgba()

    @property
    def rgba(self) -> _RGBA:
        """Return rgba."""
        return self._rgba

    @property
    def hsla(self) -> _HSLA:
        """Return hsla."""
        return self._hsla if self._hsla else _HSLA.from_rgba(self.rgba)

    def __str__(self) -> str:
        """Format Color class.

        e.g. rgba(100, 100, 100, 0.5).
        """
        return str(self.rgba)

    @staticmethod
    def _check_hex_format(hex_format: str) -> None:
        """Check if string is hex format."""
        try:
            hex = hex_format.lstrip("#")
            if not len(hex) in (3, 4, 6, 8):
                raise ValueError
            int(hex, 16)
        except ValueError:
            raise ValueError(
                f'invalid hex color format: "{hex_format}". '
                "Only support following hexadecimal notations: #RGB, #RGBA, #RRGGBB and #RRGGBBAA. "
                "R (red), G (green), B (blue), and A (alpha) are hexadecimal characters "
                "(0-9, a-f or A-F)."
            ) from None

    @staticmethod
    def from_rgba(r: int, g: int, b: int, a: int) -> Color:
        """Convert rgba to Color object."""
        rgba = _RGBA(r, g, b, a / 255)
        return Color(rgba)

    @staticmethod
    def from_hex(hex: str) -> Color:
        """Convert hex string to Color object.

        Args:
            color_hex: Color hex string.

        Returns:
            Color: Color object converted from hex.
        """
        Color._check_hex_format(hex)
        hex = hex.lstrip("#")
        r, g, b, a = 255, 0, 0, 1
        if len(hex) == 3:  # #RGB format
            r, g, b = (int(char, 16) for char in hex)
            r, g, b = 16 * r + r, 16 * g + g, 16 * b + b
        if len(hex) == 4:  # #RGBA format
            r, g, b, a = (int(char, 16) for char in hex)
            r, g, b = 16 * r + r, 16 * g + g, 16 * b + b
            a = (16 * a + a) / 255
        if len(hex) == 6:  # #RRGGBB format
            r, g, b = bytes.fromhex(hex)
            a = 1
        elif len(hex) == 8:  # #RRGGBBAA format
            r, g, b, a = bytes.fromhex(hex)
            a = a / 255
        return Color(_RGBA(r, g, b, a))

    def _to_hex(self) -> str:
        """Convert Color object to hex(#RRGGBBAA).

        Args:
            color: Color object.

        Returns:
            str: Hex converted from Color object.
        """
        r, g, b, a = self.rgba.r, self.rgba.g, self.rgba.b, self.rgba.a
        hex_color = f"{math.floor(r):02x}{math.floor(g):02x}{math.floor(b):02x}"
        if a != 1:
            hex_color += f"{math.floor(a*255):02x}"
        return hex_color

    def to_hex_argb(self) -> str:
        """Convert Color object to hex(#AARRGGBB).

        Args:
            color: Color object.

        Returns:
            str: Hex converted from Color object.
        """
        r, g, b, a = self.rgba.r, self.rgba.g, self.rgba.b, self.rgba.a
        hex_color = "" if a == 1 else f"{math.floor(a*255):02x}"
        hex_color += f"{math.floor(r):02x}{math.floor(g):02x}{math.floor(b):02x}"
        return hex_color

    def to_svg_tiny_color_format(self) -> str:
        """Convert Color object to string for svg.

        QtSvg does not support #RRGGBBAA format.
        Therefore, we need to set the alpha value to `fill-opacity` instead.

        Returns:
            str: RGBA format.
        """
        r, g, b, a = self.rgba
        if a == 1:
            return f'fill="#{self._to_hex()}"'
        return f'fill="rgb({r},{g},{b})" fill-opacity="{a}"'

    def lighten(self, factor: float) -> Color:
        """Lighten color."""
        return Color(_HSLA(self.hsla.h, self.hsla.s, self.hsla.l + self.hsla.l * factor, self.hsla.a))

    def darken(self, factor: float) -> Color:
        """Darken color."""
        return Color(_HSLA(self.hsla.h, self.hsla.s, self.hsla.l - self.hsla.l * factor, self.hsla.a))

    def transparent(self, factor: float) -> Color:
        """Make color transparent."""
        return Color(_RGBA(self.rgba.r, self.rgba.g, self.rgba.b, self.rgba.a * factor))


@lru_cache()
def _svg_resources() -> dict[str, str]:
    return json.loads(SVG_RESOURCES)


class Svg:
    """Class to manage SVG."""

    _SVG_FILL_RE = re.compile(r'fill=".*?"')
    _SVG_FILL_OPACITY_RE = re.compile(r'fill-opacity=".*?"')
    _SVG_TRANSFORM_RE = re.compile(r'transform=".*?"')

    def __init__(self, id: str) -> None:
        """Initialize svg manager."""
        self._id = id
        self._color = None
        self._rotate = None
        self._source = _svg_resources()[self._id]

    def __str__(self) -> str:
        """Return the svg source code."""
        return self._source

    def colored(self, color: Color) -> Svg:
        """Add or change svg color."""
        svg_tiny_color_formats = color.to_svg_tiny_color_format().split(" ")
        if len(svg_tiny_color_formats) == 2:
            new_svg_color, new_svg_opacity = svg_tiny_color_formats
        else:
            new_svg_color = svg_tiny_color_formats[0]
            new_svg_opacity = None

        current_svg_color = Svg._SVG_FILL_RE.search(self._source)
        current_svg_opacity = Svg._SVG_FILL_OPACITY_RE.search(self._source)

        # Add or change SVG color.
        if current_svg_color is None:
            self._source = self._source.replace("<svg ", f"<svg {new_svg_color} ")
        else:
            self._source = self._source.replace(current_svg_color.group(), new_svg_color)

        # Add or change SVG opacity.
        if new_svg_opacity is not None and current_svg_opacity is None:
            self._source = self._source.replace("<svg ", f"<svg {new_svg_opacity} ")
        elif new_svg_opacity is not None and current_svg_opacity is not None:
            self._source = self._source.replace(current_svg_opacity.group(), new_svg_opacity)

        # Remove SVG opacity
        if new_svg_opacity is None and current_svg_opacity is not None:
            self._source = self._source.replace(" " + current_svg_opacity.group(), "")
        return self

    def rotate(self, rotate: int) -> Svg:
        """Rotate svg."""
        if rotate == 0:
            return self

        current_svg_transform = Svg._SVG_TRANSFORM_RE.search(self._source)
        new_svg_transform = f'transform="rotate({rotate}, 12, 12)"'
        if current_svg_transform is None:
            self._source = self._source.replace("<svg ", f"<svg {new_svg_transform} ")
        else:
            self._source = self._source.replace(current_svg_transform.group(), new_svg_transform)

        return self
