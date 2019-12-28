# Copyright (C) 2020 Jerome Robert
#
# pdfarranger is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
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


import pikepdf
from gi.repository import Gtk
_ = gettext.gettext


def _pikepdf_meta_is_valid(meta):
    """
    Return true if m is a valid PikePDF meta data value.
    PikePDF pass meta data to re.sub which only accept str or byte-like object.
    """
    if not isinstance(meta, list):
        meta = [meta]
    for s in meta:
        try:
            re.sub('', '', s)
        except TypeError:
            return False
    return True


def merge(metadata, input_files):
    """ Merge current global metadata and each imported files meta data """
    r = metadata.copy()
    for p in input_files:
        doc = pikepdf.open(p.copyname)
        with doc.open_metadata() as meta:
            meta.load_from_docinfo(doc.docinfo)
            for k, v in meta.items():
                if k not in metadata and _pikepdf_meta_is_valid[v]:
                    r[k] = v
    return r

    
def edit(metadata, parent):
    dialog = Gtk.Dialog(title=(_('Edit meta data')),
                        parent=parent,
                        flags=Gtk.DialogFlags.MODAL,
                        buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                 Gtk.STOCK_OK, Gtk.ResponseType.OK))
    dialog.set_default_response(Gtk.ResponseType.OK)
    dialog.show_all()
    liststore = Gtk.ListStore(str, str)
    for k, v in metadata:
        liststore.append([k, v])
    treeview = Gtk.TreeView.new_with_model(liststore)
    for i, column_title in enumerate(["Software", "Release Year", "Programming Language"]):
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn(column_title, renderer, text=i)
        self.treeview.append_column(column)
    dialog.vbox.pack_start(treeview, True, True, 0)
    result = dialog.run()
    r = result == Gtk.ResponseType.OK
    dialog.destroy()
    return r
