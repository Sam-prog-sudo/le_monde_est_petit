import program.world as script
import pytest

def setup_function(function):
    """ setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    """
    print("before: ", function)

def teardown_function(function):
    """ teardown any state that was previously setup with a setup_function
    call.
    """
    print("after:", function)

##########################
######## - Agent :########
##########################

class TestAgent:
    def setup_method(self):
        self.agent = script.Agent(3)

    # - Agent : 
    #   - modifier un attribut position
    def test_set_position(self):
        self.agent.position = 5
        assert self.agent.position == 5

    #   - récupérer un attribut position
    def test_get_position(self):
        assert self.agent.position == 3

    #   - assigner un dictionnaire en tant qu'attributs
    def test_set_agent_attributes(self):
        agent = script.Agent(3, agreeableness=-1)
        assert agent.agreeableness == -1
    
#############################
######## - Position :########
#############################
class TestPosition:
    def setup_method(self):
        self.position = script.Position(100, 33)
        
    #   - modifier un attribut longitude_degrees
    def test_longitude_degrees(self):
        self.position.longitude_degrees = 50
        assert self.position.longitude_degrees == 50

    #   - modifier un attribut latitude_degrees
    def test_latitude_degrees(self):
        self.position.latitude_degrees = 22
        assert self.position.latitude_degrees == 22

    #   - modifier un attribut longitude_degrees avec une valeur supérieure à 180 renvoie une erreur. 
    def test_longitude_degrees_range(self):
        with pytest.raises(AssertionError):
            script.Position(200, 33)

    #   - modifier un attribut latitude_degrees avec une valeur supérieure à 90 renvoie une erreur. 
    def test_latitude_degrees_range(self):
        with pytest.raises(AssertionError):
            script.Position(100, 100)

    #   - récupérer une latitude
    def test_latitude(self):
        assert self.position.latitude == 0.5759586531581288

    #   - récupérer une longitude
    def test_longitude(self):
        assert self.position.longitude == 1.7453292519943295
    
#########################
######## - Zone :########
#########################

class TestZone:
    
    def setup_method(self):
        self.position1 = script.Position(100, 33)
        self.position2 = script.Position(101, 34)  
        self.zone = script.Zone(self.position1, self.position2)
        script.Zone._initialize_zones()
        agent = script.Agent(self.position1, agreeableness=1)
        self.zone.inhabitants = [agent]


    def teardown_method(self):
        script.Zone.ZONES = []

#   - récupérer toutes les instances Zone (Zone.ZONES)
# On devrait avoir exactement 64800 zones
    def test_get_zones(self):
        assert len(script.Zone.ZONES) == 64800


#   - trouver une zone qui contient une position
    def test_find_zone_that_contains(self):
        found_zone = script.Zone.find_zone_that_contains(self.position1)
        assert found_zone.contains(self.position1)

#   - ajouter un habitant dans une zone
    def test_add_inhabitant_in_zone(self):
        agent = script.Agent(self.position1, agreeableness=1)
        self.zone.add_inhabitant(agent)
        assert len(self.zone.inhabitants) == 2


#   - récupérer la densité de population d'une zone
    def test_get_population_density(self):
        assert self.zone.population_density() == 8.087793508722422e-05

#   - récupérer l'agréabilité moyenne d'une zone
    def test_get_average_agreeableness(self):
        assert self.zone.average_agreeableness() == 1

#######################################
######## - AgreeablenessGraph :########
#######################################

# setup_module(module): fonction appelée lors de l'import d'un module.

# setup_class(cls): fonction appelée lors de la création de la classe.

# setup_method(self, method): fonction appelée lors du lancement d'un test unitaire faisant partie d'une classe.

# setup_function(function): fonction appelée lors du lancement d'un test unitaire.


class TestAgreeablenessGraph:
    
    def setup_method(cls):
        # créer toutes les zones
        script.Zone._initialize_zones()
        # créer les variables de classe
        cls.zone = script.Zone.ZONES[0]
        cls.graph = script.AgreeablenessGraph()
        cls.zones = script.Zone.ZONES
        # ajouter 10 habitants
        for _ in range(0,10):
            cls.zone.add_inhabitant(script.Agent(script.Position(-180, -89), agreeableness=1))
    
    def teardown_method(self):
        script.Zone.ZONES = []
            
#   - récupérer un titre
    def test_title(self):
        assert self.graph.title == 'Nice people live in the countryside'

#   - récupérer x_label
    def test_x_label(self):
        assert self.graph.x_label == 'population density'

#   - récupérer y_label
    def test_y_label(self):
        assert self.graph.y_label == 'agreeableness'

#   - récupérer xy_values sous forme de tuples
    def test_xy_values(self):
        assert len(self.graph.xy_values(self.zones)) == 2

#   - la première valeur de xy_values est la densité de population moyenne pour la première zone
    def test_average_population_density(self):
        assert self.graph.xy_values(self.zones)[0][0] == self.zone.population_density()

#   - la seconde valeur de xy_values est l'agréabilité moyenne
    def test_average_agreeableness(self):
        assert self.graph.xy_values(self.zones)[1][0] == self.zone.average_agreeableness()

################################
######## - IncomeGraph :########
################################

class TestIncomeGraph:
    
    def setup_method(self):
        script.Zone._initialize_zones()
        self.zone = script.Zone.ZONES[0]
        self.graph = script.IncomeGraph()
        self.zones = script.Zone.ZONES
        for _ in range(0, 10):
            self.zone.add_inhabitant(script.Agent(script.Position(-180, -89), income=40, age=20))

    def setup_teardown(self):
        script.Zone.ZONES = []
        
#   - récupérer un titre
    def test_title(self):
        assert self.graph.title == 'Older people have more money'

#   - récupérer x_label
    def test_x_label(self):
        assert self.graph.x_label == 'age'

#   - récupérer y_label
    def test_y_label(self):
        assert self.graph.y_label == 'income'

#   - récupérer xy_values sous forme de tuples
    def test_xy_values(self):
        assert len(self.graph.xy_values(self.zones)) == 2
        
#   - la première valeur de xy_values est l'âge
    def test_age(self):
        assert self.graph.xy_values(self.zones)[0][20] == 20

#   - la seconde valeur de xy_values est le revenu
    def test_average_income_by_age(self):
        assert self.graph.xy_values(self.zones)[1][20] == 40

#############################################
########### AGREEABLENESS PER AGE ###########
#############################################

class TestAgreeablenessPerAgeGraph:
    
    def setup_method(self):
        script.Zone._initialize_zones()
        self.zone = script.Zone.ZONES[0]
        self.graph = script.AgreeablenessPerAgeGraph()
        self.zones = script.Zone.ZONES
        for _ in range(0, 10):
            self.zone.add_inhabitant(script.Agent(script.Position(-180, -89), agreeableness=1, age=50))

    def test_title(self):
        assert self.graph.title == 'Nice People are young'
    
    def test_x_label(self):
        assert self.graph.x_label == 'age'
    
    def test_y_label(self):
            assert self.graph.y_label == 'agreeableness'

    def test_xy_values(self):
        assert len(self.graph.xy_values(self.zones)) == 2

    def test_age(self):
        assert self.graph.xy_values(self.zones)[0][50] == 50

    def test_average_agreeableness_by_age(self):
        assert self.graph.xy_values(self.zones)[1][50] == 1