# coding:GB18030

'''
��http://life.main.com/xingming.asp��ַ���������Ա������Զ��ύ��������ȡ���ҳ���еķ������

Created on 2016��10��23��

@author: crazyant.net
'''
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import sys 

import config

reload(sys) 
sys.setdefaultencoding("GB18030")

# ����ı���ַ
REQUEST_URL = "http://life.main.com/xingming.asp"

def get_name_score(name_postfix):
    """���ýӿڣ�ִ�м��㣬���ؽ��
    """
    result_data = {}
    
    params = {}
    
    # �������ͣ�0��ʾ������1��ʾũ��
    params['data_type'] = "0"
    params['year'] = "%s" % str(config.setting["year"])
    params['month'] = "%s" % str(config.setting["month"])
    params['day'] = "%s" % str(config.setting["day"])
    params['hour'] = "%s" % str(config.setting["hour"])
    params['minute'] = "%s" % str(config.setting["minute"])
    params['pid'] = "%s" % str(config.setting["area_province"])
    params['cid'] = "%s" % str(config.setting["area_region"])
    # ϲ�����У�0��ʾ�Զ�������1��ʾ�Զ�ϲ����
    params['wxxy'] = "0"
    params['xing'] = "%s" % (config.setting["name_prefix"])
    params['ming'] = name_postfix
    # ��ʾŮ��1��ʾ��
    if config.setting["sex"] == "��":
        params['sex'] = "1"
    else:
        params['sex'] = "0"
        
    
    params['act'] = "submit"
    params['isbz'] = "1"
    
    post_data = urllib.urlencode(params)
    
    req = urllib2.urlopen(REQUEST_URL, post_data)
    
    content = req.read()
    
    soup = BeautifulSoup(content, 'html.parser', from_encoding="GB18030")
    
    full_name = get_full_name(name_postfix)
    
    # print soup.find(string=re.compile(u"�����������"))
    for node in soup.find_all("div", class_="chaxun_b"):
        node_cont = node.get_text()
        if u'�����������' in node_cont:
            name_wuge = node.find(string=re.compile(u"�����������"))
            result_data['wuge_score'] = name_wuge.next_sibling.b.get_text()
        
        if u'������������' in node_cont:
            name_wuge = node.find(string=re.compile(u"������������"))
            result_data['bazi_score'] = name_wuge.next_sibling.b.get_text()
        
    result_data['full_name'] = full_name
    return result_data

def get_full_name(name):
    return "%s%s" % ((config.setting["name_prefix"]), name)

def process(input_fpath, output_fpath):
    fout = open(output_fpath, "w")
    
    
    all_name_postfixs = set()
    for line in open(input_fpath):
        name_postfix = str(line).strip()
        
        if name_postfix is None or len(name_postfix) == 0:
            continue
        
        name_postfix_full = "%s%s" % (config.setting["middle_world"], name_postfix)
        
        all_name_postfixs.add(name_postfix_full)
        
    cur_idx = 0
    all_count = len(all_name_postfixs)
    for name_postfix in all_name_postfixs:
        cur_idx += 1
        
        try:
            # �����ֵĺ�׺��Ϊ�������м���
            name_data = get_name_score(name_postfix)
        except Exception as e:
            print "error:", name_postfix, e
            continue
        
        print "%d/%d" % (cur_idx, all_count),
        print name_data['full_name'] + "\t������������=" + name_data['bazi_score'] + "\t�����������=" + name_data['wuge_score']
        
        fout.write(name_data['full_name'] + "\t" + name_data['bazi_score'] + "\t" + name_data['wuge_score'] + "\n")

    fout.flush()
    fout.close()

if __name__ == "__main__":
    print "begin................................"
    process(config.setting["input_fpath"], config.setting["output_fpath"])
    print "over................................"

