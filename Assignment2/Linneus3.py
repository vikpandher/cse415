'''PartII.py
Chloe Nash, Vik Pandher, CSE 415, Spring 2016, University of Washington
Instructor: S. Tanimoto.
Assignment 2 Part II. ISA Heirarchy Manipulation

I worked with Vik Pandher.

Status of the implementation of new features:

All forms of redundancy detection and processing are working.
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

ISA = {}
INCLUDES = {}
ARTICLES = {}
REDUNDANCIES = {} # Tracks redundancies for checkIndirect
# Redundancies are stored as a dictionary where the key is the parent and the
# values are the children. The "is a" relations would be as follows:
# (child is a parrent)

def store_isa_fact(category1, category2):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    try :
        c1list = ISA[category1]
        c1list.append(category2)
    except KeyError :
        ISA[category1] = [category2]
    try :
        c2list = INCLUDES[category2]
        c2list.append(category1)
    except KeyError :
        INCLUDES[category2] = [category1]
        
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
    
def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    c1list = get_isa_list(category1)
    return c1list.__contains__(category2)
    
def isa_test(category1, category2, depth_limit = 10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    if category1 == category2 : return True
    if isa_test1(category1, category2) : return True
    if depth_limit < 2 : return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
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
        # print_dict() # for debugging
        # print()

# Some regular expressions used to parse the user sentences:    
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)    
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)    

def process(info) :
    'Handles the user sentence, matching and responding.'
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
        store_isa_fact(items[1], items[3])
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
                    print("Your earlier statement that " + get_article(child) +\
                          " " + child + " is " + get_article(parent) + " " + parent +\
                          " is now redundant.")
            return
        elif redundancy_count > 1:
            output = ""
            print("The following statements you made earlier are now all redundant:")
            for parent in REDUNDANCIES :
                for child in REDUNDANCIES.get(redundancy) :
                    output += (get_article(child) + " " + child + " is " + get_article(parent) + " " + parent + ";\n")
            output = output[0:-2] + ".\n"
            print(output)
            return
        print("I understand.")
        return
    result_match_object = query_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        answer = isa_test(items[1], items[3])
        if answer :
            print("Yes, it is.")
        else :
            print("No, as far as I have been informed, it is not.")
        return
    result_match_object = what_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        supersets = get_isa_list(items[1])
        if supersets != [] :
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        else :
            subsets = get_includes_list(items[1])
            if subsets != [] :
                first = subsets[0]
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
        if isa_test(sibling, child) and sibling != child:
            try :
                list = REDUNDANCIES[parent]
                list.append(sibling)
            except KeyError :
                REDUNDANCIES[parent] = [sibling]
    # Remove the redundancies from the ISA and INCLUDES ditionaries
    for source in REDUNDANCIES :
        for thing in REDUNDANCIES.get(source) :
            isa_list = get_isa_list(thing)
            for item in isa_list :
                if item == source :
                    isa_list.remove(source);
            for item in siblings :
                if item == thing :
                    siblings.remove(thing);
    # for indirect redundancies go up and do the same check for the
    # parents of the parent. depth_limit limits how far up we check
    # from the given parent.
    grandparents = get_isa_list(parent)
    for grandparent in grandparents :
        if checkIndirect(parent, grandparent, depth_limit - 1):
            return True
    return False

def answer_why(x, y):
    'Handles the answering of a Why question.'
    if x == y:
        print("Because they are identical.")
        return
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    print("Because " + report_chain(x, y))
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
    return a1 + " " + x + " is " + a2 + " " + y + ", "
    
def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x,y])
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
    
# test()
# test2()
# test3()
# test4()
linneus()

