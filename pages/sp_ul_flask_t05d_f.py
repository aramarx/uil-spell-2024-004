from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import requests
import random

# Ensure user is authenticated before showing the page
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("You must be logged in to access this page.")
    st.stop()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secret key

# Example data for alphabet test words (you can update it with real data)
ALPHABET_TESTS = {
    'a': ["abbreviate", "abnormality", "abode", "abrasion", "abundantly", "academic",
          "accessory", "accordion", "acidic", "acne", "acrobat", "adhesive",
          "admirable", "adoption", "adversary", "affected", "affliction", "affordable",
          "agenda", "airport", "alimony", "allergic", "alliance", "alpaca",
          "alphabetical", "amateur", "amplify", "amusing", "animate", "anklebone",
          "annex", "antibacterial", "antibiotic", "anxiety", "apparition", "appease",
          "applause", "aptitude", "aquamarine", "arcade", "arrangement", "assortment",
          "athletic", "attractive", "auditory", "avalanche", "avocado"],
    'b': ["badminton", "balky", "Ballyhoo", "barbarian", "bareback", "bargain", "barrette",
          "bashfulness", "beacon", "bedazzle", "bedridden", "beforehand", "behavior",
          "believable", "beneficial", "benevolent", "biannual", "bicultural", "bicycle",
          "billionaire", "bimonthly", "biodiversity", "bionics", "birthmark", "blamable",
          "blarney", "blissful", "blistering", "bluebonnet", "bolster", "bonfire",
          "boomerang", "botulism", "boulevard", "bountiful", "braggart", "braille",
          "brainstorm", "brilliance", "brisket", "brooch", "buffered", "buffoonery",
          "bulbous", "bureau", "burglarize"], 
    'c': ["calculate", "calendar", "canopy", "capitalism", "cardiac", "carnation", "cartridge",
          "cataract", "cavernous", "centimeter", "ceremony", "chaplain", "charitable", "choppiness",
          "cinema", "circulation", "circumstance", "clearance", "clergy", "clincher", "closure",
          "cohesion", "coincidence", "colander", "columnist", "combustion", "commercial",
          "communicable", "commute", "complaint", "concentrate", "concerto", "confirmed",
          "congratulate", "connection", "connive", "consultation", "convention", "convoy", "corrode",
          "corruption", "cramming", "creative", "critical", "curiosity", "currency", "curtail"],
    'd': ["damask", "dauntless", "debonair", "debt", "decagon", "deceit", "declining", "deductible",
          "deflate", "deformity", "dehydrate", "delivery", "democracy", "deodorant", "desperate", 
          "detestable", "development", "devotion", "diagram", "dictation", "dietary", "diligent",
          "diorama", "discipline", "discreet", "disembark", "disinfect", "dispensable", "disregard",
          "district", "divergence", "doleful", "domain", "dominance", "dosage", "downcast", 
          "draftsman", "drone", "dumpling", "dwindle", "dynasty"],
    'e': ["earliest", "earphone", "earsplitting", "editorial", "effective", "egoism", "elaborate", 
          "elapse", "elasticity", "electromagnet", "eligible", "emanate", "embroidery", "emergency", 
          "emotional", "employee", "encore", "endear", "endurance", "energetic", "engagement", 
          "enjoyably", "enormity", "entirety", "environment", "episode", "equate", "erase", 
          "escapism", "estimate", "ethical", "everglade", "evict", "evidence", "excel", "exercising", 
          "exhale", "existence", "expenditure", "experience", "exploration", "expound", "extremity"],
    'f': ["fabulous", "facedown", "factorization", "famish", "fanciful", "fatalism", "fattened", 
          "federalist", "feminine", "ferocious", "fiberglass", "fictionalize", "fidelity", "fiercely",
          "filbert", "filtration", "flagrant", "flatterer", "flounce", "food chain", "footbridge", 
          "foreclose", "foreign", "forerunner", "forgery", "forgetfulness", "formative", "fortitude",
          "foyer", "fraction", "fragile", "fragrance", "frankfurter", "fraternity", "freebie",
          "freedbee", "freedom", "frontier", "functional", "funeral", "furlough", "fuzziness"],
    'g': ["gangplank", "gasoline", "gaudy", "gauze", "gearless", "gemstone", "generality", 
          "generation", "genetic", "geographical", "geometric", "giddy", "gingerly", "glacier", 
          "gloominess", "gluttony", "goldenrod", "good-humored", "goodwill", "gooseneck", 
          "gorgeous", "govern", "gradually", "graffiti", "granola", "graphic", "gravitation", 
          "greasier", "greatness", "greengrocer", "griminess", "grinning", "grizzled", "grouchy", 
          "guidance", "guidebook", "gumbo", "gurgle"],
    'h': ["habitable", "haggard", "hamstring", "handicapped", "handily", "handlebar", "happiness",
          "happy-go-lucky", "harmfully", "hatchery", "hauntingly", "heatedly", "heather",
          "heatstroke", "hedgehog", "heighten", "henceforth", "hepatitis", "herbicide","hexagon", 
          "hibachi", "hideous", "hindrance", "hoist", "hominid", "homophone", "honeycomb", 
          "hoopskirt", "horoscope", "hotheaded", "hovercraft", "humidity", "hummingbird", 
          "husbandry", "hydrology", "hyena", "hygienic", "hyphen", "hypnosis", "hysterics"],
    'i': ["icicle", "idealism", "identical", "ideology", "ignoring", "illegal", "imaginable", 
          "imitative", "immense", "immodest", "immovable", "impassable", "impeach", "impossible", 
          "improper", "improvise", "incidence", "incision", "inconvenience", "indecision", 
          "independent", "indicator", "inedible", "infatuate", "inferior", "inherent", 
          "injustice", "innovative", "instructor", "insulation", "insurance", "interesting", 
          "intermittent", "internist", "intrusive", "inventory", "invigorate", "invitation", 
          "irrational", "irrigation", "issue"],
    'j': ["jaguar", "jamboree", "jawbreaker", "jellyfish", "jetty", "jitterbug", "jobholder", 
          "joggled", "joist", "jubilation", "juniper", "justify"],
    'k': ["kelp", "kernel", "kidney", "kindhearted", "kinship", "Kleenex", "knighthood", 
          "knitting", "knockabout"],
    'l': ["laboratory", "lacerate", "lamentation", "laminate", "landline", "languid", "larceny", 
          "lattice", "lawlessly", "layette", "league", "leastwise", "leathery", "lectern", 
          "leeway", "legality", "legislature", "leisure", "lemon", "levelheaded",
          "licorice", "lifeline", "light-year", "limerick", "lineage", "liquefy",
          "listener", "lobbyist", "locality", "loneliness", "loose", "lottery", "loudmouth",
          "lumberyard", "luminescent", "luxurious", "lynx"],
    'm': ["magnetic", "magnolia", "mainstream", "maize", "malefactor", "malformation", 
          "malicious", "manageable", "marathon", "mascara", "masterful", "materialize", 
          "maturity", "maximum", "Maya", "meaningful", "medication", "meditative", "melodrama", 
          "membrane", "memorial", "mercenary", "merchant", "metallic", "meteorologist", 
          "migratory", "miniature", "minivan", "minority", "misconception", "misguidance", 
          "misspend", "mistletoe", "mistrust", "monitor", "monotone", "mosquito", "motley", 
          "multitude", "murmur", "mutate"],
    'n': ["nape", "narcotic", "narrator", "nationalism", "natural resource", "navigable", 
          "navigator", "necessitate", "needful", "neglectful", "negotiate", "neighborhood", 
          "nervy", "nethermost", "nettle", "neutralize", "newcomer", "newspaperman", "nifty", 
          "nightly", "ninepin", "nitpick", "noiseless", "nonchalant", "nonprofit", "nonsense", 
          "nonverbal", "nonviolence", "normalize", "northeasterly", "nostalgic", "notoriety", 
          "nougat", "novitiate", "nozzle", "nuisance", "numeral", "nurturant", "nuthatch", 
          "nutlet", "nutriment"],
    'o': ["obese", "obeying", "obituary", "oblivious", "obscure", "observant", "obviously",
          "occupation", "odometer", "Offertory", "officiate", "olive", "ominous", "onslaught", 
          "opacity", "openhearted", "operating", "opposable", "optimal", "optometry", "orate", 
          "orbiter", "orderliness", "ordinary", "oregano", "organic", "original", "ornery", 
          "outburst", "outlying", "outwardly", "outweigh", "overestimate", "override", 
          "oversupply", "oxygen"],
    'p': ["packaging", "palpitate", "panhandle", "paradise", "paradox", "parakeet", "paralysis",
          "pathogen", "patriotic", "pedestal", "pedicure", "penalize", "penetrate", "penitence", 
          "pepperoni", "percentage", "perfection", "perilous", "perplexity", "pesticide", 
          "petroleum", "pictorial", "pineapple", "pinkie", "pinky", "plaintiff", "plasticity", 
          "poisonous", "policyholder", "polyester", "portable", "portfolio", "possession", 
          "practical", "precinct", "predestine", "predicament", "proactive", "problematic", 
          "proceed", "profession", "prosperous", "puzzling"],
    'q': ["quaintness", "qualm", "quarantine", "quarterback", "queasier", "quick bread",
          "quince", "quitting", "quizzes"],
    'r': ["racketeer", "radiantly", "radical", "railroad", "ramshackle", "raspy", "rationale", 
          "realistic", "reasoning", "reassure", "rebroadcast", "rebuttal", "receive", 
          "recession", "reconcile", "reconstruct", "rectangular", "reference", "refrigerate", 
          "regardless", "regiment", "relentless", "relevant", "reluctantly", "remnant", 
          "replacement", "replica", "reptilian", "respectable", "restaurant", "retort", 
          "retriever", "revenue", "review", "ricotta", "ridiculous", "roadrunner", "rodent", 
          "rollicking", "roughneck", "rowdiness", "rubella", "russet"],
    's': ["sabotage", "salsa", "sarcasm", "satisfactory", "scandal", "scarcely", "schedule", 
          "scorekeeper", "scourge", "seasonable", "seclusion", "sectional", "sedative", 
          "seizure", "semiarid", "sensational", "seriously", "seventh", "shrewd", "siesta", 
          "simplicity", "singular", "situation", "skittish", "sociable", "solidify", "solstice",
          "specific", "spectacle", "spectrum", "splendid", "squirm", "statement", "stationary", 
          "stereotype", "strategy", "stubborn", "subjective", "substantial", "summary", 
          "supplement", "survive", "syllabicate", "symbolism", "synthetic"],
    't': ["taffeta", "talkative", "tastefully", "taxation", "technician", "telescopic", 
          "temperament", "tension", "terrier", "terrific", "textual", "theatrical", "thermometer", 
          "thesis", "threaten", "thwart", "tightwad", "timberline", "tincture", "tinsel", 
          "toilsome", "tollgate", "tomorrow", "topical", "tousle", "toxemia", "tragedy", 
          "translate", "treasurer", "tremendous", "triangular", "trophy", "trustworthy", 
          "tunnel", "turbojet", "twentieth", "typewriter", "typify"],
    'u': ["ultima", "unaffected", "unaligned", "unbearable", "unblemished", "unclassified", 
          "underpass", "unenclosed", "uneventful", "uniformity", "university", "unlined", 
          "unplug", "unravel", "unutterable", "uproarious", "usage", "uttermost"],
    'v': ["vaccinate", "validity", "vandalism", "vanquish", "vaporize", "vegetative", "velocity", 
          "vendetta", "veneer", "venture", "Venus", "version", "veterinarian", "victimize", 
          "vigilant", "vindicate", "visitation", "vitality", "vivid", "vocation", "volcanic", 
          "volume"],
    'w': ["waistband", "wallaby", "warehouse", "warrant", "wash-and-wear", "waspish", "wearable",
          "web-footed", "wharf", "wheelchair", "wherefore", "white blood cell", "whitening", 
          "wireless", "wisecrack", "wittingly", "woozy", "workmanship"],
    'x': ["xylophone"],
    'y': ["yacht", "yearling"],
    'z': ["zealous", "zestfully"]
}

