import urllib.request
import zipfile
import os
from pathlib import Path



# tải xuống plugin
url = 'https://antcpt.com/anticaptcha-plugin.zip'
filehandle, _ = urllib.request.urlretrieve(url)
# giải nén tệp zip đó
with zipfile.ZipFile(filehandle, "r") as f:
    f.extractall("plugin")

# thiết đặt khóa API trong tệp cấu hình
api_key = "59e566f10cedd483bd51b4b37f89f6b9"
file = Path('./plugin/js/config_ac_api_key.js')
file.write_text(file.read_text().replace("antiCapthaPredefinedApiKey = ''", "antiCapthaPredefinedApiKey = '{}'".format(api_key)))

# nén thư mục plugin lại vào plugin.zip
zip_file = zipfile.ZipFile('./plugin.zip', 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk("./plugin"):
        for file in files:
            path = os.path.join(root, file)
            zip_file.write(path, arcname=path.replace("./plugin/", ""))
zip_file.close()