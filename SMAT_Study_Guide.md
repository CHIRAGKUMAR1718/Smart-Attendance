# SMAT — Complete Study Guide for Presentation
### Smart Attendance System Using Ultrasonic Audio Signals
### IIIT Surat | Dept. of Electronics & Communication Engineering

---

# OVERVIEW — What is SMAT?

**English:**
SMAT is a Smart Attendance Marking system that uses inaudible ultrasonic sound signals (18,000–20,000 Hz) to mark attendance. The teacher's laptop speaker broadcasts a secret 6-character code encoded as high-frequency tones. The student's phone microphone picks up the sound, decodes the code, and automatically marks attendance. Only students physically present in the classroom can hear the signal — it cannot travel through walls or be shared over the internet.

**Hinglish:**
SMAT ek Smart Attendance system hai jo **sunai na dene wali ultrasonic sound** (18,000–20,000 Hz) use karta hai attendance mark karne ke liye. Teacher ka laptop speaker ek secret 6-character code ko high-frequency tones mein convert karke play karta hai. Student ka phone microphone us sound ko sunta hai, code nikalta hai, aur **automatically attendance mark** kar deta hai. Sirf woh students jo **classroom mein physically baithe hain** wohi yeh signal sun sakte hain — yeh deewar paar nahi kar sakta aur internet pe share nahi ho sakta.

---

# WHY DID WE BUILD THIS? (Problem Statement)

| Problem | English | Hinglish |
|---|---|---|
| **Time Waste** | Manual roll call takes 5–10 minutes in large classes. Wasted teaching time. | Manual roll call mein 5–10 minute lagte hain bade classes mein. Teaching ka time waste hota hai. |
| **Proxy Attendance** | Friends mark absent students present. QR codes get shared on WhatsApp in seconds. | Dost absent students ki attendance laga dete hain. QR codes WhatsApp pe seconds mein share ho jaate hain. |
| **GPS Spoofing** | Location-based apps can be tricked using free spoofing apps on any phone. | Location-based apps ko free spoofing apps se aasani se dhoka diya ja sakta hai. |
| **Hardware Cost** | Biometric/RFID machines cost ₹5,000–₹50,000 per classroom. | Biometric/RFID machines ka kharcha ₹5,000–₹50,000 per classroom hota hai. |

**Our Solution / Humara Solution:**
Ultrasonic sound use karo — it **cannot be shared online**, **cannot pass through walls**, and uses **existing laptop speakers and phone microphones** — zero extra cost.

---
---

# PART 1: GENERATOR (Teacher Side — Ultrasonic Signal Broadcasting)

---

## What Does the Generator Do?

**English:**
The generator is the teacher's side of the system. It takes a 6-character session code and converts it into inaudible sound waves that play from the laptop speaker. Think of it like a radio station — but instead of music, it broadcasts a secret code using sound that humans can't hear.

**Hinglish:**
Generator teacher ka side hai. Yeh ek 6-character session code ko **sunai na dene wali sound waves mein convert** karta hai jo laptop ke speaker se play hoti hain. Ise aise socho jaise ek radio station hai — par music ki jagah yeh ek secret code broadcast karta hai aisi sound mein jo insaan sun nahi sakta.

---

## Step-by-Step: How the Generator Works

### Step 1 — Teacher starts a session

**English:**
- Teacher enters a Class ID (like "CS301") and a duration (like 5 minutes)
- The server creates a unique 6-character code like `X7K3NP`
- This code is the "message" that will be hidden in sound

**Hinglish:**
- Teacher apna Class ID daalta hai (jaise "CS301") aur time set karta hai (jaise 5 minute)
- Server ek unique **6-letter code** banata hai jaise `X7K3NP`
- Yeh code ab sound mein convert hoga

### Step 2 — Each character is mapped to a frequency

**English:**
- We use a charset of 30 characters: `ABCDEFGHJKMNPQRSTUVWXYZ23456789` (confusing ones like O/0, I/1, L removed)
- Each character gets a unique frequency:
  - Base frequency = 18,000 Hz
  - Each next character is 55 Hz higher
  - So: A = 18,000 Hz, B = 18,055 Hz, C = 18,110 Hz... up to ~19,925 Hz
- All frequencies are above 17,000 Hz — humans cannot hear them, but microphones can detect them

**Hinglish:**
- Humne 30 characters use kiye hain: `ABCDEFGHJKMNPQRSTUVWXYZ23456789` (confusing wale jaise O/0, I/1, L hataye hain)
- Har character ki ek **fixed frequency** hai:
  - Base = 18,000 Hz
  - Har agla character 55 Hz upar
  - Toh: A = 18,000 Hz, B = 18,055 Hz, C = 18,110 Hz... ~19,925 Hz tak
- Yeh sab frequencies 17,000 Hz se upar hain — insaan ko sunai nahi dete, par phone ka microphone detect kar leta hai

### Step 3 — The broadcasting sequence

**English:**
The speaker plays sounds in this exact order:

