import sqlite3
from typing import Tuple

import sqlalchemy
import sqlalchemy as sa
import pandas as pd
from sqlalchemy import create_engine, column, table, select

from sqlalchemy.orm import sessionmaker, declarative_base, Session


# # Create engine
# engine = create_engine('sqlite:///eve.db')
#
# # Create a base class for your models
# Base = declarative_base()
#
# # If you have existing tables, you can reflect them
# Base.metadata.reflect(bind=engine)
#
# # Create session factory
# Session = sessionmaker(bind=engine)
#
# # Example usage
# session = Session()
#
# #print(tables)
# session.close()


class EVE_DB:
    "'sqlite:///eve.db'"
    def __init__(self, locationURI: str = 'sqlite:///eve.db'):
        self.engine = create_engine(locationURI)
        # Create a base class for your models
        self.Base = declarative_base()

        # If you have existing tables, you can reflect them
        self.Base.metadata.reflect(bind=self.engine)
        self.metadata : sa.MetaData = self.Base.metadata
    def __enter__(self):

        self.session : Session = sessionmaker(bind=self.engine)()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    """
    
    industryActivityMaterials = Materials Required to make
    industryActivityProbabilities = Invention Prob and Output Blueprint, Base Output Quantity 
    industryActivityProducts = Output Quantity
    industryActivitySkills = Related to skills required
    industryBlueprints = Max Production Limit
    invTypes = Type, GroupID and TypeName
    planetSchematics = SchematicName, cycle time and id
    planetSchematicsTypeMap = TypeID Quantity isInput(T/F)
    """
    def get_getid_from_name(self, name : str) -> int:
        typeid = None
        invtypes_table = self.get_table('invTypes')
        stmt = invtypes_table.select().where(invtypes_table.c.typeName == name) # getattr(invtypes_table.c, 'typeName')
        data = pd.DataFrame(self.session.execute(stmt).fetchall())
        data.columns = self.get_table_keys(invtypes_table)
        typeid = data.loc[data['typeName'] == name, 'typeID'].item()
        return typeid

    def get_name_from_typeid(self, typeid : int) -> str:

        """
        Gets the name of the item based off of its typeID
        :param typeid:
        :return:
        """

        if isinstance(typeid, str):
            pass
        else:
            typeid = int(typeid)

        tablename = 'invTypes'

        returned_table = self.get_table(tablename)
        stmt = returned_table.select().where(returned_table.c.typeID == typeid) # getattr(invtypes_table.c, 'typeName')
        data = pd.DataFrame(self.session.execute(stmt).fetchall())
        data.columns = self.get_table_keys(returned_table)

        return data.loc[data['typeID'] == int(typeid), 'typeName'].item()


    def get_table(self, tablename : str) -> sa.Table:
        return sa.Table(tablename, self.metadata, autoload=True, autoload_with=self.engine)

    def get_table_keys(self, a_table : sa.Table) -> list[str]:
        return a_table.columns.keys()




    def get_eve_run_output(self, typeid) -> int:
        pass

    def get_build_duration_per_run(self, typeid : int) -> int:
        """
        industryActivity = time to make
        :param typeid:
        :return:
        """
        pass

    def get_item_name_and_id(self, typeid) -> Tuple[str, int]:
        return name,typeid

    def get_requisite_items(self, typeid) -> list[dict]:
        pass



if __name__ == '__main__':

    with EVE_DB() as a_db:
        sabre_typeid = a_db.get_getid_from_name('Sabre')
        print(a_db.get_getid_from_name('Sabre')) # Should be 22456 # TODO: Write Test
        print(a_db.get_name_from_typeid(22456)) # Should be Sabre # TODO: Write Test
        print(a_db.get_eve_run_output(sabre_typeid)) # Should be 1
        print(a_db.get_requisite_items(sabre_typeid)) # Should be a list of keys/values