# Initialize the session for storing user progress and historical words
@app.before_request
def before_request():
    if 'scoring_board' not in session:
        session['scoring_board'] = {letter: {"correct": 0, "total": len(words)} for letter, words in ALPHABET_TESTS.items()}
        session['incorrect_words'] = []
        session['retest_words'] = []

@app.route('/')
def home():
    return render_template('home.html')

def index():
    # Access the environment variable
    api_key = os.getenv('RESPONSIVE_VOICE_API_KEY', 'default_key')
    return render_template('home.html', api_key=api_key)

@app.route('/select_test')
def select_test():
    return render_template('select_test.html', tests=ALPHABET_TESTS, scoring_board=session['scoring_board'])

@app.route('/start_test/<letter>', methods=['GET', 'POST'])
def start_test(letter):
    if letter not in ALPHABET_TESTS:
        return redirect(url_for('select_test'))
    
    words = ALPHABET_TESTS[letter]
    correct = session['scoring_board'][letter]['correct']
    total = session['scoring_board'][letter]['total']

    # Get the next word (cycle through)
    if 'current_word' not in session:
        session['current_word'] = words[0]

    current_word = session['current_word']

    if request.method == 'POST':
        user_input = request.form['user_input'].lower()
        correct_word = request.form['correct_word'].lower()
        
        if user_input == correct_word:
            session['scoring_board'][letter]['correct'] += 1
        else:
            session['incorrect_words'].append(correct_word)

        # Move to the next word in the test
        current_index = words.index(current_word)
        if current_index + 1 < len(words):
            session['current_word'] = words[current_index + 1]
        else:
            session['current_word'] = None  # Test completed

        # Check if the test is complete
        if session['current_word'] is None:
            if session['scoring_board'][letter]['correct'] == total:
                return render_template('test_complete.html', message="GOOD JOB! All words are correct!", letter=letter)
            else:
                return render_template('test_complete.html', message="Test complete! Some words are incorrect. Please retake.", letter=letter)

    return render_template('test.html', letter=letter, current_word=current_word, scoring_board=session['scoring_board'])

