import geoip2.database
import requests
import os
import os

def save_ip_to_file(ip, country_code):
    country_code = country_code or 'Unknown'
    filename = f'{country_code}.txt'
    
    # 删除旧的文件（如果存在）
    if os.path.exists(filename):
        os.remove(filename)
    
    # 将IP地址写入文件
    with open(filename, 'a') as file:
        file.write(ip + '\n')
    
    # 读取文件并去除重复的IP地址
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 使用集合来存储不重复的IP地址
    unique_ips = set()
    new_lines = []
    for line in lines:
        ip_in_line = line.strip()
        if ip_in_line not in unique_ips:
            unique_ips.add(ip_in_line)
            new_lines.append(line)
    
    # 重新写入文件，只包含不重复的IP地址
    with open(filename, 'w') as file:
        file.writelines(new_lines)

# 调用save_ip_to_file函数的示例
save_ip_to_file('192.168.1.1', 'US')
save_ip_to_file('192.168.1.1', 'US')  # 这个IP将不会被重复写入
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
    with open(filename, 'a') as file:
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
