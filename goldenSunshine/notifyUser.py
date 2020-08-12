from src.Windows-10-Toast-Notifications.win10toast import ToastNotifier
import webbrowser

def notifyUser(videoId):
    #
    videoUrl = ('https://www.youtube.com/watch?v=' + videoId)

    toaster = ToastNotifier()
    toaster.show_toast(title="Golden Sunshine",
                       msg="Good morning!\nA new video is available.",
                       callback_on_click=lambda:webbrowser.open(videoUrl))