@app.route('/test_complete/<letter>', methods=['GET'])
def test_complete(letter):
    correct_words = session.get(f"{letter}_correct_words", 0)
    total_words = session.get(f"{letter}_total_words", 0)
    message = "GOOD JOB! All words are correct!" if correct_words == total_words else f"GOOD JOB! {correct_words} out of {total_words} words are correct. Please retake the test for the missed words."
    return render_template('test_complete.html', letter=letter, correct_words=correct_words, total_words=total_words, message=message)

@app.route('/retest_incorrect_words', methods=['GET', 'POST'])
def retest_incorrect_words():
    if not session['incorrect_words']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_input = request.form['user_input'].lower()
        correct_word = request.form['correct_word'].lower()

        if user_input == correct_word:
            session['retest_words'].remove(correct_word)
        else:
            session['incorrect_words'].append(correct_word)

        if not session['retest_words']:
            return render_template('retest_complete.html', message="Retest complete! All words are correct.", retest_words=session['retest_words'])

    current_word = session['retest_words'][0] if session['retest_words'] else None
    return render_template('retest.html', current_word=current_word, retest_words=session['retest_words'])

@app.route('/historical_misspelled_word_list')
def historical_misspelled_word_list():
    return render_template('historical_misspelled_word_list.html', words=session['incorrect_words'])

