import queue
import itertools


def common_member(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if len(a_set.intersection(b_set)) > 0: 
        return(True)  
    return(False) 
def get_string_from_input_and_check_validation(dfa):
    strings=[]
    answers=[]
    t = int(input())
    for i in range(t):
        string=input()
        strings.append(string)
    for string in strings:
        answers.append(dfa.string_validation(string))
    for answer in answers :
        print(answer)


class DisjointSet(object):

	def __init__(self,items):

		self._disjoint_set = list()

		if items:
			for item in set(items):
				self._disjoint_set.append([item])

	def _get_index(self,item):
		for s in self._disjoint_set:
			for _item in s:
				if _item == item:
					return self._disjoint_set.index(s)
		return None

	def find(self,item):
		for s in self._disjoint_set:
			if item in s:
				return s
		return None

	def find_set(self,item):

		s = self._get_index(item)

		return s+1 if s is not None else None 

	def union(self,item1,item2):
		i = self._get_index(item1)
		j = self._get_index(item2)

		if i != j:
			self._disjoint_set[i] += self._disjoint_set[j]
			del self._disjoint_set[j]
	
	def get(self):
		return self._disjoint_set



class NFA:
    def __init__(self):
        self.num_states = 0
        self.states = []
        self.symbols = ['a','b','c','d']
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 1
        self.transition_dict = {}
        self.e_closure = {}

    def init_states(self):
        for i in range(self.num_states):
            self.states.append(i+1)

    def print_nfa(self):
        print("NFA:")
        print("num_states:",self.num_states)
        print("states:",self.states)
        print("symbols:",self.symbols)
        print("num_accepting_states:",self.num_accepting_states)
        print("accepting_states:",self.accepting_states)
        print("start_state:",self.start_state)
        print("transition_dict:",self.transition_dict)
        print("e_closure:",self.e_closure)
        print("\n\n\n")

    def construct_nfa_from_input(self):
        n,m = input().split()
        self.num_states = int(n)
        self.init_states()
        self.start_state = 1

        for i in range(int(m)) :
            src , des , edge = input().split()
            starting_state = int(src)
            transition_symbol = edge
            ending_state = int(des)
            if (starting_state,transition_symbol) in self.transition_dict:
                self.transition_dict[(starting_state,transition_symbol)].append(ending_state)
            else:
                self.transition_dict[(starting_state,transition_symbol)] = [ending_state]

        k=int(input())
        self.num_accepting_states = k
        self.accepting_states.extend([int(x) for x in input().split()])
        self.calc_e_closure()


        # print("\n\n\nnfa is constructed from input:")
        # self.print_nfa()

    def e_closure_state (self , state , visited ):
        if (not visited [ state-1 ] ):
            if state in self.e_closure :
                self.e_closure[state].append(state)
            else:
                self.e_closure[state] = [state]
            visited [state - 1 ] = True
            if ( state,'e') in self.transition_dict :
                for value in self.transition_dict[(state,'e')] :
                    if not visited[ value - 1 ]:
                        self.e_closure_state( value , visited )
                        for x in self.e_closure[value]:
                            if x not in self.e_closure[state]:
                                self.e_closure [state].append(x)
                    if value not in self.e_closure[state]:
                        self.e_closure[state].append(value)
        else : return 

    def calc_e_closure(self):
        visited = [ False ] * self.num_states
        for state in self.states:
            if not visited [ state -1 ] :
                self.e_closure_state(state , visited )

    def del_null_move(self):
        is_nfa = True
        for key in self.transition_dict:
            if key[1] =='e':
                is_nfa=False
                break
        if is_nfa : return

        dic = {}
        for state in self.states :
            for symbol in self.symbols :
                des=set()
                for closure_state in self.e_closure[state]:
                    if (closure_state,symbol) in self.transition_dict :
                        for value in self.transition_dict[(closure_state,symbol)] :
                            des.add(value)
                update_des=set()
                for item in des :
                    for x in self.e_closure[item]:
                        update_des.add(x)
                if  des :
                    dic[(state,symbol)] = list(update_des)

        self.transition_dict=dic

        
        new_final_state=[]
        for state in self.states :
            if (common_member(self.e_closure[state],self.accepting_states)):
                if state not in self.accepting_states :
                    new_final_state.append(state)
        self.accepting_states.extend(new_final_state)
        self.num_accepting_states = len(self.accepting_states)
        self.e_closure = {}
        # self.calc_e_closure()

        # print("\n\n\nnfa after delete null move:")
        # self.print_nfa()




class DFA:
    def __init__(self):
        self.num_states = 0
        self.symbols = []
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_dict={}
        self.q = []
        self.states=[]
    
    def convert_from_nfa(self, nfa):
        self.symbols = nfa.symbols
        self.start_state = 0
        dfa_transition_dict = {}
        self.q.append((1,))
        
        for dfa_state in self.q:
            for symbol in nfa.symbols:
                if len(dfa_state) == 1 and (dfa_state[0], symbol) in nfa.transition_dict:
                    dfa_transition_dict[(dfa_state, symbol)] = nfa.transition_dict[(dfa_state[0], symbol)]
                    
                    if tuple(dfa_transition_dict[(dfa_state, symbol)]) not in self.q:
                        self.q.append(tuple(dfa_transition_dict[(dfa_state, symbol)]))
                else:
                    destinations = []
                    final_destination = []
                    
                    for nfa_state in dfa_state:
                        if (nfa_state, symbol) in nfa.transition_dict and nfa.transition_dict[(nfa_state, symbol)] not in destinations:
                            destinations.append(nfa.transition_dict[(nfa_state, symbol)])
                    
                    if not destinations:
                        final_destination.append(None)
                    else:  
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)
                        
                    dfa_transition_dict[(dfa_state, symbol)] = final_destination
                        
                    if tuple(final_destination) not in self.q:
                        self.q.append(tuple(final_destination))

        for key in dfa_transition_dict:
            if ( self.q.index(tuple(key[0])) , key[1] ) in self.transition_dict :
                self.transition_dict[( self.q.index(tuple(key[0])) , key[1] )].append(self.q.index(dfa_transition_dict[key]))
            else :
                self.transition_dict[( self.q.index(tuple(key[0])) , key[1] )]= [ self.q.index(tuple (dfa_transition_dict[key])) ]


        for q_state in self.q:
            for nfa_accepting_state in nfa.accepting_states:
                if nfa_accepting_state in q_state:
                    self.accepting_states.append(self.q.index(q_state))
                    self.num_accepting_states += 1
                    break
        self.num_states = len(self.q)
        self.states = [int(x) for x in range(self.num_states)]

    def print_dfa(self):
        print("DFA:")
        print("num_states:",self.num_states)
        print("states:",self.q)
        print("states: ", self.states)
        print("symbols:",self.symbols)
        print("num_accepting_states:",self.num_accepting_states)
        print("accepting_states:",self.accepting_states)
        print("start_state:",self.start_state)
        print("transition_dict:",self.transition_dict)
        print("\n\n\n")
        
    def string_validation(self,string):
        if string=="NONE" and self.start_state in self.accepting_states:
            return "YES"
        current_state = self.start_state
        for char in string:
            if  (current_state , char) in self.transition_dict :
                current_state = self.transition_dict[(current_state,char)][0] 
            else:
                return "NO"
        if current_state in self.accepting_states:
            return "YES"
        else : return "NO"

    
     

    def minify(self) :
        self.remove_unreachable_states()
        states_table = self.create_markable_states_table()
        self.mark_states_table_first(states_table)
        self.mark_states_table_second(states_table)
        self.join_non_marked_states(states_table)
    
    def remove_unreachable_states(self) :
        reachable_states = self.compute_reachable_states()
        unreachable_states = set(self.states) - reachable_states
        for state in unreachable_states :
            self.states.remove(state)
            del_transition=[]
            for key in self.transition_dict :
                if key[0] == state:
                    del_transition.append(key)
                if state in self.transition_dict[key] :
                    self.transition_dict[key].remove(state)
            for key in del_transition:
                del self.transition_dict[key]

    def compute_reachable_states(self):
        #simple bfs return set of reachable state
        reachable_states = set()
        states_to_check = queue.Queue()
        states_checked = set()
        states_to_check.put(self.start_state)
        while not states_to_check.empty():
            state = states_to_check.get()
            reachable_states.add(state)
            for symbol in self.symbols :
                for dst_state in self.transition_dict[(state,symbol)] :
                    if  dst_state not in states_checked :
                        states_to_check.put(dst_state)
            states_checked.add(state)
        return reachable_states

    def create_markable_states_table(self) :
        table = {
            frozenset(c): False
            for c in itertools.combinations(self.states, 2)
        }
        return table
        
        
    def mark_states_table_first(self, table) :
        for s in table.keys():
            if any((x in self.accepting_states for x in s)):
                if any((x not in self.accepting_states for x in s)):
                    table[s] = True

    def mark_states_table_second(self, table):
        changed = True
        while changed:
            changed = False
            for s in filter(lambda s: not table[s], table.keys()):
                s_ = tuple(s)
                for a in self.symbols:
                    s2 = frozenset({
                        self.transition_dict[(s_[0], a)][0],
                        self.transition_dict[(s_[1], a)][0]
                    })
                    if s2 in table and table[s2]:
                        table[s] = True
                        changed = True
                        break
    
    def join_non_marked_states(self, table):
        non_marked_states = set(filter(lambda s: not table[s], table.keys()))
        changed = True
        while changed:
            changed = False
            for s, s2 in itertools.combinations(non_marked_states, 2):
                if s2.isdisjoint(s):
                    continue
                # merge them!
                s3 = s.union(s2)
                # remove the old ones
                non_marked_states.remove(s)
                non_marked_states.remove(s2)
                # add the new one
                non_marked_states.add(s3)
                # set the changed flag
                changed = True
                break
        # finally adjust the DFA
        for s in non_marked_states:
            new_merge_state = tuple(s)
            # add the new state
            self.states.append(new_merge_state)
            # copy the transitions from one of the states
            for symbol in self.symbols:
                self.transition_dict[( new_merge_state , symbol)] = []
                self.transition_dict[(new_merge_state , symbol)].extend( self.transition_dict [ (tuple(s)[0] , symbol) ] )
            # replace all occurrences of the old states
            for state in s:
                self.states.remove(state)

                del_start_state_transition=[]
                for key in self.transition_dict:
                    if key[0]==state:
                        del_start_state_transition.append(key)
                for key in del_start_state_transition :
                    del self.transition_dict[key]
                
                for key in self.transition_dict:
                    if state in self.transition_dict[key]:
                        self.transition_dict[key].remove(state)
                        if new_merge_state not in self.transition_dict[key]:
                            self.transition_dict[key].append(new_merge_state)
                

                if state in self.accepting_states:
                    if new_merge_state not in self.accepting_states:
                        self.accepting_states.append(new_merge_state)
                    self.accepting_states.remove(state)
                if state == self.start_state:
                    self.start_state = new_merge_state

        self.num_states = len(self.states)
        self.num_accepting_states =len(self.accepting_states)





nfa = NFA()
dfa = DFA()

nfa.construct_nfa_from_input()
nfa.del_null_move()
dfa.convert_from_nfa(nfa) 
dfa.minify()
get_string_from_input_and_check_validation(dfa)

