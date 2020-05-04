import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import io
  
name='eqao_and_report_card'

  
def get_df_with_cleaned_column_names(name):
  
  row=app_tables.data.get(name=name)
  df=pd.read_csv(io.BytesIO(row['media'].get_bytes()))
  df.columns=df.columns.str.strip().str.replace('[\\\/*\-+&$|]', '').str.replace('\s', '_')
  filter_column=row['filter_column']
  
  return df, filter_column
  
@anvil.server.callable('pull_df_meta')
def pull_df_meta():
  
  df, filter_column=get_df_with_cleaned_column_names(name)
  #df=get_filtered_df(df, filter_column)
  
  d={}
  for k, v in df.items():
      if df[k].dtype=='O':
         d[k]=list(df[k].dropna().unique())
      else:
         d[k]=None
          
  return d

@anvil.server.callable('get_query_results')
def get_query_results(q):
  
  df, filter_column=get_df_with_cleaned_column_names(name)
  #df=get_filtered_df(df, filter_column)
  df=df.query(q)
  num_records=str(len(df))
  df=df.to_csv()
  m=anvil.BlobMedia('text/csv', df, name='data_based_on_query.csv')
  
  if not num_records:
    num_records='0'

  return m, num_records
  
@anvil.server.callable('save_query')
def save_query(but_data, notes):
  
  email=anvil.users.get_user()['email']
  row=app_tables.saved_queries.add_row(user_id=email, but_data=but_data, notes=notes)

@anvil.server.callable('pull_saved_queries')   
def pull_saved_queries(examples=False):
  
  if examples:
    rows=app_tables.saved_queries.search(user_id='example')
    
  else:
    rows=app_tables.saved_queries.search(user_id=anvil.users.get_user()['email'])

  rows=[{'row_id': r.get_id(), 'notes': r['notes'], 'but_data': r['but_data']} for r in rows]
  

  return rows

@anvil.server.callable('delete_query')  
def delete_query(row_id):
  row=app_tables.saved_queries.get_by_id(row_id)
  row.delete()
  
  