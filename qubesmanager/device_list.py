# The Qubes OS Project, https://www.qubes-os.org/
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from . import ui_devicelist  # pylint: disable=no-name-in-module
from PyQt6 import QtWidgets  # pylint: disable=import-error

# this is needed for icons to actually work
# pylint: disable=unused-import, no-name-in-module
from . import resources


class PCIDeviceListWindow(ui_devicelist.Ui_Dialog, QtWidgets.QDialog):
    def __init__(self, *, vm, qapp, dev_list, no_strict_reset_list,
                 parent=None):
        super().__init__(parent)

        self.vm = vm
        self.qapp = qapp
        self.dev_list = dev_list
        self.no_strict_reset_list = no_strict_reset_list

        self.setupUi(self)

        self.buttonBox.accepted.connect(self.save_and_apply)
        self.buttonBox.rejected.connect(self.reject)

        self.ident_list = {}
        self.fill_device_list()

    def fill_device_list(self):
        self.device_list.clear()

        for i in range(self.dev_list.selected_list.count()):
            text = self.dev_list.selected_list.item(i).text()
            port_id = self.dev_list.selected_list.item(i).dev.port_id
            self.device_list.addItem(text)
            self.ident_list[text] = port_id
            if port_id in self.no_strict_reset_list:
                self.device_list.item(self.device_list.count()-1).setSelected(
                    True)

    def reject(self):
        self.done(0)

    def save_and_apply(self):
        self.no_strict_reset_list.clear()
        self.no_strict_reset_list.extend([self.ident_list[item.text()] for item
                                          in self.device_list.selectedItems()])
        self.done(0)
