import requests
import json
from conf import target_school_name, target_major_code_list
from urllib.parse import quote
from xlsx import write_data_into_excel

api_host = 'api.qz100.com'  # 考研帮
yantu_api_host = 'api.kaoyanvip.cn'  # 研途考研


class KaoYanBangApi:
    """考研帮API"""
    def __init__(self, host=api_host):
        self.host = host

    def get_all_schools(self):
        """
        获取了全部的学校
        :return:
        """
        pagelimit = '20'
        pagestart = '1'
        api_url = f'http://{self.host}/api-cpp/major/schools?school_name=&page={pagestart}&limit={pagelimit}&sort_type=1&school_type=-1&is_edu=-1&is_local=-1&is_center=-1'
        headers = {
            'Q-Organization': 'kaoyan',
            'User-Agent': 'Mozilla/ (iPhone; CPU iPhone OS like Mac OS X) AppleWebKit/(KHTML, like Gecko) Mobile/KaoYanClub//K-Product-Line:kaoyan-app;/K-New-Product-Line:ky-app;/kmf_appinner;/appversion:4.3.4;'
        }
        all_result_data = []
        r_target_schools = []
        r = requests.get(api_url, headers=headers)
        r_json = json.loads(r.text)
        status = r_json['status']
        result = r_json['result']
        result_from = result['from']
        result_per_page = result['per_page']
        result_total = result['total']
        result_data = result['data']
        all_result_data += result_data
        while result_total - int(pagelimit) > 0:
            pagestart = str(int(pagestart) + 1)
            api_url = f'http://{self.host}/api-cpp/major/schools?school_name=&page={pagestart}&limit={pagelimit}&sort_type=1&school_type=-1&is_edu=-1&is_local=-1&is_center=-1'
            r1 = requests.get(api_url, headers=headers)
            r1_json = json.loads(r1.text)
            r1_result = r1_json['result']
            r1_result_data = r1_result['data']
            all_result_data += r1_result_data
            result_total = result_total - int(pagelimit)

        return all_result_data

    def get_target_schools(self):
        """
        获取目标学校
        :return:
        """
        r_school_info = []
        for school_name in target_school_name:
            _ = self.search_schools(school_name)
            school_id = _.get('school_id')
            school_code = _.get('school_code')
            school_name = _.get('school_name')
            badge = _.get('badge')
            is_211 = _.get('is_211')
            is_985 = _.get('is_985')
            is_score = _.get('is_score')
            follow_num = _.get('follow_num')  # 关注人数
            is_first_class = _.get('is_first_class')
            departments = _.get('departments')
            province_id = _.get('province_id')
            province_name = _.get('province_name')
            is_other = _.get('is_other')
            school_type = _.get('school_type')
            """
            1-理工类
            2-艺体类
            3-综合类
            4-师范类
            5-农林类
            6-文法类
            7-医药类
            8-军事类
            9-财经类
            10-其他
            """
            is_edu = _.get('is_edu')
            is_local = _.get('is_local')
            is_center = _.get('is_center')
            exam_num = _.get('exam_num')  # 今年备考人数
            week_exam_num = _.get('week_exam_num')  # 近7日新增
            bbs_id = _.get('bbs_id')
            student_recruitment = _.get('student_recruitment')
            print(f'{school_name}\n关注人数:{follow_num}\n所属省份:{province_name}\n今年备考人数:{exam_num}\n' +
                  f'近7日新增:{week_exam_num}\n学生官网:{student_recruitment}\n\n')
            r_school_info.append(_)
        return r_school_info

    def search_schools(self, school_name):
        search_url = f'http://{self.host}/api-cpp/major/schools?school_name={quote(school_name)}&page=1&limit=20&sort_type=1&school_type=-1&is_edu=-1&is_local=-1&is_center=-1'
        headers = {
            'User-Agent': 'Mozilla/ (iPhone; CPU iPhone OS like Mac OS X)AppleWebKit/(KHTML, like Gecko) Mobile/KaoYanClub//K-Product-Line:kaoyan-app;/K-New-Product-Line:ky-app;/kmf_appinner;/appversion:4.3.4;',
            'Q-Organization': 'kaoyan',
        }

        r = requests.get(search_url, headers=headers)
        r_json = json.loads(r.text)
        status = r_json['status']
        result = r_json['result']
        result_data = result['data']
        for _ in result_data:
            if _.get('school_name') == school_name:
                return _

    def get_majorlist_by_id(self, school_id):
        pagelimit = '20'
        pagestart = '1'
        major_url = f'http://{self.host}/api-cpp/major/list?first_major=&second_major=&is_tech=-1&school_id={school_id}&study_type=-1&math_type=-1&foreign_type=-1&limit={pagelimit}&page={pagestart}'
        headers = {
            'User-Agent': 'Mozilla/ (iPhone; CPU iPhone OS like Mac OS X)AppleWebKit/(KHTML, like Gecko) Mobile/KaoYanClub//K-Product-Line:kaoyan-app;/K-New-Product-Line:ky-app;/kmf_appinner;/appversion:4.3.4;',
            'Q-Organization': 'kaoyan',
        }
        all_result_data = []
        r = requests.get(major_url, headers=headers)
        r_json = json.loads(r.text)
        status = r_json['status']
        result = r_json['result']
        result_total = result['total']
        result_data = result['data']
        all_result_data += result_data
        while result_total - int(pagelimit) > 0:
            pagestart = str(int(pagestart) + 1)
            major_url = f'http://{self.host}/api-cpp/major/list?first_major=&second_major=&is_tech=-1&school_id={school_id}&study_type=-1&math_type=-1&foreign_type=-1&limit={pagelimit}&page={pagestart}'
            r1 = requests.get(major_url, headers=headers)
            r1_json = json.loads(r1.text)
            r1_result = r1_json['result']
            r1_result_data = r1_result['data']
            all_result_data += r1_result_data
            result_total = result_total - int(pagelimit)
        # print(all_result_data)
        return all_result_data

    def get_school_majors(self, school_name):
        """
        获得一个学校全量的专业
        :param school_name:学校名
        :return:
        """
        r_school_info = self.search_schools(school_name)
        r_school_id = r_school_info['school_id']
        r_majors = self.get_majorlist_by_id(r_school_id)
        return r_majors

    def get_target_majors_of_school(self, school_name):
        r_school_info = self.search_schools(school_name)
        r_school_id = r_school_info['school_id']
        r_majors = self.get_majorlist_by_id(r_school_id)
        target_majors = []
        for _ in r_majors:
            major_id = _.get('id')
            major_code = _.get('major_code')
            major_rank = _.get('rank')
            major_name = _.get('major_name')
            follow_num = _.get('follow_num')
            parent = _.get('parent')
            major_type = _.get('major_type')
            school_num = _.get('school_num')
            exam_num = _.get('exam_num')
            week_exam_num = _.get('week_exam_num')
            print(f'id:{major_id}\n专业代码:{major_code}\n专业排名:{major_rank}\n专业名称:{major_name}\n关注人数:{follow_num}\nparent:{parent}\n专业类型:{major_type}\n学校数量:{school_num}\n今年备考人数:{exam_num}\n近7日新增人数:{week_exam_num}\n\n')
        return r_majors

    def get_departments_by_school_major(self, major_code):
        """
        通过专业代码获取学校学院信息
        :return:
        """
        pagelimit = '20'
        pagestart = '1'
        school_major_url = f'http://{self.host}/api-cpp/major/schools?major_id={major_code}&sort_by_school_rank=1&math_type=-1&study_type=-1&foreign_type=-1&limit={pagelimit}&page={pagestart}&is_edu=-1&is_local=-1&is_center=-1'
        headers = {
            'User-Agent': 'Mozilla/ (iPhone; CPU iPhone OS like Mac OS X)AppleWebKit/(KHTML, like Gecko) Mobile/KaoYanClub//K-Product-Line:kaoyan-app;/K-New-Product-Line:ky-app;/kmf_appinner;/appversion:4.3.4;',
            'Q-Organization': 'kaoyan',
        }
        all_result_data = []
        want_ret = []
        r = requests.get(school_major_url, headers=headers)
        r_json = json.loads(r.text)
        status = r_json['status']
        result = r_json['result']
        result_total = result['total']
        result_data = result['data']
        all_result_data += result_data
        while result_total - int(pagelimit) > 0:
            pagestart = str(int(pagestart) + 1)
            school_major_url = f'http://{self.host}/api-cpp/major/schools?major_id={major_code}&sort_by_school_rank=1&math_type=-1&study_type=-1&foreign_type=-1&limit={pagelimit}&page={pagestart}&is_edu=-1&is_local=-1&is_center=-1'
            r1 = requests.get(school_major_url, headers=headers)
            r1_json = json.loads(r1.text)
            r1_result = r1_json['result']
            r1_result_data = r1_result['data']
            all_result_data += r1_result_data
            result_total = result_total - int(pagelimit)
        # print(all_result_data)
        for _ in all_result_data:
            if _.get('school_name') in target_school_name:
                want_ret.append(_)
        return want_ret


