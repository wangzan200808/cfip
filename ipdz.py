import os
import glob
import logging
import geoip2.database
import requests

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 其他配置
EXCEPTION_FILES = ['requirements.txt', 'dns_result.txt', 'Fission_domain.txt', 'Fission_ip.txt']
GEOIP_DATABASE_PATH = 'GeoLite2-Country.mmdb'
IP_FILE = 'Fission_ip.txt'
KNOWN_COUNTRY_CODES = ['HK', 'JP']

def read_ips(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def get_country_code(ip, reader):
    try:
        response = reader.country(ip)
        return response.country.iso_code
    except Exception as e:
        logging.error(f"Error fetching data for IP {ip}: {e}")
        return None

def get_location(ip):
    for url in ["http://whois.pconline.com.cn/ipJson.jsp?ip=", "http://ip-api.com/json/"]:
        try:
            response = requests.get(url + ip)
            data = response.json()
            if response.status_code == 200 and data.get('status') != 'fail':
                location = data.get('pro', data.get('city', ''))
                if location:
                    return location
        except Exception as e:
            logging.error(f"Error fetching location for IP {ip} using {url}: {e}")
    return None

def save_ip_to_file(ip, country_code):
    if ip and country_code in KNOWN_COUNTRY_CODES:
        filename = f'{country_code}.txt'
        if not os.path.exists(filename):
            open(filename, 'w').close()
        with open(filename, 'a+') as file:
            if ip + '\n' not in file:
                file.write(ip + '\n')

def delete_existing_country_files(exceptions):
    for file in glob.glob('*.txt'):
        if file not in exceptions:
            try:
                os.remove(file)
            except OSError as e:
                logging.error(f"Error deleting file {file}: {e}")

def main():
    delete_existing_country_files(EXCEPTION_FILES)
    with geoip2.database.Reader(GEOIP_DATABASE_PATH) as reader:
        ips = read_ips(IP_FILE)
        for ip in ips:
            country_code = get_country_code(ip, reader)
            if country_code is None:
                location = get_location(ip)
                if location:
                    country_code = location.split()[-1]  # 假设国家代码是location的最后一个词
            if country_code in KNOWN_COUNTRY_CODES:
                save_ip_to_file(ip, country_code)

if __name__ == '__main__':
    main()
