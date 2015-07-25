import sublime, sublime_plugin

class ClipStash(sublime_plugin.TextCommand):
  def window(self):
    return self.view.window()

  def get_selection(self):
    lines = []
    self.region_set = self.view.sel()
    for region in self.region_set:
      lines.append(self.view.substr(region))
    return lines

  def open_new_file(self):
    return self.window().new_file()

  def allow_file_edit(self):
    self.clip_board.set_read_only(False)
    return self.clip_board.begin_edit()

  def close_edit(self, edit):
    self.clip_board.end_edit(edit)

  def paste_in(self):
    edit = self.allow_file_edit()
    self.clip_board.insert(edit, 0, "".join(self.lines))
    self.close_edit(edit)



class ClipStashCopyCommand(ClipStash):
  def run(self, edit):
    self.lines = self.get_selection()
    self.clip_board = self.open_new_file()
    edit = self.allow_file_edit()
    self.paste_in()
    self.close_edit(edit)



class ClipStashCutCommand(ClipStash):
  def run(self, edit):
    self.lines = self.get_selection()
    self.clip_board = self.open_new_file()
    self.delete_selected()
    self.paste_in()
    self.close_edit(edit)

  def delete_selected(self):
    edit = self.allow_file_edit()
    for line in self.region_set:
      self.view.erase(edit, line)

