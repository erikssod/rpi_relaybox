#!/usr/bin/env python

import remi.gui as gui
from remi import start, App

class MyApp(App):
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self):
        container = gui.Container(width=540,
                                  margin='0px auto',
                                  style={'display':'block','overflow':'hidden'})
        
        self.lbl = gui.Label('This is a Label', width=200, height=30, margin='10px')

        self.slider = gui.Slider(10,0,100,5, width=200, height=30, margin='10px') 
        self.slider.onchange.do(self.slider_changed)

        container.append([self.lbl,self.slider])

        return container

    def dialog_confirm(self, widget):
        result = self.dialog.get_field('dslider').get_value()
        self.slider.set_value(result)

    def slider_changed(self,widget,value):
        self.lbl.set_text(f'Slider reads: {value}')

    def on_close(self):
        self.stop_flag = True
        super(MyApp, self).on_close()

if __name__ == '__main__':
    import ssl
    start(MyApp, 
          debug=True,
          address='0.0.0.0',
          port=8081,
          start_browser=False,
          multiple_instance=True
            )

