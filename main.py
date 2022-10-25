from PySide2.QtWidgets import QWidget, QApplication, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QHBoxLayout, QLabel  
import sys
# import requests
from PySide2.QtGui import QDesktopServices
from PySide2.QtCore import QUrl
import csvreader_eovpoint_to_kml
import dxf_line_to_kml
from pyproj import Transformer

# EOV Y input field

transformer_from_EOV = Transformer.from_crs("epsg:23700", "epsg:4326")
transformer_from_KML = Transformer.from_crs("epsg:4326", "epsg:23700")

class EOVy(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout(self)

        label = QLabel("EOV Y coord.:")
        main_layout.addWidget(label)

        self.eovy_field = QLineEdit()
        self.eovy_field.setPlaceholderText("650000")
        main_layout.addWidget(self.eovy_field)

# EOV x input field

class EOVx(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout(self)

        label = QLabel("EOV X coord.:")
        main_layout.addWidget(label)

        self.eovx_field = QLineEdit()
        self.eovx_field.setPlaceholderText("240000")
        main_layout.addWidget(self.eovx_field)


class EOVWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("EOV to WGS'84 and KML")
        self.resize(300, 0)

        # create message window
        self.message_box = QMessageBox()
        self.message_box.setIcon(QMessageBox.Critical)
        self.message_box.setWindowTitle("Error")

        # create root layout for other widgets
        main_layout = QVBoxLayout(self)

        # design widgets
        self.maplabel = QLabel("---------------------One point show in map----------------------")
        main_layout.addWidget(self.maplabel)

        # eov Y
        self.eovyfield = EOVy()
        main_layout.addWidget(self.eovyfield)

        # eov x
        self.eovxfield = EOVx()
        main_layout.addWidget(self.eovxfield)

        # outputs_field
        self.wgsy_text = QLabel("WGS84 λ coords")
        main_layout.addWidget(self.wgsy_text)

        self.wgsx_text = QLabel("WGS84 φ coords")
        main_layout.addWidget(self.wgsx_text)


        # show on google button
        self.showon_map_bttn = QPushButton("Show on Google map")
        self.showon_map_bttn.clicked.connect(self.button_clicked_showmap)
        main_layout.addWidget(self.showon_map_bttn)

        # design widgets    
        self.csvtokml = QLabel("---------------------Import CSV koords to kml----------------------")
        main_layout.addWidget(self.csvtokml)

        # import csv button
        self.import_from_csv_bttn = QPushButton("Import from CSV")
        self.import_from_csv_bttn.clicked.connect(self.button_clicked_pointstokml)
        main_layout.addWidget(self.import_from_csv_bttn)

        # design widgets 
        self.dxftokml = QLabel("-----------------------Import dxf lines to kml-----------------------")
        main_layout.addWidget(self.dxftokml)

        # import dxf button
        self.import_from_dxf_bttn = QPushButton("Import from dxf")
        self.import_from_dxf_bttn.clicked.connect(self.button_clicked_dxftokml)
        main_layout.addWidget(self.import_from_dxf_bttn)

                # design widgets 
        self.sign = QLabel("--------------------powered by Sándor Fényes--------------------")
        main_layout.addWidget(self.sign)

    # google button on click
    def button_clicked_showmap(self):
        if not self.eovyfield.eovy_field.text():
            self.message_box.setText("EOVy coords mut be filled")
            self.message_box.show()
            return

        if not self.eovxfield.eovx_field.text():
            self.message_box.setText("EOVx coords mut be filled")
            self.message_box.show()
            return

        input_data_y = int(f"{self.eovyfield.eovy_field.text()}")
        input_data_x = int(f"{self.eovxfield.eovx_field.text()}")
        coords=transformer_from_EOV.transform(input_data_y, input_data_x)
        # http = str(f"http://www.agt.bme.hu/on_line/etrs2eov/etrs2eov.php?e={ycoord}&n={xcoord}&sfradio=single&format=TXT")
        # coords = requests.get(http)

        wgs84y = coords[0]
        wgs84x = coords[1]
        
        swgs84y=str(wgs84y)
        swgs84x=str(wgs84x)

        str_output_datay = str("WGS84 λ coords: " + swgs84y)
        str_output_datax = str("WGS84 φ coords: " + swgs84x)
        
        wgsurl = f"https://www.google.hu/maps/?q=loc:{wgs84y},{wgs84x}&t=k&hl=hu&z=100"


        # wrote back to wgsy, wgsx QLabel

        self.wgsy_text.setText(str_output_datay)
        self.wgsx_text.setText(str_output_datax)
        QDesktopServices.openUrl(QUrl(wgsurl))
        self.eovyfield.eovy_field.clear()
        self.eovxfield.eovx_field.clear()
         
    # import csv button on click
    def button_clicked_pointstokml(self): 
        csvreader_eovpoint_to_kml.fromcsvtokml()   

    # import dxf button on click
    def button_clicked_dxftokml(self): 
        dxf_line_to_kml.dxflinetokml()      


app = QApplication(sys.argv)
my_window = EOVWidget()
my_window.show()
app.exec_()