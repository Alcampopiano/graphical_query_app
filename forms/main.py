from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from query_viewer import query_viewer

class main(mainTemplate):
  def __init__(self, previous_qry=None, **properties):
    
    self.init_components(**properties)
    
#     while not anvil.users.login_with_form():
#       pass
    
    #print(previous_qry)
    self.tag.previous_qry_comps=previous_qry
    self.saved_q.tag='saved_queries'
    self.example_q.tag='example_queries'


    self.tag.logical_map=mapping = {'and': '&', 
                                    'or': '|', 
                                    'equal to': '==', 
                                    'not equal to': '!=',
                                    'less than': '<',
                                    'greater than': '>',
                                    'less than or equal to': '<=',
                                    'greater than or equal to': '>='
                                   }
    
    self.drop_down_col.tag.color='#ff7f0e'
    self.drop_down_comp.tag.color='#1f77b4'
    self.drop_down_con.tag.color='#2ca02c'
    self.drop_down_sep.tag.color='#d62728'
    self.drop_down_val.tag.color='#9467bd'
    
    self.drop_down_col.tag.name='column'
    self.drop_down_comp.tag.name='comparison'
    self.drop_down_con.tag.name='connector'
    self.drop_down_sep.tag.name='separator'
    self.drop_down_val.tag.name='value'
    
    self.dataset_load()
    
    
  def form_show(self, **event_args):
    
    if self.tag.previous_qry_comps:
      for b in self.tag.previous_qry_comps:
        b.set_event_handler('click', self.remove_but)
        b.remove_from_parent()
        self.flow_panel_1.add_component(b)
    
    
  def dataset_load(self, **event_args):

      df_meta=anvil.server.call('pull_df_meta')
      cols=df_meta.keys()
      cols=sorted(cols)
      self.tag.values=df_meta
      self.drop_down_col.items=[''] + cols
      self.flow_panel_1.clear()
  

  def drop_down_change(self, **event_args):
    
    drop_comp=event_args['sender']
    
    if drop_comp.selected_value is not '':
      
      self.make_button(drop_comp)
        
      if drop_comp.tag.name=='column' and self.tag.values[drop_comp.selected_value]:
        self.drop_down_val.enabled=True
        self.text_box_1.enabled=False
        items=self.tag.values[drop_comp.selected_value]
        items=[(x,'"{x}"'.format(x=x)) for x in items]
        self.drop_down_val.items=[''] + items
        
      elif drop_comp.tag.name=='column' and not self.tag.values[drop_comp.selected_value]:
        self.text_box_1.enabled=True
        self.drop_down_val.enabled=False
        
      drop_comp.selected_value=''    
      

  def make_button(self, drop_comp):
    
      b=Button(text=drop_comp.selected_value.strip('"'), 
          background=drop_comp.tag.color,
          foreground='white')
      
      if drop_comp.tag.name=='comparison' or drop_comp.tag.name=='connector':
        
        logical_map=self.tag.logical_map
        currently_selected=drop_comp.selected_value
        b.tag.query_frag = logical_map[currently_selected]

      else:
        b.tag.query_frag=drop_comp.selected_value
        
      b.set_event_handler('click', self.remove_but)
      self.flow_panel_1.add_component(b)
     

  def run_query_button_click(self, **event_args):
    
    q=' '.join([c.tag.query_frag for c in self.flow_panel_1.get_components()])
    m, num_records=anvil.server.call('get_query_results', q)
    self.label_num_records.text="Number of records returned from query: " + \
      num_records
      
    download(m)
    Notification('', title="Your data have been downloaded to your computer").show()
    
    
  def save_query_button_click(self, **event_args):
    
    t = TextArea()
    c=confirm(content=t, title="Before saving, please add a note to clearly describe this query",
              buttons=[('save', 'save'), ("cancel", 'cancel')])
    
    if c=='save':
    
      but_text=[c.text for c in self.flow_panel_1.get_components()]
      query_frags=[c.tag.query_frag for c in self.flow_panel_1.get_components()]
      but_color=[c.background for c in self.flow_panel_1.get_components()]
      
      but_data={'but_text': [c.text for c in self.flow_panel_1.get_components()],
      'query_frags': [c.tag.query_frag for c in self.flow_panel_1.get_components()],
      'but_color': [c.background for c in self.flow_panel_1.get_components()]
      }
      
      anvil.server.call('save_query', but_data, t.text)
      Notification('You can access your saved queries in the side panel', 
                  title='Your query has been saved').show()
    

  def text_box_1_pressed_enter(self, **event_args):
    
    if self.text_box_1.text or self.text_box_1.text==0:
      
      b=Button(text=self.text_box_1.text, 
        background=self.drop_down_val.tag.color,
        foreground='white')
      
      b.tag.query_frag=str(self.text_box_1.text)
      b.set_event_handler('click', self.remove_but)
      self.flow_panel_1.add_component(b)
      self.text_box_1.text=None
      
      
  def query_viewer_click(self, **event_args):
    
    if event_args['sender'].tag=='saved_queries':
      form=query_viewer(title_label='Saved Queries')
      
    else:
      form=query_viewer(title_label='Example Queries')

    self.content_panel.clear()
    self.content_panel.add_component(form)
  
      
  def remove_but(self, **event_args):
    event_args['sender'].remove_from_parent()

  def dataset_desc_click(self, **event_args):
     Notification('', title='coming soon!').show()
      
  def tutorial_link_click(self, **event_args):
    Notification('', title='coming soon!').show()
    
  def home_link(self, **event_args):
    open_form('main')

  def file_loader_1_change(self, file, **event_args):
    anvil.server.call('file_upload', file)

