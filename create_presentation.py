from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

DARK_BLUE = RGBColor(0x00, 0x33, 0x66)
TEAL = RGBColor(0x00, 0x80, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
LIGHT_GRAY = RGBColor(0xF0, 0xF0, 0xF0)
ACCENT_BLUE = RGBColor(0x00, 0x6B, 0xB6)
DARK_BG = RGBColor(0x1A, 0x1A, 0x2E)
ORANGE = RGBColor(0xFF, 0x8C, 0x00)
GREEN = RGBColor(0x00, 0x80, 0x00)
RED = RGBColor(0xCC, 0x00, 0x00)
PURPLE = RGBColor(0x66, 0x00, 0x99)

def add_header_bar(slide, text):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.9))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT
    tf.margin_left = Inches(0.5)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

def add_footer_bar(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.0), prs.slide_width, Inches(0.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = TEAL
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Department of Electronics and Communication Engineering  |  IIIT Surat"
    p.font.size = Pt(14)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

def add_bullet_text(tf, text, level=0, font_size=20, bold=False, color=BLACK, spacing_before=6):
    p = tf.add_paragraph()
    p.text = text
    p.level = level
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_before = Pt(spacing_before)
    return p

def add_textbox(slide, left, top, width, height, text, font_size=18, bold=False, color=BLACK, alignment=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = alignment
    return tf

def add_rounded_box(slide, left, top, width, height, fill_color, text, font_size=16, font_color=WHITE):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = font_color
    p.alignment = PP_ALIGN.CENTER
    return shape


# ========== SLIDE 0: TITLE PAGE ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.6))
top_bar.fill.solid()
top_bar.fill.fore_color.rgb = DARK_BLUE
top_bar.line.fill.background()

tf = add_textbox(slide, Inches(1.8), Inches(0.15), Inches(10), Inches(0.5),
                 "भारतीय सूचना प्रौद्योगिकी संस्थान सूरत", 22, True, WHITE, PP_ALIGN.CENTER)
tf = add_textbox(slide, Inches(1.8), Inches(0.5), Inches(10), Inches(0.5),
                 "Indian Institute of Information Technology Surat", 26, True, WHITE, PP_ALIGN.CENTER)
tf = add_textbox(slide, Inches(1.8), Inches(0.9), Inches(10), Inches(0.4),
                 "ભારતીય સૂચના પ્રૌદ્યોગિકી સંસ્થા સુરત", 16, False, RGBColor(0xCC, 0xCC, 0xCC), PP_ALIGN.CENTER)
tf = add_textbox(slide, Inches(1.8), Inches(1.2), Inches(10), Inches(0.3),
                 "(An Institute of National Importance under Act of Parliament)", 14, False, RGBColor(0xAA, 0xAA, 0xAA), PP_ALIGN.CENTER)

tf = add_textbox(slide, Inches(1), Inches(2.2), Inches(11), Inches(0.5),
                 "Presentation on", 24, False, DARK_BLUE, PP_ALIGN.CENTER)
p = tf.paragraphs[0]
p.font.italic = True

tf = add_textbox(slide, Inches(1), Inches(2.8), Inches(11), Inches(0.7),
                 "SMAT: Smart Attendance System Using Ultrasonic Audio", 36, True, BLACK, PP_ALIGN.CENTER)

tf = add_textbox(slide, Inches(1), Inches(3.8), Inches(11), Inches(0.4),
                 "Group Members", 22, True, DARK_BLUE, PP_ALIGN.CENTER)

members_box = slide.shapes.add_textbox(Inches(3), Inches(4.3), Inches(7), Inches(1.2))
members_tf = members_box.text_frame
members_tf.word_wrap = True
headers = members_tf.paragraphs[0]
headers.text = "<Name>                    <Number>"
headers.font.size = Pt(20)
headers.font.bold = True
headers.font.italic = True
headers.alignment = PP_ALIGN.CENTER
headers.font.color.rgb = BLACK

tf = add_textbox(slide, Inches(1), Inches(5.6), Inches(11), Inches(0.4),
                 "Under the guidance of", 18, False, BLACK, PP_ALIGN.CENTER)
p = tf.paragraphs[0]
p.font.italic = True
tf = add_textbox(slide, Inches(1), Inches(6.0), Inches(11), Inches(0.4),
                 "<Name of the Guide>", 20, True, TEAL, PP_ALIGN.CENTER)
p = tf.paragraphs[0]
p.font.italic = True

bot_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(6.8), prs.slide_width, Inches(0.7))
bot_bar.fill.solid()
bot_bar.fill.fore_color.rgb = TEAL
bot_bar.line.fill.background()
tf = add_textbox(slide, Inches(1), Inches(6.85), Inches(11), Inches(0.4),
                 "Department of Electronics and Communication Engineering", 20, True, WHITE, PP_ALIGN.CENTER)


# ========== SLIDE 1: OUTLINE ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Outline of Presentation")
add_footer_bar(slide)

outline_items = [
    "1.  Introduction",
    "2.  Literature Survey",
    "3.  Problem Statement",
    "4.  Proposed System Architecture",
    "5.  Hardware & Software Requirements",
    "6.  Implementation Updates",
    "7.  Results & Demonstrations",
    "8.  Advantages & Applications",
    "9.  Budget",
    "10. Workflow for Remaining Work",
    "11. Future Scope",
    "12. References",
]

left_items = outline_items[:6]
right_items = outline_items[6:]

for i, item in enumerate(left_items):
    box = add_rounded_box(slide, Inches(0.5), Inches(1.2 + i * 0.85), Inches(5.8), Inches(0.65),
                          ACCENT_BLUE, item, 20, WHITE)

for i, item in enumerate(right_items):
    box = add_rounded_box(slide, Inches(7), Inches(1.2 + i * 0.85), Inches(5.8), Inches(0.65),
                          TEAL, item, 20, WHITE)


# ========== SLIDE 2: INTRODUCTION ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Introduction")
add_footer_bar(slide)

left_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(1.2), Inches(6.2), Inches(5.5))
left_box.fill.solid()
left_box.fill.fore_color.rgb = RGBColor(0xE8, 0xF4, 0xFD)
left_box.line.color.rgb = ACCENT_BLUE
left_box.line.width = Pt(2)

