# questions_50.py
# ------------------------------------------------------
# 45 MCQs (A: 20 Basic Civil, B: 10 Home Inspection, C: 5 RCC, D: 10 Leakage)
# 5 Descriptive (short, report-style)
# ------------------------------------------------------

TEST_DURATION_MIN = 60       # minutes
MCQ_MARKS = 1                # each MCQ
LONG_MARKS = 3               # each descriptive
PASS_MARK = 30               # total out of 60

# ---------- A) 20 Basic Civil Engineering ----------
BASIC_CIVIL = [
    ("Initial setting time of OPC (IS 269) is:", 
     ["10 min","30 min","60 min","90 min"], "30 min"),
    ("Workability of concrete is commonly measured by:", 
     ["Flow table","Slump test","Vee-Bee test","Kelly ball"], "Slump test"),
    ("Curing period for normal concrete (min recommended):",
     ["3 days","7 days","14 days","28 days"], "7 days"),
    ("Most suitable sand for concrete is:",
     ["Sea sand","River sand (well-graded)","Desert sand","Crushed dust only"], "River sand (well-graded)"),
    ("Bulking of sand occurs due to:",
     ["Cement reaction","Moisture film on particles","Clay content","Temperature"], "Moisture film on particles"),
    ("Consistency of cement is tested by:",
     ["Le Chatelier","Vicat apparatus","Blaine's air permeability","Jolting table"], "Vicat apparatus"),
    ("Fineness modulus indicates:",
     ["Grading of aggregate","Strength of cement","Soundness","Workability"], "Grading of aggregate"),
    ("Water–cement ratio primarily controls:",
      ["Strength and permeability","Setting time only","Workability only","Shrinkage only"], "Strength and permeability"),
    ("Brick crushing strength (common burnt clay bricks) should be approx.:",
     ["1–3 MPa","3–7 MPa","7–10 MPa",">10 MPa"], "7–10 MPa"),
    ("Compaction of soil increases:",
     ["Void ratio","Permeability","Shear strength","Compressibility"], "Shear strength"),
    ("Silt content in fine aggregate (IS limit) generally not more than:",
     ["2%","4%","8%","12%"], "8%"),
    ("Cement storage should avoid contact with:",
     ["Wood","Metal","Moisture","Paint"], "Moisture"),
    ("Best concrete for high sulphate exposure:",
     ["OPC 33","PPC","SRC (Sulphate Resisting Cement)","Rapid hardening cement"], "SRC (Sulphate Resisting Cement)"),
    ("Typical density of PCC (kg/m³):",
     ["1200–1400","1600–1700","2200–2400","2600–2800"], "2200–2400"),
    ("Segregation in concrete is caused by:",
     ["Excessive vibration/height of fall","Adequate grading","Correct water content","Use of admixtures"], "Excessive vibration/height of fall"),
    ("Bleeding in concrete refers to:",
     ["Loss of cement","Rising of water to surface","Air entrainment","Shrinkage cracks"], "Rising of water to surface"),
    ("Plaster curing period (minimum):",
     ["1 day","3 days","7 days","14 days"], "7 days"),
    ("Bitumen grade indicating penetration value 60/70 means:",
     ["Softest","Hardest","Medium hardness","Cutback"], "Medium hardness"),
    ("Standard size of modular brick (mm):",
     ["190×90×90","200×100×100","230×110×70","190×90×80"], "190×90×90"),
    ("The purpose of damp proof course (DPC) is:",
     ["Thermal insulation","Prevent rising damp","Improve aesthetics","Increase strength"], "Prevent rising damp"),
]

# ---------- B) 10 Home Inspection ----------
HOME_INSPECTION = [
    ("Hollow sound in floor tiles indicates:", 
     ["Colour issue","Improper bonding/air gap","Excess grout","Paint defect"], "Improper bonding/air gap"),
    ("Efflorescence on wall tiles signals:", 
     ["Tile defect","Water ingress behind surface","Fungal attack","Paint issue"], "Water ingress behind surface"),
    ("Before water testing a bathroom you should:", 
     ["Close all drains","Seal all joints","Check slope & outlet direction","Apply coating first"], "Check slope & outlet direction"),
    ("Tool to measure carpet area quickly:", 
     ["Moisture meter","Laser distance meter","Crack gauge","Plumb bob"], "Laser distance meter"),
    ("UPVC frame flush with wall (no drip edge) risk:", 
     ["Noise leak","Air imbalance","Water backflow to joint","Frame cracking"], "Water backflow to joint"),
    ("Best material to seal around AC pipe sleeve:", 
     ["POP","Silicone/PU sealant","Cement slurry","Tape"], "Silicone/PU sealant"),
    ("Observation to record for tiles in app:", 
     ["Only photo","Say 'replace tile'","Separate counts: hollow/cracked/stained/broken","Skip minor issues"], "Separate counts: hollow/cracked/stained/broken"),
    ("When client disputes on site you should:",
     ["Argue","Ignore","Note concern, inform TL, document","Stop work immediately"], "Note concern, inform TL, document"),
    ("External corner damp patch most often due to:",
     ["Rising damp","Condensation only","Leak from parapet/roof edge joint","Paint shade"], "Leak from parapet/roof edge joint"),
    ("Best coating for exterior damp wall:",
     ["Oil paint","Cement slurry","Elastomeric waterproof coating","Distemper"], "Elastomeric waterproof coating"),
]

