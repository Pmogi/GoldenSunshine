from queryYT import queryYT
import time

def main():
    '''
    A subprocess for Windows 10 to check for new David Lynch weather videos.
    '''
    query = queryYT()

    while True:
        query.constructDate()
        query.checkDate()
        query.search()
        time.sleep(3600) # Sleep 1 hour

if __name__ == "__main__":
    main()