tf = add_textbox(slide, Inches(0.5), Inches(1.3), Inches(5.8), Inches(0.5),
                 "SMAT – Smart Attendance System", 24, True, PURPLE, PP_ALIGN.LEFT)

content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.9), Inches(5.8), Inches(4.5))
ctf = content_box.text_frame
ctf.word_wrap = True
ctf.paragraphs[0].text = ""

items = [
    "Uses ultrasonic audio signals (18-20 kHz) to mark attendance automatically",
    "Teacher's device broadcasts inaudible sound; student's device receives & decodes it",
    "Ensures physical presence — no proxy attendance possible",
    "Works on standard devices (laptops/phones) — no special hardware needed",
    "Uses Web Audio API for signal generation & FFT-based detection",
    "Role-based system: Teacher (broadcast) & Student (listen)",
]
for item in items:
    add_bullet_text(ctf, "▸  " + item, 0, 18, False, BLACK, 8)

right_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.2), Inches(6.2), Inches(2.5))
right_box.fill.solid()
right_box.fill.fore_color.rgb = DARK_BG
right_box.line.fill.background()
tf = add_textbox(slide, Inches(7.0), Inches(1.4), Inches(5.8), Inches(0.4),
                 "How It Works", 22, True, WHITE, PP_ALIGN.CENTER)
flow_items = [
    "1. Teacher starts session → Ultrasonic broadcast",
    "2. Student's mic captures signal → FFT decode",
    "3. 6-char code extracted → Attendance marked",
    "4. Server validates → Stored in database",
]
flow_box = slide.shapes.add_textbox(Inches(7.2), Inches(1.9), Inches(5.5), Inches(1.6))
ftf = flow_box.text_frame
ftf.word_wrap = True
ftf.paragraphs[0].text = ""
for item in flow_items:
    add_bullet_text(ftf, item, 0, 16, False, RGBColor(0xBB, 0xDD, 0xFF), 4)

