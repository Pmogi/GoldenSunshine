import googleapiclient.discovery
import googleapiclient.errors
import datetime
import re
from config import API_KEY # Users will need to include their own config.py that contains the API key named API_KEY

# Comment out logger when not in develop
import logging

# from logging import getLogger

from notifyUser import notifyUser

class queryYT(object):
    """
    The container for searching Youtube for a new weather check by David Lynch.
    If a new video is available, and the date in the video title matches the
    date of the current day, return the video URL. After which, the notified
    flag is set to True, the next day, the flag is reset by checking the date.

    A major limitation is the use of the YouTube API for searching, which uses
    a large amount of bandwidth. Each call has a quota cost, search being a
    pricier 100 units out of a pool of 10,000 units, giving a limit of 100
    searches per day.
    """

    # A flag used to determine if the video has been seen today
    notified = False

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = API_KEY)

    request = youtube.search().list(
        part="id,snippet",                    # refer to YT API documentation
        channelId="UCDLD_zxiuyh1IMasq9nbjrA", # YT id for David Lynch's channel
        order='date',                         # Search by most recent
        maxResults=5                          # Request 5 video search results
        )

    # For logging errors to a log file
    # hdlr = logging.FileHandler(output_filename, mode='w',
                              # encoding=None, delay=False)

    def __init__(self):
        super(queryYT, self).__init__()
        self.date = self.constructDate()
        
        # Comment out logger when not developing
        self.logger = logging.getLogger()
        dt = datetime.datetime.today()
        
        self.output_filename = 'logs/{}_LOG.log'.format(str(dt.day) + "_" + str(dt.second))
        hdlr = logging.FileHandler(self.output_filename, mode='w', encoding=None, delay=False)
        formatter = logging.Formatter('%(asctime)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)
        

    def search(self):
        '''
        Execute a new search request, if the repsonse is a video use the
        notifyUser function to push
        '''

        # Check if the day has changed since last call
        self.checkDate()
        self.logger.debug("DEBUGGER: Trying to search.")

        # If the user has not been notified of a new video yet today
        # check for a new upload.
        if (not self.notified):

            # Request a new search result
            try:
                response = self.request.execute()

            # except the error of no quota units remainingg
            except googleapiclient.errors.HttpError:
                print("Error: API overdraft. Cannot request search information for the rest of today.")
                self.logger.debug("DEBUGGER: API overdraft.")
                return

            # Put the search results in a list
            results = response.get('items', [])

            # iterate through the list and look for the daily video
            for result in results:

                # Checking if the result is a video.
                if (result['id']['kind'] == 'youtube#video'):

                    # Get the title of the video from the  dictonary
                    videoTitle = result['snippet']['title']

                    # The ID of the video found
                    videoId = result['id']['videoId']

                    # Regex object for checking the date in the title
                    checkDateRegex = re.compile('(\d+)/(\d+)/(\d+)')

                    # attempt to obtain the date from the title
                    dateFromTitle = checkDateRegex.search(videoTitle)

                    # If there's a result from the regex, is it the right date?
                    if dateFromTitle is not None:
                        # print(dateFromTitle[0])

                        # if the date from the title
                        if (self.date == dateFromTitle[0]):
                            self.notified = True
                            notifyUser(videoId)
                            self.logger.debug("DEBUGGER: Search Successful.")
                            return
                            



    def constructDate(self):
        '''
        Constructs a string for the date as represented by the way it's listed
        in the video title.
        @PARAM Self
        @OUT   VOID
        '''
        dt = datetime.datetime.today()

        # Construct the date like the way it's listed in the video titles.
        return (str(dt.month) + "/" + str(dt.day) + "/" + str(dt.year)[2:4])

    def checkDate(self):
        '''
        Check the date to determine if it's a new day. If so, the notified flag
        flag is reset to false.

        @PARAM  Self object
        @OUT    VOID
        '''
        if (self.date != self.constructDate()):
            self.date = self.constructDate()
            self.notified = False
            self.logger.debug("DEBUGGER: Reset notify status successfully.")
            


    def getDate(self):
        return self.date
