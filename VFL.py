import os
import sys
import re
import Parse_ast
import Coverage
import SBFL_Formular as SF

languages = ['py', 'cpp', 'c']


def read_file(file_path):
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def is_operator(ch):

    op_list = '!@#$%^&*()_+{}|:\"<>?`-=[]\\;\',./ '
    # print(op_list)
    if op_list.find(ch) != -1:
        return True
    else:
        return False

def find_pos(str1, str2):
    str1_len = len(str1)
    while str2.find(str1) != -1:
        pos = str2.find(str1)
        # print(pos, len(str2))
        if pos == 0 and is_operator(str2[pos + str1_len]):
            return True
        elif pos == len(str2) - str1_len - 1 and is_operator(str2[pos - 1]):
            return True
        elif is_operator(str2[pos - 1]) and is_operator(str2[pos + str1_len]):
            return True
        str2 = str2[pos + str1_len : len(str2)]
    return False


def collect_variable_info(variable_name_list, file_path):

    variable_info = {}
    for i in range(len(variable_name_list)):
        variable_info[variable_name_list[i]] = []

    lines = read_file(file_path)
    for i in range(len(lines)):
        # if i != 3:
        #     continue
        for j in range(len(variable_name_list)):
            # if j != 3:
            #     continue
            # print(variable_name_list[j], lines[i])
            # print(find_pos(variable_name_list[j], lines[i]))
            if find_pos(variable_name_list[j], lines[i]):
                variable_info[variable_name_list[j]].append(i+1)
    
    return variable_info


def cal_N_tuple(passed_test_num, failed_test_num, lines_passed,  lines_failed):

    N_tuple = []
    line_num = len(lines_passed)  #其实比实际行数多一行，因为有个第0行
    for i in range(1, line_num):
        Ncf = lines_failed[i]
        Nuf = failed_test_num - lines_failed[i]
        Ncp = lines_passed[i]
        Nup = passed_test_num - lines_passed[i]
        # Tarantula = SF.cal_turantula(Ncf, Nuf, Ncp, Nup)
        Jaccard = SF.cal_jaccard(Ncf, Nuf, Ncp, Nup)
        # Naish = SF.cal_naish(Ncf, Nuf, Ncp, Nup)
        # GP08 = SF.cal_GP08(Ncf, Nuf, Ncp, Nup)
        # GP10 = SF.cal_GP10(Ncf, Nuf, Ncp, Nup)
        # GP11 = SF.cal_GP11(Ncf, Nuf, Ncp, Nup)
        # GP13 = SF.cal_GP13(Ncf, Nuf, Ncp, Nup)
        # GP20 = SF.cal_GP20(Ncf, Nuf, Ncp, Nup)
        # GP26 = SF.cal_GP26(Ncf, Nuf, Ncp, Nup)
        # print(i, Jaccard)
        N_tuple.append(Jaccard)
    return N_tuple  #返回值没有第0行

def get_SFL_rank(N_tuple):

    N_tuple_c = []
    for i in range(len(N_tuple)):
        N_tuple_c.append({
            'no': i + 1,
            'similarity': N_tuple[i]
        })
    N_tuple_c.sort(key=lambda s:(s['similarity']), reverse=True)
    SFL_rank = []
    for i in N_tuple_c:
        SFL_rank.append(i['no'])
    return SFL_rank

def cal_VFL_rank(N_tuple, variable_info):

    VFL_score = {}
    VFL_rank = []
    VFL_score_c = []

    for variable in variable_info:
        cover_line = variable_info[variable]
        ans = 0
        for i in cover_line:
            ans += N_tuple[i-1]
        if len(cover_line) == 0:
            VFL_score[variable] = 0
        else:
            VFL_score[variable] = ans / len(cover_line)
        VFL_score_c.append({
            'variable': variable,
            'score': VFL_score[variable]
        })
    VFL_score_c.sort(key=lambda s:(s['score']), reverse=True)
    for i in VFL_score_c:
        VFL_rank.append(i['variable'])
    # print(VFL_rank)
    return VFL_rank

def cal_final_rank(VFL_rank, SFL_rank, variable_info):

    final_rank = []
    for variable in VFL_rank:
        cover_line = variable_info[variable]
        cover_line_c = []
        for i in cover_line:
            cover_line_c.append({
                'no': i,
                'pos': SFL_rank.index(i)
            })
        cover_line_c.sort(key=lambda s:(s['pos']))
        for i in cover_line_c:
            try:
                final_rank.index(i['no'])
            except:
                final_rank.append(i['no'])
    return final_rank

