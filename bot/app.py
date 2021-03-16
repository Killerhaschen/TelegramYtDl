import youtube_dl
import subprocess, os, getpass
import asyncio, sys, toml
from samt import Bot, Answer, Context, Mode, logger

#https://stackoverflow.com/questions/18054500/how-to-use-youtube-dl-from-a-python-program#18947879

global telegamId
telegamId=""
path="/app"

################################################################################
#####################################  def  ####################################
################################################################################

def initWithEnvVar():
    global telegamId
    try:
        configFilePath = path+'/config/config.toml'
        telegramBotToken=os.environ['telegramBotToken']
        configFile=toml.load(configFilePath)
        configFile['bot']['token']=str(telegramBotToken)
        formatted_data = toml.dumps(configFile).rstrip()
        with open(configFilePath, 'w') as f:
               f.write(formatted_data)
    except:
        print("ERROR: telegramBotToken ist Notwendig!!", file=sys.stderr)
        print("\n", file=sys.stderr)
        exit()

    try:
        telegamId=os.environ['telegramId']
        telegamId = str(telegamId)
        telegamId = telegamId.split(",")
        print("Set telegamId to:", telegamId)
    except:
        print("ERROR: telegramID ist Notwendig!!", file=sys.stderr)
        print("\n", file=sys.stderr)
        exit()



def getModes(ytUrl):
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})

    with ydl:
        result = ydl.extract_info(
            ytUrl,
            download=False # We just want to extract the info
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    fs = video['formats']
    formats={}
    for f in fs:
        formats[f['format_note']+ ' ' +f['ext']] = f['format_id']
    return formats

#run a command in the given path
def ausfuehren(argus,path):
    ret=subprocess.run(argus, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd=path).stdout.decode('utf-8')
    ret=ret.strip()
    #print(ret)
    return ret

def downloadVideo(ytUrl, mode):
    cmd=['youtube-dl', '-f', mode, ytUrl]
    ausfuehren(cmd, path+'/data')

def getVideoFilename(ytUrl, mode):
    cmd=['youtube-dl', '--get-filename', '-f', mode, ytUrl]
    return ausfuehren(cmd, path+'/data')



################################################################################
####################################  INIT  ####################################
################################################################################

initWithEnvVar()
bot = Bot()


################################################################################
#####################################  BOT  ####################################
################################################################################


@bot.answer("/start")
def start():
    return "greeting", Context.get('user').id


@bot.default_answer
def default():
    return "You have to send an youtube URL to this bot"

@bot.answer('https://www.youtube.com/{}', mode=Mode.PARSE) # {} is a placeholder for any chars
@bot.answer('https://youtu.be/{}', mode=Mode.PARSE) # {} is a placeholder for any chars
@bot.answer('http://www.youtube.com/{}', mode=Mode.PARSE) # {} is a placeholder for any chars
@bot.answer('http://youtu.be/{}', mode=Mode.PARSE) # {} is a placeholder for any chars
def start():
    ant=['file', 'video', 'nothing']
    blubb = yield Answer("Return Type\n/cancel", choices=ant)
    if (blubb == '/cancel') or (blubb not in ant):
        yield Answer('canceld')
        return
    url = Context.get('message').text #get the full URL
    modes = getModes(url)
    selection = yield Answer("formatChoice", choices=list(modes))
    #selection = '720p60 mp4'
    downloadVideo(url, modes[selection])
    filename = getVideoFilename(url, modes[selection])
    if blubb == 'nothing':
        yield Answer("Done")
    elif blubb == 'file':
        yield 'document:'+path+'/data/'+ filename +";It's me!\n"+filename
    elif blubb == 'video':
        yield 'video:'+path+'/data/'+ filename +";It's me!\n"+filename

@bot.before_processing
def auth():
    userIdStr = str(Context.get('user').id)
    print(telegamId, userIdStr)
    if userIdStr in telegamId:
        return True
    else:
        print(telegamId, userIdStr, "false")
        return False

if __name__ == "__main__":
    bot.listen()
