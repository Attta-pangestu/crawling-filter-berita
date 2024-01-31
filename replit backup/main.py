import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from selenium.common.exceptions import NoSuchElementException

# Fixed module
from helper import init_driver
from helper import keyword_counter_filter
from helper import convert_date_format
from gsheet_helper import gsheet_upload
from link_interface import generate_array_search



