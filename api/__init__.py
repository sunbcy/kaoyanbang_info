import requests
import json
from conf import target_school_name
from urllib.parse import quote

api_host = 'api.qz100.com'


class KaoYanBangApi:
    def __init__(self, host=api_host):
        self.host = host

    def get_schools(self):
        api_url = f'http://{self.host}/api-cpp/major/schools?school_name=&page=1&limit=20&sort_type=1&school_type=-1&is_edu=-1&is_local=-1&is_center=-1'
        headers = {
            'Authorization': 'Bearer null',
            'Sec-Fetch-Site': 'same-site',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Q-Organization': 'kaoyan',
            'Origin': 'https://activity.qz100.com',
            'User-Agent': 'Mozilla/ (iPhone; CPU iPhone OS like Mac OS X) AppleWebKit/(KHTML, like Gecko) Mobile/KaoYanClub//K-Product-Line:kaoyan-app;/K-New-Product-Line:ky-app;/kmf_appinner;/appversion:4.3.4;',
            'Referer': 'https://activity.qz100.com/',
            'Accept': 'application/json, text/plain, */*'
        }
        r = requests.get(api_url, headers=headers)
        r_json = json.loads(r.text)
        status = r_json['status']
        result = r_json['result']
        result_from = result['from']
        result_per_page = result['per_page']
        result_total = result['total']
        result_data = result['data']

        print(r_json)

        # for _ in result_data:
        #     school_id = _.get('school_id')
        #     school_code = _.get('school_code')
        #     school_name = _.get('school_name')
        #     badge = _.get('badge')
        #     is_211 = _.get('is_211')
        #     is_985 = _.get('is_985')
        #     is_score = _.get('is_score')
        #     follow_num = _.get('follow_num')  # 关注人数
        #     is_first_class = _.get('is_first_class')
        #     departments = _.get('departments')
        #     province_id = _.get('province_id')
        #     province_name = _.get('province_name')
        #     is_other = _.get('is_other')
        #     school_type = _.get('school_type')
        #     is_edu = _.get('is_edu')
        #     is_local = _.get('is_local')
        #     is_center = _.get('is_center')
        #     exam_num = _.get('exam_num')  # 今年备考人数
        #     week_exam_num = _.get('week_exam_num')  # 近7日新增
        #     bbs_id = _.get('bbs_id')
        #     student_recruitment = _.get('student_recruitment')



            # if school_name in target_school_name:
            #     print(f'{school_name}\n关注人数:{follow_num}\n所属省份:{province_name}\n今年备考人数:{exam_num}\n' +
            #           f'近7日新增:{week_exam_num}\n学生官网:{student_recruitment}\n\n')
            # break

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
        pages = result_total / int(pagelimit)
        page_ = result_total % int(pagelimit)
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
        获得全量的学校的专业
        :param school_name:学校名
        :return:
        """
        r_school_info = self.search_schools(school_name)
        r_school_id = r_school_info['school_id']
        r_majors = self.get_majorlist_by_id(r_school_id)
        # print(r_majors[0])
        # quit()
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

    # def get_target_school_majors_info

if __name__ == '__main__':
    kyb = KaoYanBangApi()
    # ret_school = kyb.search_schools('重庆邮电大学')
    # ret_school = kyb.get_majorlist_by_id('1902')
    # ret_school = kyb.get_target_majors_of_school('重庆邮电大学')  # 重庆邮电大学 南方科技大学 重庆大学
    ret_school = kyb.get_schools()
    print(ret_school)