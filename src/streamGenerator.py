from src.logger import Logger
from src.logger import LogLevel
import os
import re
import src.utils as utils
class Movie(object):

  def __init__(self, title, url):
    self.title = title.strip()
    self.url = url

  def getFilename(self):
    filestring = [self.title.replace(':','-').replace('*','_').replace('/','_').replace('?','')]
    return ('movies/' + ' - '.join(filestring) + ".strm")
  
  def makeStream(self):
    filename = self.getFilename()
    directories = filename.split('/')
    directories = directories[:-1]
    typedir = directories[0]
    if not os.path.exists(typedir):
      os.mkdir(typedir)
    utils.generateStreamFile(filename, self.url)
  
class TVEpisode(object):
  def __init__(self, showtitle, url, seasonnumber=None, episodenumber=None, episodename=None):
    self.showtitle = showtitle
    self.episodenumber = episodenumber
    self.seasonnumber = seasonnumber
    self.episodenumber = episodenumber
    self.url = url
    self.episodename = episodename
    self.seasonepisode = "S" + str(self.seasonnumber) + "E" + str(self.episodenumber)

  def getFilename(self):
    filestring = [self.showtitle.replace(':','-').replace('*','_').replace('/','_').replace('?','')]
    filestring.append(self.seasonepisode.strip())
    if self.episodename:
      filestring.append(self.episodename.strip())
    if self.seasonnumber:
      return ('series/' + self.showtitle.strip().replace(':','-').replace('/','_').replace('*','_').replace('?','') + "/" + self.showtitle.strip().replace(':','-').replace('/','-').replace('*','_').replace('?','') + " - Season " + str(self.seasonnumber.strip()) + '/' + ' - '.join(filestring).replace(':','-').replace('*','_') + ".strm")
    else:
      return ('series/' + self.showtitle.strip().replace(':','-').replace('/','_').replace('*','_').replace('?','') +"/" +' - '.join(filestring).replace(':','-').replace('*','_') + ".strm")
  
  def makeStream(self):
    filename = self.getFilename()
    directories = filename.split('/')
    directories = directories[:-1]
    typedir = directories[0]
    showdir = '/'.join([typedir, directories[1]])
    if not os.path.exists(typedir):
      os.mkdir(typedir)
    if not os.path.exists(showdir):
      os.mkdir(showdir)
    if len(directories) > 2:
      seasondir = '/'.join([showdir, directories[2]])
      if not os.path.exists(seasondir):
        os.mkdir(seasondir)
    utils.generateStreamFile(filename, self.url)

class rawStreamList(object):
  def __init__(self, filename):
    self.log = Logger(__file__, log_level=LogLevel.DEBUG)
    self.streams = {}
    self.filename = filename
    self.readLines()
    self.parseLine()

  def readLines(self):
    self.lines = [line.rstrip('\n') for line in open(self.filename, encoding="utf8")]
    return len(self.lines)
 
  def parseLine(self):
    linenumber=0
    for j in range(len(self.lines)):
      numlines = len(self.lines)
      if linenumber >= numlines:
        return 0
      if not linenumber:
        linenumber = 0
      thisline = self.lines[linenumber]
      nextline = self.lines[linenumber + 1]
      # if its the first line.
      firstline = re.compile('EXTM3U', re.IGNORECASE).search(thisline)
      if firstline:
        linenumber += 1
        continue
      #if file has file information on first line #extinf and group information on second line #extgrp.
      if thisline[0] == "#" and nextline[0] == "#":
        if utils.verifyURL(self.lines[linenumber+2]):  #if stream url is found at 3rd line then read the stream information.
          self.log.write_to_log(msg=' '.join(["raw stream found:", str(linenumber),'\n', ' '.join([thisline, nextline]),self.lines[linenumber+2]]))
          self.parseStream(' '.join([thisline, nextline]),self.lines[linenumber+2])
          linenumber += 3
        else: #else if stream url is not found then throw error.
          self.log.write_to_log(msg=' '.join(['Error finding raw stream in linenumber:', str(linenumber),'\n', ' '.join(self.lines[linenumber:linenumber+2])]))
          linenumber += 1
      elif utils.verifyURL(nextline): #else try checking the if stream url on 2nd line.
        self.log.write_to_log(msg=' '.join(["raw stream found: ", str(linenumber),'\n', '\n'.join([thisline,nextline])]))
        self.parseStream(thisline, nextline)
        linenumber += 2

  def parseStreamType(self, streaminfo):
    typematch = utils.tvgTypeMatch(streaminfo) # get the tvg-type information from the stream informaiton.
    if typematch:
      return utils.getResult(typematch) 
    
  def parseStreamTitle(self, streaminfo):
    typematch = utils.tvgNameMatch(streaminfo) # get the tvg-name information from the stream informaiton.
    if typematch:
      return utils.getResult(typematch) 

  def parseStream(self, streaminfo, streamURL):
    streamtype = self.parseStreamType(streaminfo) # get the type of the stream from stream information.
    if streamtype == 'series': # parse stream as series
      self.parseSeries(streaminfo, streamURL)
    elif streamtype == 'movies': # parse stream as movie
      self.parseMovies(streaminfo, streamURL)
    else: # parse stream as tv channel
      self.parseLiveStream(streaminfo, streamURL)
  
  def parseSeries(self, streaminfo, streamURL):
    title = self.parseStreamTitle(streaminfo) # read the stream Name from line
    episodeinfo = utils.parseEpisode(title) # get the episode information from title
    if episodeinfo:
        showtitle = episodeinfo[0]
        episodename = episodeinfo[1]
        seasonnumber = episodeinfo[2]
        episodenumber = episodeinfo[3]
        language = episodeinfo[4]
        episode = TVEpisode(showtitle, streamURL, seasonnumber, episodenumber, episodename)
    print(episode.__dict__, 'Series')
    print(episode.getFilename())
    episode.makeStream()
  
  def parseLiveStream(self, streaminfo, streamURL):
    #print(streaminfo, "LIVETV")
    pass

  def parseMovies(self, streaminfo, streamURL):
    title = utils.parseMovieInfo(streaminfo)
    moviestream = Movie(title, streamURL)
    print(moviestream.__dict__, "movies")
    print(moviestream.getFilename())
    moviestream.makeStream()






