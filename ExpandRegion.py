import sublime, sublime_plugin, os

try:
  import expand_region_handler
except:
  from . import expand_region_handler

class ExpandRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit, debug=True):

    settings = self.view.settings()
    initialName = 'expand_region_initialPosition'
    startName = 'expand_region_lastStart'
    endName = 'expand_region_lastEnd'
    selections = self.view.sel()
    
    # get previous expansion coordinates if they exist
    lastStart = settings.get(startName)
    lastEnd = settings.get(endName)

    extension = ""
    if (self.view.file_name()):
      name, fileex = os.path.splitext(self.view.file_name())
      extension = fileex[1:]

    for region in selections:
      string = self.view.substr(sublime.Region(0, self.view.size()))
      start = region.begin()
      end = region.end()

      # reset initial position when selecting area outside current expansion
      if (lastStart == None) or (lastStart < start) or (lastEnd > end):
        settings.set(initialName,start);

      # we're at limit - reset to first position
      if start == lastStart and end == lastEnd:
        selections.clear();
        region = sublime.Region(settings.get(initialName))
        selections.add(region)
        settings.erase(startName);
        settings.erase(endName);

      result = expand_region_handler.expand(string, start, end, extension)
      if result:
        selections.add(sublime.Region(result["start"], result["end"]))
        settings.set(startName,result["start"]);
        settings.set(endName,result["end"]);
        if debug:
          print('printing')
          print("startIndex: {0}, endIndex: {1}, type: {2}".format(result["start"], result["end"], result["type"]))
