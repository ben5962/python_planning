'''
Created on 31 août 2017

@author: Utilisateur
'''
# http://pyexcel-io.readthedocs.io/en/latest/sqlalchemy.html#read-data-from-a-database-table
import models

from pyexcel_io import get_data
#from pyexcel_io import save_data
from pyexcel_io.constants import DB_SQL, DEFAULT_SHEET_NAME
from pyexcel_io.database.common import SQLTableExporter, SQLTableExportAdapter


import pyexcel as p



def sauver_excel():

    # fonctionne pour table complete:   
    ##    p.save_as(session=models.session,
    ##              table=models.Documents,
    ##              dest_file_name="essai_export_excel.xls",
    ##              dest_sheet_name="destination")
    #todo : pb d encoding mais pour l instant on fera avec

    # table partielle :
    # errors: AttributeError: 'Query' object has no attribute 'is_clause_element'
    #q = models.session.query(models.Documents).filter(models.Documents.documents_id==1).all()
    # error : sqlalchemy.exc.InvalidRequestError: SQL expression, column, or mapped entity expected - got '[Documents(document_id = 1, date_document = 2013-03-01, titre_document = RIB, type_document = ml, origine =,debut_periode_couverte = None,fin_periode_couverte = None]' 
    #q = models.session.query(models.Documents).filter(models.Documents.documents_id==1)
    # NameError: name 'documents_id' is not defined
    # q = models.session.query(models.Documents).filter_by(documents_id == 1)
    # AttributeError: 'Query' object has no attribute 'is_clause_element'
    q = models.session.query(models.Documents).filter_by(documents_id = 1)
    #q = models.session.query(models.Documents).filter_by(documents_id = 1).all()
    #print(q)
    p.save_as(
        #session=models.session,
        dest_file_name="essai_export_excel.xls",
        dest_sheet_name="destination",
        column_names = ['documents_id'], 
        query_sets = q.all()
        )
    

    


    
if __name__ == '__main__':
    sauver_excel()
