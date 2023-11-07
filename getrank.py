import requests
from bs4 import BeautifulSoup

def get_opgg_ranking(summoner_name, region):
    url = f'https://{region}.op.gg/summoner/userName={summoner_name.replace(" ", "+")}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # print("Status Code:", response.status_code)  # 打印状态码
    # print("Response Text:", response.text[:500])  # 打印响应文本的前500个字符

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # 下面的选择器依赖于OP.GG的当前网页结构，可能会随时变化
        tier_div = soup.find('div', class_='tier')
        p_div = soup.find('div', class_='lp')
        return tier_div.text.strip()+" "+p_div.text.strip()

# # 使用函数
# print(get_opgg_ranking('Topformakaier', 'na'))
