import re
import os

def verifyURL(line):
  verifyurl  = re.compile('://').search(line)
  if verifyurl:
    return True
  return

def tvgTypeMatch(line):
  return re.compile('tvg-type=\"(.*?)\"', re.IGNORECASE).search(line)

def tvgNameMatch(line):
  return re.compile('tvg-name=\"(.*?)\"', re.IGNORECASE).search(line)

def tvgLogoMatch(line):
  logomatch = re.compile('tvg-logo=\"(.*?)\"', re.IGNORECASE).search(line)
  if logomatch:
    return logomatch
  return

def tvgGroupMatch(line):
  groupmatch = re.compile('group-title=\"(.*?)\"', re.IGNORECASE).search(line)
  if groupmatch:
    return groupmatch
  return
      
def infoMatch(line):
  infomatch = re.compile('[,](?!.*[,])(.*?)$', re.IGNORECASE).search(line)
  if infomatch:
    return infomatch
  return

def getResult(re_match):
  return re_match.group().split('\"')[1]
      
def seasonEpisodeMatch(line):
  tvshowmatch = re.compile('[s][0-9][0-9][e][0-9][0-9]|[s][0-9][e][0-9]', re.IGNORECASE).search(line)
  if tvshowmatch:
    return tvshowmatch
  seasonMatch = seasonMatch(line)
  if tvshowmatch:
    return seasonMatch
  return

def tvgChannelMatch(line):
  tvgchnomatch = re.compile('tvg-chno=\"(.*?)\"', re.IGNORECASE).search(line)
  if tvgchnomatch:
    return tvgchnomatch
  tvgchannelid = re.compile('tvg-chno=\"(.*?)\"', re.IGNORECASE).search(line)
  if tvgchannelid:
    return tvgchannelid
  return

def getEpisodeNumber(line):
  episodematch = re.compile('[e][0-9][0-9]|[e][0-9]', re.IGNORECASE).search(line)
  return episodematch.group()[1:]

def seasonMatch(line):
  return re.compile('[s][0-9][0-9]', re.IGNORECASE).search(line)

def getSeasonNumber(line):
  seasonmatch = re.compile('[s][0-9][0-9]|[s][0-9]', re.IGNORECASE).search(line)
  return seasonmatch.group()[1:]

def parseMovieInfo(info):
  if ',' in info:
    info = info.split(',')
  if info[0] == "":
    del info[0]
  info = info[-1]
  if '#' in info:
    info = info.split('#')[0]
  if ':' in info:
    info = info.split(':')
  return info.strip()

def generateStreamFile(filename, url):
  if not os.path.exists(filename):
    streamfile = open(filename, "w+")
    streamfile.write(url)
    print("stream file created:", filename)
    streamfile.close()

def makeDirectory(directory):
  if not os.path.exists(directory):
    os.mkdir(directory)
  else:
    print("directory found:", directory)

def stripYear(title):
  yearmatch = re.sub('d{4}', "", title)
  if yearmatch:
    return yearmatch.strip()
  return

def languageMatch(line):
  languagematch = re.compile('[|][A-Z][A-Z][|]', re.IGNORECASE).search(line)
  if languagematch:
    return languagematch
  return

def stripLanguage(title):
  languagematch = re.sub('[|][A-Z][A-Z][|]', "", title, flags=re.IGNORECASE)
  if languagematch:
    return languagematch.strip()
  return

def stripSeasonEpisode(title):
  sematch = re.sub('[s][0-9][0-9][e][0-9][0-9]|[s][0-9][e][0-9]', "", title, flags=re.IGNORECASE)
  if sematch:
    return sematch.strip()
  return

def parseEpisode(title):
  showtitle, episodetitle, language = None, None, None
  seasonepisode = seasonEpisodeMatch(title)
  if seasonepisode:
    seasonnumber = getSeasonNumber(title)
    episodenumber = getEpisodeNumber(title)
    showtitle = stripSeasonEpisode(title)
    if seasonepisode.end() - seasonepisode.start() > 6 or len(seasonepisode.group()) == 5:
      episodetitle = title[seasonepisode.end():].strip()
      seasonnumber = getSeasonNumber(title)
      episodenumber = getEpisodeNumber(title)
      showtitle = title[:seasonepisode.start()]
    else:
      seasonnumber = getSeasonNumber(title)
      episodenumber = getEpisodeNumber(title)
      showtitle = stripSeasonEpisode(title)
    return [showtitle, episodetitle, seasonnumber, episodenumber, language]
  
 