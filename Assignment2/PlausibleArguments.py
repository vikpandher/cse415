'''PartIII.py
Chloe Nash, Vik Pandher, CSE 415, Spring 2016, University of Washington
Instructor: S. Tanimoto.
Assignment 2 Part III. ISA Heirarchy Manipulation

I worked with Vik Pandher.

Status of the implementation of new features:

Qualified and unqualified statements both work properly.
Both why questions work as specified.
'''

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
ISA = {} # [A is a [B, God], [c, joe]], [Jones is a reliable, God], [Stef is an [unreliable, Jones]]
INCLUDES = {} # B includes A, etc.
ARTICLES = {} # (a) C
REDUNDANCIES = {} # Tracks redundancies for checkIndirect
# Redundancies are stored as a dictionary where the key is the parent and the
# values are the children. The "is a" relations would be as follows:
# (child is a parrent)

# Modified isa to store who qualified the statement.
# If no qualifier, automatically set to God, taken as fact.
# Isa is a list of tuples 
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

# all_god is True when no qualified statements, False if a qualified statement is specified
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

# Some regular expressions used to parse the user sentences:    
assertion_pattern = compile(r".*(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)    
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
# Matches when the user asks why something is possible
# ex: Why is it possible that a dog is an organism?
why_possible_pattern = compile(r"^Why\s+is\s+it\s+possible\s+that\s+(a|an)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
# Matches when a statement is qualified
qualified_pattern = compile(r"^([-\w]+)\s+says\s+that.*", IGNORECASE)
# Matches when a statement declares the reliability of someone
reliability_pattern = compile(r"^([-\w]+\s+says\s+that\s+)?([-\w]+)\s+is\s+(a|an)\s+(reliable|unreliable)\s+source\.?$", IGNORECASE)
# Matches when the user only types why?
only_why_pattern = compile(r"^Why\?$", IGNORECASE)

# Stores the last question asked so when the user types Why? it can be answered
last_is_question = {}
def process(info) :
    global last_is_question
    # in case not qualified, God is default speaker
    speaker = "God"
    'Handles the user sentence, matching and responding.'
    result_match_object = qualified_pattern.match(info)
    if result_match_object != None :
        # speaker is either the specified or default God
        # after speaker updated, move on to match rest of sentence
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
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        # If already told something, no need to store it
        if isa_test1(items[1], items[3]) :
            print("You told me that earlier.")
            return
        if isa_test(items[1], items[3]) :
            print("You don't have to tell me that.")
            return
        store_article(items[1], items[0])
        store_article(items[3], items[2])
        store_isa_fact(items[1], items[3], speaker)
        # Clear REDUNDANCIES and check for them
        REDUNDANCIES.clear()
        checkIndirect(items[1], items[3])
        redundancy_count = 0
        # Go through REDUNDANCIES and count all the redundancies
        for redundancy in REDUNDANCIES :
            redundancy_count += len(REDUNDANCIES.get(redundancy))
        # The output message varies depending on the number of redundancies
        if redundancy_count == 1 :
            for parent in REDUNDANCIES :
                for child in REDUNDANCIES.get(redundancy) :
                    print("Your earlier statement that " + get_article(child[0]) +\
                          " " + child[0] + " is " + get_article(parent) + " " + parent +\
                          " is now redundant.")
            return
        elif redundancy_count > 1:
            output = ""
            print("The following statements you made earlier are now all redundant:")
            for parent in REDUNDANCIES :
                for child in REDUNDANCIES.get(redundancy) :
                    output += (get_article(child[0]) + " " + child[0] +\
                    " is " + get_article(parent) + " " + parent + ";\n")
            output = output[0:-2] + ".\n"
            print(output)
            return
        print("I understand.")
        return
    result_match_object = query_pattern.match(info)
    if result_match_object != None :
        global all_god
        all_god = True
        items = result_match_object.groups()
        last_is_question = items # update the last question asked for why? case
        answer = isa_test(items[1], items[3]) # stores if it is even true
        immediate = isa_test1(items[1], items[3]) # stores if directly true
        if answer and all_god :
            print("Yes.")
        elif answer and not all_god and immediate :
            for isa in get_isa_list(items[1]) :
                if isa[0] == items[3] :
                    print("" + isa[1] + " says that it is.")
        elif answer and not all_god :
            print("It's quite possible that " + get_article(items[1]) +" " + str(items[1]) +\
                  " is " + get_article(items[3]) + " " + str(items[3]) + ".")
        else :
            print("I have no reason to believe so.")
        return
    result_match_object = what_pattern.match(info)
    if result_match_object != None :
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
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]) :
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return
    result_match_object = only_why_pattern.match(info)
    if result_match_object != None :
        if len(last_is_question) == 0 :
            # If Why? is the first thing typed
            print("Why what?")
        else :
            answer_why(last_is_question[1], last_is_question[3])
        return
    print("I do not understand.  You entered: ")
    print(info)

