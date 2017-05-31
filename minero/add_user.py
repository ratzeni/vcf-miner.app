import os
import sys

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

class AddUserWorkflow(object):
    def __init__(self, args=None, logger=None):
        self.logger = logger