advantages_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.0), Inches(6.2), Inches(2.7))
advantages_box.fill.solid()
advantages_box.fill.fore_color.rgb = RGBColor(0xE8, 0xF8, 0xE8)
advantages_box.line.color.rgb = GREEN
advantages_box.line.width = Pt(2)
tf = add_textbox(slide, Inches(7.0), Inches(4.1), Inches(5.8), Inches(0.4),
                 "Key Innovation", 22, True, GREEN, PP_ALIGN.CENTER)

innovations = [
    "▸  Proximity verification via ultrasound",
    "▸  No QR codes, no manual roll calls",
    "▸  Browser-based — zero installation",
    "▸  Real-time attendance tracking",
]
inno_box = slide.shapes.add_textbox(Inches(7.2), Inches(4.6), Inches(5.5), Inches(2.0))
itf = inno_box.text_frame
itf.word_wrap = True
itf.paragraphs[0].text = ""
for item in innovations:
    add_bullet_text(itf, item, 0, 18, False, RGBColor(0x00, 0x55, 0x00), 6)


# ========== SLIDE 3: LITERATURE SURVEY ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Literature Survey")
add_footer_bar(slide)

papers = [
    {
        "title": "Traditional Attendance Systems",
        "color": ACCENT_BLUE,
        "points": [
            "Manual roll call — time-consuming, error-prone",
            "Biometric systems — expensive hardware, privacy concerns",
            "RFID-based — requires tags, infrastructure cost",
        ]
    },
    {
        "title": "QR Code / GPS Based Systems",
        "color": TEAL,
        "points": [
            "QR codes can be shared remotely — proxy possible",
            "GPS spoofing allows fake location-based attendance",
            "Bluetooth beacons — require additional hardware setup",
        ]
    },
    {
        "title": "Audio-Based Approaches",
        "color": PURPLE,
        "points": [
            "Near-ultrasonic communication (18-22 kHz) researched for indoor positioning",
            "Inaudible to humans, detectable by standard microphones",
            "Used in proximity verification (Google Nearby, Chirp SDK)",
        ]
    },
    {
        "title": "Research Gap",
        "color": RED,
        "points": [
            "No lightweight, web-based ultrasonic attendance system exists",
            "Existing solutions need native apps or special hardware",
            "Our approach: browser-only, zero-install, ultrasonic verification",
        ]
    },
]

for i, paper in enumerate(papers):
    col = i % 2
    row = i // 2
    left = Inches(0.3 + col * 6.5)
    top = Inches(1.2 + row * 2.9)

    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(6.2), Inches(2.6))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = paper["color"]
    box.line.width = Pt(3)

    title_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.1), top + Inches(0.1),
                                        Inches(6.0), Inches(0.55))
    title_bar.fill.solid()
    title_bar.fill.fore_color.rgb = paper["color"]
    title_bar.line.fill.background()
    ttf = title_bar.text_frame
    ttf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tp = ttf.paragraphs[0]
    tp.text = paper["title"]
    tp.font.size = Pt(20)
    tp.font.bold = True
    tp.font.color.rgb = WHITE
    tp.alignment = PP_ALIGN.CENTER

    content = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.75), Inches(5.6), Inches(1.7))
    ctf = content.text_frame
    ctf.word_wrap = True
    ctf.paragraphs[0].text = ""
    for pt in paper["points"]:
        add_bullet_text(ctf, "▸  " + pt, 0, 16, False, BLACK, 6)


# ========== SLIDE 4: PROBLEM STATEMENT ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Problem Statement")
add_footer_bar(slide)

problems = [
    ("Manual Roll Call", "Time-consuming for large classes;\nerror-prone and disruptive", ACCENT_BLUE),
    ("Proxy Attendance", "Students mark attendance for\nabsent peers using shared codes", RED),
    ("QR / GPS Spoofing", "Digital methods easily bypassed\nwithout physical presence check", ORANGE),
    ("Hardware Cost", "Biometric / RFID systems require\nexpensive infrastructure", PURPLE),
]

for i, (title, desc, color) in enumerate(problems):
    left = Inches(0.3 + i * 3.2)
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.3), Inches(3.0), Inches(2.5))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.fill.background()
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = "\n" + desc
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(0xEE, 0xEE, 0xEE)
    p2.alignment = PP_ALIGN.CENTER

