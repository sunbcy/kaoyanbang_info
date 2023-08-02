from api import KaoYanBangApi
from xlsx import write_data_into_excel


def main():
    kyb = KaoYanBangApi()
    ret_school = kyb.get_all_schools()
    write_data_into_excel('kyb_all_schools.xlsx', ret_school)


def second():
    kyb = KaoYanBangApi()
    ret_school = kyb.get_target_schools()
    write_data_into_excel('kyb_target_schools.xlsx', ret_school)


if __name__ == '__main__':
    # main()  # 全部院校
    second()  # 目标院校