| Part | Frequency | Duration | Purpose |
|---|---|---|---|
| **Preamble** | 17,800 Hz | 250 ms | Sync signal — tells receiver "data is about to start" |
| **Character 1** | e.g. 18,000 Hz (for 'A') | 180 ms | First letter of the code |
| **Silence** | — | 90 ms | Gap between characters |
| **Character 2** | e.g. 18,275 Hz (for 'F') | 180 ms | Second letter |
| **Silence** | — | 90 ms | Gap |
| ... | ... | ... | Characters 3, 4, 5, 6 same pattern |
| **Pause** | — | 650 ms | Rest before repeating the whole cycle |

Then the entire sequence repeats in a loop until the session expires. One full cycle takes about **2.3 seconds**.

**Hinglish:**
Speaker is order mein sound play karta hai:

| Kya play hota hai | Frequency | Kitni der | Kyun |
|---|---|---|---|
| **Preamble** (tayyari ka signal) | 17,800 Hz | 250 ms | "Data aane wala hai!" — receiver ko alert karta hai |
| **Pehla character** | jaise 18,000 Hz ('A' ke liye) | 180 ms | Code ka pehla letter |
| **Silence** (khamoshi) | — | 90 ms | Do letters ke beech gap |
| **Doosra character** | jaise 18,275 Hz ('F' ke liye) | 180 ms | Code ka doosra letter |
| ... | ... | ... | Aise hi 6 characters play hote hain |
| **Bada pause** | — | 650 ms | Cycle khatam — phir se repeat hoga |

Phir **poora sequence repeat** hota hai — jab tak session ka time khatam na ho. Ek poora cycle = lagbhag **2.3 second**.

### Step 4 — How the sound is generated in the browser

**English:**
- We use the browser's **Web Audio API** — specifically an **OscillatorNode**
- An oscillator generates a pure **sine wave** at the desired frequency
- We use **gain ramping** (6ms fade in/out) to prevent audio "pops" or "clicks" when switching tones
- The oscillator connects to the speaker output through a **GainNode** (volume control)
- In simple terms: The browser creates a tiny invisible "music player" that plays one pure tone at a time. Each tone represents one letter of the code.

**Hinglish:**
- Browser ki **Web Audio API** use hoti hai — specifically **OscillatorNode**
- Oscillator ek pure **sine wave** generate karta hai jo frequency hum set karte hain
- **GainNode** se volume control hota hai — 6ms mein dheere se sound badhta/ghatta hai taaki "tick" ya "pop" na aaye
- Simple bhasha mein: Browser ke andar ek chhota sa invisible music player banta hai. Yeh ek waqt mein ek hi note bajata hai. Har tone ek letter represent karta hai.

---

## Generator — Key Technical Parameters

| Parameter | Value | English Why | Hinglish Kyun |
|---|---|---|---|
| Frequency range | 18,000–19,925 Hz | Above human hearing (~17 kHz), within speaker/mic capability | Insaan ko sunai nahi deta, phone mic ko deta hai |
| Preamble frequency | 17,800 Hz | Below data range so it's never confused with a character | Data range se neeche hai — kabhi character samjha nahi jaayega |
| Tone duration | 180 ms | Long enough for FFT to detect, short enough for fast transmission | FFT ko detect karne ke liye enough, par fast bhi hai |
| Gap between tones | 90 ms | Prevents tone bleeding/overlap | Ek tone doosre mein mix na ho |
| Cycle pause | 650 ms | Gives receiver time to process and reset | Receiver ko process karne ka time milta hai |
| Gain ramp | 6 ms | Prevents clicking sounds when tones start/stop | Tones switch hone pe "tick" sound na aaye |

---

## Generator — Common Teacher Questions

**Q: "Why ultrasonic and not normal sound?"**
- **English:** Normal sound (<17 kHz) would be audible and annoying in a classroom. Ultrasonic frequencies (18–20 kHz) are completely silent to humans but still detectable by standard phone/laptop microphones.
- **Hinglish:** Normal sound (17,000 Hz se neeche) classroom mein sabko sunai degi — disturbing hoga. Ultrasonic (18,000+ Hz) completely silent hai insaan ke liye, par phone ka microphone ise easily detect kar leta hai.

**Q: "Why sine waves specifically?"**
- **English:** A sine wave has energy at only one frequency — it creates a clean, sharp peak in FFT analysis. Complex sounds spread energy across many frequencies, making detection harder.
- **Hinglish:** Sine wave mein energy sirf ek hi frequency par hoti hai — FFT mein ek clean, sharp peak dikhta hai. Complex sound mein bahut saari frequencies mix ho jaatein aur detect karna mushkil hota.

**Q: "Can the speaker actually play 18 kHz?"**
- **English:** Yes. Most laptop speakers can produce frequencies up to 20–22 kHz. Some cheaper speakers may drop off above 18 kHz, but still produce enough signal for the microphone to detect.
- **Hinglish:** Haan. Zyaadatar laptop speakers 20,000–22,000 Hz tak sound produce kar sakte hain. Kuch saste speakers mein 18 kHz ke baad sound thoda weak hota hai, par phir bhi microphone detect kar leta hai.