arrow_box = add_textbox(slide, Inches(0.3), Inches(4.1), Inches(12.7), Inches(0.5),
                        "⬇", 36, True, DARK_BLUE, PP_ALIGN.CENTER)

solution_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(4.7), Inches(10.3), Inches(2.0))
solution_box.fill.solid()
solution_box.fill.fore_color.rgb = RGBColor(0xE8, 0xF8, 0xE8)
solution_box.line.color.rgb = GREEN
solution_box.line.width = Pt(3)

tf = solution_box.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.text = "Our Solution: SMAT"
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = GREEN
p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph()
p2.text = "A web-based smart attendance system using ultrasonic audio signals for physical presence verification.\nNo special hardware • No installation • No proxy possible"
p2.font.size = Pt(18)
p2.font.color.rgb = BLACK
p2.alignment = PP_ALIGN.CENTER


# ========== SLIDE 5: PROPOSED SYSTEM ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Proposed System Architecture")
add_footer_bar(slide)

layers = [
    ("Frontend (Browser)", "index.html  |  student.html  |  teacher.html\nWeb Audio API  |  FFT Visualization  |  Responsive UI", RGBColor(0x4C, 0xAF, 0x50)),
    ("REST API (Express 5)", "/auth  |  /sessions  |  /attendance\nJWT Auth  |  Role-based Access  |  Rate Limiting", ACCENT_BLUE),
    ("Service Layer", "Auth Service  |  Session Service  |  Attendance Service\nbcrypt hashing  |  Token management  |  Dedup logic", PURPLE),
    ("Data Layer", "PostgreSQL (users, sessions, records)\nRedis (live sessions, code lookup, dedup, rate limits)", DARK_BLUE),
]

for i, (title, desc, color) in enumerate(layers):
    top = Inches(1.2 + i * 1.35)
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), top, Inches(12.3), Inches(1.15))
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.fill.background()

    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.3)
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(15)
    p2.font.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
    p2.alignment = PP_ALIGN.LEFT

    if i < len(layers) - 1:
        arrow = add_textbox(slide, Inches(6), top + Inches(1.15), Inches(1.3), Inches(0.25),
                            "⬇", 18, True, DARK_BLUE, PP_ALIGN.CENTER)

flow_title = add_textbox(slide, Inches(0.5), Inches(5.8), Inches(12.3), Inches(0.4),
                         "Ultrasonic Signal Flow", 20, True, DARK_BLUE, PP_ALIGN.CENTER)
flow_steps = [
    ("Teacher\nStarts Session", ACCENT_BLUE),
    ("Ultrasonic\nBroadcast", TEAL),
    ("Student Mic\nCapture", ORANGE),
    ("FFT Decode\n6-char Code", PURPLE),
    ("Server\nValidation", RED),
    ("Attendance\nRecorded", GREEN),
]
for i, (label, color) in enumerate(flow_steps):
    left = Inches(0.3 + i * 2.15)
    box = add_rounded_box(slide, left, Inches(6.2), Inches(1.85), Inches(0.7), color, label, 13, WHITE)
    if i < len(flow_steps) - 1:
        add_textbox(slide, left + Inches(1.85), Inches(6.3), Inches(0.3), Inches(0.5),
                    "→", 22, True, BLACK, PP_ALIGN.CENTER)


# ========== SLIDE 6: HW/SW REQUIREMENTS ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Hardware & Software Requirements")
add_footer_bar(slide)

hw_title = add_rounded_box(slide, Inches(0.3), Inches(1.2), Inches(6.2), Inches(0.6), ACCENT_BLUE,
                           "Hardware Requirements", 22, WHITE)
hw_items = [
    "Computer/Laptop with speakers (Teacher side)",
    "Smartphone/Laptop with microphone (Student side)",
    "Standard audio hardware — no special equipment",
    "Network connectivity (Wi-Fi / LAN / Mobile data)",
    "Server machine (for deployment)",
]
hw_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(6.0), Inches(4.0))
htf = hw_box.text_frame
htf.word_wrap = True
htf.paragraphs[0].text = ""
for item in hw_items:
    add_bullet_text(htf, "▸  " + item, 0, 18, False, BLACK, 8)

sw_title = add_rounded_box(slide, Inches(6.8), Inches(1.2), Inches(6.2), Inches(0.6), TEAL,
                           "Software Requirements", 22, WHITE)
