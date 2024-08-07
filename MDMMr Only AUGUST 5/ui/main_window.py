import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QTextEdit, QPushButton, QDialog, QFormLayout, QLineEdit
from PyQt6.QtPrintSupport import QPrintDialog

import tracker_config as tkc

#############################################################################
# UI
from ui.main_ui.gui import Ui_MainWindow

#############################################################################
# LOGGER
#############################################################################
from logger_setup import logger

#############################################################################
# NAVIGATION
#############################################################################
from navigation.master_navigation import change_mainStack
#############################################################################
# UTILITY
#############################################################################
from utility.app_operations.diet_calc import (
    calculate_calories)
from utility.app_operations.save_generic import (
    TextEditSaver)
from utility.widgets_set_widgets.slider_spinbox_connections import (
    connect_slider_spinbox)

# Window geometry and frame
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)
from utility.app_operations.current_date_highlighter import (
    DateHighlighter)
from utility.widgets_set_widgets.line_connections import (
    line_edit_times)

from utility.widgets_set_widgets.slider_timers import (
    connect_slider_timeedits)
from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)

from utility.app_operations.show_hide import (
    toggle_views)

from utility.widgets_set_widgets.buttons_set_time import (
    btn_times)

# Database connections
from database.database_manager import (
    DataManager)

# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)

# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)
# Setup add_data modules
from database.add_data.mind_mod.mental_mental import add_mentalsolo_data


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    This class represents the main window of the application. It inherits from FramelessWindow,
    QtWidgets.QMainWindow, and Ui_MainWindow. It contains various models, setup functions,
    and operations related to the application.

    Attributes:
    - exercise_model: The exercise model.
    - tooth_model: The tooth model.
    - shower_model: The shower model.
    - hydro_model: The hydro model.
    - diet_model: The diet model.
    - lily_walk_note_model: The lily walk note model.
    - lily_note_model: The lily note model.
    - lily_room_model: The lily room model.
    - lily_walk_model: The lily walk model.
    - lily_mood_model: The lily mood model.
    - lily_diet_model: The lily diet model.
    - mental_mental_model: The mental mental model.
    - cspr_model: The cspr model.
    - wefe_model: The wefe model.
    - btn_times: The button times.
    - sleep_quality_model: The sleep quality model.
    - woke_up_like_model: The woke up like model.
    - sleep_model: The sleep model.
    - total_hours_slept_model: The total hours slept model.
    - total_hrs_slept: The total hours slept.
    - basics_model: The basics model.
    - ui: The UI object.
    - db_manager: The database manager.
    - settings: The QSettings object.
    - window_controller: The WindowController object.

    Methods:
    - __init__: Initializes the MainWindow object.
    - commits_setup: Sets up the commits.
    - slider_set_spinbox: Connects sliders to spinboxes.
    - update_time: Updates the time displayed on the time_label widget.
    - update_beck_summary: Updates the averages of the sliders in the wellbeing and pain module.
    - init_hydration_tracker: Initializes the hydration tracker buttons.
    - switch_to_mmdm_page: Switches to the bds page.
    - switch_to_wefe_page: Switches to the sleep data page.
    - switch_to_cspr_page: Switches to the diet data page.
    - switch_to_basics_data_page: Switches to the basics data page.
    - switch_to_mmdm_measures: Switches to the mmdm measures page.
    - switch_to_wefe_measures: Switches to the wefe measures page.
    - cspr_measures: Switches to the cspr measures page.
    - mmwefecspr_datapage: Switches to the mmwefecspr datapage.
    - switch_lilys_mod: Switches to the lilys mod page.
    - switch_to_lilys_dataviews: Switches to the lilys dataviews page.
    - auto_date_setters: Automatically sets the date for various widgets.
    - auto_time_setters: Automatically sets the time for various widgets.
    - app_operations: Performs various operations related to the application.
    """
    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.mental_mental_model = None
        self.cspr_model = None
        self.wefe_model = None
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        # Database init
        self.db_manager = DataManager()
        self.setup_models()
        # QSettings settings_manager setup
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.window_controller = WindowController()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.restore_state()
        self.app_operations()
        self.auto_date_setters()
        self.stack_navigation()
        self.delete_actions()
        self.switch_page_view_setup()
        self.commits_setup()
        self.auto_time_setters()
        self.actionExit.triggered.connect(self.close_app)
        
    def close_app(self):
        self.close()
        
    def commits_setup(self):        
        self.mental_mental_table_commit()
        self.slider_set_spinbox()
    
    def slider_set_spinbox(self):
        """
        Connects sliders to their corresponding spinboxes.

        This method establishes a connection between sliders and spinboxes
        by mapping each slider to its corresponding spinbox. It then calls
        the `connect_slider_spinbox` function to establish the connection.

        Returns:
            None
        """
        connect_slider_to_spinbox = {
            self.mood_slider: self.mood,
            self.mania_slider: self.mania,
            self.depression_slider: self.depression,
            self.mixed_risk_slider: self.mixed_risk,
        }
        
        for slider, spinbox in connect_slider_to_spinbox.items():
            connect_slider_spinbox(slider, spinbox)

    @staticmethod
    def update_time(state, time_label):
        """
        Update the time displayed on the time_label widget based on the given state.

        Parameters:
        state (int): The state of the time_label widget. If state is 2, the time will be updated.
        time_label (QLabel): The QLabel widget to display the time.

        Raises:
        Exception: If there is an error updating the time.

        Returns:
        None
        """
        try:
            if state == 2:  # checked state
                current_time = QTime.currentTime()
                time_label.setTime(current_time)
        except Exception as e:
            logger.error(f"Error updating time. {e}", exc_info=True)
            
    def switch_to_mmdm_page(self):
        self.mainStack.setCurrentWidget(self.mmdm_page)
        self.resize(325, 390)
        self.setFixedSize(325, 390)
    
    def switch_to_mmdm_tableview(self):
        self.mainStack.setCurrentWidget(self.mmdm_data_page)
        self.resize(800, 460)
        self.setFixedSize(800, 460)
    
    def auto_date_setters(self) -> None:
        """
        Sets the date for various widgets to the current date.

        This method sets the date for the following widgets to the current date:
        - diet_date
        - sleep_date
        - basics_date
        - mental_mental_date
        - wefe_date
        - cspr_date
        - lily_date

        If any exception occurs during the process, it will be logged with the error message.

        Returns:
            None
        """
        try:
            self.mental_mental_date.setDate(QDate.currentDate())
        except Exception as e:
            logger.error(f"Probs with auto dates, {e}", exc_info=True)
    
    def auto_time_setters(self) -> None:
        """
        Sets the time for various components in the UI to the current system time.

        This method sets the time for the following components to the current system time:
        - diet_time
        - sleep_time
        - mental_mental_time
        - basics_time
        - wefe_time
        - cspr_time
        - lily_time

        If any exception occurs during the process, it will be logged with the appropriate error message.

        Returns:
            None
        """
        try:
            self.mental_mental_time.setTime(QTime.currentTime())
        except Exception as e:
            logger.error(f"Probs with auto time, {e}", exc_info=True)
    
    ##########################################################################################
    # APP-OPERATIONS setup
    ##########################################################################################
    def app_operations(self):
        """
        Performs the necessary operations for setting up the application.

        This method connects the currentChanged signal of the mainStack to the on_page_changed slot,
        hides the check frame, connects the triggered signal of the actionTotalHours to the
        calculate_total_hours_slept slot, and sets the current index of the mainStack based on the
        last saved index.

        Raises:
            Exception: If an error occurs while setting up the app_operations.

        """
        try:
            self.mainStack.currentChanged.connect(self.on_page_changed)
            last_index = self.settings.value("lastPageIndex", 0, type=int)
            self.mainStack.setCurrentIndex(last_index)
        except Exception as e:
            logger.error(f"Error occurred while setting up app_operations : {e}", exc_info=True)
    
    def on_page_changed(self, index):
        """
        Callback method triggered when the page is changed in the UI.

        Args:
            index (int): The index of the new page.
        """
        self.settings.setValue("lastPageIndex", index)
    
    def stack_navigation(self):
        """
        Handles the stack navigation for the main window.

        This method maps actions and buttons to stack page indices for the agenda journal.
        It connects the actions to the corresponding pages in the stack.

        Raises:
            Exception: If an error occurs during the stack navigation.

        """
        try:
            # Mapping actions and buttons to stack page indices for the agenda journal
            mainStackNavvy = {
                self.actionMMDMInputView: 0, self.actionMMDMTableView: 1,
            }
            
            # Main Stack Navigation
            for action, page in mainStackNavvy.items():
                action.triggered.connect(
                    lambda _, p=page: change_mainStack(self.mainStack, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def switch_page_view_setup(self):
        """
        Connects the various actions to their corresponding methods for switching pages/views.

        This method sets up the connections between the menu actions and the methods that handle
        switching to different pages/views in the application.

        """
        self.actionMMDMInputView.triggered.connect(self.switch_to_mmdm_page)
        self.actionMMDMTableView.triggered.connect(self.switch_to_mmdm_tableview)
    
    def mental_mental_table_commit(self) -> None:
        """
        Connects the 'commit' action to the 'add_mentalsolo_data' function and inserts data into the mental_mental_table.

        This method connects the 'commit' action to the 'add_mentalsolo_data' function, which is responsible for inserting data into the mental_mental_table. It sets up the connection using the `triggered.connect()` method and passes the necessary data to the `add_mentalsolo_data` function.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommit.triggered.connect(
                lambda: add_mentalsolo_data(
                    self, {
                        "mental_mental_date": "mental_mental_date",
                        "mental_mental_time": "mental_mental_time",
                        "mood_slider": "mood_slider",
                        "mania_slider": "mania_slider",
                        "depression_slider": "depression_slider",
                        "mixed_risk_slider": "mixed_risk_slider",
                        "model": "mental_mental_model"
                    },
                    self.db_manager.insert_into_mental_mental_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def delete_actions(self):
        """
        Connects the `actionDelete` trigger to multiple `delete_selected_rows` functions for different tables and models.
        """
        try:
            self.actionDelete.triggered.connect(
                lambda: delete_selected_rows(
                    self,
                    'mental_mental_table',
                    'mental_mental_model'
                )
            )
        except Exception as e:
            logger.error(f"Error setting up delete actions: {e}", exc_info=True)
        
    def setup_models(self) -> None:
        """
        Set up models for various tables in the main window.

        This method creates and sets models for different tables in the main window.
        It uses the `create_and_set_model` function to create and set the models.

        Raises:
            Exception: If there is an error setting up the models.

        """
        try:
            self.mental_mental_model = create_and_set_model(
                "mental_mental_table",
                self.mental_mental_table
            )
            
        except Exception as e:
            logger.error(f"Error setting up models: {e}", exc_info=True)
    
    def save_state(self):
        """
        Saves the state of the main window.

        This method saves the values of various sliders, inputs, and other UI elements
        as well as the window geometry and state to the application settings.

        Raises:
            Exception: If there is an error while saving the state.

        """
        
        try:
            self.settings.setValue("geometry", self.saveGeometry())
        except Exception as e:
            logger.error(f"Geometry not good fail. {e}", exc_info=True)
        
        try:
            self.settings.setValue("windowState", self.saveState())
        except Exception as e:
            logger.error(f"Geometry not good fail. {e}", exc_info=True)
            
    def restore_state(self) -> None:
        """
        Restores the state of the main window by retrieving values from the settings.

        This method restores the values of various sliders, text fields, and window geometry
        from the settings. If an error occurs during the restoration process, it is logged
        with the corresponding exception.

        Returns:
            None
        """
        
        try:
            # restore window geometry state
            self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring the minds module : stress state {e}")
        
        try:
            self.restoreState(self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Event handler for the close event of the main window.

        This method is called when the user tries to close the main window.
        It saves the state of the application before closing.

        Args:
            event (QCloseEvent): The close event object.

        Returns:
            None
        """
        try:
            self.save_state()
        except Exception as e:
            logger.error(f"error saving state during closure: {e}", exc_info=True)
