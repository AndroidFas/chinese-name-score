# coding:GB18030

'''
��http://life.httpcn.com/xingming.asp��ַ���������Ա������Զ��ύ��������ȡ���ҳ���еķ������

Created on 2016��10��23��

@author: crazyant.net
'''
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import sys 


reload(sys) 
sys.setdefaultencoding("GB18030")

# ����ı���ַ
REQUEST_URL = "http://life.httpcn.com/xingming.asp"

def get_name_score(name):
    result_data = {}
    
    params = {}
    
    params['data_type'] = "0"
    params['year'] = "2016"
    params['month'] = "10"
    params['day'] = "18"
    params['hour'] = "8"
    params['minute'] = "38"
    params['pid'] = "����"
    params['cid'] = "����"
    params['wxxy'] = "0"
    params['xishen'] = "ˮ"
    params['yongshen'] = "ˮ"
    params['xing'] = name[:2]  # "��"
    params['ming'] = name[2:]  # "����"
    params['sex'] = "1"
    params['act'] = "submit"
    params['isbz'] = "1"
    
    post_data = urllib.urlencode(params)
    
    req = urllib2.urlopen(REQUEST_URL, post_data)
    
    content = req.read()
    
    soup = BeautifulSoup(content, 'html.parser', from_encoding="GB18030")
    
    # print soup.find(string=re.compile(u"�����������"))
    for node in soup.find_all("div", class_="chaxun_b"):
        node_cont = node.get_text()
        if u'�����������' in node_cont:
            name_wuge = node.find(string=re.compile(u"�����������"))
            result_data['wuge_score'] = name_wuge.next_sibling.b.get_text()
        
        if u'������������' in node_cont:
            name_wuge = node.find(string=re.compile(u"������������"))
            result_data['bazi_score'] = name_wuge.next_sibling.b.get_text()
        
    result_data['name'] = name
    return result_data


if __name__ == "__main__":
    
    fname_input_name = "data/names_han_input.txt"
    fname_output_name = fname_input_name.replace("input", "output")
    
    fout = open(fname_output_name, "w")
    all_input_names = set()
    
    for line in open(fname_input_name):
        name = line[:-1]
        if len(name) == 4:
            print "����Ҫ����" + name
            continue
        
        all_input_names.add(name)
   
    total_count = len(all_input_names)
    print '�ܹ���Ҫ�������ָ�����%d' % total_count
    
    idx = 1    
    for name in all_input_names:
        print "�����У�%d/%d, %s" % (idx, total_count, name)
        name_data = get_name_score(name)
        
        total_score = str(float(name_data['bazi_score']) + float(name_data['wuge_score']))
        
        print "\t������������=" + name_data['bazi_score'] + "\t�����������=" + name_data['wuge_score'] + "\t�ܷ�=" + total_score
        fout.write(name_data['name'] + "\t" + name_data['bazi_score'] + "\t" + name_data['wuge_score'] + "\t" + total_score + "\n")
        fout.flush()
        
        idx += 1
    
    fout.close()