sw_items = [
    ("Backend:", "Node.js (ESM), Express 5"),
    ("Database:", "PostgreSQL 16"),
    ("Cache:", "Redis 7 (ioredis)"),
    ("Auth:", "JWT + bcrypt"),
    ("Frontend:", "HTML/CSS/JS, Web Audio API"),
    ("Audio:", "Ultrasonic encoding (18-20 kHz)"),
    ("DevOps:", "Docker, docker-compose"),
    ("Others:", "uuid, dotenv, cors"),
]
sw_box = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(6.0), Inches(4.5))
stf = sw_box.text_frame
stf.word_wrap = True
stf.paragraphs[0].text = ""
for label, value in sw_items:
    p = stf.add_paragraph()
    run1 = p.add_run()
    run1.text = "▸  " + label + "  "
    run1.font.size = Pt(18)
    run1.font.bold = True
    run1.font.color.rgb = DARK_BLUE
    run2 = p.add_run()
    run2.text = value
    run2.font.size = Pt(18)
    run2.font.color.rgb = BLACK
    p.space_before = Pt(8)


# ========== SLIDE 7: IMPLEMENTATION UPDATES ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Implementation Updates")
add_footer_bar(slide)

completed = [
    "User authentication (JWT + bcrypt) with role-based access",
    "Teacher dashboard — start sessions, broadcast ultrasonic signal",
    "Student interface — mic-based signal detection with FFT",
    "Ultrasonic encoding protocol (preamble 17.8 kHz + 6 data tones)",
    "PostgreSQL schema (users, sessions, attendance_records)",
    "Redis integration (live sessions, dedup, rate limiting)",
    "REST API — auth, sessions, attendance endpoints",
    "Real-time attendance count display for teachers",
    "Attendance history for both teachers and students",
    "Docker containerization (docker-compose setup)",
]

done_title = add_rounded_box(slide, Inches(0.3), Inches(1.2), Inches(12.7), Inches(0.6), GREEN,
                              "✓  Completed Modules", 22, WHITE)

left_col = slide.shapes.add_textbox(Inches(0.5), Inches(2.0), Inches(6.2), Inches(4.5))
ltf = left_col.text_frame
ltf.word_wrap = True
ltf.paragraphs[0].text = ""
for item in completed[:5]:
    add_bullet_text(ltf, "✓  " + item, 0, 16, False, RGBColor(0x00, 0x66, 0x00), 6)

right_col = slide.shapes.add_textbox(Inches(6.8), Inches(2.0), Inches(6.2), Inches(4.5))
rtf = right_col.text_frame
rtf.word_wrap = True
rtf.paragraphs[0].text = ""
for item in completed[5:]:
    add_bullet_text(rtf, "✓  " + item, 0, 16, False, RGBColor(0x00, 0x66, 0x00), 6)

progress_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), Inches(5.2), Inches(12.7), Inches(1.5))
progress_box.fill.solid()
progress_box.fill.fore_color.rgb = RGBColor(0xFE, 0xF3, 0xE2)
progress_box.line.color.rgb = ORANGE
progress_box.line.width = Pt(2)
tf = progress_box.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.3)
p = tf.paragraphs[0]
p.text = "Overall Progress: ~85% Complete"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = ORANGE
p.alignment = PP_ALIGN.CENTER
p2 = tf.add_paragraph()
p2.text = "Core functionality fully operational  |  Testing & optimization in progress"
p2.font.size = Pt(16)
p2.font.color.rgb = BLACK
p2.alignment = PP_ALIGN.CENTER


# ========== SLIDE 8: RESULTS ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Results & Demonstrations")
add_footer_bar(slide)

results = [
    {
        "title": "Ultrasonic Signal Generation",
        "desc": "Successfully generates 18-20 kHz tones\nfrom browser using Web Audio API.\nPreamble at 17.8 kHz + 6 data tones.",
        "color": ACCENT_BLUE,
    },
    {
        "title": "Signal Detection & Decoding",
        "desc": "FFT-based mic analysis decodes\n6-character session code in real-time.\nState machine: preamble → decode → done.",
        "color": TEAL,
    },
    {
        "title": "Attendance Accuracy",
        "desc": "Proximity-based verification works\nwithin classroom range (~5-10 meters).\nDuplicate submissions rejected (409).",
        "color": GREEN,
    },
    {
        "title": "System Performance",
        "desc": "JWT auth < 100ms response time.\nRedis dedup prevents race conditions.\nRate limiting handles concurrent users.",
        "color": PURPLE,
    },
]

