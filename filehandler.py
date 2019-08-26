import os
import pafy
from proxy_generater import proxy_request
from os.path import expanduser

def downloadFile(url, filename= None, foldername=None):
    """
    function to download and save mp4 file from a given url.
    Input
        url: url of the mp4 file
        filename: optional. If given file will be saved with the name provided.
        foldername: Optional.Provide the path where you want to save file. If not provided, it will save in the script location
    Out:
        None

    """

    if filename is None:
        filename = url.split("/")[-1]
    else:
        filename = filename +  ".mp4"
    
    #print(filename)

    cur_dir = os.getcwd()
    vid_dir = os.path.join(expanduser("~"), "videos")
    #print(vid_dir)

    if not os.path.exists(vid_dir):
        os.mkdir(vid_dir)
    
    if foldername is not None:
        try:
            os.makedirs(foldername)
        except:
            print("not able to create path")
    file_path = os.path.join(vid_dir, filename)
    # download image using GET
    rawImage = proxy_request('get',url, stream=True)
    #rawImage = requests.get(url, stream=True)
    
    # save the image recieved into the file
    with open(file_path, 'wb') as fd:
        try:
            for chunk in rawImage.iter_content(chunk_size=1024):
                fd.write(chunk)
        except:

            pass
            #print("Something went wrong while writing the file")
    return

def download_youtube_file(ids = None):
    """
    This function will be responsible for downloading youtube files.
    ids: List or single id.
    ex:
        download_youtube_file('gMxK1k26yRE')
        download_youtube_file(['gMxK1k26yRE', 'tADvFcj7Cm4'])
    """
    def download_single_youtube_file(id):
        """
        This function will be responsible for downloading single youtube file.
        ids: single id.
        
        """
        url = "https://www.youtube.com/watch?v={}".format(id)
        # create video object
        video = pafy.new(url)
        # extract information about best resolution video available 
        bestResolutionVideo = video.getbest()
        # download the video
        bestResolutionVideo.download()
        return 
    if isinstance(ids,list):
        for id in ids:
            download_single_youtube_file(id)
    else:
        download_single_youtube_file(ids)
    return

if __name__ =='__main__':
    #function to download single youtube file.
    download_youtube_file('gMxK1k26yRE')
    #function to download multiple youtube file.
    download_youtube_file(['gMxK1k26yRE', 'tADvFcj7Cm4'])
    #download file from site_url ="https://www.newsflare.com"
    url = "https://d5jmjyzrse4ui.cloudfront.net/720p/zNQCbkw5MlRRthTZsMfQpIDQrSXAlDi4.mp4"
    downloadFile(url, "test", "videos")
        
