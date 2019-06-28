import queue
import string

symbols=list(string.ascii_lowercase)
symbols.append('+')
transition_dict={}
transition_functions=[]
num_of_nodes = 0
num_of_edges = 0
num_of_final_states = 0
final_states = []
path_dic={}
epsilon_closure={}








def construct_from_regx(regex):
    global symbols
    global transition_dict
    global num_of_nodes , num_of_edges , num_of_final_states
    global final_states
    global transition_functions
    global path_dic

    curr_state = 0

    for symbol in symbols :
        path_dic[symbol]=[]

 
    
    
    for char in regex : 
        if char =='*' :
            for symbol in symbols :
                if  ( curr_state , symbol , curr_state ) not in transition_functions :
                        transition_functions.append( ( curr_state , symbol , curr_state ) )
            if ( curr_state , '+' , curr_state ) not in transition_functions :
                    transition_functions.append(( curr_state , '+' , curr_state ))


        elif char == '?' :
            for symbol in symbols :
                if (curr_state  , symbol , curr_state + 1 ) not in transition_functions :
                    transition_functions.append( ( curr_state  , symbol , curr_state + 1 ) )
            curr_state += 1

        else :
            if ( curr_state , char , curr_state + 1 ) not in transition_functions :
                transition_functions.append ((  curr_state , char , curr_state + 1))
            curr_state += 1

    num_of_nodes = curr_state + 1
    num_of_edges = len(transition_functions)
    num_of_final_states = 1
    final_states = [curr_state]

    
    for symbol in symbols :
        for i in range(0,int(num_of_nodes)):
            path_dic[symbol].append([])


    for transition in transition_functions:
        starting_state = transition[0]
        transition_symbol = transition[1]
        ending_state = transition[2]
        if (starting_state, transition_symbol) in transition_dict:
            transition_dict[(starting_state, transition_symbol)].append(ending_state)
        else:
            transition_dict[(starting_state, transition_symbol)] = [ending_state]

        path_dic[transition_symbol][starting_state].append(ending_state)
def calc_epsilon_closure_for_one_state(start_state):
    global transition_dict
    global path_dic
    reachable_states = set()
    states_to_check = queue.Queue()
    states_checked = set()
    states_to_check.put(start_state)
    while not states_to_check.empty():
        state = states_to_check.get()
        reachable_states.add(state)
        if (state,'+') in transition_dict :
            for dst_state in transition_dict[(state,'+')] :
                if  dst_state not in states_checked :
                    states_to_check.put(dst_state)
            states_checked.add(state)
    return reachable_states
def calc_epsilon_closure_for_all_state():
    global epsilon_closure
    global num_of_nodes
    for state in range(int(num_of_nodes)):
        epsilon_closure[state] = list(calc_epsilon_closure_for_one_state(state))
def applying_landa(start_states):
    closure=set()
    for state in start_states:
        closure.update(epsilon_closure[state])
    return closure
def function_get_input_print_result():
    string=input()
    regex=input()
    construct_from_regx(regex)
    calc_epsilon_closure_for_all_state()
    # print_all()
    traverse_string_on_fa(string)
def traverse_string_on_fa(input_string):
    global final_states
    global path_dic
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
            end_states.update(path_dic[char][state])
        end_states = applying_landa(set(end_states))
        start_states=set()
        start_states=end_states
    if end_states.isdisjoint(final_states) :
        print("NO")
    else:
        print("YES")


def print_all():
    print("symbols: ",symbols)
    print("transition_dict: " ,transition_dict)
    print("transition_functions: " ,transition_functions)
    print("num_of_nodes: " ,num_of_nodes ) 
    print("num_of_edges: " ,num_of_edges ) 
    print("num_of_final_states: " ,num_of_final_states)
    print("final_states :" ,final_states)
    print("path_dic: " ,path_dic)
    print("epsilon_closure: ",epsilon_closure)


function_get_input_print_result()