---
---

# PART 2: RECEIVER (Student Side — Ultrasonic Signal Detection & Decoding)

---

## What Does the Receiver Do?

**English:**
The receiver is the student's side. It uses the phone's microphone to listen for the ultrasonic code being broadcast by the teacher's speaker. It decodes the hidden message from the sound and automatically submits it to the server. The student doesn't need to type anything — just click "Start Listening" and wait.

**Hinglish:**
Receiver student ka side hai. Yeh phone ke **microphone** se teacher ke speaker ki ultrasonic sound sunta hai, usme chhupa hua code nikalta hai, aur **automatically server ko bhej deta hai**. Student ko kuch type nahi karna — sirf "Start Listening" button dabao aur wait karo.

---

## Step-by-Step: How the Receiver Works

### Step 1 — Microphone is activated

**English:**
- Student clicks "Start Listening" on `student.html`
- Browser asks for microphone permission (requires HTTPS)
- A MediaStream is created from the microphone input
- This stream is connected to an AnalyserNode (part of Web Audio API)

**Hinglish:**
- Student "Start Listening" button dabata hai
- Browser microphone ki permission maangta hai (HTTPS zaroori hai)
- Microphone on hote hi, audio data ek **AnalyserNode** ko jaata hai (yeh Web Audio API ka ek tool hai)

### Step 2 — FFT analysis begins

**English:**
FFT stands for **Fast Fourier Transform**. It takes a sound wave and breaks it into its individual frequencies. Imagine you hear a chord on a piano — multiple keys pressed together. FFT is like a magic tool that tells you "this chord contains the notes C, E, and G." In our case, if the sound has 18,110 Hz in it, FFT will show a peak at 18,110 Hz, and we know that means the character 'C'.

FFT settings:
- **FFT Size = 8192 bins** — breaks audio into 8192 frequency slots
- At ~48,000 Hz sample rate, each bin = ~5.86 Hz resolution
- We need to detect 55 Hz difference between characters — 5.86 Hz precision is more than enough
- FFT runs **every 30 milliseconds** (~33 checks per second)

**Hinglish:**
FFT ka matlab hai **Fast Fourier Transform**. Yeh mixed sound ko alag-alag frequencies mein tod deta hai. Socho tumne piano pe 3 keys ek saath press ki — tumhe ek mila-jula sound sunai dega. FFT ek aisa jadui tool hai jo bolta hai "is sound mein C note hai, E note hai, aur G note hai." Humare case mein — agar sound mein 18,110 Hz hai, toh FFT wahan peak dikhayega, aur hum jaante hain 18,110 Hz matlab character 'C'.

FFT ke settings:
- **FFT Size = 8192 bins** — sound ko 8192 chhoti frequency slots mein todta hai
- Phone ka sample rate ~48,000 Hz hota hai, toh har bin = ~5.86 Hz
- Humein 55 Hz ka difference detect karna hai — 5.86 Hz precision kaafi hai
- Yeh analysis **har 30 millisecond** mein hoti hai (1 second mein ~33 baar check)

### Step 3 — State machine decoding

**English:**
The receiver works like a state machine with these states:

```
IDLE → PREAMBLE_DETECTED → RECEIVING_CHARACTERS → COMPLETE
```

- **IDLE:** Constantly scanning all frequencies, looking for a peak at 17,800 Hz (the preamble)
- **PREAMBLE_DETECTED:** 17,800 Hz found! Must be detected for at least **4 consecutive frames** (~120ms) to confirm it's real signal, not random noise
- **RECEIVING_CHARACTERS:** After the preamble ends, reads 6 tones one by one:
  - Find the **peak frequency** in the 18,000–20,000 Hz range
  - Use **quadratic interpolation** for sub-bin accuracy (looks at a bin and its two neighbours, fits a curve to estimate the exact peak)
  - Convert frequency to character: `character index = (frequency - 18000) / 55`
  - Take **median** of multiple readings per tone (most common value) to reject noise errors
- **COMPLETE:** All 6 characters decoded! Code assembled and sent to server

If decoding is stuck for **8 seconds** → timeout → resets to IDLE. Generator repeats every ~2.3s, so it tries again on the next cycle.

**Hinglish:**
Receiver ek **state machine** ki tarah kaam karta hai:

```
IDLE → PREAMBLE MILA → CHARACTERS PADH RAHA HOON → COMPLETE
```