@app.route('/edit_misspelled_word_list', methods=['GET', 'POST'])
def edit_misspelled_word_list():
    if request.method == 'POST':
        word = request.form['word']
        action = request.form['action']
        
        if action == 'add' and word not in session['incorrect_words']:
            session['incorrect_words'].append(word)
        elif action == 'delete' and word in session['incorrect_words']:
            session['incorrect_words'].remove(word)
        
        session.modified = True

    return render_template('edit_misspelled_word_list.html', words=session['incorrect_words'])

@app.route('/pronounce_word/<word>')
def pronounce_word(word):
    # Replace with ResponsiveVoice or another AI TTS API call
    return render_template('play_sound.html', current_word=word)

@app.route('/get_definition/<word>')
def get_definition(word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    data = response.json()
    definition = data[0]['meanings'][0]['definitions'][0]['definition'] if data else "No definition found."
    
    #api_key = 'your_wordnik_api_key'  # Replace with your Wordnik API key
    #response = requests.get(f"https://api.wordnik.com/v4/word.json/{word}/definitions?api_key={api_key}")
    #data = response.json()
    #definition = data[0]['text'] if data else "No definition found."
    
    return definition

@app.route('/get_example_sentence/<word>')
def get_example_sentence(word):
    #url = f'https://api.datamuse.com/words?rel_syn={word}'
    #response = requests.get(url)
    #data = response.json()
    #return data
    
    response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
    #response = requests.get(f'https://api.datamuse.com/words?sp={word}&tags=pron')
    #response = requests.get(f'https://api.datamuse.com/words?rel_rhy={word)
    data = response.json()
    #sentence = data[0]['meanings'][0]['definitions'][0]['example'] if data else "No sentence example found."
    return data
    
    #api_key = cfkfozedk4amxz92tyh1boi833dv7t881s8df9aqvy5e5261h  # Replace with your Wordnik API key
    #response = requests.get(f"https://api.wordnik.com/v4/word.json/{word}/exampleSentences?api_key={api_key}")
    #data = response.json()
    #sentence = data[0]['text'] if data else "No sentence example found."
    
    #return sentence

if __name__ == '__main__':
    app.run(debug=True)      
