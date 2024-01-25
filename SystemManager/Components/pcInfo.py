import __init
from Conf.loggingSetup import *
import socket
import psutil # pip install psutil
from pprint import *

class pcInfoClass ():
  def pcName():
    '''`EX =>` LOTUS-PC'''
    return socket.gethostname()
  
  def IpAddress():
    '''`EX =>` 192.168.1.64'''
    return socket.gethostbyname(socket.gethostname())
  
  def WanIpAddress():
    '''`EX =>` 115.79.142.188'''
    from requests import get
    ip = get('https://api.ipify.org').text
    # print(f'My public IP address is: {ip}')
    return ip
  
  def compareWanUrlIp(url="lotus1104.synology.me"):
    '''Đoạn chương trình sẽ kiểm tra xem máy đang truy vấn có WANIP là bao nhiêu
      và so sánh với IP của một URL nào đó (mặc định là lotus1104.synology.me).
      + Nếu 2 IP trùng nhau thì trả về "SAME"
      + Nếu 2 IP không trùng nhau thì trả về "DIFFERENT"
      
      `Ex:` compareWanUrlIp(url="lotus1104.synology.me")
      => {'wanIp': '171.227.222.97', 'urlIp': '171.227.222.97', 'compare': 'SAME'}
      '''
    # Get WAN IP address via Whatismyip.com
    import requests
    print('Requesting WANIP to https://api.ipify.org ...')
    response = requests.get('https://api.ipify.org')
    wanIp = response.text.strip()
    print('+ WAN IP address:', wanIp)
    # Get public IP address from a website
    import os
    response = os.popen("ping -n 1 -w 0 "+url).read()
    urlIp = response.split("[")[-1].split("]")[0].strip()
    print('+ URL IP address:', urlIp)
    # Compare WAN IP and DDNS IP
    if wanIp == urlIp:
      compare = "SAME"
      # print("Access from LOCAL network (LAN)")
    else:
      compare = "DIFFERENT"
      # print("Access from REMOTE network")
    return {"wanIp":wanIp, "urlIp":urlIp, "compare":compare}

  def cpuPercent():
    '''`EX =>` 12.4'''
    return psutil.cpu_percent(interval=1)
  
  def cpuCore():
    '''`EX Máy 8 Cores =>` 8'''
    return psutil.cpu_count()
  
  def cpuFreq():
    '''`EX =>` scpufreq(current=1609.0, min=0.0, max=2112.0)'''
    return psutil.cpu_freq()
  
  def cpuRunTime():
    '''`EX ~4d:01h:15m:00s =>` 350346.3009152'''
    import time
    return time.perf_counter()

  def memUsage():
    '''`EX: Máy 16GB, còn trống ~2GB =>` svmem(total=17006641152, available=2009518080, percent=88.2, used=14997123072, free=2009518080)'''
    return psutil.virtual_memory()

  def diskUsage(diskPartition = "/"):
    '''`EX1 Window: diskUsage('C:\\') =>` sdiskusage(total=196859654144, used=188199620608, free=8660033536, percent=95.6)
       `EX2 Linux:  diskUsage('/')    =>` sdiskusage(total=314571747328, used=111515049984, free=203056697344, percent=35.4)
      '''
    return psutil.disk_usage(diskPartition)

  def processManangement():
    '''REFERENCE: https://pypi.org/project/psutil/'''
    print("REFERENCE: https://pypi.org/project/psutil/")

  def speedTestDownloadBps():
    '''`EX 152.34Mbit/s=>` 152.34'''
    import speedtest
    s = speedtest.Speedtest()
    s.get_servers()
    s.download()
    return round(s.download()/1048576, 2)
    
  def speedTestUploadBps():
    '''`EX 192.24Mbit/s=>` 192.24'''
    import speedtest
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.upload()
    return round(s.upload()/1048576, 2)

  def speedTestFullDict():
    '''
    {'bytes_received': 182866796,\\
    'bytes_sent': 151519232,\\
    'client': {'country': 'VN',
                'ip': '115.79.142.188',
                'isp': 'Viettel Group',
                'ispdlavg': '0',
                'isprating': '3.7',
                'ispulavg': '0',
                'lat': '10.8326',
                'loggedin': '0',
                'lon': '106.6581',
                'rating': '0'},
    'download': 146093738.34705102,\\
    'ping': 8.577,\\
    'server': {'cc': 'VN',
                'country': 'Vietnam',
                'd': 9.232612757974787,
                'host': 'speedtest4.hcmc.netnam.vn:8080',
                'id': '3381',
                'lat': '10.7500',
                'latency': 8.577,
                'lon': '106.6667',
                'name': 'Ho Chi Minh City',
                'sponsor': 'NetNam',
                'url': 'http://speedtest4.hcmc.netnam.vn:8080/speedtest/upload.php'},
    'share': None,\\
    'timestamp': '2022-07-15T13:57:34.685566Z',\\
    'upload': 172470234.87533835}
    '''
    import speedtest
    s = speedtest.Speedtest()
    s.get_servers()
    s.download()
    s.upload()
    results_dict = s.results.dict()
    return results_dict




