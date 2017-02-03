import sublime
import sublime_plugin
import base64
import os
import re

class SmilesPreview(sublime_plugin.EventListener):
    def on_hover(self, view, point, hover_zone):
        if (hover_zone == sublime.HOVER_TEXT):
            # locate smiles in the string. smiles string should be at the beginning and followed by tab (cxsmiles)
            hovered_line_text = view.substr(view.line(point)).strip()
            smiles_regex = re.compile(r'^([^J][A-Za-z0-9@+\-\[\]\(\)\\\/%=#$\.]+)\t', re.IGNORECASE)
            if (smiles_regex.match(hovered_line_text)):
                smiles_string = smiles_regex.match(hovered_line_text).group(0)
                file_name = "1.png"
                os.system("obabel -ismi -:" + smiles_string + "-opng -O " + file_name)
                # Check that file exists
                if (file_name and os.path.isfile(file_name)):
                    encoded = str(base64.b64encode(
                                    open(file_name, "rb").read()
                                ), "utf-8")
                    view.show_popup('<img src="data:image/png;base64,' + 
                                        encoded + 
                                    '">', 
                                     flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY, 
                                     location=point)
                    return
            return
        return
        