# This method checks for indirect connections and reports them
# in the dictionary called REDUNDANCIES
def checkIndirect(child, parent, depth_limit = 3):
    # Depth limit reached
    if depth_limit < 1 :
        return False
    # siblings are all the things that are directly under the parent
    siblings = get_includes_list(parent)
    for sibling in siblings :
        # If a sibling "isa" child, record the redundancy,
        # Ignore the case where sibling == child since that will
        # always be true (A spade is a spade.)
        if isa_test(sibling[0], child) and sibling[0] != child:
            try :
                list = REDUNDANCIES[parent]
                list.append(sibling)
            except KeyError :
                REDUNDANCIES[parent] = [sibling]
    # Remove the redundancies from the ISA and INCLUDES ditionaries
    for source in REDUNDANCIES :
        for thing in REDUNDANCIES.get(source) :
            isa_list = get_isa_list(thing[0])
            for item in isa_list :
                if item[0] == source :
                    isa_list.remove(item);
            for item in siblings :
                if item == thing :
                    siblings.remove(thing);
    # for indirect redundancies go up and do the same check for the
    # parents of the parent. depth_limit limits how far up we check
    # from the given parent.
    grandparents = get_isa_list(parent)
    for grandparent in grandparents :
        if checkIndirect(parent, grandparent[0], depth_limit - 1):
            return True
    return False

# tracks if all the speakers are reliable, False if 1 or more are not reliable
reliable = True
# Tracks who the unreliable speaker is
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
    if isa_test(x, y) :
        print("Because " + report_chain(x, y))
    else :
        print("Because I have no reason to believe so.")
        return
    global reliable
    if not all_god and not reliable:
        # Only prints if a speaker is found to be unreliable
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
    new_last_phrase = last_phrase[0:-3] + '.'
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
        # If speaker is God, taken as fact 
        return a1 + " " + x + " is definitely " + a2 + " " + y + ", \n"
    else :
        return speaker + " says that " + a1 + " " + x + " is " + a2 + " " + y + ", \n"

# checks if current speaker is unreliable and updates 'reliable'
def check_reliability(speaker) :
    for el in get_includes_list("unreliable"):
        if el[0] == speaker :
            global bad_speaker
            bad_speaker = speaker
            return False
    return True

# returns the current speaker for the specified isa relationship
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

# output dictionary info for debugging
def print_dict() :
    print("ISA      = " + str(ISA))
    print("INCLUDES = " + str(INCLUDES))
    print("ARTICLES = " + str(ARTICLES))

# Stock test
def test() :
    process("A turtle is a reptile.")
    process("A turtle is a shelled-creature.")
    process("A reptile is an animal.")
    process("An animal is a thing.")

# Part 2.3 test
def test2() :
    print(">>> A hawk is a raptor")
    process("A hawk is a raptor")
    print_dict()
    print();
    print(">>> A hawk is an animal")
    process("A hawk is an animal")
    print_dict()
    print();
    print(">>> A bird is an animal")
    process("A bird is an animal")
    print_dict()
    print();
    print(">>> A raptor is a bird")
    process("A raptor is a bird")
    print_dict()
    print();

def test3_0() :
    print(">>> Jones says that a chinook is an organism.")
    process("Jones says that a chinook is an organism.")
    print_dict()
    print();
    print(">>> Jones says that a sockeye is a salmon.")
    process("Jones says that a sockeye is a salmon.")
    print_dict()
    print();
    print(">>> Jones says that a fish is an animal.")
    process("Jones says that a fish is an animal.")
    print_dict()
    print();
    print(">>> Jones says that a sockeye is an organism.")
    process("Jones says that a sockeye is an organism.")
    print_dict()
    print();
    print(">>> Jones says that a chinook is an animal.")
    process("Jones says that a chinook is an animal.")
    print_dict()
    print();
    print(">>> Jones says that a chinook is a salmon.")
    process("Jones says that a chinook is a salmon.")
    print_dict()
    print();
    print(">>> Jones says that a sockeye is an animal.")
    process("Jones says that a sockeye is an animal.")
    print_dict()
    print();
    print(">>> Jones says that a fish is an organism.")
    process("Jones says that a fish is an organism.")
    print_dict()
    print();

# Part 2.4 test
def test3() :
    print(">>> A chinook is an organism.")
    process("A chinook is an organism.")
    print_dict()
    print();
    print(">>> A sockeye is a salmon.")
    process("A sockeye is a salmon.")
    print_dict()
    print();
    print(">>> A fish is an animal.")
    process("A fish is an animal.")
    print_dict()
    print();
    print(">>> A sockeye is an organism.")
    process("A sockeye is an organism.")
    print_dict()
    print();
    print(">>> A chinook is an animal.")
    process("A chinook is an animal.")
    print_dict()
    print();
    print(">>> A chinook is a salmon.")
    process("A chinook is a salmon.")
    print_dict()
    print();
    print(">>> A sockeye is an animal.")
    process("A sockeye is an animal.")
    print_dict()
    print();
    print(">>> A fish is an organism.")
    process("A fish is an organism.")
    print_dict()
    print();
    print(">>> A salmon is a fish.")
    process("A salmon is a fish.")
    print_dict()
    print();
    
def test4() :
    print(">>> An ant is an insect.")
    process("An ant is an insect.")
    print_dict()
    print();
    print(">>> An insect is an animal.")
    process("An insect is an animal.")
    print_dict()
    print();
    print(">>> An animal is a thing.")
    process("An animal is a thing.")
    print_dict()
    print();
    print(">>> Why is an ant a thing.")
    process("Why is an ant a thing.")
    print_dict()
    print();

def test5() :
    print(">>> Joe said an ant is an insect.")
    process("Joe said an ant is an insect.")
    print_dict()
    print();
    print(">>> Steve said an insect is an animal.")
    process("Steve said an insect is an animal.")
    print_dict()
    print();
    print(">>> An animal is a thing.")
    process("An animal is a thing.")
    print_dict()
    print();
    print(">>> Why is an ant a thing.")
    process("Why is an ant a thing.")
    print_dict()
    print();

def test6() :
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


# test()
# test2()
# test3_0() 
# test3()
# test4()
# test5()
# test6()
linneus()
