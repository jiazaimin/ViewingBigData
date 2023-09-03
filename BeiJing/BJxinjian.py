import csv
import os
import time

from lxml import etree
from selenium import webdriver

# 创建csv
outPath = 'C:\letter\letters_data.csv'
if (os.path.exists(outPath)):
    os.remove(outPath)
fp = open(outPath, 'wt', newline='', encoding='UTF-8')
writer = csv.writer(fp)
writer.writerow(('kind', 'time', 'processingDepartment', 'content'))

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# 创建浏览器对象
driver = webdriver.Chrome()


# 得到网页信息
def get_info(num):
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element('id', 'pageNum').clear()
    # driver.find_element_by_id('pageNum').send_keys(num)
    driver.find_element('xpath', '//*[@id="pageNum"]').send_keys(num)  # 输入页数
    driver.find_element('xpath', '//*[@id="judgeFlag"]/a').click()  # 单击确认框
    time.sleep(1)
    html = driver.page_source
    return html

# 解析HTML文件，获取数据
def get_data(html):
    selector = etree.HTML(html)
    infos = selector.xpath('//*[@id="mailul"]/div')
    for info in infos:
        kind = info.xpath('div[1]/a/font/text()')[0]
        time = info.xpath('div[2]/div[1]/div[1]/text()')[0]
        processingDepartment = info.xpath('div[2]/div[1]/div[2]/span/text()')[0]
        content = info.xpath('div[1]/a/span/text()')[0]
        # 处理得到的字符串
        parsekind = kind.strip().strip('·【').strip('】')

        parsetime = time.strip().strip('发起时间：').replace("-", "/")

        parsepd = processingDepartment.strip().strip('处理部门：')

        parsecontent = content.strip()

        writer.writerow((parsekind, parsetime, parsepd, parsecontent))


if __name__ == '__main__':
    url = 'https://www.beijing.gov.cn/hudong/hdjl/com.web.search.mailList.flow'
    for i in range(1, 1000):
        html = get_info(i)
        get_data(html)
        time.sleep(1)
