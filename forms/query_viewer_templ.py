from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class query_viewer_templ(query_viewer_templTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    but_data=self.item['but_data']
    
    for text, color, qry in zip(but_data['but_text'], 
                                but_data['but_color'], 
                                but_data['query_frags']):
      
      b=Button(text=text, 
          background=color,
          foreground='white')
      
      b.tag.query_frag=qry
      self.flow_panel_1.add_component(b)
      
      
  def delete_click(self, **event_args):
    anvil.server.call('delete_query', self.tag)
    self.remove_from_parent()

  def reuse_click(self, **event_args):
    previous_qry_comps=self.flow_panel_1.get_components()
    open_form('main', previous_qry=previous_qry_comps)


