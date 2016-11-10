import sys
import csv


def main():
    """
    Reads a sanitized batch file
    The general idea is to use a graph and find the shortest path
    args ../paymo_input/batch_payment_cleaned.txt ../paymo_input/stream_payment.txt ../paymo_output/output1.txt ../paymo_output/output2.txt ../paymo_output/output3.txt
    """
    feature_one = open(sys.argv[3], 'w')
    feature_two = open(sys.argv[4], 'w')
    feature_three = open(sys.argv[5], 'w')
    network_data = open(sys.argv[1], 'rt')
    network_data_reader = csv.reader(network_data)
    next(network_data_reader, None)
    new_payments_file = open(sys.argv[2], 'rt')
    # Analyze relationships of incoming payments against data in the system.
    try:
        grafo = build_network(network_data_reader)
        reader = csv.reader(new_payments_file)
        next(reader, None)
        for payment in reader:
            index_user_who_pays = str(payment[1].replace(" ", ""))
            index_user_who_receives = str(payment[2].replace(" ", ""))
            is_friend = grafo.build_path(index_user_who_pays, index_user_who_receives, 1)
            if is_friend is True:
                feature_one.write('trusted\n')
            else:
                feature_one.write('unverified\n')

            is_friend = grafo.build_path(index_user_who_pays, index_user_who_receives, 2)
            if is_friend is True:
                feature_two.write('trusted\n')
            else:
                feature_two.write('unverified\n')

            is_friend = grafo.build_path(index_user_who_pays, index_user_who_receives, 3)
            if is_friend is True:
                feature_three.write('trusted\n')
            else:
                feature_three.write('unverified\n')

    finally:
        new_payments_file.close()


def build_network(network_data):
    """Return True or False whether the user has a relationship at nth-degree or not"""
    grafo = Graph()
    for row in network_data:
        who_pays = row[0]
        who_rec = row[1]
        grafo.add(who_pays)
        grafo.add(who_rec)
        grafo.add_relationship(grafo.relationships[who_pays], grafo.relationships[who_rec])
    return grafo


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


class Graph(object):
    """Holds network based on the incoming payment info"""

    def __init__(self):
        self.relationships = {}

    def __str__(self):
        return str(self.relationships)

    def add(self, element):
        # New relationship.
        if element not in self.relationships:
            self.relationships.update({element: Vertex(element)})

    def unilateral_relationship(self, origin, destination):
        # Relationship in both sides.
        origin.adjacent.update({destination.get_id(): destination})

    def add_relationship(self, element, second_element):
        # Make relationship unidirectional.
        self.unilateral_relationship(element, second_element)
        self.unilateral_relationship(second_element, element)

    def build_path(self, origin_index, destination_index, max_deph=4, neighbors={}, visited=[], current_level=0):
        # if what we are looking for is not in the network then return.
        if self.relationships.__contains__(origin_index) is False or self.relationships.__contains__(destination_index) is False:
            return False
        # track origin based on its id
        origin = self.relationships[origin_index]
        # track destination based on its id
        destination = self.relationships[destination_index]
        # this could be the very first item in the network/path; Next time it will have relationships/neighbors
        if len(neighbors) == 0:
            # Starts populating origin's neighbors at this level.
            neighbors.update({current_level: origin.adjacent})
            # Keeps track of this visited node
            visited.append(origin.get_id())
            # Analyze once again but with new relationship
            self.build_path(origin_index, destination_index, max_deph, neighbors, visited, current_level)

        # Check if destination lives in the current relationships/neighbors. If so, we found a valid relationship
        if destination.get_id() in neighbors[current_level]:
            #print("it has relationship")
            return True

        # If max depth is reach just return; probably False.
        if current_level == max_deph:
            #print("not relationship so far")
            return False

        # Keep track of new neighbors at this level for the node being analyzed.
        new_neighbors = {}
        # Iterate current list of neighbors.
        for this_neighbor in neighbors[current_level]:
            # Iterate list of neighbors/nodes of the current neighbor being analyzed.
            for its_neighbor in neighbors[current_level][this_neighbor].adjacent:
                # Verify that the node hasn't been visited and it's not actually part of the nodes/neighbors already visited.
                if its_neighbor not in neighbors[current_level] and its_neighbor not in visited:
                    # If not visited and analyzed before then add parent neighbor to this node/neighbor
                    neighbors[current_level][this_neighbor].adjacent[its_neighbor].set_previous(
                        neighbors[current_level][this_neighbor])
                    # Update the new list of neighbors at this level of the new neighbors(nodes)
                    new_neighbors.update({neighbors[current_level][this_neighbor].adjacent[its_neighbor].get_id():
                                              neighbors[current_level][this_neighbor].adjacent[its_neighbor]})
                    # Keep track of this analyzed neighbor
                    visited.append(this_neighbor)
        # Next level
        current_level += 1
        # Keep track of new neighbors at this level for
        neighbors.update({current_level: new_neighbors})
        # Analyze once again with new relationships, new level, upated list of visited nodes.
        self.build_path(origin_index, destination_index, max_deph, neighbors, visited, current_level)


if __name__ == '__main__':
    main()