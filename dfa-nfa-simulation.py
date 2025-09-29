# simulating a deterministic state machine

# example State 1 --0---> State 2
#         State 1 --1---> State 1
#          State 2 --0---> State 3
#          State 2 --1---> State 1
#          State 3 --0---> State 3
#          State 3 --1---> State 1
# string: input string
# current state
# FSM edges
# accepting states
# test input

# complete the following method

def dfasim(string, current, edges, accepting):
    pass

#test input
current = 1
edges = {(1,'0'):2, (1,'1'):1, (2,'0'):3, (2,'1'):1, (3,'0'):3, (3,'1'):1}
accepting = [3]

print(dfasim("100100", current, edges, accepting))

print(dfasim("101001001", current, edges, accepting))

def dfasim(string, current, edges, accepting):
    if string == "":
        return current in accepting
    else:
        # string is not empty, at-least one char left
        letter = string[0]
        #print("current letter: " + letter)
        if (current, letter) in edges:
            # make a transition
            next = edges[(current, letter)] # next state
            return dfasim(string[1:], next, edges, accepting)
        else:
            # no transition found
            return False


# COMMAND ----------

#test
current = 1
edges = {(1,'0'):2, (1,'1'):1, (2,'0'):3, (2,'1'):1, (3,'0'):3, (3,'1'):1}
accepting = [3]

print(dfasim("100100", current, edges, accepting))

print(dfasim("101001001", current, edges, accepting))


# COMMAND ----------

#NFA simulation

edges = {(1,'0'): [1,2], (1,'1'): [1], (2,'0'): [3]}
accepting = [3]

# COMMAND ----------

# simulating a non-deterministic state machine

# example State 1 --0---> State 1 or State 2
#         State 1 --1---> State 1
#          State 2 --0---> State 3
# string: input string
# current state
# FSM edges
# accepting states
# test input

# complete the following method

def nfasim(string, current, edges, accepting):
    pass

# test
edges = {(1,'0'): [1,2], (1,'1'): [1], (2,'0'): [3]}
accepting = [3]
print(nfasim("1010101010101010111110001111100", 1, edges, accepting))

# COMMAND ----------

# string: input
# current state
# graph def
# accepting states
def nfasim(string, current, edges, accepting):
    if string == "":
        return current in accepting
    else:
        letter = string[0:1]
        if (current, letter) in edges:
            remainder = string[1:]
            nextstates = edges[(current, letter)]
            for nextstate in nextstates:
                result = nfasim(remainder, nextstate, edges, accepting)
                if result:
                    return True
    return False
        
    

# COMMAND ----------

print(nfasim("1010101010101010111110001111100", 1, edges, accepting))

# COMMAND ----------

edges

# COMMAND ----------

def nfaaccepts(current, edges, accepting, visited):
    if current in visited:
        return None
    elif current in accepting:
        return ""
    else:
        newvisited = visited + [current]
        for edge in edges:
            if edge[0] == current:
                for newstate in edges:
                    foo = nfaaccepts(newstate, edges, accepting, newvisited)
                    if foo != None:
                        return edges[1] + foo
            return None
                
        

# COMMAND ----------

    
