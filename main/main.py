from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtCore
from PyQt5 import QtGui
# import os
import sys

print("Stuart - A Web Browser")

print("\nBy: Ayush Chauhan.")

#Main window.
class MainWindow(QMainWindow):

    #Constructor.
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.setWindowIcon(QtGui.QIcon("Thing.png"))
        self.showMaximized()
 
        #Creating a tab widget.
        self.tabs = QTabWidget()
 
        #Making document mode true.
        self.tabs.setDocumentMode(True)
 
        #Adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
 
        #Adding action when tab is changed.
        self.tabs.currentChanged.connect(self.current_tab_changed)
 
        #Making tabs closeable.
        self.tabs.setTabsClosable(True)
 
        #Adding action when tab close is requested.
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
 
        #Making tabs as central widget.
        self.setCentralWidget(self.tabs)
 
        #Creating a status bar.
        self.status = QStatusBar()
 
        #Setting status bar to the main window.
        self.setStatusBar(self.status)
 
        #Creating a tool bar for navigation.
        navtb = QToolBar("Navigation")
 
        #Adding tool bar tot he main window.
        self.addToolBar(navtb)
 
        #Creating back action.
        back_btn = QAction("👈", self)
        #Setting status tip.
        back_btn.setStatusTip("Go Back To Previous Page.")
        #Adding action to back button.
        #Making current tab go back.
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        #Adding this to the navigation tool bar.
        navtb.addAction(back_btn)
 
        #Similarly adding forward button.
        next_btn = QAction("👉", self)
        next_btn.setStatusTip("Go Forward To Next Page.")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)
 
        #Similarly adding reload button.
        reload_btn = QAction("🔄", self)
        reload_btn.setStatusTip("Reload The Page.")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)
 
        #Creating home action.
        home_btn = QAction("🏠", self)
        home_btn.setStatusTip("Go To The Home Page.")
 
        #Adding action to home button.
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        #Adding a separator.
        navtb.addSeparator()
 
        #Creating a line edit widget for URL.
        self.urlbar = QLineEdit()
 
        #Adding action to line edit when enter key is pressed.
        self.urlbar.returnPressed.connect(self.navigate_to_url)
 
        #Adding line edit to tool bar.
        navtb.addWidget(self.urlbar)

        #Similarly adding stop action.
        stop_btn = QAction("🛑", self)
        stop_btn.setStatusTip("Stop Loading The Current Page.")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
 
        #Creating first tab.
        self.add_new_tab(QUrl('http://google.com'), "Homepage")
 
        #Showing all the components.
        self.show()
 
        #Setting window title.
        self.setWindowTitle("Stuart")
 
    #Method for adding new tab.
    def add_new_tab(self, qurl = None, label ="Blank"):
 
        #If url is blank.
        if qurl is None:
            #Creating a url to be the default one.
            qurl = QUrl('http://google.com')
            # window.close()
 
        #Creating a QWebEngineView object.
        browser = QWebEngineView()
 
        #Setting url to browser.
        browser.setUrl(qurl)
 
        #Setting tab index.
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
 
        #Adding action to the browser when url is changed.
        #Update the url
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))

        #Adding action to the browser when loading is finished.
        #Set the tab title.
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))
 
    #When double clicked is pressed on tabs.
    def tab_open_doubleclick(self, i):
 
        #Checking index.
        #No tab under the click.
        if i == -1:
            #Creating a new tab.
            self.add_new_tab()
 
    #When tab is changed.
    def current_tab_changed(self, i):
 
        #Get the current url.
        qurl = self.tabs.currentWidget().url()
 
        #Update that url.
        self.update_urlbar(qurl, self.tabs.currentWidget())
 
        #Update that title.
        self.update_title(self.tabs.currentWidget())
 
    #If the tab is closed.
    def close_current_tab(self, i):
 
        #If there is only one tab as well.
        if self.tabs.count() < 2:
            #Do nothing.
            return
        page = self.tabs.widget(i)
        self.tabs.removeTab(i)
        page.deleteLater()
 
        #Otherwise remove the tab.
        self.tabs.removeTab(i)
 
    #Method for updating the title.
    def update_title(self, browser):
 
        #If signal is not from the current tab.
        if browser != self.tabs.currentWidget():
            #Then do nothing.
            return
 
        #Get the page title.
        title = self.tabs.currentWidget().page().title()
 
        #Set the window title.
        self.setWindowTitle("% s  |  Browser" % title)
 
    #Action to go to home.
    def navigate_home(self):

        #Go to home page.
        self.tabs.currentWidget().setUrl(QUrl('http://google.com'))
 
    #Method for navigate to url.
    def navigate_to_url(self):
 
        #Get the line edit text.
        #Convert it to QUrl object.
        q = QUrl(self.urlbar.text())
 
        #If the scheme is blank.
        if q.scheme() == "":
            #Set a scheme.
            qurl = (self.tabs.currentWidget()).url()
            q.setScheme("https")
 
        #Then set the url.
        self.tabs.currentWidget().setUrl(q)
 
    #Method to update the url.
    def update_urlbar(self, q, browser = None):
 
        #If this signal is not from the current tab then ignore it.
        if browser != self.tabs.currentWidget():
 
            return
 
        #Set text to the url bar.
        self.urlbar.setText(q.toString())
 
        #Set cursor position.
        self.urlbar.setCursorPosition(0)

#Creating a PyQt5 application.
app = QApplication(sys.argv)
 
#Setting name to the application.
app.setApplicationName("Stuart")
 
#Creating MainWindow object.
window = MainWindow()
 
#Main Loop.
app.exec_()