def get_py_VFL_rank(file_path, test_dir_path):
    '''
    单个py文件的VFL排名
    '''
    variable_name_list = Parse_ast.get_py_variable_name_list(file_path)
    # print(variable_name_list)
    variable_info = collect_variable_info(variable_name_list, file_path)
    # print(variable_info)
    passed_test_num, failed_test_num, lines_passed,  lines_failed = Coverage.get_python_cov_info(file_path, test_dir_path)
    # print(lines_passed,  lines_failed)
    # return
    N_tuple = cal_N_tuple(passed_test_num, failed_test_num, lines_passed,  lines_failed)
    # print(N_tuple)
    SFL_rank = get_SFL_rank(N_tuple)
    # print(SFL_rank)
    VFL_rank = cal_VFL_rank(N_tuple, variable_info)
    final_VFL_rank = cal_final_rank(VFL_rank, SFL_rank, variable_info)
    print(final_VFL_rank)

def get_cpp_VFL_rank(file_path, test_dir_path):
    '''
    单个cpp文件的VFL排名
    '''
    variable_name_list = Parse_ast.get_cpp_variable_name_list(file_path)
    # print(variable_name_list)
    variable_info = collect_variable_info(variable_name_list, file_path)
    # print(variable_info)
    passed_test_num, failed_test_num, lines_passed,  lines_failed = Coverage.get_cpp_cov_info(file_path, test_dir_path)
    # print(lines_passed,  lines_failed)
    N_tuple = cal_N_tuple(passed_test_num, failed_test_num, lines_passed,  lines_failed)
    # print(N_tuple)
    SFL_rank = get_SFL_rank(N_tuple)
    VFL_rank = cal_VFL_rank(N_tuple, variable_info)
    final_VFL_rank = cal_final_rank(VFL_rank, SFL_rank, variable_info)
    print(final_VFL_rank)

def get_c_VFL_rank(file_path, test_dir_path):
    '''
    单个c文件的VFL排名
    '''
    variable_name_list = Parse_ast.get_cpp_variable_name_list(file_path)
    # print(variable_name_list)
    variable_info = collect_variable_info(variable_name_list, file_path)
    # print(variable_info)
    passed_test_num, failed_test_num, lines_passed,  lines_failed = Coverage.get_cpp_cov_info(file_path, test_dir_path)
    # print(lines_passed,  lines_failed)
    N_tuple = cal_N_tuple(passed_test_num, failed_test_num, lines_passed,  lines_failed)
    # print(N_tuple)
    SFL_rank = get_SFL_rank(N_tuple)
    VFL_rank = cal_VFL_rank(N_tuple, variable_info)
    final_VFL_rank = cal_final_rank(VFL_rank, SFL_rank, variable_info)
    print(final_VFL_rank)  # 最后排名在这里

def get_all_VFL_rank(file_dir_path, test_dir_path):
    '''
    一个文件夹内所有文件各自的VFL排名
    '''
    file_list = os.listdir(file_dir_path)
    count = 0
    for i in file_list:
        file_type = i.split('.')[-1]
        if file_type not in languages:
            continue
        
        file_path = os.path.join(file_dir_path, i)
        if not os.path.exists('log\\' + i + '\\'):
            os.makedirs('log\\' + i)
        
        print(file_path)
        # continue
        try:
            if file_type == 'py':
                get_py_VFL_rank(file_path, test_dir_path)
            elif file_type == 'cpp':
                get_cpp_VFL_rank(file_path, test_dir_path)
            elif filr_type == 'c':
                get_c_VFL_rank(file_path, test_dir_path)
        except:
            print('some error happend, pass')
            continue
        else:
            pass
        
        # count += 1
        # if count > 10:
        #     break

if __name__ == "__main__":
    
    file_path = r'..\TCG\data\3920\WA_py\502141.py'
    test_dir_path = r'..\TCG\data\3920\TEST_DATA'
    get_py_VFL_rank(file_path, test_dir_path)

    # file_path = r'..\data\3310\WA_cpp\287675.cpp'
    # test_dir_path = r'..\data\3310\TEST_DATA_TCG1'
    # get_cpp_VFL_rank(file_path, test_dir_path)
    
    # file_path = r'..\data\2174\WA_c\35505.c'
    # test_dir_path = r'..\data\2174\TEST_DATA_TCG1'
    # get_c_VFL_rank(file_path, test_dir_path)

    # file_dir_path = r'..\data\2174\WA_cpp'
    # test_dir_path = r'..\data\2174\TEST_DATA_TCG1'
    # get_all_VFL_rank(file_dir_path, test_dir_path)
    