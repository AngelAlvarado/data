import pandas as pd
import sys
import csv

def main():
    """
    Reads sanitized batch file into a datafrme
    The general idea is to use a graph and find the shortest path
    args ../paymo_input/batch_payment_cleaned.txt ../paymo_input/stream_payment.txt ../paymo_output/output1.txt ../paymo_output/output2.txt ../paymo_output/output3.txt
    """
    feature_one = open(sys.argv[3], 'w')
    feature_two = open(sys.argv[4], 'w')
    feature_three = open(sys.argv[5], 'w')
    # Reads initial file
    datafrme = pd.read_csv(sys.argv[1], sep=',',
                            header=0, skipinitialspace=True, error_bad_lines=False)
    # @todo do not calculate 2nd, 3rd and 4th-degree friends using a for loop. It won't work.
    new_payments_file = open(sys.argv[2], 'rt')
    # Analyze relationships of incoming payments against data in the system.
    try:
        reader = csv.reader(new_payments_file)
        next(reader, None)
        for payment in reader:
            index_user_who_pays = int(payment[1].replace(" ", ""))
            index_user_who_receives = int(payment[2].replace(" ", ""))
            try:
                is_friend = build_network(index_user_who_pays, index_user_who_receives, datafrme)
                if is_friend is True:
                    feature_one.write('trusted\n')
                    feature_two.write('trusted\n')
                    feature_three.write('trusted\n')
                else:
                    feature_one.write('unverified\n')
                    feature_two.write('unverified\n')
                    feature_three.write('unverified\n')
            except KeyError:
                print("error")
    finally:
        new_payments_file.close()


def build_network(index_user_who_pays,index_user_who_receives,datafrme):
    """Return True or False whether the user has a relationship at nth-degree or not"""
    grafo = Graph()
    user_who_pays_vertex = Vertex(index_user_who_pays)
    user_who_receives_vertex = Vertex(index_user_who_receives)
    is_relationship_via_network = False
    is_relationship_via_batch = False

    if int(datafrme[datafrme.id1 == index_user_who_pays].size) is not 0:
        for index, row in datafrme[datafrme.id1 == index_user_who_pays].drop_duplicates('id2')['id2'].iteritems():
            grafo.add_relationship(user_who_pays_vertex, Vertex(row))
        if int(datafrme[datafrme.id1 == index_user_who_receives][datafrme.id2 == index_user_who_pays].size) is not 0:
            is_relationship_via_batch = True
            # this means there is a relationship and prolly I should just return it.
            grafo.add_relationship(user_who_pays_vertex, Vertex(index_user_who_receives)) # just to test tree.
        return grafo.build_path(user_who_pays_vertex, user_who_receives_vertex)
    if is_relationship_via_batch is False:
        if int(datafrme[datafrme.id1 == index_user_who_receives][datafrme.id2 == index_user_who_pays].size) is not 0:
            # this means there is a relationship and prolly I should just return it.
            grafo.add_relationship(user_who_pays_vertex, Vertex(index_user_who_receives))  # just to test tree.
            return grafo.build_path(user_who_pays_vertex, user_who_receives_vertex)
    else:
        # Maybe relationship should be added to the original dataframe. So new payments takes it into consideartion.
        grafo.add_relationship(user_who_pays_vertex, user_who_pays_vertex)
        return False

class Vertex(object):
    """Create a vertex per each user"""
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Mark all nodes unvisited by default.
        self.visited = False
        # Predecessor
        self.previous = None

    def get_connections(self):
        return self.adjacent

    def get_id(self):
        return self.id

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self, status):
        self.visited = status

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class Graph(object):
    """Holds network based on the incoming payment info"""
    def __init__(self):
        self.relationships = {}

    def __str__(self):
        return str(self.relationships)

    def add(self, element):
        self.relationships.update({element.get_id(): Vertex(element)})

    def unilateral_relationship(self, origin, destination):
        origin.adjacent.update({destination.get_id(): destination})

    def add_relationship(self, element, second_element):
        """Make relationship unidirectional"""
        self.unilateral_relationship(element, second_element)
        self.unilateral_relationship(second_element, element)

    def build_path(self, origin, destination):
        """For now it takes care of feature 1"""
        origin.set_visited(True)
        has_relationship = False
        for neighbor in origin.adjacent:
            if origin.adjacent[neighbor].visited is False:
                if origin.adjacent[neighbor].get_id() == destination.get_id():
                    has_relationship = True
                    return has_relationship
        return has_relationship

if __name__ == '__main__':
    main()

