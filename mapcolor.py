"""
Make sure to fill in the following information before submitting your
assignment. Your grade may be affected if you leave it blank!
For usernames, make sure to use your Whitman usernames (i.e. exleyas). 
File name: mapcolor.py
Author username(s): taylorba ashleygw
Date: 2/23/18
"""

'''
mapcolor.py
Code for a map-coloring problem solver 
'''
import sys
import re
import itertools as it
from collections import defaultdict

class MapColor:
    def __init__(self, neighborpairs, colors):
        '''
        
        '''
        assert isinstance(neighborpairs, str), 'neighborpairs must be a string'
        assert isinstance(colors, list), 'colors must be a list of strings'
        self.color_list = colors

        self.neighbors = defaultdict(list)
        self.neighbor_list = []
        specs = [spec.split(':') for spec in neighborpairs.split(';')]

        vset = set()
        for (A, Aneigh) in specs:
            A = A.strip()
            for B in Aneigh.split():
                self.neighbors[A].append(B)
                self.neighbors[B].append(A)
                self.neighbor_list.append((A,B))
                vset.add(A)
                vset.add(B)

        self.variable_list = list(vset)
        self.bf_count = 0
        self.bt_count = 0

    def solve_brute_force(self):
        '''Brute force solver for map coloring. Simply uses a DFS to try all combinations of colors with
        the map locations we have until it finds one that is a legal coloring.
        '''
        assignment = {}
        self.rec_brute_force(assignment)
        return assignment

    def rec_brute_force(self, assignment):
        '''Recursive helper for brute force
            assignment is a dictionary from variables to values
        '''
        var = self.select_unassigned_variable(assignment)
        if var == None:
            return self.is_solution(assignment)
        for val in self.color_list:
            assignment[var] = val
            self.bf_count += 1
            result = self.rec_brute_force(assignment)
            if result != False:
                return True
            del assignment[var]
        return False

    def is_solution(self, assignment):
        '''Checks whether a given assignment is actually a solution.
        '''
        for pair in self.neighbor_list:
            if assignment[pair[0]] == assignment[pair[1]]:
                return False
        return True

    def select_unassigned_variable(self, assignment, domains = None):
        '''Selects a variable that has not yet been given a value according to
        the given assignment.
        Currently this just selects the first variable in variable_list that
        has not yet been given a value in the assignment. 
        Large increases in efficiency are possible with some more intelligent 
        selection criteria, but it isn't necessary to do this for the map-coloring problem.
        '''
        if domains == None:
            for var in self.variable_list:
                if var not in assignment:
                    return var
        return None

    def solve_backtrack_search(self):
        '''A helper function that sets up our domains and initial assignment, then 
        calls a recursive backtracking search that will do the hard work.
        
        You should not need to change this function.
        '''
        domains = {}
        for var in self.variable_list:
            domains[var] = self.color_list[:]
        result = self.backtrack({}, domains)
        if self.is_solution(result):
            return result
        else:
            return "Error! Backtrack returned an assignment that is not a solution"

    def backtrack(self, assignment, domains):
        '''Perform the actual backtracking search
            assignment: A dictionary of variable: value assignments
            domains: A dictionary of variable: list of value possibilities

            You will need to add to this code and some helper methods
        '''
        # helper functions: order_domain_values -- determines in what order a variable's values should be tried
        
#         if assignment is complete:
#             return assignment
#         var = select_unassigned_variable(csp, assignment)
#         for each value in order_domain_values(var, assignment, csp):
#             if value is consistent with assignment:
#                 add {var=value} to assignment
#                 inferences = inference(csp,var,assignment)
#                 if inferences != failure:
#                     add inferences to assignment
#                     result = backtrack(assignment, csp)
#                     if result != failure:
#                         return result
#             remove {var=value} and inferences from assignment
#         return failure
        return None

def main():
    # m0: Washington, Oregon, Idaho, Nevada. Can we color them with 3 colors?
    m0 = MapColor("""WA: OR ID; 
                     OR: ID NV; 
                     ID: NV""" , ['R', 'G', 'B'])
    print(m0.solve_brute_force())
    print("Brute force assignments made: " + str(m0.bf_count))

    # m1: Washington, Oregon, Idaho, Montana, Nevada, California, Utah, Colorado, Wyoming, New Mexico and Arizona
    oldm1 = MapColor('''WA: OR ID;
                     OR: ID NV CA;
                     CA: NV AZ;
                     NV: UT AZ;
                     ID: NV MT UT CO;
                     UT: AZ CO WY;
                     CO: MT WY;
                     WY: NM;
                     NM: AZ''', 
                     ['R', 'G', 'B', 'Y'])

    m1 = MapColor('''WA: OR ID;
                     OR: ID NV CA;
                     CA: NV AZ;
                     NV: UT AZ;
                     ID: NV MT UT WY;
                     UT: AZ CO WY;
                     CO: NM WY;
                     WY: MT;
                     NM: AZ;
                     ND: MT SD;
                     SD: WY MT''', 
                     ['R', 'G', 'B', 'Y'])

    print(m1.solve_brute_force())
    print("Brute force assignments made: " + str(m1.bf_count))


if __name__ == '__main__':
    main()
