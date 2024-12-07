import streamlit as st
from gtts import gTTS
import nltk
from nltk.corpus import wordnet
import io

# Ensure user is authenticated before showing the page
if 'authenticated' not in st.session_state or not st.session_state['authenticated']:
    st.warning("You must be logged in to access this page.")
    st.stop()

nltk.download('wordnet')

# Updated list of words
words = [
    "abbreviate", "abnormality", "abode", "abrasion", "abundantly", "academic",
    "athletic", "attractive", "auditory", "avalanche", "avocado",
    "badminton", "balky", "Ballyhoo", "barbarian", "bareback", "bargain", "barrette",
    "bulbous", "bureau", "burglarize",
    "calculate", "calendar", "canopy", "capitalism", "cardiac", "carnation", "cartridge",
    "corruption", "cramming", "creative", "critical", "curiosity", "currency", "curtail",
    "damask", "dauntless", "debonair", "debt", "decagon", "deceit", "declining", "deductible",
    "draftsman", "drone", "dumpling", "dwindle", "dynasty",
    "earliest", "earphone", "earsplitting", "editorial", "effective", "egoism", "elaborate", 
    "exhale", "existence", "expenditure", "experience", "exploration", "expound", "extremity",
    "fabulous", "facedown", "factorization", "famish", "fanciful", "fatalism", "fattened", 
    "freedbee", "freedom", "frontier", "functional", "funeral", "furlough", "fuzziness",
    "gangplank", "gasoline", "gaudy", "gauze", "gearless", "gemstone", "generality", 
    "guidance", "guidebook", "gumbo", "gurgle",
    "habitable", "haggard", "hamstring", "handicapped", "handily", "handlebar", "happiness",
    "husbandry", "hydrology", "hyena", "hygienic", "hyphen", "hypnosis", "hysterics",
    "icicle", "idealism", "identical", "ideology", "ignoring", "illegal", "imaginable", 
    "irrational", "irrigation", "issue",
    "jaguar", "jamboree", "jawbreaker", "jellyfish", "jetty", "jitterbug", "jobholder", 
    "joggled", "joist", "jubilation", "juniper", "justify",
    "kelp", "kernel", "kidney", "kindhearted", "kinship", "Kleenex", "knighthood", 
    "knitting", "knockabout",
    "laboratory", "lacerate", "lamentation", "laminate", "landline", "languid", "larceny", 
    "lumberyard", "luminescent", "luxurious", "lynx",
    "magnetic", "magnolia", "mainstream", "maize", "malefactor", "malformation", 
    "multitude", "murmur", "mutate",
    "nape", "narcotic", "narrator", "nationalism", "natural resource", "navigable", 
    "nutlet", "nutriment",
    "obese", "obeying", "obituary", "oblivious", "obscure", "observant", "obviously",
    "oversupply", "oxygen",
    "packaging", "palpitate", "panhandle", "paradise", "paradox", "parakeet", "paralysis",
    "proceed", "profession", "prosperous", "puzzling",
    "quaintness", "qualm", "quarantine", "quarterback", "queasier", "quick bread",
    "quince", "quitting", "quizzes",
    "racketeer", "radiantly", "radical", "railroad", "ramshackle", "raspy", "rationale", 
    "rollicking", "roughneck", "rowdiness", "rubella", "russet",
    "sabotage", "salsa", "sarcasm", "satisfactory", "scandal", "scarcely", "schedule", 
    "supplement", "survive", "syllabicate", "symbolism", "synthetic",
    "taffeta", "talkative", "tastefully", "taxation", "technician", "telescopic", 
    "tunnel", "turbojet", "twentieth", "typewriter", "typify",
    "ultima", "unaffected", "unaligned", "unbearable", "unblemished", "unclassified", 
    "unplug", "unravel", "unutterable", "uproarious", "usage", "uttermost",
    "vaccinate", "validity", "vandalism", "vanquish", "vaporize", "vegetative", "velocity", 
    "volume",
    "waistband", "wallaby", "warehouse", "warrant", "wash-and-wear", "waspish", "wearable",
    "wireless", "wisecrack", "wittingly", "woozy", "workmanship",
    "xylophone",
    "yacht", "yearling",
    "zealous", "zestfully"
]

# Create tests
def create_tests(words_list):
    tests = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        filtered_words = [word for word in words_list if word.startswith(letter)]
        tests[letter] = filtered_words
    return tests

tests = create_tests(words)

class SpellingApp:
    def __init__(self):
        self.score = 0
        self.incorrect_words = set()
        self.current_word = None
        self.words_to_test = []
        self.current_index = 0

    def display_main_menu(self):
        st.title("Spelling Test")
        st.button("Start Test", on_click=self.select_test)
        st.button("View Words", on_click=self.view_words)

    def select_test(self):
        letter = st.selectbox("Select a letter for the test:", list(tests.keys()))
        self.words_to_test = tests[letter]
        self.current_index = 0
        self.score = 0
        self.start_test()

    def start_test(self):
        if self.current_index < len(self.words_to_test):
            self.current_word = self.words_to_test[self.current_index]
            st.write(f"Spell the word: **{self.current_word}**")
            self.play_audio(self.current_word)
            user_input = st.text_input("Your answer:", "")
            if st.button("Submit"):
                self.check_spelling(user_input)
        else:
            st.write(f"Test complete! Your score: {self.score} / {len(self.words_to_test)}")
            self.display_main_menu()

    def check_spelling(self, user_input):
        if user_input.lower() == self.current_word.lower():
            self.score += 1
            st.success("Correct!")
        else:
            self.incorrect_words.add(self.current_word)
            st.error(f"Incorrect! The correct spelling is: {self.current_word}")
        
        self.current_index += 1
        self.start_test()

    def play_audio(self, text):
        tts = gTTS(text=text, lang='en')
        audio_file = io.BytesIO()
        tts.save(audio_file)
        audio_file.seek(0)
        st.audio(audio_file, format='audio/mp3')

    def view_words(self):
        st.title("List of Words")
        for letter, word_list in tests.items():
            st.subheader(f"Words starting with '{letter.upper()}':")
            st.write(", ".join(word_list))
        st.button("Back to Main Menu", on_click=self.display_main_menu)

# Initialize the application
app = SpellingApp()
app.display_main_menu()
