from database.EVEDBParser import eve_db_getid_from_name, eve_db_name_from_typeid, EVE_DB

eve_db_get_output_per_run, eve_db_get_time_to_build_per_run, eve_db_get_produced_item_name_typeid

"""
Just a cheatsheet for what does what
"""

"""
industryActivity = time to make
industryActivityMaterials = Materials Required to make
industryActivityProbabilities = Invention Prob and Output Blueprint, Base Output Quantity 
industryActivityProducts = Output Quantity
industryActivitySkills = Related to skills required
industryBlueprints = Max Production Limit
invTypes = Type, GroupID and TypeName
planetSchematics = SchematicName, cycle time and id
planetSchematicsTypeMap = TypeID Quantity isInput(T/F)
"""


class Blueprint:

    def __init__(self, typeid : int = None, name : str= None, db : EVE_DB = None):
        """

        :param typeid:
        :param name:
        :param db: an eve online Database in sqlalchemy used as a singleton reference
        """
        if not typeid:
            self.typeid = eve_db_getid_from_name(name)
            self.name = name
        elif not name:
            self.name = eve_db_name_from_typeid(typeid)
            self.typeid = typeid
        elif not typeid and not name:
            raise SyntaxError('There must be a typeID or a name or both')
        else:
            self.name = name
            self.typeid = typeid


        if 'Blueprint' in self.name or 'Reaction' in self.name:
            self.output = EVE_DB.get_eve_run_output(self.typeid)
            self.time_to_build = EVE_DB.get_build_duration_per_run(self.typeid)
            self.produced_item_name, self.produced_item_typeid = EVE_DB.get_item_name_and_id(self.typeid)
            self.required_items_per_run : list[dict] = EVE_DB.get_requisite_items(self.typeid)

        else:
            print(f'Not a blueprint or reaction {self.name}')