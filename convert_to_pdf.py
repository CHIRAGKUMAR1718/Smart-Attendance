import re
from fpdf import FPDF

class StudyGuidePDF(FPDF):
    def __init__(self):
        super().__init__('P', 'mm', 'A4')
        self.add_font("NotoSans", "", "C:/Windows/Fonts/arial.ttf")
        self.add_font("NotoSans", "B", "C:/Windows/Fonts/arialbd.ttf")
        self.add_font("NotoSans", "I", "C:/Windows/Fonts/ariali.ttf")
        self.add_font("NotoSans", "BI", "C:/Windows/Fonts/arialbi.ttf")
        self.add_font("Consolas", "", "C:/Windows/Fonts/consola.ttf")
        self.set_auto_page_break(auto=True, margin=18)

    def header(self):
        if self.page_no() > 1:
            self.set_font("NotoSans", "I", 7.5)
            self.set_text_color(120, 130, 150)
            self.cell(0, 5, "SMAT Study Guide — IIIT Surat", align="L")
            self.ln(2)
            self.set_draw_color(200, 200, 220)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-14)
        self.set_font("NotoSans", "", 8)
        self.set_text_color(150, 160, 180)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")

    def section_title(self, text):
        self.set_font("NotoSans", "B", 18)
        self.set_text_color(10, 31, 60)
        self.ln(4)
        self.multi_cell(0, 9, text)
        self.set_draw_color(99, 102, 241)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def sub_heading(self, text):
        self.set_font("NotoSans", "B", 14)
        self.set_text_color(0, 51, 102)
        self.ln(3)
        self.multi_cell(0, 7.5, text)
        self.set_draw_color(0, 180, 216)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(3)

    def sub_sub_heading(self, text):
        self.set_font("NotoSans", "B", 12)
        self.set_text_color(99, 102, 241)
        self.ln(2)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def body_text(self, text, bold=False, italic=False):
        style = ""
        if bold and italic: style = "BI"
        elif bold: style = "B"
        elif italic: style = "I"
        self.set_x(10)
        self.set_font("NotoSans", style, 10)
        self.set_text_color(30, 41, 59)
        self.multi_cell(190, 5.5, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Consolas", "", 9)
        self.set_fill_color(15, 23, 42)
        self.set_text_color(226, 232, 240)
        x = self.get_x()
        self.set_x(12)
        self.multi_cell(186, 5, text, fill=True)
        self.set_x(x)
        self.ln(2)

    def bullet(self, text, indent=12):
        self.set_font("NotoSans", "", 10)
        self.set_text_color(30, 41, 59)
        self.set_x(indent)
        self.cell(5, 5.5, chr(8226))
        self.set_x(indent + 5)
        self.multi_cell(190 - indent, 5.5, text)

    def label_value(self, label, value):
        self.set_x(10)
        self.set_font("NotoSans", "B", 10)
        self.set_text_color(0, 51, 102)
        lw = self.get_string_width(label + "  ") + 2
        self.cell(lw, 5.5, label + "  ")
        self.set_font("NotoSans", "", 10)
        self.set_text_color(51, 65, 85)
        self.multi_cell(190 - lw, 5.5, value)

    def table(self, headers, rows):
        n = len(headers)
        col_w = (190) / n
        self.set_font("NotoSans", "B", 9)
        self.set_fill_color(10, 31, 60)
        self.set_text_color(255, 255, 255)
        for h in headers:
            self.cell(col_w, 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_font("NotoSans", "", 8.5)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(248, 250, 252)
            else:
                self.set_fill_color(255, 255, 255)
            self.set_text_color(30, 41, 59)
            row_h = 6
            for cell_text in row:
                self.cell(col_w, row_h, cell_text, border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(2)

    def separator(self):
        self.ln(2)
        self.set_draw_color(226, 232, 240)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def highlight_box(self, text, bg=(238, 242, 255), border_color=(99, 102, 241)):
        self.set_fill_color(*bg)
        self.set_draw_color(*border_color)
        self.set_line_width(0.5)
        self.set_font("NotoSans", "I", 10)
        self.set_text_color(51, 65, 85)
        y = self.get_y()
        self.rect(10, y, 190, 14, style="DF")
        self.set_xy(14, y + 2)
        self.multi_cell(182, 5, text)
        self.ln(4)

    def qa_block(self, q, a_en, a_hi):
        self.set_x(10)
        self.set_font("NotoSans", "B", 10)
        self.set_text_color(190, 24, 93)
        self.multi_cell(190, 5.5, "Q: " + q)
        self.set_x(10)
        self.set_font("NotoSans", "", 9.5)
        self.set_text_color(0, 80, 0)
        self.multi_cell(190, 5, "Eng: " + a_en)
        self.set_x(10)
        self.set_text_color(80, 50, 0)
        self.multi_cell(190, 5, "Hin: " + a_hi)
        self.ln(2)


pdf = StudyGuidePDF()
pdf.set_title("SMAT Study Guide")
pdf.set_author("IIIT Surat")

# ─── COVER PAGE ───
pdf.add_page()
pdf.ln(30)
pdf.set_font("NotoSans", "B", 28)
pdf.set_text_color(10, 31, 60)
pdf.cell(0, 14, "SMAT", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("NotoSans", "", 14)
pdf.set_text_color(99, 102, 241)
pdf.cell(0, 8, "Smart Attendance System", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 8, "Using Ultrasonic Audio Signals", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(4)
pdf.set_draw_color(99, 102, 241)
pdf.set_line_width(0.8)
pdf.line(60, pdf.get_y(), 150, pdf.get_y())
pdf.ln(8)
pdf.set_font("NotoSans", "", 12)
pdf.set_text_color(51, 65, 85)
pdf.cell(0, 7, "Complete Study Guide for Project Presentation", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.cell(0, 7, "English + Hinglish", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(15)
pdf.set_font("NotoSans", "B", 11)
pdf.set_text_color(0, 128, 128)
pdf.cell(0, 7, "Indian Institute of Information Technology Surat", align="C", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("NotoSans", "", 10)
pdf.set_text_color(100, 116, 139)
pdf.cell(0, 7, "Department of Electronics & Communication Engineering", align="C", new_x="LMARGIN", new_y="NEXT")

# ─── TABLE OF CONTENTS ───
pdf.add_page()
pdf.section_title("Table of Contents")
toc = [
    "1. Overview — What is SMAT?",
    "2. Problem Statement — Why We Built This",
    "3. PART 1: GENERATOR (Teacher Side)",
    "   3.1 How the Generator Works (Step by Step)",
    "   3.2 Key Technical Parameters",
    "   3.3 Common Teacher Questions",
    "4. PART 2: RECEIVER (Student Side)",
    "   4.1 How the Receiver Works (Step by Step)",
    "   4.2 Key Technical Parameters",
    "   4.3 Common Teacher Questions",
    "5. PART 3: WEBSITE (Backend & Database)",
    "   5.1 Authentication (Login System)",
    "   5.2 Session Management",
    "   5.3 Attendance Marking (Core Logic)",
    "   5.4 Database Design (3 Tables)",
    "   5.5 API Endpoints",
    "   5.6 Security Features",
    "   5.7 Docker Deployment",
    "   5.8 Common Teacher Questions",
    "6. How All Three Parts Connect",
    "7. Comparison Table — SMAT vs Others",
    "8. Quick Glossary",
]
for item in toc:
    pdf.set_font("NotoSans", "", 10.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6.5, item, new_x="LMARGIN", new_y="NEXT")

# ─── OVERVIEW ───
pdf.add_page()
pdf.section_title("1. Overview — What is SMAT?")

pdf.sub_sub_heading("English:")
pdf.body_text("SMAT is a Smart Attendance Marking system that uses inaudible ultrasonic sound signals (18,000-20,000 Hz) to mark attendance. The teacher's laptop speaker broadcasts a secret 6-character code encoded as high-frequency tones. The student's phone microphone picks up the sound, decodes the code, and automatically marks attendance. Only students physically present in the classroom can hear the signal — it cannot travel through walls or be shared over the internet.")

pdf.sub_sub_heading("Hinglish:")
pdf.body_text("SMAT ek Smart Attendance system hai jo sunai na dene wali ultrasonic sound (18,000-20,000 Hz) use karta hai attendance mark karne ke liye. Teacher ka laptop speaker ek secret 6-character code ko high-frequency tones mein convert karke play karta hai. Student ka phone microphone us sound ko sunta hai, code nikalta hai, aur automatically attendance mark kar deta hai. Sirf woh students jo classroom mein physically baithe hain wohi yeh signal sun sakte hain — yeh deewar paar nahi kar sakta aur internet pe share nahi ho sakta.")

# ─── PROBLEM STATEMENT ───
pdf.separator()
pdf.section_title("2. Problem Statement — Why We Built This")

problems = [
    ("Time Waste", "Manual roll call takes 5-10 minutes in large classes. Wasted teaching time.", "Manual roll call mein 5-10 minute lagte hain. Teaching ka time waste."),
    ("Proxy Attendance", "Friends mark absent students present. QR codes shared on WhatsApp.", "Dost absent students ki attendance laga dete hain. QR WhatsApp pe share."),
    ("GPS Spoofing", "Location-based apps tricked using free spoofing apps.", "Location apps ko free spoofing apps se dhoka diya ja sakta hai."),
    ("Hardware Cost", "Biometric/RFID machines cost Rs 5,000-50,000 per classroom.", "Biometric/RFID ka kharcha Rs 5,000-50,000 per classroom."),
]
pdf.table(["Problem", "English", "Hinglish"],
          [(p[0], p[1], p[2]) for p in problems])

pdf.highlight_box("Our Solution: Use ultrasonic sound — cannot be shared online, cannot pass through walls, uses existing laptop speakers and phone microphones — zero extra cost.")

# ═══════════════════════════════════════
# PART 1: GENERATOR
# ═══════════════════════════════════════
pdf.add_page()
pdf.section_title("3. PART 1: GENERATOR")
pdf.sub_heading("Teacher Side — Ultrasonic Signal Broadcasting")

pdf.sub_sub_heading("What Does the Generator Do?")
pdf.body_text("English: The generator is the teacher's side. It takes a 6-character session code and converts it into inaudible sound waves that play from the laptop speaker. Like a radio station — but broadcasting a secret code using sound humans can't hear.")
pdf.body_text("Hinglish: Generator teacher ka side hai. Yeh ek 6-character code ko sunai na dene wali sound waves mein convert karta hai jo speaker se play hoti hain. Jaise radio station — par music ki jagah secret code broadcast karta hai aisi sound mein jo insaan sun nahi sakta.")

pdf.sub_heading("3.1 How the Generator Works")

pdf.sub_sub_heading("Step 1 — Teacher starts a session")
pdf.body_text("English: Teacher enters a Class ID (like 'CS301') and duration (like 5 min). Server creates a unique 6-character code like X7K3NP. This code will be hidden in sound.")
pdf.body_text("Hinglish: Teacher Class ID daalta hai (jaise 'CS301') aur time set karta hai. Server ek 6-letter code banata hai jaise X7K3NP. Yeh code ab sound mein convert hoga.")

pdf.sub_sub_heading("Step 2 — Each character mapped to a frequency")
pdf.body_text("English: We use 30 characters: ABCDEFGHJKMNPQRSTUVWXYZ23456789 (confusing ones removed). Each gets a unique frequency: Base = 18,000 Hz, step = 55 Hz per character. So A = 18,000 Hz, B = 18,055 Hz, C = 18,110 Hz... up to ~19,925 Hz. All above 17,000 Hz — humans can't hear, microphones can detect.")
pdf.body_text("Hinglish: 30 characters use kiye: ABCDEFGHJKMNPQRSTUVWXYZ23456789. Har character ki fixed frequency: Base = 18,000 Hz, har agla 55 Hz upar. A = 18,000 Hz, B = 18,055 Hz... Sab 17,000 Hz se upar — insaan ko sunai nahi, phone mic detect kar leta hai.")

pdf.sub_sub_heading("Step 3 — Broadcasting sequence")
pdf.table(
    ["Part", "Frequency", "Duration", "Purpose"],
    [
        ("Preamble", "17,800 Hz", "250 ms", "Sync — 'data coming!'"),
        ("Char 1", "e.g. 18,000 Hz", "180 ms", "1st letter of code"),
        ("Silence", "—", "90 ms", "Gap between chars"),
        ("Char 2", "e.g. 18,275 Hz", "180 ms", "2nd letter"),
        ("... (3-6)", "...", "180+90 ms", "Same pattern"),
        ("Pause", "—", "650 ms", "Before repeating"),
    ]
)
pdf.body_text("Entire sequence repeats in a loop until session expires. One full cycle = ~2.3 seconds.")

pdf.sub_sub_heading("Step 4 — How sound is generated in browser")
pdf.body_text("English: Uses Web Audio API's OscillatorNode to generate pure sine waves. GainNode controls volume with 6ms fade to prevent pops. Simple: browser makes an invisible tone player — one tone per letter, one at a time.")
pdf.body_text("Hinglish: Browser ki Web Audio API ka OscillatorNode pure sine wave generate karta hai. GainNode volume control karta hai — 6ms fade se pop/tick nahi aata. Simple: browser ek invisible tone player banata hai — ek tone = ek letter.")

pdf.sub_heading("3.2 Key Technical Parameters")
pdf.table(
    ["Parameter", "Value", "Why (English)", "Kyun (Hinglish)"],
    [
        ("Freq range", "18,000-19,925 Hz", "Above hearing, within mic range", "Sunai nahi, mic detect kare"),
        ("Preamble", "17,800 Hz", "Below data range, no confusion", "Data se neeche, confuse nahi"),
        ("Tone dur.", "180 ms", "Enough for FFT, still fast", "FFT detect kare, fast bhi"),
        ("Gap", "90 ms", "Prevents tone overlap", "Tone mix na ho"),
        ("Cycle pause", "650 ms", "Receiver processing time", "Receiver ko time mile"),
        ("Gain ramp", "6 ms", "No click sounds", "Tick sound na aaye"),
    ]
)

pdf.sub_heading("3.3 Generator — Teacher Questions")

pdf.qa_block(
    "Why ultrasonic and not normal sound?",
    "Normal sound (below 17 kHz) would be audible and annoying. Ultrasonic (18-20 kHz) is silent to humans but detectable by standard microphones.",
    "Normal sound sunai degi — disturbing hoga. Ultrasonic silent hai insaan ke liye, par mic detect kar leta hai."
)
pdf.qa_block(
    "Why sine waves specifically?",
    "Sine wave has energy at only one frequency — clean sharp peak in FFT. Complex sounds spread across frequencies, harder to detect.",
    "Sine wave mein ek hi frequency pe energy — FFT mein clean peak. Complex sound mein bahut frequencies mix, detect mushkil."
)
pdf.qa_block(
    "Can speakers actually play 18 kHz?",
    "Yes. Most laptop speakers produce up to 20-22 kHz. Some may drop off but still enough for mic detection.",
    "Haan. Zyaadatar speakers 20-22 kHz tak produce kar sakte hain. Thoda weak ho toh bhi mic detect kar leta hai."
)

# ═══════════════════════════════════════
# PART 2: RECEIVER
# ═══════════════════════════════════════
pdf.add_page()
pdf.section_title("4. PART 2: RECEIVER")
pdf.sub_heading("Student Side — Signal Detection & Decoding")

pdf.sub_sub_heading("What Does the Receiver Do?")
pdf.body_text("English: Uses the phone's microphone to listen for the ultrasonic code from teacher's speaker. Decodes the hidden message and automatically submits to server. Student just clicks 'Start Listening' and waits.")
pdf.body_text("Hinglish: Phone ke microphone se teacher ke speaker ki ultrasonic sound sunta hai, code nikalta hai, aur automatically server ko bhej deta hai. Student sirf 'Start Listening' dabaye aur wait kare.")

pdf.sub_heading("4.1 How the Receiver Works")

pdf.sub_sub_heading("Step 1 — Microphone activated")
pdf.body_text("English: Student clicks 'Start Listening'. Browser asks mic permission (needs HTTPS). Audio stream connects to AnalyserNode (Web Audio API).")
pdf.body_text("Hinglish: Student button dabata hai. Browser mic permission maangta hai (HTTPS zaroori). Audio data AnalyserNode ko jaata hai.")

pdf.sub_sub_heading("Step 2 — FFT analysis begins")
pdf.body_text("English: FFT = Fast Fourier Transform. It takes mixed sound and separates into individual frequencies. Like hearing a piano chord and identifying each note. If sound has 18,110 Hz, FFT shows a peak there = character 'C'. Settings: 8192 bins, ~5.86 Hz per bin, checks every 30ms.")
pdf.body_text("Hinglish: FFT = Fast Fourier Transform. Mixed sound ko alag frequencies mein todta hai. Jaise piano chord sun ke har note pehchanno. Agar sound mein 18,110 Hz hai toh FFT wahan peak dikhayega = character 'C'. Settings: 8192 bins, ~5.86 Hz per bin, har 30ms check.")

pdf.sub_sub_heading("Step 3 — State machine decoding")
pdf.code_block("IDLE -> PREAMBLE DETECTED -> RECEIVING CHARS -> COMPLETE")
pdf.body_text("English:\n- IDLE: Scanning for 17,800 Hz preamble\n- PREAMBLE: Found! Must appear 4 consecutive times (~120ms) to confirm\n- RECEIVING: Reads 6 tones, finds peak frequency, uses quadratic interpolation for accuracy, converts to character, median filter rejects noise\n- COMPLETE: All 6 decoded, sends to server\n- 8-second timeout resets to IDLE if stuck")
pdf.body_text("Hinglish:\n- IDLE: 17,800 Hz dhoondh raha hai\n- PREAMBLE MILA: 4 baar lagaataar dikhna chahiye — noise nahi hai confirm\n- RECEIVING: 6 tones padho, peak frequency dhoondho, interpolation se accurate karo, median filter noise hataye\n- COMPLETE: 6 chars decode, server ko bhejo\n- 8 second stuck toh reset, agla cycle mein try")

pdf.sub_sub_heading("Step 4 — Auto-submission")
pdf.body_text("English: Decoded code sent to API -> server looks up in Redis -> finds session -> marks attendance. Student sees success. Fully automatic.")
pdf.body_text("Hinglish: Code server ko jaata hai -> Redis mein check -> session milta hai -> attendance mark. Screen pe success dikhe. Sab automatic.")

pdf.sub_sub_heading("What is Quadratic Interpolation? (Simple)")
pdf.body_text("English: FFT gives discrete bins. True frequency may fall between two bins. We look at a bin + its 2 neighbours, fit a curve, estimate exact peak. Gives sub-bin accuracy.")
pdf.body_text("Hinglish: FFT fixed boxes mein answer deta hai. Asli frequency do boxes ke beech ho sakti hai. Teen boxes dekh ke curve fit karte hain, exact peak nikaalte hain. Zyada accurate.")

pdf.sub_heading("4.2 Key Technical Parameters")
pdf.table(
    ["Parameter", "Value", "Why (English)", "Kyun (Hinglish)"],
    [
        ("FFT Size", "8192 bins", "~5.86 Hz resolution for 55 Hz steps", "5.86 Hz precision, 55 Hz fark pakde"),
        ("Sample rate", "~48,000 Hz", "Standard mic, up to 24 kHz", "Standard phone mic rate"),
        ("Polling", "Every 30 ms", "~6 readings per 180ms tone", "1 sec mein 33 baar check"),
        ("Threshold", "-70 dB", "Ignore weak noise", "Weak signals ignore karo"),
        ("Preamble", "4 frames", "Confirm real signal", "4 baar = pakka signal"),
        ("Timeout", "8 seconds", "Reset if stuck", "Stuck toh reset, phir try"),
        ("Noise", "Median filter", "Most common reading wins", "Sabse common value = answer"),
    ]
)

pdf.sub_heading("4.3 Receiver — Teacher Questions")
pdf.qa_block(
    "What if classroom has fan noise or talking?",
    "Ambient noise is below 5,000 Hz. Our range is 17,800-20,000 Hz — completely separate zones. Like AM and FM radio don't interfere.",
    "Fan/baatein 5,000 Hz se neeche. Humara range 17,800-20,000 Hz — completely alag zone. Jaise AM aur FM radio ek doosre ko disturb nahi karte."
)
pdf.qa_block(
    "What if 50 students listen simultaneously?",
    "No problem. Microphones only receive. Like 50 students reading the same whiteboard — they don't block each other.",
    "Koi problem nahi. Mic sirf sunta hai. Jaise 50 students ek whiteboard padh sakte hain bina roke."
)
pdf.qa_block(
    "What if decoding fails halfway?",
    "8-second timeout resets to IDLE. Generator loops every 2.3s, so it retries. Most succeed in 1-2 cycles.",
    "8 sec timeout reset karta hai. Generator 2.3s mein repeat, agla cycle mein try. 1-2 cycle mein ho jaata hai."
)
pdf.qa_block(
    "Maximum range?",
    "5-10 meters. Intentional — only students inside classroom can hear. Cannot pass through walls.",
    "5-10 meter. Feature hai — sirf classroom ke students detect karein. Deewar paar nahi hota."
)
pdf.qa_block(
    "Can someone record and replay later?",
    "Each code expires via Redis TTL. Replaying after session ends fails — code no longer exists.",
    "Har code expire hota hai TTL se. Session khatam ke baad play karo toh fail — code exist nahi karega."
)

# ═══════════════════════════════════════
# PART 3: WEBSITE
# ═══════════════════════════════════════
pdf.add_page()
pdf.section_title("5. PART 3: WEBSITE")
pdf.sub_heading("Backend, Database, Auth & Deployment")

pdf.sub_sub_heading("What Does the Website Do?")
pdf.body_text("English: The backbone connecting everything. Handles user accounts, creates/manages sessions, records attendance, and prevents cheating. Generator and Receiver are delivery — Website is where data lives.")
pdf.body_text("Hinglish: Backbone jo sab connect karta hai. Accounts, sessions, attendance record, cheating rokna. Generator/Receiver sirf delivery — asli data Website mein.")

pdf.sub_sub_heading("Architecture (4 Layers)")
pdf.table(
    ["Layer", "What", "Role"],
    [
        ("Frontend", "HTML pages", "User interface — buttons, forms, FFT visual"),
        ("API", "Express 5 / Node.js", "Handle HTTP requests"),
        ("Services", "Business logic", "Password, code gen, dedup"),
        ("Data", "PostgreSQL + Redis", "Permanent + temporary storage"),
    ]
)

pdf.sub_heading("5.1 Authentication (Login System)")

pdf.sub_sub_heading("Registration")
pdf.body_text("English: User sends email + password + role. Server hashes password with bcrypt (12 rounds) — 'mypass123' becomes '$2b$12$xYz...' which CANNOT be reversed. Stores in DB. Returns 2 JWT tokens.")
pdf.body_text("Hinglish: User email + password + role bhejta hai. Server bcrypt se hash karta hai — 'mypass123' convert hota hai unreadable string mein — wapas badalna IMPOSSIBLE. DB mein save. 2 JWT tokens milte hain.")

pdf.sub_sub_heading("Login")
pdf.body_text("English: User sends email + password. Server fetches hash from DB. bcrypt.compare() checks match. If yes -> 2 tokens returned.")
pdf.body_text("Hinglish: Email + password bhejo. Server DB se hash nikalti hai. bcrypt.compare() match check karta hai. Match -> 2 tokens milte hain.")

pdf.sub_sub_heading("The Two Tokens")
pdf.table(
    ["Token", "Expires", "English", "Hinglish"],
    [
        ("Access Token", "2 hours", "Sent with every request", "Har request ke saath jaata hai"),
        ("Refresh Token", "7 days", "Get new access token", "Naya access token lo bina password"),
    ]
)

pdf.sub_sub_heading("What is JWT?")
pdf.body_text("English: JWT = digitally signed ID card. Contains user ID + role, signed with server's secret key. If tampered, signature breaks = request rejected.")
pdf.body_text("Hinglish: JWT = digital signed ID card. User ID + role likha hai, server ki secret key se sign. Kuch change karo toh signature match nahi = reject.")

pdf.sub_sub_heading("Role-Based Access")
pdf.body_text("English: Middleware (security guard) before every protected API. Checks role — teachers use teacher APIs, students use student APIs only.")
pdf.body_text("Hinglish: Middleware (security guard) har protected API ke aage. Role check — teacher teacher ka kaam, student student ka.")

pdf.sub_heading("5.2 Session Management")
pdf.body_text("English: Teacher sends classId + duration. Server generates UUID + 6-char code. Stores in Redis (with TTL auto-expiry) AND PostgreSQL (permanent). Two Redis keys: chirp:session:{uuid} for session details, chirp:code:{code} for code-to-session lookup.")
pdf.body_text("Hinglish: Teacher classId + duration bhejta hai. Server UUID + 6-char code banata hai. Redis mein (TTL se auto-delete) AUR PostgreSQL mein (permanent) save. Do Redis keys: chirp:session:{uuid} session details ke liye, chirp:code:{code} code se session dhundhne ke liye.")

pdf.sub_sub_heading("What is TTL?")
pdf.body_text("TTL = Time To Live. Redis mein data daalte waqt bolte hain 'ise 300 seconds baad delete kar dena.' Code automatically expire hota hai — manually kuch nahi karna.")

pdf.sub_heading("5.3 Attendance Marking (Core Logic)")
pdf.body_text("Step 1 — Code Lookup: Check chirp:code:{code} in Redis -> get session ID. Not found = 'expired'.")
pdf.body_text("Step 2 — Session Check: Check chirp:session:{id} in Redis. Not found = expired.")
pdf.body_text("Step 3 — Duplicate Check (Redis): Check attendance:{sid}:{uid}. Exists = 'Already marked'. Not = create key with 120s TTL.")
pdf.body_text("Step 4 — DB Insert: Insert into attendance_records. Unique constraint violation = 'Already marked'. Otherwise = Success!")

pdf.sub_sub_heading("Why duplicate check at two levels?")
pdf.body_text("English: Redis is first check — microseconds fast, catches most duplicates. DB unique constraint is safety net — if Redis fails, DB blocks duplicates. Defense in depth = two protection layers.")
pdf.body_text("Hinglish: Redis pehla check — bohot fast. DB unique constraint backup — Redis fail toh bhi duplicate nahi. Do layers — jaise gate bhi lock bhi.")

pdf.sub_heading("5.4 Database Design (3 Tables)")
pdf.table(
    ["Table", "Key Columns", "Purpose"],
    [
        ("users", "id, email, password_hash, role", "User accounts"),
        ("sessions", "id, class_id, code, teacher_id, duration", "Attendance sessions"),
        ("attendance_records", "session_id, student_id, timestamp", "Who attended when"),
    ]
)

pdf.sub_heading("5.5 API Endpoints")
pdf.table(
    ["Endpoint", "Method", "Who", "What"],
    [
        ("/auth/register", "POST", "Both", "Create account"),
        ("/auth/login", "POST", "Both", "Login, get tokens"),
        ("/auth/refresh", "POST", "Both", "Renew token"),
        ("/sessions/start", "POST", "Teacher", "New session"),
        ("/sessions/active", "GET", "Teacher", "Running sessions"),
        ("/sessions/history", "GET", "Teacher", "Past sessions"),
        ("/sessions/code/:code", "GET", "Student", "Lookup by code"),
        ("/attendance/mark", "POST", "Student", "Mark attendance"),
        ("/attendance/me", "GET", "Student", "Own history"),
        ("/attendance/session/:id", "GET", "Teacher", "Who attended"),
        ("/attendance/class/:id", "GET", "Teacher", "Class attendance"),
    ]
)

pdf.sub_heading("5.6 Security Features")
pdf.table(
    ["Feature", "English", "Hinglish"],
    [
        ("bcrypt 12 rounds", "Password safe even if DB leaked", "DB leak ho toh bhi password safe"),
        ("JWT tokens", "Tamper = rejected", "Tamper karo toh reject"),
        ("Role middleware", "Teacher/student separated", "Alag alag access"),
        ("Rate limiting", "Max 10 marks/min", "Brute force ruke"),
        ("Redis dedup", "120s duplicate lock", "120s tak dobara nahi"),
        ("DB constraint", "Backup dedup", "Redis fail toh bhi safe"),
        ("TTL expiry", "Auto-delete old codes", "Purana code auto delete"),
        ("CORS", "Only allowed domains", "Sirf allowed websites"),
    ]
)

pdf.sub_heading("5.7 Docker Deployment")
pdf.code_block("docker compose up --build")
pdf.body_text("Starts 3 containers: smat-postgres (DB, port 5432), smat-redis (cache, port 6379), smat-api (Node.js server, port 3000). Handles health checks, data persistence, auto schema apply.")
pdf.body_text("Hinglish: 3 containers start: postgres (database), redis (cache), api (humara server). Health checks, data safe on restart, tables automatically ban jaate hain.")

pdf.sub_heading("5.8 Website — Teacher Questions")
pdf.qa_block(
    "Why PostgreSQL over MySQL?",
    "Native UUID support, better JSON handling, reliable concurrent writes. Industry standard.",
    "UUID natively support, JSON better, concurrent writes reliable. Industry standard hai."
)
pdf.qa_block(
    "Why Redis? Can't PostgreSQL do everything?",
    "It can but slowly. Redis stores in RAM = microseconds. Every attendance checks session = must be fast. Plus Redis has TTL auto-delete. PostgreSQL is disk-based, no auto-expiry.",
    "Chal sakta hai par slow. Redis RAM mein = microseconds fast. Har attendance pe session check = fast chahiye. Redis mein TTL auto-delete hai. PostgreSQL disk pe hai, auto-expiry nahi."
)
pdf.qa_block(
    "What if server crashes?",
    "PostgreSQL data on disk = safe. Redis data (active sessions) lost = current sessions end. No permanent loss. Docker can auto-restart.",
    "PostgreSQL disk pe = safe. Redis data (active sessions) jaayega = chal rahe sessions band. Permanent loss nahi. Docker auto-restart kar sakta."
)
pdf.qa_block(
    "Budget?",
    "Near zero. All tools free/open source. Free cloud hosting tiers. Optional domain ~Rs 500-1000/year.",
    "Almost zero. Sab free/open source. Free hosting. Optional domain Rs 500-1000/year."
)

# ═══════════════════════════════════════
# CONNECTING ALL THREE
# ═══════════════════════════════════════
pdf.add_page()
pdf.section_title("6. How All Three Parts Connect")
pdf.highlight_box("Generator encodes code into ultrasonic tones, broadcasts from speaker -> Receiver detects via mic, decodes with FFT -> Website validates, prevents duplicates, records attendance.")
pdf.ln(2)
pdf.body_text("Hinglish: Generator code ko ultrasonic tones mein convert karke speaker se play karta hai -> Receiver phone mic se sunta hai, FFT se decode karta hai -> Website code check, duplicate rokta, database mein save karta hai.")
pdf.ln(2)
pdf.body_text("Teenon milke ek complete, zero-hardware, cheat-proof attendance system banate hain.", bold=True)

# ═══════════════════════════════════════
# COMPARISON TABLE
# ═══════════════════════════════════════
pdf.separator()
pdf.section_title("7. Comparison — SMAT vs Other Methods")
pdf.table(
    ["Feature", "QR Code", "GPS", "Bluetooth", "SMAT (Ours)"],
    [
        ("Physical presence", "No", "No", "Mostly", "YES"),
        ("Extra hardware", "No", "No", "Yes (BLE)", "No"),
        ("App install", "Sometimes", "Yes", "Yes", "No (browser)"),
        ("Cost", "Free", "Free", "Rs 2000+", "Free"),
        ("Cheatable?", "Easy", "Easy", "Hard", "Very Hard"),
        ("Speed", "5-10s manual", "Auto", "Auto", "Auto ~2-3s"),
    ]
)

# ═══════════════════════════════════════
# GLOSSARY
# ═══════════════════════════════════════
pdf.section_title("8. Quick Glossary")
glossary = [
    ("Ultrasonic", "Sound above human hearing (>17 kHz)", "Insaan ki range se upar ki sound"),
    ("FFT", "Fast Fourier Transform — sound to frequencies", "Sound ko frequencies mein todne wala"),
    ("JWT", "JSON Web Token — secure login token", "Digitally signed login card"),
    ("bcrypt", "Password hashing (one-way)", "Password one-way encrypt karne wala"),
    ("Redis", "In-memory DB for fast temp data", "RAM mein fast temporary database"),
    ("PostgreSQL", "Relational DB for permanent data", "Permanent data ka database"),
    ("TTL", "Time To Live — auto-delete timer", "Auto-delete timer"),
    ("Preamble", "Sync signal before data tones", "Data se pehle 'get ready' signal"),
    ("REST API", "Frontend-backend via HTTP", "HTTP se frontend-backend baat karte"),
    ("Docker", "Packages apps in containers", "Apps ko containers mein pack karta"),
    ("Middleware", "Code between request/response", "Request-response ke beech ka code"),
    ("UUID", "Universally Unique Identifier", "Duniya mein unique ID"),
    ("Sine Wave", "Purest sound — single frequency", "Ek hi frequency ki sound wave"),
    ("OscillatorNode", "Web Audio — generates tones", "Browser mein tone banane wala"),
    ("AnalyserNode", "Web Audio — analyzes frequencies", "Browser mein frequency dekhne wala"),
    ("Quad. Interp.", "Precise freq estimation", "Do bins ke beech exact freq nikalo"),
    ("Median Filter", "Most common value wins", "Sabse common value = answer"),
    ("CORS", "API domain security", "Sirf allowed websites se API call"),
]
pdf.table(
    ["Term", "English", "Hinglish"],
    glossary
)

pdf.ln(6)
pdf.set_font("NotoSans", "I", 9)
pdf.set_text_color(100, 116, 139)
pdf.cell(0, 6, "Prepared for SMAT Project Presentation — IIIT Surat", align="C")

# SAVE
output = "SMAT_Study_Guide.pdf"
pdf.output(output)
print(f"PDF saved: {output}")
print(f"Total pages: {pdf.pages_count}")
