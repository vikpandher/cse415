# Linneus3.py
# Implements storage and inference on an ISA hierarchy
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version runs under Python 3.x.

# Steven Tanimoto
# (C) 2012.

# The ISA relation is represented using a dictionary, ISA.
# There is a corresponding inverse dictionary, INCLUDES.
# Each entry in the ISA dictionary is of the form
#  ('turtle' : ['reptile', 'shelled-creature'])

from re import *   # Loads the regular expression module.
ISA = {} # [A is a [B, God], [c, joe]], [Jones is a reliable, God], [Stef is an unreliable, Jones]
INCLUDES = {} # B includes A, etc.
ARTICLES = {} # (a) C

# Possibly add a parameter for 'speaker' make tuples.........
def store_isa_fact(category1, category2, speaker):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    try :
        c1list = ISA[category1]
        c1list.append([category2, speaker])
    except KeyError :
        ISA[category1] = [[category2, speaker]]
    try :
        c2list = INCLUDES[category2]
        c2list.append([category1, speaker])
    except KeyError :
        INCLUDES[category2] = [[category1, speaker]]
        
def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    try:
        c1list = ISA[category1]
        return c1list
    except:
        return []
    
def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    try:
        c1list = INCLUDES[category1]
        return c1list
    except:
        return []

all_god = True
def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    c1list = get_isa_list(category1)
    for isa in c1list :
        if isa[0] == category2 :
            if isa[1] != "God" :
                global all_god
                all_god = False
            return True
    return False
    
def isa_test(category1, category2, depth_limit = 10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    if category1 == category2 : return True
    if isa_test1(category1, category2) : return True
    if depth_limit < 2 : return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category[0], category2, depth_limit - 1):
            return True
    return False

def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()

def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    try:
        article = ARTICLES[noun]
        return article
    except KeyError:
        return ''

def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    while True :
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': return 'Goodbye now!'
        process(info)
        print_dict() ###
        print() ###

# Some regular expressions used to parse the user sentences:    
assertion_pattern = compile(r".*(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)    
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
# ex: Why is it possible that a dog is an organism?
why_possible_pattern = compile(r"^Why\s+is\s+it\s+possible\s+that\s+(a|an)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
# see if qualified
qualified_pattern = compile(r"^([-\w]+)\s+says\s+that.*", IGNORECASE)
reliability_pattern = compile(r"^([-\w]+\s+says\s+that\s+)?([-\w]+)\s+is\s+(a|an)\s+(reliable|unreliable)\s+source$", IGNORECASE)
only_why_pattern = compile(r"^Why\?$", IGNORECASE)

last_is_question = {}
def process(info) :
    global last_is_question
    # in case not qualified
    speaker = "God"
    result_match_object = qualified_pattern.match(info)
    if result_match_object != None :
        # speaker is either the specified or default God
        items = result_match_object.groups()
        speaker = items[0]
    result_match_object = reliability_pattern.match(info)
    if result_match_object != None :
        # speaker says items[0] is a items[2] source
        items = result_match_object.groups()
        store_article(items[3], items[2])
        store_isa_fact(items[1], items[3], speaker)
        print("I understand.")
        return
    result_match_object = why_possible_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]) :
            print("But that's not true, as far as I know!")
        else :
            answer_why(items[1], items[3])
        return
    'Handles the user sentence, matching and responding.'
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None :
        # speaker says isa relationship
        items = result_match_object.groups()
        store_article(items[1], items[0])
        store_article(items[3], items[2])
        store_isa_fact(items[1], items[3], speaker)
        print("I understand.")
        return
    result_match_object = query_pattern.match(info)
    if result_match_object != None :
        global all_god
        all_god = True
        # have to check reliability of a speaker
        items = result_match_object.groups()
        last_is_question = items
        answer = isa_test(items[1], items[3])
        immediate = isa_test1(items[1], items[3])
        if answer and all_god :
            print("Yes.")
        elif answer and not all_god and immediate :
            for isa in get_isa_list(items[1]) :
                if isa[0] == items[3] :
                    print("" + isa[1] + " says that it is.")
        elif answer and not all_god :
            print("It's quite possible that " + get_article(items[1]) +" " + str(items[1]) + " is " + get_article(items[3]) + " " + str(items[3]) + ".")
        else :
            print("I have no reason to believe so.")
        return
    result_match_object = what_pattern.match(info)
    if result_match_object != None :
        # have to check statements, who said them, and their reliability
        items = result_match_object.groups()
        supersets = get_isa_list(items[1])
        if supersets != [] :
            first = supersets[0][0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        else :
            subsets = get_includes_list(items[1])
            if subsets != [] :
                first = subsets[0][0]
                a1 = get_article(items[1]).capitalize()
                a2 = get_article(first)
                print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
                return
            else :
                print("I don't know.")
        return
    result_match_object = why_pattern.match(info)
    if result_match_object != None :
        # link reliabliity with who said what
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]) :
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return
    result_match_object = only_why_pattern.match(info)
    if result_match_object != None :
        if len(last_is_question) == 0 :
            print("Why what?")
        else :
            answer_why(last_is_question[1], last_is_question[3])
        return
    print("I do not understand.  You entered: ")
    print(info)