for i, r in enumerate(results):
    col = i % 2
    row = i // 2
    left = Inches(0.3 + col * 6.5)
    top = Inches(1.2 + row * 2.9)

    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(6.2), Inches(2.6))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = r["color"]
    box.line.width = Pt(3)

    title_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.1), top + Inches(0.1),
                                        Inches(6.0), Inches(0.55))
    title_bar.fill.solid()
    title_bar.fill.fore_color.rgb = r["color"]
    title_bar.line.fill.background()
    ttf = title_bar.text_frame
    ttf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tp = ttf.paragraphs[0]
    tp.text = r["title"]
    tp.font.size = Pt(22)
    tp.font.bold = True
    tp.font.color.rgb = WHITE
    tp.alignment = PP_ALIGN.CENTER

    desc_box = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.8), Inches(5.6), Inches(1.6))
    dtf = desc_box.text_frame
    dtf.word_wrap = True
    dp = dtf.paragraphs[0]
    dp.text = r["desc"]
    dp.font.size = Pt(17)
    dp.font.color.rgb = BLACK
    dp.line_spacing = Pt(24)


# ========== SLIDE 9: ADVANTAGES & APPLICATIONS ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Advantages & Applications")
add_footer_bar(slide)

adv_title = add_rounded_box(slide, Inches(0.3), Inches(1.2), Inches(6.2), Inches(0.55), GREEN,
                             "Advantages", 22, WHITE)
advantages = [
    ("Proximity Verified", "Ultrasonic range ensures physical presence"),
    ("Zero Hardware Cost", "Uses existing speakers & microphones"),
    ("No Installation", "100% browser-based, works on any device"),
    ("Anti-Proxy", "Signal can't be forwarded remotely easily"),
    ("Real-time Tracking", "Teachers see live attendance count"),
    ("Fast & Efficient", "Entire process takes < 30 seconds"),
]
for i, (title, desc) in enumerate(advantages):
    y = Inches(1.9 + i * 0.8)
    p_box = slide.shapes.add_textbox(Inches(0.5), y, Inches(6.0), Inches(0.7))
    ptf = p_box.text_frame
    ptf.word_wrap = True
    run1 = ptf.paragraphs[0].add_run()
    run1.text = "▸  " + title + ":  "
    run1.font.size = Pt(17)
    run1.font.bold = True
    run1.font.color.rgb = GREEN
    run2 = ptf.paragraphs[0].add_run()
    run2.text = desc
    run2.font.size = Pt(17)
    run2.font.color.rgb = BLACK

app_title = add_rounded_box(slide, Inches(6.8), Inches(1.2), Inches(6.2), Inches(0.55), ACCENT_BLUE,
                             "Applications", 22, WHITE)
applications = [
    "Universities & Colleges",
    "Schools (K-12)",
    "Corporate Training Sessions",
    "Workshops & Seminars",
    "Examination Halls",
    "Conference Attendance Tracking",
]
for i, app in enumerate(applications):
    box = add_rounded_box(slide, Inches(7.0), Inches(2.0 + i * 0.82), Inches(5.8), Inches(0.62),
                          RGBColor(0xE8, 0xF4, 0xFD), "▸  " + app, 18, DARK_BLUE)
    box.line.color.rgb = ACCENT_BLUE
    box.line.width = Pt(1)


# ========== SLIDE 10: BUDGET ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Budget")
add_footer_bar(slide)

budget_title = add_textbox(slide, Inches(0.5), Inches(1.3), Inches(12.3), Inches(0.5),
                           "Cost Analysis — Minimal Budget Project", 24, True, DARK_BLUE, PP_ALIGN.CENTER)

headers_row = [("Item", 4.0), ("Cost", 2.5), ("Notes", 5.5)]
col_starts = [Inches(0.7), Inches(4.7), Inches(7.2)]
col_widths = [Inches(4.0), Inches(2.5), Inches(5.5)]