- **IDLE (Intezaar):** Har 30ms mein check — kya 17,800 Hz dikh raha hai?
- **PREAMBLE MILA (Tayyar Ho Jao):** 17,800 Hz mil gaya! Par **lagaataar 4 baar** dikhna chahiye (~120ms) — agar 4 baar dikhe toh pakka signal hai, ek baar dikhe toh noise ho sakta hai
- **CHARACTERS PADH RAHA HOON:** Preamble ke baad 6 tones aate hain. Har tone ke liye:
  - 18,000–20,000 Hz range mein **sabse strong frequency** dhoondho
  - **Quadratic interpolation** — agar exact frequency do bins ke beech mein hai, toh neighbours dekh ke accurate answer nikalo
  - Formula: `Character number = (frequency - 18000) / 55`
  - Kai readings lo, phir **median** (sabse zyada baar aane wali value) lo — noise wali galat readings hat jaati hain
- **COMPLETE:** 6 characters decode ho gaye! Code (jaise X7K3NP) server ko bhej do

Agar 8 second tak decode pura na ho → **timeout** → IDLE mein wapas. Generator loop mein hai, agla cycle ~2.3 second mein aayega.

### Step 4 — Auto-submission

**English:**
- The decoded 6-character code is sent to the API: `GET /sessions/code/X7K3NP`
- Server looks up the code in Redis, finds the session ID
- Then calls `POST /attendance/mark` with the session ID
- Attendance is marked — student sees a success message
- Entire process is automatic — student just waits

**Hinglish:**
- Decoded code (jaise "X7K3NP") server ko jaata hai
- Server code check karta hai Redis mein, session dhundhta hai
- Attendance mark ho jaati hai
- Student ko screen pe success message dikhta hai
- **Student ko kuch type ya click nahi karna** — sab automatic hai

---

## Receiver — Key Technical Parameters

| Parameter | Value | English Why | Hinglish Kyun |
|---|---|---|---|
| FFT Size | 8192 bins | High frequency resolution (~5.86 Hz/bin) to distinguish 55 Hz steps | Bahut precise — 5.86 Hz tak ka fark pakad sakta hai |
| Sample rate | ~48,000 Hz | Standard mic sample rate, supports up to 24 kHz detection | Standard phone microphone rate |
| Polling rate | Every 30 ms | Fast enough to catch 180ms tones (~6 readings per tone) | 1 second mein 33 baar check hota hai |
| Detection threshold | -70 dB | Ignores weak noise, only considers strong peaks | Weak signals ignore karo, sirf strong peaks lo |
| Preamble confirm | 4 consecutive frames | Confirms real signal, rejects random noise | Noise se bachne ke liye — 4 baar dikhe toh pakka |
| Timeout | 8 seconds | Resets if decoding is stuck, tries again next cycle | Stuck ho jaye toh reset, agla cycle mein try karo |
| Noise rejection | Median filtering | Takes most frequent reading from multiple samples | 10 mein 8 baar "C" aaya toh answer "C" hai |

---

## Receiver — Common Teacher Questions

**Q: "What if the classroom has fan noise or people talking?"**
- **English:** Ambient noise (fans, voices, traffic) is mostly below 5,000 Hz. Our detection range is 17,800–20,000 Hz — completely separate zones. The -70 dB threshold also filters out weak stray energy. Like AM radio and FM radio don't interfere with each other.
- **Hinglish:** Fan, AC, baatein — yeh sab 5,000 Hz se neeche ki sound hai. Humara detection range 17,800–20,000 Hz hai — completely alag zone. Jaise AM radio aur FM radio ek doosre ko disturb nahi karte, waise hi yeh bhi nahi karta.

**Q: "What if 50 students listen at the same time?"**
- **English:** No problem. Microphones only receive — they don't interfere with each other. Like 50 students reading the same whiteboard — they don't block each other.
- **Hinglish:** Koi problem nahi. Microphone sirf sunta hai — kisi ko disturb nahi karta. Jaise 50 students ek hi whiteboard padh sakte hain bina ek doosre ko roke.

**Q: "What if decoding fails halfway?"**
- **English:** The 8-second timeout resets the state machine to IDLE. Since the generator broadcasts in a loop (every ~2.3s), the receiver tries again on the next cycle. Most successful detections happen within 1–2 cycles.
- **Hinglish:** 8 second ka timeout hai — reset ho jaayega. Generator har 2.3 second mein repeat karta hai, toh agla cycle mein phir se try hoga. Zyaadatar 1–2 cycle mein successfully ho jaata hai.

**Q: "What is the maximum range?"**
- **English:** About 5–10 meters depending on speaker volume and room acoustics. This is intentional — ensures only students inside the classroom can hear it. Signal cannot travel through walls.
- **Hinglish:** Lagbhag 5–10 meter. Yeh feature hai, bug nahi — baaju wale classroom ke students detect nahi kar sakte. Sound deewar paar nahi karti.

**Q: "What is Quadratic Interpolation?"**
- **English:** FFT gives discrete bins (boxes). The true frequency might fall between two bins. Quadratic interpolation looks at a bin and its two neighbours, fits a curve through them, and estimates the exact peak — giving sub-bin accuracy.
- **Hinglish:** FFT humein fixed-size boxes (bins) mein answer deta hai. Par asli frequency do boxes ke beech mein ho sakti hai. Toh hum teen boxes dekhte hain — beech wala aur dono neighbours — curve fit karte hain aur exact peak estimate karte hain. Isse answer zyada accurate milta hai.