# ---------- C) 5 RCC ----------
RCC = [
    ("Minimum clear cover for slab reinforcement:", 
     ["10 mm","15 mm","20 mm","25 mm"], "20 mm"),
    ("Main bars in one-way slab are placed along:", 
     ["Short span","Long span","Either","Diagonal"], "Short span"),
    ("Typical w/c ratio for M20 (nominal):",
     ["0.35–0.45","0.50–0.55","0.60–0.70",">0.70"], "0.50–0.55"),
    ("Lapping of rebars should be avoided in:", 
     ["Negative moment zones","Midspan","Anywhere","Support free edges"], "Negative moment zones"),
    ("Honeycombing primarily caused by:",
     ["Low vibration/poor compaction","High grade cement","Over curing","Good grading"], "Low vibration/poor compaction"),
]

# ---------- D) 10 Leakage (detailed case-based) ----------
LEAKAGE = [
    ("Ceiling damp below upper toilet usually points to:",
     ["Surface condensation","Concealed pipe/Floor trap leak","Paint issue","Light fixture heat"], "Concealed pipe/Floor trap leak"),
    ("Balcony door corner damp inside bedroom likely due to:",
     ["Air leakage","Sealant failure at frame edge/drip detail","Paint overcoat","Tile shade"], "Sealant failure at frame edge/drip detail"),
    ("Parapet coping cracks allow:",
     ["Heat only","UV attack only","Direct ingress at wall top","Noise"), "Direct ingress at wall top"],
    ("AC drain T-joint inside wall can cause:",
     ["Tile hollowness only","Localized damp streaks vertically","Structural settlement","Rusting door hinges"], "Localized damp streaks vertically"),
    ("Best confirmation for concealed leak:",
     ["Hammer tiles","Moisture meter + isolation tests","Repaint area","Close valves only"], "Moisture meter + isolation tests"),
    ("Ponding test depth & duration (typical):",
     ["10 mm for 2 hr","50–75 mm for 24–48 hr","100 mm for 1 hr","None"], "50–75 mm for 24–48 hr"),
    ("Sealant for drain/pipe collars:",
     ["POP","PU/Silicone sealant","Distemper","Bitumen felt only"], "PU/Silicone sealant"),
    ("Efflorescence indicates:",
     ["Salt migration from moisture source","Paint shade issue","Fungal growth","Dry wall"], "Salt migration from moisture source"),
    ("Wall base blistering indoors is typical of:",
     ["Rising damp/capillary action","UV attack","Condensation only","Loose putty"], "Rising damp/capillary action"),
    ("To avoid water stagnation on roof, slope should be:",
     ["1:60","1:100–1:120 toward drain","1:20","Flat"], "1:100–1:120 toward drain"),
]

# ---------- Build MCQ list (45 total) ----------
def _make(section_name, tuples):
    out = []
    for i, (q, opts, ans) in enumerate(tuples, start=1):
        out.append({
            "id": f"{section_name.lower()}_{i}",
            "section": section_name,
            "question": q,
            "options": opts,
            "answer": ans
        })
    return out

MCQ_QUESTIONS = (
    _make("Basic Civil", BASIC_CIVIL) +
    _make("Home Inspection", HOME_INSPECTION) +
    _make("RCC", RCC) +
    _make("Leakage", LEAKAGE)
)
assert len(MCQ_QUESTIONS) == 45, f"MCQs must be 45, got {len(MCQ_QUESTIONS)}"

# ---------- E) 5 Descriptive (short report style) ----------
LONG_QUESTIONS = [
    {
        "id": "desc_1",
        "prompt": "Bedroom tiles: 5 hollow, 3 stained, 2 cracked. Write a short inspection note with probable causes and repair actions.",
        "keywords": ["hollow", "re-fix", "remove", "epoxy grout", "stained", "cleaning", "cracked", "replace", "photographs", "room-wise"]
    },
    {
        "id": "desc_2",
        "prompt": "Blistering at lower bedroom wall (near entrance) — write cause, confirmation method, and repair steps.",
        "keywords": ["rising damp", "capillary", "skirting", "moisture meter", "scrape", "biocide", "primer", "waterproof coat", "repaint"]
    },
    {
        "id": "desc_3",
        "prompt": "Roof slab waterproofing — list field checks to verify quality during handover.",
        "keywords": ["surface preparation", "slope", "ponding", "24", "drain", "fillet", "coating", "upturn", "thickness"]
    },
    {
        "id": "desc_4",
        "prompt": "Toilet inspection shows water stagnation near floor trap. Write likely reasons and step-by-step rectification.",
        "keywords": ["reverse slope", "trap level", "re-screed", "grout", "sealant", "water test", "slope"]
    },
    {
        "id": "desc_5",
        "prompt": "Exterior wall efflorescence near parapet — cause, repair, and preventive maintenance.",
        "keywords": ["salt", "moisture", "scrub", "wash", "primer", "elastomeric", "coping", "drain", "seal"]
    },
]