header_top = Inches(2.2)
for i, (h, w) in enumerate(headers_row):
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_starts[i], header_top, col_widths[i], Inches(0.55))
    box.fill.solid()
    box.fill.fore_color.rgb = DARK_BLUE
    box.line.color.rgb = WHITE
    box.line.width = Pt(1)
    tf = box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = h
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

budget_rows = [
    ("Server Hosting (VPS)", "₹0 – ₹500/mo", "Free tier available (Render, Railway)"),
    ("PostgreSQL Database", "₹0", "Free tier on cloud providers"),
    ("Redis Cache", "₹0", "Free tier (Upstash / Railway)"),
    ("Domain Name (optional)", "₹500 – ₹1000/yr", "Optional for deployment"),
    ("Development Tools", "₹0", "VS Code, Git, Docker — all free"),
    ("Hardware", "₹0", "Uses existing devices"),
]

for r, (item, cost, notes) in enumerate(budget_rows):
    row_top = Inches(2.75 + r * 0.55)
    bg = WHITE if r % 2 == 0 else LIGHT_GRAY
    vals = [item, cost, notes]
    for i in range(3):
        box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_starts[i], row_top, col_widths[i], Inches(0.55))
        box.fill.solid()
        box.fill.fore_color.rgb = bg
        box.line.color.rgb = RGBColor(0xCC, 0xCC, 0xCC)
        box.line.width = Pt(1)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = vals[i]
        p.font.size = Pt(16)
        p.font.color.rgb = BLACK
        p.alignment = PP_ALIGN.CENTER

total_top = Inches(2.75 + len(budget_rows) * 0.55)
total_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, col_starts[0], total_top,
                                    Inches(12.0), Inches(0.6))
total_box.fill.solid()
total_box.fill.fore_color.rgb = RGBColor(0xE8, 0xF8, 0xE8)
total_box.line.color.rgb = GREEN
total_box.line.width = Pt(2)
tf = total_box.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.text = "Total Estimated Cost:  ₹0 – ₹1,500  (Minimal / Near-Zero Budget)"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = GREEN
p.alignment = PP_ALIGN.CENTER


# ========== SLIDE 11: WORKFLOW ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Workflow for Remaining Work")
add_footer_bar(slide)

tasks = [
    ("Week 1-2", "Testing & Bug Fixes", "Cross-browser testing, edge case handling,\naudio reliability in noisy environments", ACCENT_BLUE),
    ("Week 3", "Security Hardening", "Input validation, HTTPS enforcement,\ntoken rotation, penetration testing", RED),
    ("Week 4", "UI/UX Polish", "Responsive design improvements,\naccessibility, loading states, error handling", PURPLE),
    ("Week 5", "Performance Optimization", "Audio detection accuracy tuning,\nAPI response optimization, caching strategy", ORANGE),
    ("Week 6", "Deployment & Documentation", "Production deployment, user manual,\nAPI documentation, final testing", GREEN),
]

for i, (week, title, desc, color) in enumerate(tasks):
    top = Inches(1.15 + i * 1.1)
    
    week_box = add_rounded_box(slide, Inches(0.3), top, Inches(2.0), Inches(0.9), color, week, 18, WHITE)
    
    title_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.5), top, Inches(3.5), Inches(0.9))
    title_box.fill.solid()
    title_box.fill.fore_color.rgb = WHITE
    title_box.line.color.rgb = color
    title_box.line.width = Pt(2)
    tf = title_box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color
    p.alignment = PP_ALIGN.CENTER

    desc_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.2), top, Inches(6.8), Inches(0.9))
    desc_box.fill.solid()
    desc_box.fill.fore_color.rgb = LIGHT_GRAY
    desc_box.line.color.rgb = color
    desc_box.line.width = Pt(1)
    tf = desc_box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = desc
    p.font.size = Pt(15)
    p.font.color.rgb = BLACK
    p.alignment = PP_ALIGN.LEFT


# ========== SLIDE 12: FUTURE SCOPE ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  Future Scope")
add_footer_bar(slide)