**Q: "Can someone record the sound and play it later?"**
- **English:** Each session generates a unique code that expires after the set duration (stored in Redis with TTL). Even if recorded, replaying it after the session ends will fail because the code no longer exists in the system.
- **Hinglish:** Har session ka unique code hota hai jo set time ke baad expire ho jaata hai (Redis mein TTL se). Agar koi record karke baad mein play kare, toh fail hoga kyunki code system mein exist hi nahi karega.

---
---

# PART 3: WEBSITE (Backend, Database, Authentication & Deployment)

---

## What Does the Website Part Do?

**English:**
The website is the backbone that connects everything. It handles user accounts (login/register), creates and manages attendance sessions, records who attended, and prevents cheating (duplicate marking, expired sessions). The generator and receiver are just the delivery mechanism — the website is where the actual attendance data lives.

**Hinglish:**
Website woh **backbone** hai jo sab kuch connect karta hai. Yeh accounts banata hai, sessions manage karta hai, attendance record karta hai, aur **cheating rokta hai** (duplicate marking, expired sessions). Generator aur Receiver sirf delivery ka kaam karte hain — asli data website mein stored hota hai.

---

## Architecture Overview (4 Layers)

**English:**
```
┌──────────────────────────────────────────────┐
│  FRONTEND (Browser)                          │
│  index.html, teacher.html, student.html      │
├──────────────────────────────────────────────┤
│  REST API (Express 5 on Node.js)             │
│  Routes → Controllers → Services             │
├──────────────────────────────────────────────┤
│  DATABASE: PostgreSQL 16 (permanent storage) │
├──────────────────────────────────────────────┤
│  CACHE: Redis 7 (temporary/fast storage)     │
└──────────────────────────────────────────────┘
```

**Hinglish:** Socho building ke 4 floors hain:

| Floor | Kya Hai | Kya Karta Hai |
|---|---|---|
| **4th Floor** — Frontend | HTML pages | User ko dikhta hai — buttons, forms, FFT visualization |
| **3rd Floor** — API | Express 5 (Node.js) | HTTP requests handle karta hai — login, session, attendance |
| **2nd Floor** — Services | Business logic | Password check, code generate, duplicate detect |
| **1st Floor** — Data | PostgreSQL + Redis | Data store — permanent (PostgreSQL) aur temporary (Redis) |

---

## A. Authentication (Login System)

### Registration

**English:**
1. User sends email + password + role ("teacher" or "student")
2. Server hashes the password using **bcrypt with 12 rounds** — converts "mypassword" into a random-looking string that cannot be reversed
3. Stores email + hashed password + role in the `users` table
4. Returns two JWT tokens

**Hinglish:**
1. User email + password + role ("teacher" ya "student") bhejta hai
2. Server password ko **bcrypt** se hash karta hai — "mypass123" convert hota hai kuch aisa: `$2b$12$xYzAb...` — ise wapas "mypass123" mein badalna **impossible** hai
3. Email + hashed password database mein save hota hai
4. Server 2 **tokens** wapas bhejta hai

### Login

**English:**
1. User sends email + password
2. Server fetches the stored hash from the database
3. Uses `bcrypt.compare()` to check if the password matches the hash
4. If match → creates and returns two JWT tokens

**Hinglish:**
1. User email + password bhejta hai
2. Server database se hashed password nikalti hai
3. `bcrypt.compare()` check karta hai — match karta hai ya nahi?
4. Agar match → 2 tokens milte hain

### The Two Tokens

| Token | Expires In | English Purpose | Hinglish Matlab |
|---|---|---|---|
| **Access Token** | 2 hours | Sent with every API request to prove identity | Har request ke saath jaata hai — "main hoon Prateek" |
| **Refresh Token** | 7 days | Gets new access token without re-entering password | Password dobara daale bina naya access token lo |

### What is JWT?

**English:**
A JWT is like a digitally signed ID card. It contains your user ID and role, signed with a secret key only the server knows. When you send a request, the server checks the signature. If someone tampers with the token, the signature won't match and the request is rejected.

**Hinglish:**
JWT ek **digitally signed ID card** hai. Isme likha hai "User ID = 123, Role = student" aur server ne ise apni secret key se sign kiya hai. Agar kisi ne token mein kuch change kiya — signature match nahi karega aur request reject ho jayegi.

### Role-Based Access

**English:**
A middleware function (like a security guard) runs before every protected API endpoint. It checks the user's role — teachers can only use teacher APIs, students can only use student APIs.

**Hinglish:**
Har protected API ke aage ek **middleware** baitha hai (jaise security guard). Guard check karta hai: "Kya tum teacher ho?" — sirf tab session create hoga. "Kya tum student ho?" — sirf tab attendance mark hogi.

---

## B. Session Management

### Creating a Session

