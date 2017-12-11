      
class CityTrack(object)


    def __init__(self,city_name)


        self._map = CarlaMap(city_name)

        self._astar = AStar()

        # Refers to the start position of the previous route computation
        self._previous_node = []
 
   




    def project_node(self,node,node_orientation):
        """
            Projecting the graph node into the city road
        """

        # To change the orientation with respect to the map standards
        node_orientation = np.array([node_orientation[0],
                            node_orientation[1],node_orientation[2]])
        node_orientation = source_ori.dot(self.worldrotation)

        node  =   tuple([ int(x) for x in node ])

        # Set to zero if it is less than zero.


        node =(max(0,node[0]),max(0,node[1]))
        node =(min(self._map.get_graph_resolution()[0]-1,node[0]),
               min(self._map.get_graph_resolution()[1]-1,node[1]))
        # is it x or y ? Check to avoid  special corner cases


        if math.fabs(node_orientation[0]) > math.fabs(node_orientation[1]):
            node_orientation = (source_ori[0],0.0,0.0)
        else:
            node_orientation = (0.0,source_ori[1],0.0)

        node = self.map.grid_search(node[0],node[1])


        return node

    def is_at_goal(self,source,target):
        return source == target

    def is_at_new_node(self,current_node):
        return current_node != self._previous_node


    def is_away_from_intersection(self,current_node):
        return self._closest_intersection_position(current_node) > 1

    def is_far_away_from_route_intersection(self,current_node):
        # CHECK FOR THE EMPTY CASE
        return self._closest_intersection_route_position(current_node,
                       self._previous_route) > 4



    def compute_route(self,node_source,source_ori,node_target,target_ori):


        self._previous_node = node_source


        a_star =AStar()
        a_star.init_grid(node_source,self._map.get_graph_resolution()[0],
            self._map.get_graph_resolution()[1],
            self._map.get_walls_directed(node_target,target_ori,node_source),
            node_target)


        route = a_star.solve()



        #print route # JuSt a Corner Case 
        # REALLY, I want to remove this
        if route == None:
            a_star =AStar()
            a_star.init_grid(node_source,self._map.get_graph_resolution()[0],
            self._map.get_graph_resolution()[1],self._map.get_walls(), node_target)

            route = a_star.solve()

            

        return route




    def _closest_intersection_position(self, current_node):

        distance_vector = []
        for node_iterator in self._map._graph.intersection_nodes():

            distance_vector.append(sldist(node_iterator, current_node))

        return sorted(distance_vector)[0]

    def _closest_intersection_route_position(self, current_node):

        distance_vector = []
        for node_iterator in self._map._graph.intersection_nodes():

            distance_vector.append(sldist(node_iterator, current_node))

        return sorted(distance_vector)[0]



