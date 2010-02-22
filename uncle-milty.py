from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document
from waveapi.ops import OpBuilder

import logging
import urllib2
from BeautifulSoup import BeautifulSoup

def OnBlipSubmitted(properties, context):
  """ Invoked every time a blip is submitted while Milty is in the conversation """
  blip = context.GetBlipById(properties['blipId'])

  page = urllib2.urlopen("https://catalog.library.jhu.edu/ipac20/ipac.jsp?menu=search&aspect=subtab22&npp=5&ipp=20&spp=20&profile=general&ri=&index=ALTITLE&term=" + blip.GetDocument().GetText() + "&x=0&y=0&aspect=subtab22")
  soup = BeautifulSoup(page)
  results = soup.findAll(title="View more information")

  sub_blip = context.GetRootWavelet().CreateBlip()
  sub_blipdoc = sub_blip.GetDocument()
  
  outputstr = ""
  count = 0

  for i  in results:
    if count >= 5:
      break
    else:
      itemstr = str(i)
      itemstr = itemstr.replace('class="smallBoldAnchor"', '')
      outputstr = outputstr + itemstr + "<br/>"
      count = count + 1
      
  logging.debug(outputstr)
  
  sub_blipdoc.SetText(" ")
  builder = OpBuilder(context)
  builder.DocumentAppendMarkup(sub_blip.waveId, sub_blip.waveletId, sub_blip.blipId, outputstr)
  logging.debug(sub_blip.waveId + " " + sub_blip.waveletId + " " + sub_blip.blipId)


def OnRobotAdded(properties, context):
  """Invoked when the robot has been added."""
  logging.debug("created")
  root_wavelet = context.GetRootWavelet()
  root_wavelet.CreateBlip().GetDocument().SetText("Hi, I'm Milton S. Eisenhower and I'd be happy to help you with your research. I will search the JHU catalog for anything that you say to me and I'll let you know if I find anything.")

if __name__ == '__main__':
  myRobot = robot.Robot('Milton S. Eisenhower', 
      image_url='http://uncle-milty.appspot.com/assets/milty.png',
      version='2',
      profile_url='http://uncle-milty.appspot.com/')
  myRobot.RegisterHandler(events.BLIP_SUBMITTED, OnBlipSubmitted)
  myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
  myRobot.Run()