import sublime, sublime_plugin
import time
import os
from os.path import dirname, realpath

CLIPBOARD = os.path.join(sublime.packages_path(), os.path.dirname(os.path.realpath(__file__)), 'clipstash-clipboard.txt')

class ClipStash(sublime_plugin.TextCommand):
  def window(self):
    return self.view.window()

  def get_selection(self):
    lines = []
    self.region_set = self.view.sel()
    if self.region_set[0].empty():
      line = self.view.line(self.region_set[0])
      lineContents = self.view.substr(line) + '\n'
      lines.append(lineContents)
    else:
      for region in self.region_set:
        lines.append(self.view.substr(region))
    return lines

  def open_paste_buffer(self):
    self.clip_board = self.window().open_file(CLIPBOARD)
    self.clip_board.set_read_only(False)
    self.edit = self.clip_board.begin_edit()


  def close_edit(self):
    self.clip_board.end_edit(self.edit)
    self.clip_board.set_read_only(True)
    self.clip_board.run_command('save')

  def paste_in(self, cut=False):
    timestamp = time.strftime("%m-%d-%Y %I:%M:%S")
    name = "Unsaved File" if self.view.name() == "" else self.view.name()
    label  = "Cut" if cut else "Copied"
    label += " from " + name

    if self.view.file_name() != None:
      self.clip_board.insert(self.edit, 0, "\n\n=========="+ self.view.file_name() +"\n\n\n")
    else:
      self.clip_board.insert(self.edit, 0, "\n\n\n")
    self.clip_board.insert(self.edit, 0, "\n\n".join(self.lines))
    self.clip_board.insert(self.edit, 0, "============  "+ label +": "+ timestamp +"  ============\n\n")
    self.close_edit()


# ClipStash Copy Command
class ClipStashCopyCommand(ClipStash):
  def run(self, edit):
    self.lines = self.get_selection()
    self.open_paste_buffer()
    self.paste_in()


# ClipStash Cut Command
class ClipStashCutCommand(ClipStash):
  def run(self, edit):
    self.lines = self.get_selection()
    self.open_paste_buffer()
    self.delete_selected()
    self.paste_in(True)

  def delete_selected(self):
    if self.region_set[0].empty():
      line = self.view.line(self.region_set[0])
      self.view.erase(self.edit, line)
    else:
      for line in self.region_set:
        self.view.erase(self.edit, line)


# ClipStash Clear Clipboard Command
class ClipStashClear(ClipStash):
  def run(self, edit):
    open(CLIPBOARD, 'w').close()