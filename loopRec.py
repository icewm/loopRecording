import wave
from pyaudio import PyAudio,paInt16

import ctypes
import os,sys
from sys import argv
import platform
import time

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2
minut=15
secend=minut*60
#secend=10
rec_time=secend*2
procbar=50

def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record(fileN):
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    my_buf=[]
    count=0
    rowperc=''
    while count<TIME*rec_time:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        percent=(count/(secend/procbar))//2+1
        hashes = '#' * int(percent / 100.0 * procbar)
        spaces = ' ' * (procbar - len(hashes))
        sys.stdout.write("\rTime:[%d/%d secends/%d minutes] Percent:[%s] %d%%  " % (count//4+1,secend,minut,hashes + spaces, percent))
        sys.stdout.flush()

        count+=1
        #print('.')
    save_wave_file(fileN,my_buf)
    stream.close()
    print('Done!')


chunk=2014
def play():
    wf=wave.open(r"01.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()

def get_free_space_mb(folder):
    """ Return folder/drive free space (in bytes)
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / 1024 / 1024
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / 1024 / 1024

'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def file_extension(path):
  return os.path.splitext(path)[1]

if __name__ == '__main__':
    #my_record()
    print(argv)
    #print(len(argv))
    myargv=['','1024','15.0']
    if len(argv)==3:
        myargv=argv
    if len(argv)==2:
        myargv[0]=argv[0]
        myargv[1]=argv[1]
    print(myargv)
    minut=float(myargv[2])
    secend = minut * 60
    rec_time = secend * 2

    rPath = os.path.realpath(__file__)
    rDir = os.path.dirname(rPath)
    volMark = rPath[0:3] + '\\'

    while True:
        remainDisk = get_free_space_mb(volMark)

        if remainDisk > float(myargv[1]):
            #print('good disk')
            showP = ""

            datet = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # print(datet)
            if not os.path.exists(datet):
                os.mkdir(datet)
            showP += datet + "\t"
            # print(get_free_space_mb('D:\\'), 'MB')
            showP += str(remainDisk) + "MB" + "\t"
            showP += rDir
            print(showP)
            # showP+=os.path.dirname(os.path.realpath(__file__)) + "\r\n"
            wavName = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).replace(':', '-') + '.wav'
            currentFileP = os.path.join(rDir, datet)
            currentFileP = os.path.join(currentFileP, wavName)
            print(currentFileP)
            my_record(currentFileP)

        else:
            print('bad disk')

            wFileList = []
            for (dirpath, dirnames, filenames) in os.walk(os.path.dirname(os.path.realpath(__file__))):
                for filename in filenames:
                    # print(filename)
                    if file_extension(filename) == '.wav':
                        filePN = os.path.join(dirpath, filename)
                        wFileList.append([filePN, os.path.getmtime(filePN)])
                        # print(filePN)
            #print(wFileList)
            if len(wFileList)==0:
                print(str(len(wFileList))+'  No file to delete ,no space...')
                break
            else:
                fileCD = [x[1] for x in wFileList]
                #print(fileCD.index(min(fileCD)))
                print('Deleting files: ',wFileList[fileCD.index(min(fileCD))])
                #print(wFileList[fileCD.index(min(fileCD))][0])
                os.remove(wFileList[fileCD.index(min(fileCD))][0])
                #print(fileCD.index(max(fileCD)))
                #print(wFileList[fileCD.index(max(fileCD))])


    #play()




    '''
    print("__file__=%s" % __file__)
    print("os.path.realpath(__file__)=%s" % os.path.realpath(__file__))
    print("os.path.dirname(os.path.realpath(__file__))=%s" % os.path.dirname(os.path.realpath(__file__)))
    print("os.path.split(os.path.realpath(__file__))=%s" % os.path.split(os.path.realpath(__file__))[0])
    print("os.path.abspath(__file__)=%s" % os.path.abspath(__file__))
    print("os.getcwd()=%s" % os.getcwd())
    print("sys.path[0]=%s" % sys.path[0])
    print("sys.argv[0]=%s" % sys.argv[0])
    
    
    
    
    
    
    for (dirpath, dirnames, filenames) in os.walk(os.path.dirname(os.path.realpath(__file__))):
        for filename in filenames:
            print(filename)
            print(os.path.join(dirpath, filename))
            
            
            
        for fileP in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        # if os.path.isfile(fileP):
        file_path = os.path.split(fileP)  # 分割出目录与文件
        lists = file_path[1].split('.')  # 分割出文件与文件扩展名
        file_ext = lists[-1]  # 取出后缀名(列表切片操作)
        img_ext = ['wav']
        if file_ext in img_ext:
            # listP.append(os.path.abspath(fileP))
            print(fileP)
            fsize = os.path.getsize(fileP)
            fsize = fsize / float(1024 * 1024)
            fsize = round(fsize, 2)
            print(fsize)
    '''
