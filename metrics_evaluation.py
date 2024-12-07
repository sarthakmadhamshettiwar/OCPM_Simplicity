import ocpa
import pm4py
from statistics import mean
from ocpa.objects.log.importer.ocel import factory as ocel_import_factory
from ocpa.algo.discovery.ocpn import algorithm as ocpn_discovery_factory
from ocpa.visualization.oc_petri_net import factory as ocpn_vis_factory
from ocpa.objects.log.importer.ocel import factory as ocel_import_factory
from ocpa.algo.conformance.precision_and_fitness import evaluator as quality_measure_factory
from ocpa.objects.log.ocel import OCEL
# from pm4py.objects.petri.importer import factory as pnml_import_factory

class ocel_metrics_calculation:
    def __init__(self, filename):
        self.path = filename
        self.ocel_log = ocel_import_factory.apply(filename)
        self.ocpn = ocpn_discovery_factory.apply(self.ocel_log)  # Discover Petri net
        self.object_types = list(self.ocel_log.object_types)  # Extract object types
        # self.ocel_= pm4py.read_ocel(filename)
        self.precision = None
        self.fitness = None

    def discover_petrinet(self):
        self.ocpn = ocpn_discovery_factory(self.ocel_log)
        self.precision, self.fitness = quality_measure_factory.apply(self.ocel_log, self.ocpn)
        # saving the image
        ocpn_vis_factory.save(ocpn_vis_factory.apply(self.ocpn), self.path+"_petrinet.png") # saving the image of petrinet
        return self.ocpn
   
    def calculate_ocel_simplicity(self, ocpn=None, object_types=None, k=1.5):
        """
        Calculate the simplicity of an object-centric Petri net (OCPN).
        Parameters:
        -----------
        ocpn : ObjectCentricPetriNet
            The object-centric Petri net discovered from OCEL.
        object_types : List[str]
            The list of object types in the OCEL.
        k : float
            Baseline complexity constant. Default is 2.0.

        Returns:
        --------
        overall_simplicity : float
            The simplicity of the object-centric Petri net.
        """

        if ocpn is None:
            ocpn = self.ocpn

        if object_types is None:
            object_types = self.object_types

        arc_degrees_by_type = {obj_type: [] for obj_type in object_types}

        # Analyze places
        for place in ocpn.places:
            # Infer the object type from the place name (assuming convention-based naming)
            for obj_type in object_types:
                if obj_type in place.name:
                    in_degree = len(place.in_arcs)
                    out_degree = len(place.out_arcs)
                    arc_degrees_by_type[obj_type].append(in_degree + out_degree)

        # Analyze transitions
        for transition in ocpn.transitions:
            # Infer the object type from the transition name (assuming convention-based naming)
            for obj_type in object_types:
                if obj_type in transition.name:
                    in_degree = len(transition.in_arcs)
                    out_degree = len(transition.out_arcs)
                    arc_degrees_by_type[obj_type].append(in_degree + out_degree)


        # Compute mean arc degree for each object type
        mean_degrees_by_type = {
            obj_type: mean(arc_degrees) if arc_degrees else 0.0
            for obj_type, arc_degrees in arc_degrees_by_type.items()
        }


        # Compute simplicity for each object type
        simplicity_by_type = {
            obj_type: 1.0 / (1.0 + max(mean_degree - k, 0))
            for obj_type, mean_degree in mean_degrees_by_type.items()
        }

        # Calculate overall simplicity as the average simplicity across all object types
        overall_simplicity = mean(simplicity_by_type.values())
        return overall_simplicity
   

    def calculate_ocel_fitness(self):
        if self.fitness is None:
            self.discover_petrinet()
       
        return self.fitness


    def calculate_ocel_precision(self):
        if self.precision is None:
            self.discover_petrinet
        return self.precision