# %% Import dataframes
import pandas as pd
buildings = pd.read_csv("buildings.csv") 
equipment = pd.read_csv("equipment.csv")
measurement_types = pd.read_csv("measurement_types.csv")
point_types = pd.read_csv("point_types.csv")
points = pd.read_csv("points.csv")
tags = pd.read_csv("tags.csv")

# %% Create the graph basics
import rdflib
from rdflib.namespace import NamespaceManager, XSD
from rdflib import Graph, RDF, URIRef, Literal, BNode
import brickschema
from brickschema.namespaces import A, BRICK

NS_om = "http://openmetrics.eu/openmetrics#"
NS_bot = "https://w3id.org/bot#"
NS_brick = "https://brickschema.org/schema/Brick#"
NS_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
NS_owl = "http://www.w3.org/2002/07/owl#"
NS_schema = "http://schema.org#"
NS_xsd = "http://www.w3.org/2001/XMLSchema#"
NS_unit = "http://qudt.org/vocab/unit#"

g = Graph()

g.namespace_manager.bind("om", URIRef(NS_om))
g.namespace_manager.bind("bot", URIRef(NS_bot))
g.namespace_manager.bind("brick", URIRef(NS_brick))
g.namespace_manager.bind("rdf", URIRef(NS_rdf))
g.namespace_manager.bind("owl", URIRef(NS_owl))
g.namespace_manager.bind("schema", URIRef(NS_schema))
g.namespace_manager.bind("xsd", URIRef(NS_xsd))
g.namespace_manager.bind("unit", URIRef(NS_unit))
     
# %% Extract metadata from buildings.csv 

for i in range(0,len(buildings)):
    # Create: inst_1234 a brick:building
    id = buildings['id'][i]
    inst_building = URIRef(NS_om + "Building_" + str(id))
    brick_building = URIRef(NS_brick + "Building")
    g.add((inst_building, RDF.type, brick_building))
    
    # Create: brick:building brick:area xsd:sq_ft    
    area = Literal(buildings['sq_ft'][i]) # passing a float
    brick_area = URIRef(NS_brick + "area") 
    brick_value = URIRef(NS_brick + "value")
    brick_hasUnit = URIRef(NS_brick + "hasUnit")
    unit = URIRef(NS_unit + "FT2")
    bn = BNode()
    g.add((inst_building, brick_area, bn))
    g.add((bn, brick_value, area))
    g.add((bn, brick_hasUnit, unit))

    # Create: buildings["info.customerType"] type of building use
    brick_primary_function = URIRef(NS_brick + "buildingPrimaryFunction")
    building_type = Literal(buildings["info.customerType"][i])
    g.add((inst_building, brick_primary_function, building_type))

    # Create: buildings["info.geoCity"] location of building
    brcik_location = URIRef(NS_brick+"hasLocation")
    building_geolocation = Literal(buildings["info.geoCity"][i])
    g.add((inst_building, brcik_location, building_geolocation ))


# %% Export metadata from equipment.csv

for i in range(0,len(equipment)):
    # Create equipment instances
    id = equipment["id"][i]
    building_id = equipment["building_id"][i]
    if equipment["equip_type_name"][i] == "Boiler":
        inst_boiler = URIRef(NS_om + "Boiler_"+str(id))
        brick_boiler = URIRef(NS_brick + "Boiler")

        # Create: inst_boiler_1213 a brick:boiler 
        g.add((inst_boiler, RDF.type, brick_boiler))
        inst_building = URIRef(NS_om + "Building_" + str(building_id))
        brick_hasLocation = URIRef(NS_brick + "hasLocation")  
        
        # Create the relationship between buildings and equipment      
        g.add((inst_boiler, brick_hasLocation, inst_building))
    
    elif equipment["equip_type_name"][i] == "Pump":
        inst_pump = URIRef(NS_om + "Pump_"+str(id))
        brick_pump = URIRef(NS_brick + "Pump")
    
        # Create: inst_boiler_1213 a brick:boiler 
        g.add((inst_boiler, RDF.type, brick_boiler))
        inst_building = URIRef(NS_om + "Building_" + str(building_id))
        brick_hasLocation = URIRef(NS_brick + "hasLocation")  
    
        # Create the relationship between buildings and equipment      
        g.add((inst_boiler, brick_hasLocation, inst_building))

# %% Serialise the graph
g.serialize(destination="rtem_graph.ttl", format="turtle")