class YanTuApi:
    """研途考研API"""
    def __init__(self, host=yantu_api_host):
        self.host = host

    def get_all_schools(self):
        pagelimit = '872'
        pagestart = '1'
        api_url = f'https://{self.host}/wx/v1/rcmd/search/school/?level=&mold=&page={pagestart}&size={pagelimit}'
        headers = {
            'auth-sys': 'rcmd',
            'User-Agent': '%E7%A0%94%E9%80%94%E8%80%83%E7%A0%94/2023071405 CFNetwork/1469 Darwin/23.0.0',
            'x-yt-application': 'wxapp',
        }
        r = requests.get(api_url, headers=headers)
        r_json = json.loads(r.text)
        code = r_json['code']
        msg = r_json['msg']
        data = r_json['data']
        data_count = data['count']
        data_results = data['results']
        return data_results

    def search_title_by_schoolcode_major_code(self, sch_code='10611', maj_code='081000'):
        """通过学校代码和专业代码返回信息"""
        api_url = f'https://{self.host}/wx/v1/rcmd/search/title/?school_code={sch_code}&major_code={maj_code}'
        headers = {
            'auth-sys': 'rcmd',
            'User-Agent': '%E7%A0%94%E9%80%94%E8%80%83%E7%A0%94/2023071405 CFNetwork/1469 Darwin/23.0.0',
            'x-yt-application': 'wxapp',
        }
        r = requests.get(api_url, headers=headers)
        r_json = json.loads(r.text)
        code = r_json['code']
        msg = r_json['msg']
        data = r_json['data']
        school_name = data['school_name']
        major_name = data['major_name']
        province = data['province']
        badge_url = data['badge_url']
        level = data['level']
        return data


if __name__ == '__main__':
    # kyb = KaoYanBangApi()
    # # ret_school = kyb.search_schools('重庆邮电大学')
    # # ret_school = kyb.get_majorlist_by_id('1902')
    # # ret_school = kyb.get_target_majors_of_school('重庆邮电大学')  # 重庆邮电大学 南方科技大学 重庆大学
    # # ret_school = kyb.get_target_schools()
    # ret_school = kyb.get_departments_by_school_major('20085400')
    # print(ret_school)
    # write_data_into_excel(xlspath='kyb_target_major_schools_20230804.xlsx', data_json_list=ret_school)

    yt = YanTuApi()
    all_schools = yt.search_title_by_schoolcode_major_code()
    print(all_schools)
