#!/usr/bin/env python3

def edgelist(n,l):
    a=[]
    for i in range(len(l)):
        if n in l[i]:
            a.append(l[i])
    return a

import re
import itertools
import copy

ROLLNUM_REGEX = "2018417"

class Graph(object):
    name = "Udit Arora"
    email = "udit18417@iiitd.ac.in"
    roll_num = "2018417"

    def __init__ (self, vertices, edges):
        """
        Initializes object for the class Graph

        Args:
            vertices: List of integers specifying vertices in graph
            edges: List of 2-tuples specifying edges in graph
        """

        self.vertices = vertices
        
        ordered_edges = list(map(lambda x: (min(x), max(x)), edges))
        
        self.edges    = ordered_edges
        
        self.validate()

    def validate(self):
        """
        Validates if Graph if valid or not

        Raises:
            Exception if:
                - Name is empty or not a string
                - Email is empty or not a string
                - Roll Number is not in correct format
                - vertices contains duplicates
                - edges contain duplicates
                - any endpoint of an edge is not in vertices
        """

        if (not isinstance(self.name, str)) or self.name == "":
            raise Exception("Name can't be empty")

        if (not isinstance(self.email, str)) or self.email == "":
            raise Exception("Email can't be empty")

        if (not isinstance(self.roll_num, str)) or (not re.match(ROLLNUM_REGEX, self.roll_num)):
            raise Exception("Invalid roll number, roll number must be a string of form 201XXXX. Provided roll number: {}".format(self.roll_num))

        if not all([isinstance(node, int) for node in self.vertices]):
            raise Exception("All vertices should be integers")

        elif len(self.vertices) != len(set(self.vertices)):
            duplicate_vertices = set([node for node in self.vertices if self.vertices.count(node) > 1])

            raise Exception("Vertices contain duplicates.\nVertices: {}\nDuplicate vertices: {}".format(vertices, duplicate_vertices))

        edge_vertices = list(set(itertools.chain(*self.edges)))

        if not all([node in self.vertices for node in edge_vertices]):
            raise Exception("All endpoints of edges must belong in vertices")

        if len(self.edges) != len(set(self.edges)):
            duplicate_edges = set([edge for edge in self.edges if self.edges.count(edge) > 1])

            raise Exception("Edges contain duplicates.\nEdges: {}\nDuplicate vertices: {}".format(edges, duplicate_edges))

    def min_dist(self, start_node, end_node):
        '''
        Finds minimum distance between start_node and end_node

        Args:
            start_node: Vertex to find distance from
            end_node: Vertex to find distance to

        Returns:
            An integer denoting minimum distance between start_node
            and end_node
        '''
        s=start_node
        l=[s]
        d=[]
        for i in range(len(self.vertices)):
            d.append(0)
        d[s-1]=0
        done=[s]
        for i in range(len(self.vertices)):
            elist=edgelist(l[i],self.edges)
            for p in elist:
                for q in p:
                    if q!=l[i] and (q not in done):
                        l.append(q)
                        done.append(q)
                        d[q-1]=d[l[i]-1]+1
        return d[end_node-1]
        #raise NotImplementedError

    def all_shortest_paths(self, start_node, end_node):
        """
        Finds all shortest paths between start_node and end_node

        Args:
            start_node: Starting node for paths
            end_node: Destination node for paths

        Returns:
            A list of path, where each path is a list of integers.
        """
        s=start_node
        e=end_node
        dist=self.min_dist(s,e)
        en=[]
        for i in range(len(self.vertices)):
            en.append([])
            for j in self.edges:
                if i+1 in j:
                    if j[0]!=i+1:
                        en[i].append(j[0])
                    else:
                        en[i].append(j[1])
        k=[]

        for i in range(len(self.vertices)):
            k.append([])

        l=[s]
        d=[]
        for i in range(len(self.vertices)):
            d.append(0)
        d[s-1]=0
        done=[s]
        for i in range(len(self.vertices)):
            elist=edgelist(l[i],self.edges)
            for p in elist:
                for q in p:
                    if q!=l[i] and (q not in done):
                        l.append(q)
                        done.append(q)
                        d[q-1]=d[l[i]-1]+1
                    if q!=l[i] and (d[l[i]-1]<d[q-1]):
                        k[l[i]-1].append(q)
        paths=[]
        for i in range(len(k[s-1])):
            paths.append([s])
        for j in range(len(k[s-1])):
            paths[j].append(k[s-1][j])
        for i in range(1,dist):
            nop=len(paths)
            for j in range(nop):
                for l in range(len(k[paths[j][-1]-1])):
                    t=copy.deepcopy(paths[j])
                    t.append(k[paths[j][-1]-1][l])
                    paths.append(t)
            paths=paths[nop:]
        x=[]
        for i in paths:
            if i[-1]!=end_node:
                x.append(i)
        for i in x:
            paths.remove(i)
        return paths
        raise NotImplementedError

    def paths_having_node(self,start_node,end_node,node):
        c=0
        paths=self.all_shortest_paths(start_node,end_node)
        for i in paths:
            if node in i:
                c+=1
        return c        
        raise NotImplementedError

    def betweenness_centrality(self, node):
        """
        Find betweenness centrality of the given node

        Args:
            node: Node to find betweenness centrality of.

        Returns:
            Single floating point number, denoting betweenness centrality
            of the given node
        """
        t=0
        for i in range(len(self.vertices)):
            if self.vertices[i]!=node:
                for j in range(i+1,len(self.vertices)):
                    if self.vertices[j]!=node and self.paths_having_node(i+1,j+1,node)!=0:
                        t+=(self.paths_having_node(i+1,j+1,node)/len(self.all_shortest_paths(i+1,j+1)))
        return t*2/((len(self.vertices)-1)*(len(self.vertices)-2))
        raise NotImplementedError

    def top_k_betweenness_centrality(self):
        """
        Find top k nodes based on highest equal betweenness centrality.
        
        
        Returns:
            List a integer, denoting top k nodes based on betweenness
            centrality.
        """
        l=[]
        for i in self.vertices:
            l.append(self.betweenness_centrality(i))
        p=[]
        m=max(l)
        for i in range(len(l)):
            if l[i]==m:
                p.append(self.vertices[i])
        return p
        raise NotImplementedError

if __name__ == "__main__":
    vertices = [1, 2, 3, 4, 5, 6, 7, 8]
    edges    = [(1,2),(1,3),(2,3),(3,5),(3,4),(4,5),(4,6),(2,6),(5,6),(6,7),(7,8),(8,6),(5,8),(5,7)]
    vertices=sorted(vertices)
    graph = Graph(vertices, edges)
    print(graph.top_k_betweenness_centrality())
