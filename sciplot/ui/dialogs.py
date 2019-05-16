from PyQt5.QtWidgets import (QWidget, QDialogButtonBox, QApplication, 
                             QDialog, QHBoxLayout, QVBoxLayout,
                             QLabel, QDoubleSpinBox, QSpinBox)
import sys

class DualEntry(QDialog):
    """ Just a simple Dialog for retrieving 2 values """    
    def __init__(self, entry1, entry2, input_type, text, min, max, parent=None):
        """
        Note: Use the static method
        """
        super().__init__(parent=parent)
        self.initUI(entry1, entry2, input_type, text, min, max)
        
    def initUI(self, entry1, entry2, input_type, text, min, max):      
        self.setObjectName('Dialog')
        self.setStyleSheet("font: 10pt \"Arial\";")
        self.setWindowTitle('Input dialog')
        
        # Setting the parent makes it the default layout
        self.vlayout = QVBoxLayout(self)
        self.vlayout.setObjectName('vlayout')
        
        self.main_text = QLabel(self)
        self.main_text.setText(text)
        self.vlayout.insertWidget(0, self.main_text)
        self.hlayout = QHBoxLayout()
        self.hlayout.setObjectName('hlayout')
        self.vlayout.insertLayout(1,self.hlayout)

        if input_type is float:
            self.entry1 = QDoubleSpinBox(self)
            self.entry2 = QDoubleSpinBox(self)
        elif input_type is int:
            self.entry1 = QSpinBox(self)
            self.entry2 = QSpinBox(self)
        self.entry1.setMaximum(max)
        self.entry1.setMinimum(min)
        self.entry2.setMaximum(max)
        self.entry2.setMinimum(min)
        self.entry1.setValue(entry1)
        self.entry2.setValue(entry2)

        self.hlayout.insertWidget(0, self.entry1)
        self.hlayout.insertWidget(1, self.entry2)

        self.bb = QDialogButtonBox(self)
        self.bb.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.bb.accepted.connect(self.accept)
        self.bb.rejected.connect(self.reject)
        self.vlayout.insertWidget(-1,self.bb)
        self.show()

    @staticmethod
    def getDualEntries(entry1, entry2, input_type=float, text='Enter Values:', min=-10000000000,
                       max=10000000000, parent=None):
        """
        Pops up a dialog box that retrieves 2 values, either float or int

        Parameters
        ----------
        entry1: int or float
            Default value in the left box

        entry2: int or float
            Default value in the right box

        input_type : type
            Either float or int are currently supported

        text : str
            Text describing the values to set

        min : int or float
            Minimum value for entries

        max : int or float
            Maximum value for entries

        parent : object or None
            Parent of the Dialog (QDialog) box.

        Returns
        -------
        (numeric, numeric), int
            Returns (left value, right value), Ok pressed. If Ok was pressed, value == 1, else 0.    

        """
        dialog = DualEntry(entry1, entry2, input_type, text, min, max, parent)
        result = dialog.exec_()
        if result:
            return (dialog.entry1.value(), dialog.entry2.value()), result
        else:
            return (), result

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = DualEntry.getDualEntries(0, 100, float, 'Tets', 0, 100)
    print(ex)
    # sys.exit(app.exec_())