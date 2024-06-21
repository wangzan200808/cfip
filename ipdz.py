import geoip2.database
import requests
import os

def download_geolite_mmdb(file_url, save_path):
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

# 使用P3TERX仓库中的最新GeoLite2-Country.mmdb文件的直接下载链接
#file_url = '<url id="cpqfvntdl8mnd4l1cm00" type="url" status="failed" title="" wc="0">https://github.com/P3TERX/GeoLite.mmdb/releases/latest/download/GeoLite2-Country.mmdb</url>'
#save_path = 'GeoLite2-Country.mmdb'  # 保存到当前脚本目录

#download_geolite_mmdb(file_url, save_path)

# 下面是你的主脚本代码，现在你可以安全地假设GeoLite2-Country.mmdb已经下载并保存在当前目录
# ...
# 读取IPv4地址的文件
def read_ips(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# 使用geoip2获取IP的国家代码
def get_country_code(ip, reader):
    try:
        response = reader.country(ip)
        return response.country.iso_code
    except Exception as e:
        print(f"Error fetching data for IP {ip}: {e}")
        return 'Unknown'

# 保存IP到对应的国家代码文件
def save_ip_to_file(ip, country_code):
    country_code = country_code or 'Unknown'  # 避免保存到None.txt文件
    filename = f'{country_code}.txt'
    with open(filename, 'w') as file:
        file.write(ip + '\n')

# 主函数
def main():
    # 指定GeoLite2数据库文件的路径
    database_path = 'GeoLite2-Country.mmdb'
    with geoip2.database.Reader(database_path) as reader:
        ips = read_ips('Fission_ip.txt')
        for ip in ips:
            country_code = get_country_code(ip, reader)
            save_ip_to_file(ip, country_code)

if __name__ == '__main__':
    main()
