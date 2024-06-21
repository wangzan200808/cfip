import geoip2.database

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
    database_path = 'path/to/GeoLite2-Country.mmdb'
    with geoip2.database.Reader(database_path) as reader:
        ips = read_ips('Fission_ip.txt')
        for ip in ips:
            country_code = get_country_code(ip, reader)
            save_ip_to_file(ip, country_code)

if __name__ == '__main__':
    main()