# pprint(pcInfoClass.speedTestFullDict())
# print(pcInfoClass.speedTestUploadBps())

# REFERENCE: https://pypi.org/project/psutil/
# >>> import psutil
# >>> psutil.pids()
# [1, 2, 3, 4, 5, 6, 7, 46, 48, 50, 51, 178, 182, 222, 223, 224, 268, 1215,
#  1216, 1220, 1221, 1243, 1244, 1301, 1601, 2237, 2355, 2637, 2774, 3932,
#  4176, 4177, 4185, 4187, 4189, 4225, 4243, 4245, 4263, 4282, 4306, 4311,
#  4312, 4313, 4314, 4337, 4339, 4357, 4358, 4363, 4383, 4395, 4408, 4433,
#  4443, 4445, 4446, 5167, 5234, 5235, 5252, 5318, 5424, 5644, 6987, 7054,
#  7055, 7071]
# >>>
# >>> p = psutil.Process(7055)
# >>> p
# psutil.Process(pid=7055, name='python3', status='running', started='09:04:44')
# >>> p.name()
# 'python3'
# >>> p.exe()
# '/usr/bin/python3'
# >>> p.cwd()
# '/home/giampaolo'
# >>> p.cmdline()
# ['/usr/bin/python', 'main.py']
# >>>
# >>> p.pid
# 7055
# >>> p.ppid()
# 7054
# >>> p.children(recursive=True)
# [psutil.Process(pid=29835, name='python3', status='sleeping', started='11:45:38'),
#  psutil.Process(pid=29836, name='python3', status='waking', started='11:43:39')]
# >>>
# >>> p.parent()
# psutil.Process(pid=4699, name='bash', status='sleeping', started='09:06:44')
# >>> p.parents()
# [psutil.Process(pid=4699, name='bash', started='09:06:44'),
#  psutil.Process(pid=4689, name='gnome-terminal-server', status='sleeping', started='0:06:44'),
#  psutil.Process(pid=1, name='systemd', status='sleeping', started='05:56:55')]
# >>>
# >>> p.status()
# 'running'
# >>> p.username()
# 'giampaolo'
# >>> p.create_time()
# 1267551141.5019531
# >>> p.terminal()
# '/dev/pts/0'
# >>>
# >>> p.uids()
# puids(real=1000, effective=1000, saved=1000)
# >>> p.gids()
# pgids(real=1000, effective=1000, saved=1000)
# >>>
# >>> p.cpu_times()
# pcputimes(user=1.02, system=0.31, children_user=0.32, children_system=0.1, iowait=0.0)
# >>> p.cpu_percent(interval=1.0)
# 12.1
# >>> p.cpu_affinity()
# [0, 1, 2, 3]
# >>> p.cpu_affinity([0, 1])  # set
# >>> p.cpu_num()
# 1
# >>>
# >>> p.memory_info()
# pmem(rss=10915840, vms=67608576, shared=3313664, text=2310144, lib=0, data=7262208, dirty=0)
# >>> p.memory_full_info()  # "real" USS memory usage (Linux, macOS, Win only)
# pfullmem(rss=10199040, vms=52133888, shared=3887104, text=2867200, lib=0, data=5967872, dirty=0, uss=6545408, pss=6872064, swap=0)
# >>> p.memory_percent()
# 0.7823
# >>> p.memory_maps()
# [pmmap_grouped(path='/lib/x8664-linux-gnu/libutil-2.15.so', rss=32768, size=2125824, pss=32768, shared_clean=0, shared_dirty=0, private_clean=20480, private_dirty=12288, referenced=32768, anonymous=12288, swap=0),
#  pmmap_grouped(path='/lib/x8664-linux-gnu/libc-2.15.so', rss=3821568, size=3842048, pss=3821568, shared_clean=0, shared_dirty=0, private_clean=0, private_dirty=3821568, referenced=3575808, anonymous=3821568, swap=0),
#  pmmap_grouped(path='[heap]',  rss=32768, size=139264, pss=32768, shared_clean=0, shared_dirty=0, private_clean=0, private_dirty=32768, referenced=32768, anonymous=32768, swap=0),
#  pmmap_grouped(path='[stack]', rss=2465792, size=2494464, pss=2465792, shared_clean=0, shared_dirty=0, private_clean=0, private_dirty=2465792, referenced=2277376, anonymous=2465792, swap=0),
#  ...]
# >>>
# >>> p.io_counters()
# pio(read_count=478001, write_count=59371, read_bytes=700416, write_bytes=69632, read_chars=456232, write_chars=517543)
# >>>
# >>> p.open_files()
# [popenfile(path='/home/giampaolo/monit.py', fd=3, position=0, mode='r', flags=32768),
#  popenfile(path='/var/log/monit.log', fd=4, position=235542, mode='a', flags=33793)]
# >>>
# >>> p.connections(kind='tcp')
# [pconn(fd=115, family=<AddressFamily.AF_INET: 2>, type=<SocketType.SOCK_STREAM: 1>, laddr=addr(ip='10.0.0.1', port=48776), raddr=addr(ip='93.186.135.91', port=80), status='ESTABLISHED'),
#  pconn(fd=117, family=<AddressFamily.AF_INET: 2>, type=<SocketType.SOCK_STREAM: 1>, laddr=addr(ip='10.0.0.1', port=43761), raddr=addr(ip='72.14.234.100', port=80), status='CLOSING')]
# >>>
# >>> p.num_threads()
# 4
# >>> p.num_fds()
# 8
# >>> p.threads()
# [pthread(id=5234, user_time=22.5, system_time=9.2891),
#  pthread(id=5237, user_time=0.0707, system_time=1.1)]
# >>>
# >>> p.num_ctx_switches()
# pctxsw(voluntary=78, involuntary=19)
# >>>
# >>> p.nice()
# 0
# >>> p.nice(10)  # set
# >>>
# >>> p.ionice(psutil.IOPRIO_CLASS_IDLE)  # IO priority (Win and Linux only)
# >>> p.ionice()
# pionice(ioclass=<IOPriority.IOPRIO_CLASS_IDLE: 3>, value=0)
# >>>
# >>> p.rlimit(psutil.RLIMIT_NOFILE, (5, 5))  # set resource limits (Linux only)
# >>> p.rlimit(psutil.RLIMIT_NOFILE)
# (5, 5)
# >>>
# >>> p.environ()
# {'LC_PAPER': 'it_IT.UTF-8', 'SHELL': '/bin/bash', 'GREP_OPTIONS': '--color=auto',
# 'XDG_CONFIG_DIRS': '/etc/xdg/xdg-ubuntu:/usr/share/upstart/xdg:/etc/xdg',
#  ...}
# >>>
# >>> p.as_dict()
# {'status': 'running', 'num_ctx_switches': pctxsw(voluntary=63, involuntary=1), 'pid': 5457, ...}
# >>> p.is_running()
# True
# >>> p.suspend()
# >>> p.resume()
# >>>
# >>> p.terminate()
# >>> p.kill()
# >>> p.wait(timeout=3)
# <Exitcode.EX_OK: 0>
# >>>
# >>> psutil.test()
# USER         PID %CPU %MEM     VSZ     RSS TTY        START    TIME  COMMAND
# root           1  0.0  0.0   24584    2240            Jun17   00:00  init
# root           2  0.0  0.0       0       0            Jun17   00:00  kthreadd
# ...
# giampaolo  31475  0.0  0.0   20760    3024 /dev/pts/0 Jun19   00:00  python2.4
# giampaolo  31721  0.0  2.2  773060  181896            00:04   10:30  chrome
# root       31763  0.0  0.0       0       0            00:05   00:00  kworker/0:1
# >>>
########################################
