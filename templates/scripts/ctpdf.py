import os
import re
from datetime import datetime

from fpdf import FPDF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class PDF(FPDF):
    def header(self):
        self.image(f"{BASE_DIR}/static/images/RedSpear_red_logo.png", 10, 8, 33)
        self.set_font('Arial', 'B', 15)

        w = self.get_string_width(title) + 6
        self.set_x((210 - w) / 2)

        self.set_draw_color(166, 1, 3)

        self.set_fill_color(1, 1, 3)
        self.set_text_color(254, 253, 254)

        self.set_line_width(1)

        self.cell(w, 9, title, 1, 1, 'C', 1)
        self.ln(3)