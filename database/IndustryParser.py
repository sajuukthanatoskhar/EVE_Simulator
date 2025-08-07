from database.EVEDBParser import EVE_DB

#eve_db_get_output_per_run, eve_db_get_time_to_build_per_run, eve_db_get_produced_item_name_typeid

"""
Just a cheatsheet for what does what
"""

"""
industryActivity = time to make
industryActivityMaterials = Materials Required to make
    typeID, activityID, materialTypeID, quantity
industryActivityProbabilities = Invention Prob and Output Blueprint, Base Output Quantity 
    typeID, activityID, productTypeID, probability

industryActivityProducts = Output Quantity
    typeID, activityID, productTypeID, quantity

industryActivitySkills = Related to skills required
industryBlueprints = Max Production Limit
    typeID, maxProductionLimit
    
invTypes = Type, GroupID and TypeName
planetSchematics = SchematicName, cycle time and id
    schematicID, schematicName, cycleTime
planetSchematicsTypeMap = TypeID Quantity isInput(T/F)
    schematicID, typeID,quantity,isInput
"""


class Blueprint:

    def __init__(self, typeid : int = None, name : str= None, db : EVE_DB  = None):
        """

        :param typeid:
        :param name:
        :param db: an eve online Database in sqlalchemy used as a singleton reference
        """
        if not typeid:
            self.typeid = db.get_getid_from_name(name)
            self.name = name
        elif not name:
            self.name = db.get_name_from_typeid(typeid)
            self.typeid = typeid
        elif not typeid and not name:
            raise SyntaxError('There must be a typeID or a name or both')
        else:
            self.name = name
            self.typeid = typeid


        if 'Blueprint' in self.name or 'Reaction' in self.name:
            self.output = db.get_eve_run_output(self.typeid)
            self.time_to_build = db.get_build_duration_per_run(self.typeid)
            self.produced_item_name, self.produced_item_typeid = db.get_item_name_and_id(self.typeid)
            self.required_items_per_run : list[dict] = db.get_requisite_items(self.typeid)

        else:
            print(f'Not a blueprint or reaction {self.name}')