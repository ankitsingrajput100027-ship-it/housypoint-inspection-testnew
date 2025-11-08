# questions.py
# === MCQs ===
MCQ_QUESTIONS = [
    {
        "id": "q1",
        "question": "During a tile inspection, a 'hollow sound' when tapped usually indicates:",
        "options": [
            "Tile colour defect",
            "Improper bonding or air gap below tile",
            "Excess grout",
            "Water seepage only",
        ],
        "answer": "Improper bonding or air gap below tile",
    },
    {
        "id": "q2",
        "question": "Before starting water testing in a bathroom, what should be done?",
        "options": [
            "Close all drains",
            "Seal all tile joints",
            "Check slope and drainage outlet flow direction",
            "Apply waterproof coating again",
        ],
        "answer": "Check slope and drainage outlet flow direction",
    },
    {
        "id": "q3",
        "question": "Efflorescence on wall tiles indicates:",
        "options": [
            "Poor tile quality",
            "Paint peeling",
            "Water ingress from behind the surface",
            "Fungal attack",
        ],
        "answer": "Water ingress from behind the surface",
    },
    {
        "id": "q4",
        "question": "Which tool is most suitable for measuring carpet area during inspection?",
        "options": [
            "Hammer",
            "Moisture meter",
            "Laser measuring device",
            "Crack width gauge",
        ],
        "answer": "Laser measuring device",
    },
    {
        "id": "q5",
        "question": "If a UPVC door frame is fixed flush with the wall without drip edges, the most likely issue is:",
        "options": [
            "Noise leakage",
            "Air pressure imbalance",
            "Water backflow toward wall or roof joint",
            "Cracking of plaster",
        ],
        "answer": "Water backflow toward wall or roof joint",
    },
    {
        "id": "q6",
        "question": "What is the best way to confirm plumbing line leakage in concealed walls?",
        "options": [
            "Hammer the tiles",
            "Use moisture meter and observe damp patches",
            "Replace all fittings",
            "Repaint and observe after drying",
        ],
        "answer": "Use moisture meter and observe damp patches",
    },
    {
        "id": "q7",
        "question": "For sealing gaps near a drain or around AC pipes, which material is preferred?",
        "options": [
            "POP mix",
            "Silicone sealant / polyurethane sealant",
            "Paint thinner",
            "White cement only",
        ],
        "answer": "Silicone sealant / polyurethane sealant",
    },
    {
        "id": "q8",
        "question": "What is the primary purpose of primer before applying waterproof coating?",
        "options": [
            "Improve adhesion and surface grip",
            "Add shine to the surface",
            "Cover cracks",
            "Reduce waterproofing material cost",
        ],
        "answer": "Improve adhesion and surface grip",
    },
    {
        "id": "q9",
        "question": "Correct sequence for repairing a cracked bathroom tile joint:",
        "options": [
            "Clean → Fill with sealant → Test water flow",
            "Paint → Apply grout → Seal edges",
            "Clean → Apply waterproof layer → Tile → Grout",
            "Hammer tile → Replace pipe → Repaint",
        ],
        "answer": "Clean → Apply waterproof layer → Tile → Grout",
    },
    {
        "id": "q10",
        "question": "For external wall leakage, the most recommended product type is:",
        "options": [
            "Oil paint",
            "Cement slurry",
            "Elastomeric waterproof coating",
            "POP paste",
        ],
        "answer": "Elastomeric waterproof coating",
    },
    {
        "id": "q11",
        "question": "You observe gaps in parapet wall tiles. The first step should be:",
        "options": [
            "Apply waterproof coat immediately",
            "Identify and mark missing tile zones for repair",
            "Clean and ignore",
            "Repaint the area",
        ],
        "answer": "Identify and mark missing tile zones for repair",
    },
    {
        "id": "q12",
        "question": "Which should not be included in the inspection summary report?",
        "options": [
            "Defect locations and photos",
            "Materials required for repair",
            "Worker names and salaries",
            "Recommended actions",
        ],
        "answer": "Worker names and salaries",
    },
    {
        "id": "q13",
        "question": "While documenting leakage, which detail is most critical for report clarity?",
        "options": [
            "Source and path of water ingress",
            "Room paint shade",
            "Contractor’s name",
            "Type of door hinge",
        ],
        "answer": "Source and path of water ingress",
    },
    {
        "id": "q14",
        "question": "How should an inspector record tile issues in the Housypoint app?",
        "options": [
            "Separate count of cracked, hollow, stained, and broken tiles",
            "Only take a photo",
            "Mention 'tiles need replacement'",
            "Skip minor issues",
        ],
        "answer": "Separate count of cracked, hollow, stained, and broken tiles",
    },
    {
        "id": "q15",
        "question": "In case of a client dispute during inspection, the employee should:",
        "options": [
            "Argue and prove their point",
            "Politely note client concern, inform the team lead, and document it in the report",
            "Ignore client and finish inspection",
            "Leave site immediately",
        ],
        "answer": "Politely note client concern, inform the team lead, and document it in the report",
    },
]

# === LONG ANSWERS (auto-check via simple keyword rubric; edit keywords freely) ===
LONG_QUESTIONS = [
    {
        "id": "q16",
        "prompt": "Explain the step-by-step process of bathroom leakage inspection (slope test, tile inspection, plumbing checks, documentation).",
        "keywords": ["slope", "drain", "ponding", "moisture meter", "grout", "plumbing", "trap", "photos", "report"]
    },
    {
        "id": "q17",
        "prompt": "Dampness in the ceiling below an upper floor bathroom: causes, how to confirm the source, repair recommendations.",
        "keywords": ["concealed", "pipe", "shower area", "toilet", "moisture", "pressure test", "sealant", "replace tile", "waterproofing"]
    },
    {
        "id": "q18",
        "prompt": "Standard method for roof slab waterproofing inspection (surface prep, ponding test, cracks/gaps, drain sealing).",
        "keywords": ["surface preparation", "cleaning", "cracks", "PU", "elastomeric", "ponding", "24 hours", "drain", "fillet"]
    },
    {
        "id": "q19",
        "prompt": "Paint peeling & fungal growth on external walls: technical cause, correct repair steps, preventive maintenance.",
        "keywords": ["capillary", "efflorescence", "fungal", "scraping", "biocide", "primer", "topcoat", "drainage", "rain"]
    },
    {
        "id": "q20",
        "prompt": "Write a professional inspection summary report for a 2BHK flat (structure, key points, photos/remarks/materials).",
        "keywords": ["scope", "location", "findings", "photos", "recommendations", "materials", "priority", "room-wise"]
    },
]

# Marks config
MCQ_MARKS = 2
LONG_MARKS = 4
PASS_MARK = 30  # change anytime
TEST_DURATION_MIN = 30
