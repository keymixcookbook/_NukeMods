## example PySide panel that implements a simple web browser in Nuke
## JW 12/10/11

import nuke
import nukescripts
from nukescripts import panels

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtWebKit import *


class WebBrowserWidget(QWidget):
  def changeLocation(self):
    url = self.locationEdit.text()
    if not url.startswith( 'http://' ):
      url = 'http://' + url
    self.webView.load( QUrl(url) )

  def urlChanged(self, url):
    self.locationEdit.setText( url.toString() )

  def __init__(self):
    QWidget.__init__(self)
    self.webView = QWebView()
   
    self.setLayout( QVBoxLayout() )  
    
    self.locationEdit = QLineEdit( 'http://www.google.com' )
    self.locationEdit.setSizePolicy( QSizePolicy.Expanding, self.locationEdit.sizePolicy().verticalPolicy() )
    
    QObject.connect( self.locationEdit, SIGNAL('returnPressed()'),  self.changeLocation )
    QObject.connect( self.webView,   SIGNAL('urlChanged(QUrl)'),     self.urlChanged )

    self.layout().addWidget( self.locationEdit )
  
    bar = QToolBar()
    bar.addAction( self.webView.pageAction(QWebPage.Back))
    bar.addAction( self.webView.pageAction(QWebPage.Forward))
    bar.addAction( self.webView.pageAction(QWebPage.Stop))
    bar.addAction( self.webView.pageAction(QWebPage.Reload))
    bar.addSeparator()
    
    self.layout().addWidget( bar )
    self.layout().addWidget( self.webView )

    url = 'http://www.thefoundry.co.uk/' 
    self.webView.load( QUrl( url ) )
    self.locationEdit.setText( url ) 
    self.setSizePolicy( QSizePolicy( QSizePolicy.Expanding,  QSizePolicy.Expanding))

## make this work in a .py file and in 'copy and paste' into the script editor
moduleName = __name__
if moduleName == '__main__':
  moduleName = ''
else:
  moduleName = moduleName + '.'

panels.registerWidgetAsPanel( moduleName + 'WebBrowserWidget', 'Web Browser','uk.co.thefoundry.WebBrowserWidget')



