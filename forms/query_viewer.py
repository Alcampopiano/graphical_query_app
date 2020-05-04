from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class query_viewer(query_viewerTemplate):
  def __init__(self, title_label, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.tag.title_label=title_label
    
  def form_show(self, **event_args):
    
    title_label=self.tag.title_label
    self.label_1.text=title_label
    
    if title_label=='Saved Queries':
      items=anvil.server.call('pull_saved_queries')
      self.repeating_panel_1.items=items
      
    else:
      
      items=anvil.server.call('pull_saved_queries', 'examples')
      self.repeating_panel_1.items=items
       
      # make this better
      for c in self.repeating_panel_1.get_components():
        for x in c.get_components():
          if type(x) is Button and x.text=='delete':
            x.visible=False