**English:**
1. Teacher sends classId (e.g., "CS301") and duration (e.g., 300 seconds)
2. Server generates a UUID (universally unique ID) for the session
3. Server generates a 6-character code from charset `ABCDEFGHJKMNPQRSTUVWXYZ23456789`
4. Checks Redis to ensure the code isn't already in use
5. Stores in three places:

| Where | What | When Deleted |
|---|---|---|
| Redis — `chirp:session:{uuid}` | Session details (classId, teacherId, code) | Automatically when duration expires (TTL) |
| Redis — `chirp:code:{X7K3NP}` | Maps code to session ID | Automatically — same TTL |
| PostgreSQL — sessions table | Permanent record | Never — kept for history |

**Hinglish:**
1. Teacher bhejta hai: classId = "CS301", duration = 300 seconds
2. Server ek **UUID** (bohot lamba unique ID) banata hai
3. Server ek **6-character code** banata hai jaise `X7K3NP`
4. Redis mein check karta hai — yeh code kisi aur session mein toh nahi use ho raha?
5. Teen jagah save hota hai:

| Kahan | Kya | Kab Delete |
|---|---|---|
| Redis — `chirp:session:{uuid}` | Session details | **Automatically** — TTL khatam hone pe |
| Redis — `chirp:code:{X7K3NP}` | Code → Session ID mapping | **Automatically** — same TTL |
| PostgreSQL — sessions table | Permanent record | **Kabhi nahi** — history ke liye |

### What is TTL?

**English:**
TTL = Time To Live. When we store data in Redis, we say "delete this automatically after 300 seconds." So the code stops working after 5 minutes — no one needs to manually delete it.

**Hinglish:**
TTL = Time To Live. Redis mein data daalte waqt bolte hain "ise 300 seconds baad apne aap delete kar dena." Toh 5 minute baad code kaam karna band kar deta hai — manually delete nahi karna padta.

### Why Two Redis Keys?

**English:**
- Student has the 6-char code → `chirp:code:X7K3NP` gives the session ID
- Session ID needed for details → `chirp:session:{uuid}` gives session info
- Both directions of lookup are needed

**Hinglish:**
- Student ke paas sirf code hai → `chirp:code:X7K3NP` se session ID milta hai
- Session ID se details chahiye → `chirp:session:{uuid}` se milti hain
- Dono taraf se lookup hota hai — isliye do keys

---

## C. Attendance Marking (Core Logic)

**English — Step by step:**
1. **Code Lookup:** Server checks `chirp:code:{code}` in Redis → gets session ID
   - Not found → "Session expired or invalid"
2. **Session Validation:** Checks `chirp:session:{sessionId}` in Redis
   - Not found → session expired
3. **Duplicate Check (Redis):** Checks `attendance:{sessionId}:{studentId}`
   - Exists → "Already marked" (409 error)
   - Not exists → creates this key with 120-second TTL (fast duplicate blocker)
4. **Database Insert:** Inserts into `attendance_records` table
   - Unique constraint violation → "Already marked"
   - Success → **Attendance recorded!**

**Hinglish — Step by step:**
1. **Code Lookup:** Server Redis mein dekhta hai `chirp:code:X7K3NP` → session ID milta hai
   - Nahi mila → "Session expired ya invalid"
2. **Session Check:** `chirp:session:{sessionId}` check karta hai
   - Nahi mila → session expire ho gaya
3. **Duplicate Check (Redis):** `attendance:{sessionId}:{studentId}` dekhta hai
   - Hai → "Already marked" (409 error)
   - Nahi → yeh key banao 120 second TTL ke saath
4. **Database Insert:** `attendance_records` table mein daalo
   - Agar already hai → "Already marked"
   - Nahi → **Success! Attendance recorded!**

### Why Duplicate Check at Two Levels?

**English:**
- **Redis** is the first check — extremely fast (microseconds), handles most duplicates
- **Database unique constraint** is the safety net — even if Redis fails, DB won't allow duplicates
- This is called **defense in depth** — two layers of protection

**Hinglish:**
- **Redis** pehla check hai — bohot fast (microseconds). Zyaadatar duplicates yahan ruk jaate hain
- **Database unique constraint** backup hai — Redis fail ho toh bhi DB duplicate nahi hone dega
- Do layers of protection — jaise ghar mein gate bhi hai aur darwaze pe lock bhi

---

## D. Database Design (3 Tables)

### Table 1: `users`

| Column | English | Hinglish |
|---|---|---|
| id | Unique UUID per user | Har user ka alag unique ID |
| email | Login email (unique) | Login email |
| password_hash | bcrypt-hashed password | Hashed password — asli password nahi |
| role | "teacher" or "student" | Teacher ya student |
| created_at | When account was created | Account kab bana |

### Table 2: `sessions`