future_items = [
    ("Multi-Frequency Encoding", "Use multiple simultaneous frequencies\nfor faster, more robust code transmission", ACCENT_BLUE),
    ("Mobile App (PWA)", "Convert to Progressive Web App for\noffline support and push notifications", TEAL),
    ("Analytics Dashboard", "Attendance trends, class-wise reports,\nstudent engagement metrics", PURPLE),
    ("AI-based Anomaly Detection", "Detect unusual patterns like\nsudden attendance spikes or drops", RED),
    ("Integration with LMS", "Connect with Moodle, Google Classroom,\nor university ERP systems", ORANGE),
    ("Multi-room Support", "Unique frequency bands per room to\navoid cross-room interference", GREEN),
]

for i, (title, desc, color) in enumerate(future_items):
    col = i % 3
    row = i // 3
    left = Inches(0.3 + col * 4.3)
    top = Inches(1.2 + row * 2.9)

    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(4.0), Inches(2.6))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = color
    box.line.width = Pt(3)

    icon_box = add_rounded_box(slide, left + Inches(0.2), top + Inches(0.2), Inches(3.6), Inches(0.55),
                                color, title, 18, WHITE)

    desc_tb = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.9), Inches(3.4), Inches(1.5))
    dtf = desc_tb.text_frame
    dtf.word_wrap = True
    dp = dtf.paragraphs[0]
    dp.text = desc
    dp.font.size = Pt(16)
    dp.font.color.rgb = BLACK
    dp.line_spacing = Pt(22)


# ========== SLIDE 13: REFERENCES ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_header_bar(slide, "  References")
add_footer_bar(slide)

references = [
    '[1]  W3C, "Web Audio API Specification," W3C Working Draft, 2024.',
    '[2]  Mozilla Developer Network, "Using the Web Audio API," MDN Web Docs.',
    '[3]  R. Nandakumar et al., "Dhwani: Secure Peer-to-Peer Acoustic NFC," ACM SIGCOMM, 2013.',
    '[4]  Google, "Nearby Connections API — Audio-based proximity detection," Google Developers.',
    '[5]  Chirp.io (Asio Ltd.), "Data-over-sound technology for IoT and mobile," 2020.',
    '[6]  A. Madhavapeddy et al., "Audio Networking: The Forgotten Wireless Technology," IEEE Pervasive Computing, 2005.',
    '[7]  Express.js Documentation, "Express 5.x API Reference," expressjs.com.',
    '[8]  PostgreSQL Global Development Group, "PostgreSQL 16 Documentation," postgresql.org.',
    '[9]  Redis Ltd., "Redis 7 Documentation," redis.io.',
    '[10] Auth0, "Introduction to JSON Web Tokens," jwt.io.',
]

ref_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.3), Inches(5.5))
rtf = ref_box.text_frame
rtf.word_wrap = True
rtf.paragraphs[0].text = ""
for ref in references:
    add_bullet_text(rtf, ref, 0, 16, False, BLACK, 10)


# ========== SLIDE 14: THANK YOU ==========
slide = prs.slides.add_slide(prs.slide_layouts[6])

bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = DARK_BLUE
bg.line.fill.background()

tf = add_textbox(slide, Inches(1), Inches(2.0), Inches(11), Inches(1.0),
                 "Thank You!", 54, True, WHITE, PP_ALIGN.CENTER)

tf = add_textbox(slide, Inches(1), Inches(3.5), Inches(11), Inches(0.6),
                 "SMAT: Smart Attendance System Using Ultrasonic Audio", 24, False, RGBColor(0xBB, 0xDD, 0xFF), PP_ALIGN.CENTER)

tf = add_textbox(slide, Inches(1), Inches(4.5), Inches(11), Inches(0.6),
                 "Questions & Discussion", 28, True, ORANGE, PP_ALIGN.CENTER)

bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(6.5), prs.slide_width, Inches(1.0))
bot.fill.solid()
bot.fill.fore_color.rgb = TEAL
bot.line.fill.background()
tf = add_textbox(slide, Inches(1), Inches(6.6), Inches(11), Inches(0.5),
                 "Department of Electronics and Communication Engineering  |  IIIT Surat", 18, False, WHITE, PP_ALIGN.CENTER)


# Save
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SMAT_Attendance_Presentation.pptx")
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