reliable = True
bad_speaker = ""
def answer_why(x, y):
    global bad_speaker
    'Handles the answering of a Why question.'
    if x == y:
        print("Because they are identical.")
        return
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    print("Because " + report_chain(x, y))
    global reliable
    if not all_god and not reliable:
        print("However, " + bad_speaker + " is an unreliable source,")
        print("and therefore we cannot be certain about this chain of reasoning.")
        reliable = True
        bad_speaker = ""
    return

from functools import reduce
def report_chain(x, y):
    'Returns a phrase that describes a chain of facts.'
    chain = find_chain(x, y)
    all_but_last = chain[0:-1]
    last_link = chain[-1]
    main_phrase = reduce(lambda x, y: x + y, map(report_link, all_but_last))
    last_phrase = "and " + report_link(last_link)
    new_last_phrase = last_phrase[0:-2] + '.'
    return main_phrase + new_last_phrase

def report_link(link):
    'Returns a phrase that describes one fact.'
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    speaker = get_speaker(x, y)
    global reliable
    reliable = check_reliability(speaker)
    if speaker == "God" :
        return a1 + " " + x + " is definitely " + a2 + " " + y + ", "
    else :
        return speaker + " says that " + a1 + " " + x + " is " + a2 + " " + y + ", "

def check_reliability(speaker) :
    for el in get_includes_list("unreliable"):
        if el[0] == speaker :
            global bad_speaker
            bad_speaker = speaker
            return False
    return True

def get_speaker(x, y) :
    for isa in get_isa_list(x) :
        if isa[0] == y :
            return isa[1]
    
def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y[0], z):
                temp = find_chain(y[0], z)
                temp.insert(0, [x,y[0]])
                return temp

### For Testing
def print_dict() :
    print("ISA      = " + str(ISA))
    print("INCLUDES = " + str(INCLUDES))
    print("ARTICLES = " + str(ARTICLES))

def test() :
    process("A turtle is a reptile.")
    process("A turtle is a shelled-creature.")
    process("A reptile is an animal.")
    process("An animal is a thing.")

def test1() :
    print(">>> Jones says that an animal is an organism.")
    process("Jones says that an animal is an organism.")
    print_dict()
    print();
    print(">>> Jones says that Smith is a reliable source.")
    process("Jones says that Smith is a reliable source.")
    print_dict()
    print();
    print(">>> A dog is an animal.")
    process("A dog is an animal.")
    print_dict()
    print();
    print(">>> Is a dog a pet?")
    process("Is a dog a pet?")
    print_dict()
    print();
    print(">>> Is a dog an organism?")
    process("Is a dog an organism?")
    print_dict()
    print();
    print(">>> Is a dog an animal?")
    process("Is a dog an animal?")
    print_dict()
    print();
    print(">>> Is an animal an organism?")
    process("Is an animal an organism?")
    print_dict()
    print();
    print(">>> Jones is an unreliable source.")
    process("Jones is an unreliable source.")
    print_dict()
    print();
    print(">>> Why is it possible that a dog is an organism?")
    process("Why is it possible that a dog is an organism?")
    print_dict()
    print();

#test1()
test()
linneus()
