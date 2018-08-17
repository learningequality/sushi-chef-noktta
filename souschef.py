#!/usr/bin/env python
import os
import sys
sys.path.append(os.getcwd()) # Handle relative imports
import logging
from ricecooker.chefs import SushiChef
from le_utils.constants import licenses
from ricecooker.classes.nodes import DocumentNode, VideoNode, TopicNode, HTML5AppNode
from ricecooker.classes.files import HTMLZipFile, VideoFile, SubtitleFile, DownloadFile, YouTubeVideoFile, YouTubeSubtitleFile
from le_utils.constants.languages import getlang
from arabic import catnum, CHANNEL_NAME
import crawl
import localise

LOGGER = logging.getLogger()

class Nok6aChef(SushiChef):
    channel_info = {
        'CHANNEL_SOURCE_DOMAIN': 'nok6a.net', # who is providing the content (e.g. learningequality.org)
        'CHANNEL_SOURCE_ID': 'sushi-chef-noktta-ar',         # channel's unique id
        'CHANNEL_TITLE': CHANNEL_NAME,
        'CHANNEL_LANGUAGE': 'ar',                          # Use language codes from le_utils
        # 'CHANNEL_THUMBNAIL': 'https://im.openupresources.org/assets/im-logo.svg', # (optional) local path or url to image file
        #'CHANNEL_DESCRIPTION': "",  # (optional) description of the channel (optional)
    }

    def construct_channel(self, **kwargs):
        channel = self.get_channel(**kwargs)
        for name, _id in catnum.items():
            cat_node = TopicNode(source_id=str(_id), title=name)
            channel.add_child(cat_node)
            links = crawl.get_all_links(_id)
            for link in list(links)[:4]:
                zipfilename, title = localise.zip_from_url(link)
                appzip = HTMLZipFile(zipfilename)
                zipnode = HTML5AppNode(source_id=link,
                                       title=title,
                                       license = licenses.CC_BY,
                                       copyright_holder=CHANNEL_NAME,
                                       files = [appzip])
                zipnode.validate()
                cat_node.add_child(zipnode)
                
            
            cat_node.validate()
        print ("DONE")
        return channel
    
if __name__ == '__main__':
    """
    Set the environment var `CONTENT_CURATION_TOKEN` (or `KOLIBRI_STUDIO_TOKEN`)
    to your Kolibri Studio token, then call this script using:
        python souschef.py  -v --reset
    """
    mychef = Nok6aChef()
    if 'KOLIBRI_STUDIO_TOKEN' in os.environ:
        os.environ['CONTENT_CURATION_TOKEN'] = os.environ['KOLIBRI_STUDIO_TOKEN']
    mychef.main( )