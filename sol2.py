import queue



num_of_nodes = 0
num_of_edges = 0
a_paths = []
b_paths = []
c_paths = []
d_paths = []
e_paths = []
num_of_final_states = 0
final_states = []
num_of_inputs = 0
strings = []
epsilon_closure={}
transition_dict={}



def creating_edges_path():
    global num_of_nodes,num_of_edges
    global a_paths,b_paths,c_paths,d_paths,e_paths
    global transition_dict
    num_of_nodes, num_of_edges = input().split()
    for i in range(0, int(num_of_nodes)):
        a_paths.append([])
        b_paths.append([])
        c_paths.append([])
        d_paths.append([])
        e_paths.append([])

    for i in range(0, int(num_of_edges)):
        start_edge, end_edge, character = input().split()
        start_edge = int(start_edge) - 1
        end_edge = int(end_edge) - 1
        if (start_edge , character) in transition_dict :
            if end_edge not in transition_dict[(start_edge,character)] :
                transition_dict[(start_edge,character)].append(end_edge) 
        else :
            transition_dict[(start_edge,character)]=[end_edge]

        if character == 'a':
            a_paths[start_edge].append(end_edge)
        if character == 'b':
            b_paths[start_edge].append(end_edge)
        if character == 'c':
            c_paths[start_edge].append(end_edge)
        if character == 'd':
            d_paths[start_edge].append(end_edge)
        if character == 'e':
            e_paths[start_edge].append(end_edge)
def getting_final_states():
    global final_states
    global num_of_final_states
    num_of_final_states = int(input())
    final_states = [int(x)-1 for x in input().split()]
def getting_input_strings():
    global num_of_inputs
    global strings
    num_of_inputs = int(input())
    for i in range(num_of_inputs):
        strings.append(input())


def calc_epsilon_closure_for_one_state(start_state):
    global transition_dict
    reachable_states = set()
    states_to_check = queue.Queue()
    states_checked = set()
    states_to_check.put(start_state)
    while not states_to_check.empty():
        state = states_to_check.get()
        reachable_states.add(state)
        if (state,'e') in transition_dict :
            for dst_state in transition_dict[(state,'e')] :
                if  dst_state not in states_checked :
                    states_to_check.put(dst_state)
            states_checked.add(state)
    return reachable_states
def calc_epsilon_closure_for_all_state():
    global epsilon_closure
    global e_paths
    global num_of_nodes
    for state in range(int(num_of_nodes)):
        epsilon_closure[state] = list(calc_epsilon_closure_for_one_state(state))
def applying_landa(start_states):
    closure=set()
    for state in start_states:
        closure.update(epsilon_closure[state])
    return closure


def getting_inputs():
    creating_edges_path()
    getting_final_states()
    getting_input_strings()
    calc_epsilon_closure_for_all_state()


def traverse_string_on_fa(input_string):
    global final_states
    global a_paths,b_paths,c_paths,e_paths,d_paths
    start_states = set([0])
    start_states = applying_landa(start_states)
    if input_string == "NONE":
        if  not start_states.isdisjoint(set(final_states)) :
            print( "YES")
            return
        else : 
            print("NO") 
            return
    end_states=set()
    for char in input_string:
        end_states = set()
        start_states = applying_landa(start_states)
        for state in start_states:
            if(char == 'a'):
                end_states.update(a_paths[state])
            if(char == 'b'):
                end_states.update(b_paths[state])
            if(char == 'c'):
                end_states.update(c_paths[state])
            if(char == 'd'):
                end_states.update(d_paths[state])
        end_states = applying_landa(set(end_states))
        start_states=set()
        start_states=end_states
        # print(start_states)
    if end_states.isdisjoint(final_states) :
        print("NO")
    else:
        print("YES")

def output_result():
    global strings
    for string in strings:
        traverse_string_on_fa(string)



getting_inputs()
output_result()
