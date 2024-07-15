import requests
import time
import os

def fetch_and_save_urls(input_file, output_directory):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Cookie': 'pgv_pvid=8057044995; fqm_pvqid=faf0491e-3335-4313-9e41-ac8854087182; fqm_sessionid=7e8bfa9e-333f-4ad2-8447-8f9f3e191323; pgv_info=ssid=s992207344; ts_refer=www.google.com/; ts_uid=6480193085; ts_last=y.qq.com/n/ryqq/singer/0025NhlN2yWrP4; _qpsvr_localtk=0.7641184622294444; RK=gLklxYv2xf; ptcz=9aa9b010da4881893bdc9f6242bfaff675a83d86469e62696935ba1ba6cde986; login_type=1; psrf_musickey_createtime=1720773477; psrf_qqrefresh_token=C2489026BEBC0540DF25DFBDE9AF211B; qm_keyst=Q_H_L_63k3NFacBbUmgBfKyy78MWJC8LypGKYQf6-dsO5QEE56Pl74vqZ1YxypJY-TH4DkrX-gA6j-JOWM0i9-PFw-73j4u; euin=ow457i6ioe4Foc**; psrf_qqopenid=579CF24B905D141D223C92CA9BACD654; psrf_access_token_expiresAt=1728549477; psrf_qqaccess_token=637CE646F233D365211E966F748062FE; wxrefresh_token=; music_ignore_pskey=202306271436Hn@vBj; uin=2517130582; qqmusic_key=Q_H_L_63k3NFacBbUmgBfKyy78MWJC8LypGKYQf6-dsO5QEE56Pl74vqZ1YxypJY-TH4DkrX-gA6j-JOWM0i9-PFw-73j4u; wxopenid=; wxunionid=; tmeLoginType=2; psrf_qqunionid=91045BA8098EEFA086A72DBC9DCD54FF',
        'Priority': 'u=0, i',
        'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }

    # 读取URL列表
    with open(input_file, 'r', encoding='utf-8') as file:
        urls = file.readlines()

    # 遍历URL列表并发送请求
    for url in urls:
        url = url.strip()
        if not url:
            continue

        full_url = f'https://y.qq.com{url}'
        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            content = response.text
            # 生成保存文件的路径
            singer_id = url.split('/')[-1]
            output_file = f'{output_directory}/{singer_id}.html'
            
            # 保存响应内容到文件
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f'HTML文件保存成功: {output_file}')
        else:
            print(f'请求失败: {full_url} 状态码: {response.status_code}')

        # 等待0.1秒
        # time.sleep(0.1)


input_file = 'singer_urls1.txt'
output_directory = 'singer_info1'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
fetch_and_save_urls(input_file, output_directory)

input_file = 'singer_urls2.txt'
output_directory = 'singer_info2'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
fetch_and_save_urls(input_file, output_directory)

input_file = 'singer_urls3.txt'
output_directory = 'singer_info3'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
fetch_and_save_urls(input_file, output_directory)

input_file = 'singer_urls4.txt'
output_directory = 'singer_info4'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
fetch_and_save_urls(input_file, output_directory)

input_file = 'singer_urls5.txt'
output_directory = 'singer_info5'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
fetch_and_save_urls(input_file, output_directory)