| Column | English | Hinglish |
|---|---|---|
| id | Session UUID | Session ka unique ID |
| class_id | Class identifier like "CS301" | Class ka naam jaise "CS301" |
| code | 6-character code like "X7K3NP" | 6-character code |
| teacher_id | Who created it | Kisne banaya |
| duration | Session length in seconds | Kitne seconds ke liye |
| created_at | When session started | Kab bana |

### Table 3: `attendance_records`

| Column | English | Hinglish |
|---|---|---|
| id | Auto-incrementing number | Auto-incrementing number |
| session_id | Which session | Kis session mein |
| student_id | Which student | Kaunsa student |
| timestamp | When attendance was marked | Kab mark hua |

---

## E. API Endpoints

| Endpoint | Method | Who | English | Hinglish |
|---|---|---|---|---|
| `/auth/register` | POST | Both | Create account | Naya account banao |
| `/auth/login` | POST | Both | Login, get tokens | Login karo, tokens lo |
| `/auth/refresh` | POST | Both | Renew expiring token | Token renew karo |
| `/sessions/start` | POST | Teacher | Create new session | Naya session shuru karo |
| `/sessions/active` | GET | Teacher | List running sessions | Chal rahe sessions dekho |
| `/sessions/history` | GET | Teacher | List past sessions | Purane sessions dekho |
| `/sessions/code/:code` | GET | Student | Look up session by code | Code se session dhoondho |
| `/attendance/mark` | POST | Student | Mark attendance | Attendance mark karo |
| `/attendance/me` | GET | Student | Own attendance history | Apni history dekho |
| `/attendance/session/:id` | GET | Teacher | Who attended a session | Kaun aaya session mein |
| `/attendance/class/:id` | GET | Teacher | Attendance by class | Class ki attendance dekho |

---

## F. Security Features

| Feature | English | Hinglish |
|---|---|---|
| **bcrypt (12 rounds)** | Password hashed — safe even if DB leaked | Database leak ho jaye toh bhi password safe |
| **JWT tokens** | Signed ID card — tamper = rejected | Tamper karo toh reject ho jayega |
| **Role middleware** | Teacher can't access student APIs & vice versa | Teacher student ka kaam nahi kar sakta |
| **Rate limiting** | Max 10 marks per minute per user | 1 minute mein max 10 baar — brute force ruk jaata hai |
| **Redis dedup** | 120-second lock prevents double marking | 120 second lock — dobara mark nahi hoga |
| **DB unique constraint** | Backup duplicate prevention | Redis fail ho toh bhi DB duplicate nahi dega |
| **TTL auto-expiry** | Sessions and codes auto-delete | Code apne aap delete — purana code kaam nahi karega |
| **CORS** | Controls which domains can call our API | Sirf allowed domains se API call ho sakti hai |

---

## G. Docker Deployment

**English:**
One command starts the entire system:
```
docker compose up --build
```

This starts 3 containers:

| Container | Image | Port | Purpose |
|---|---|---|---|
| smat-postgres | postgres:16-alpine | 5432 | Database |
| smat-redis | redis:7-alpine | 6379 | Cache |
| smat-api | Custom Dockerfile | 3000 | Our Node.js server |

Docker Compose also handles health checks (API waits until Postgres and Redis are ready), volume persistence (data survives restarts), and schema auto-apply (tables created automatically on first run).

**Hinglish:**
Ek command se poora system start:
```
docker compose up --build
```

3 containers start hote hain:

| Container | Kya Hai | Port |
|---|---|---|
| smat-postgres | Database | 5432 |
| smat-redis | Cache | 6379 |
| smat-api | Humara Node.js server | 3000 |

Docker Compose health checks bhi handle karta hai (API tab start hota hai jab Postgres aur Redis ready hon), data persist karta hai (restart pe data nahi jaata), aur schema automatically apply hota hai.

**Why Docker? / Docker kyun?**
- **English:** Docker puts each service in its own container. Anyone can run the project on any computer without installing PostgreSQL, Redis, or Node.js separately. One command, everything works.
- **Hinglish:** Docker har service ko ek alag container (dabba) mein rakhta hai. Koi bhi insaan kisi bhi computer pe ek command se poora project chala sakta hai. Alag se install kuch nahi karna.

---

## Website — Common Teacher Questions

**Q: "Why Express 5 and not Express 4?"**
- **English:** Express 5 has built-in async error handling. If a route throws an error, Express catches it automatically. In Express 4, you had to wrap every route in try-catch manually.
- **Hinglish:** Express 5 mein async errors apne aap handle hote hain. Express 4 mein har route ko manually try-catch mein wrap karna padta tha.

**Q: "Why PostgreSQL over MySQL?"**
- **English:** PostgreSQL supports UUIDs natively, has better JSON support, and handles concurrent writes better. It's the industry standard for production applications.
- **Hinglish:** PostgreSQL mein UUID natively support hota hai, JSON handling better hai, aur concurrent writes mein zyada reliable hai. Industry standard hai.

**Q: "Why Redis? Can't PostgreSQL do everything?"**
- **English:** It can — but it would be slow. Redis stores data in RAM, so reads/writes take microseconds. Every attendance request checks the session — that must be fast. Plus Redis has built-in TTL (auto-delete), perfect for expiring sessions. PostgreSQL stores on disk and doesn't have auto-expiry.
- **Hinglish:** Chal sakta hai — par bohot slow hoga. Redis data RAM mein rakhta hai, toh microseconds mein answer milta hai. Har attendance request pe session check hota hai — woh fast hona chahiye. Plus Redis mein TTL hai — data apne aap delete hota hai. PostgreSQL disk pe store karta hai aur auto-expiry nahi hai.

**Q: "What if the server crashes?"**
- **English:** PostgreSQL data is on disk and survives crashes. Redis data (active sessions) is lost, meaning current sessions end early — but no permanent data loss. Docker can be configured to auto-restart containers.
- **Hinglish:** PostgreSQL ka data disk pe hai — safe hai. Redis ka data (active sessions) chala jaayega — chal rahe sessions band honge. Par permanent data loss nahi hoga. Docker auto-restart bhi set kar sakte hain.

**Q: "What was the budget?"**
- **English:** Almost zero. Node.js, Express, PostgreSQL, Redis, Docker — all free and open source. Hosting on free cloud tiers (Render, Railway). Only optional custom domain costs ₹500–1,000/year.
- **Hinglish:** Almost zero. Sab tools free aur open source hain. Hosting free tiers pe. Sirf optional domain mein ₹500–1,000/year.

---
---

# HOW ALL THREE PARTS CONNECT (End-to-End Flow)

**English:**
> **Generator** encodes the 6-char code into ultrasonic tones and broadcasts from the speaker →
> **Receiver** detects the tones via microphone, decodes them using FFT back into the code →
> **Website** validates the code, checks the session, prevents duplicates, and records attendance in the database.

All three together make a **complete, zero-hardware, cheat-proof attendance system**.

**Hinglish:**
> **Generator** 6-char code ko ultrasonic tones mein convert karke speaker se play karta hai →
> **Receiver** phone ke mic se tones sunta hai, FFT se decode karke code nikalta hai →
> **Website** code check karta hai, session validate karta hai, duplicate rokta hai, aur database mein attendance save karta hai.

Teenon milke ek **complete, zero-hardware, cheat-proof attendance system** banate hain.

---

# QUICK GLOSSARY

| Term | English Meaning | Hinglish Matlab |
|---|---|---|
| **Ultrasonic** | Sound above human hearing (>17 kHz) | Insaan ki sunne ki range se upar ki sound |
| **FFT** | Fast Fourier Transform — converts sound to frequencies | Sound ko frequencies mein todne wala tool |
| **JWT** | JSON Web Token — secure login token | Digitally signed login card |
| **bcrypt** | Password hashing algorithm (one-way) | Password ko one-way encrypt karne wala |
| **Redis** | In-memory database for fast temporary data | RAM mein data rakhne wala fast database |
| **PostgreSQL** | Relational database for permanent storage | Permanent data rakhne wala database |
| **TTL** | Time To Live — auto-delete timer | Auto-delete timer |
| **Preamble** | Sync signal before data | Data se pehle "get ready" signal |
| **REST API** | Frontend-backend communication via HTTP | HTTP se frontend-backend baat karte hain |
| **Docker** | Packages apps into containers | Apps ko containers mein pack karta hai |
| **Middleware** | Code between request and response (like auth check) | Request aur response ke beech ka code (jaise security guard) |
| **UUID** | Universally Unique Identifier | Duniya mein unique ID |
| **Sine Wave** | Purest form of sound — single frequency | Sabse simple sound wave — ek hi frequency |
| **OscillatorNode** | Web Audio API tool that generates tones | Browser mein tone generate karne wala tool |
| **AnalyserNode** | Web Audio API tool that analyzes frequencies | Browser mein frequency analyze karne wala tool |
| **Quadratic Interpolation** | Math technique for precise frequency estimation | Do bins ke beech exact frequency nikalne ki technique |
| **Median Filter** | Takes most common value to reject noise | Noise hatane ke liye sabse common value lo |
| **CORS** | Cross-Origin Resource Sharing — API security | API ko sirf allowed websites se access karne do |

---

# COMPARISON TABLE — SMAT vs Other Methods

| Feature | QR Code | GPS | Bluetooth | SMAT (Ours) |
|---|---|---|---|---|
| Physical presence needed | No (screenshot shared) | No (GPS spoofing) | Mostly yes | **Yes** (sound can't pass walls) |
| Extra hardware | No | No | Yes (BLE beacons) | **No** |
| App installation | Sometimes | Yes | Yes | **No** (browser only) |
| Cost | Free | Free | ₹2000+/room | **Free** |
| Can be cheated | Easy | Easy | Hard | **Very Hard** |
| Speed | 5-10 sec (manual) | Auto | Auto | **Auto (~2-3 sec)** |

---

*Prepared for SMAT Project Presentation — IIIT Surat*
