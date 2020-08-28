import os
import sys
import shutil

##############################################
# 若是在win平台下实验，我强烈不建议修改这个路径  #
coverage_file_name = 'coverage.log'          #
temp_cpp_src_file = 'temp.cpp'               #
temp_py_src_file = 'temp.py'                 #
temp_output_file = 'temp.out'                #
temp_compile_file = 'temp'                   #
                                             #
##############################################

if sys.platform == "linux":
    COMLINE_PY_COV = "timeout 5 coverage run %s < %s > %s"
    COMLINE_PY_RUN = "timeout 5 python3 %s <%s >%s "
    COMLINE_PY2_RUN = "timeout 5 python2 %s <%s >%s "
    COMLINE_CPP_COM = "g++ -fprofile-arcs -ftest-coverage %s -o %s"
    COMLINE_CPP_RUN = "./%s <%s >%s"
    COMLINE_CPP_COV = "timeout 5 gcov %s"
else:
    COMLINE_PY_COV = "coverage run %s<%s > %s"
    COMLINE_PY_RUN = "python %s <%s >%s "
    COMLINE_CPP_COM = "g++ -fprofile-arcs -ftest-coverage %s -o %s"
    COMLINE_CPP_RUN = "%s<%s>%s"
    COMLINE_CPP_COV = "gcov %s"

def is_correct(now_output_file, output_file):

    with open(now_output_file, 'r') as f:
        temp_output_str = f.read()
    with open(output_file, 'r') as f:
        output_str = f.read()
    if temp_output_str == output_str:
        return True
    else:
        return False

def get_same(variable_cov_list, cover_lines):

    ans = 0
    for i in variable_cov_list:
        try:
            cover_lines.index(i)
            ans += 1
        except:
            continue
    return ans


def get_python_cover_line(src_file_path, input_file):

    cmd = COMLINE_PY_COV % (src_file_path, input_file, temp_output_file)
    os.system(cmd)
    os.system('coverage report -m > ' + coverage_file_name)
    with open(src_file_path, 'r') as f:
        line_num = len(f.readlines())
    cover_lines = []
    missing_lines = []
    for i in range(line_num):
        cover_lines.append(i + 1)
    with open(coverage_file_name, 'r') as f:
        text = f.readlines()[2] 
        items = text.split(' ')
        items = list(filter(lambda str: str != '' , items))
        items = items[4:len(items)]
        for item in items:
            item = item.replace(',', '').replace('\n', '')
            if item.find('-') == -1:
                missing_lines.append(int(item))
                cover_lines.remove(int(item))
            else:
                pre_line = int(item.split('-')[0])
                end_line = int(item.split('-')[1])
                for i in range(pre_line, end_line + 1):
                    missing_lines.append(i)
                    cover_lines.remove(i)
    return cover_lines, missing_lines

def get_python_cov_info(src_file_path, test_dir_path):

    if not os.path.exists('log/'):
        os.makedirs('log')

    failed_test_num = 0
    passed_test_num = 0
    lines_failed = []
    lines_passed = []
    with open(src_file_path, 'r') as f:
        line_num = len(f.readlines())
        for i in range(line_num + 1):
            lines_failed.append(0)
            lines_passed.append(0)
            
    if sys.platform == "linux":
        file_short_path = 'log/' + src_file_path.split('/')[-1] + '/'
    else:
        file_short_path = 'log/' + src_file_path.split('\\')[-1] + '/'
    shutil.copy(src_file_path, file_short_path + temp_py_src_file)
    os.chdir(file_short_path)
    test_dir_path = '../../' + test_dir_path
    # print(file_short_path)
    # return
    test_files = os.listdir(test_dir_path)
    for i in test_files:
        if ".in" not in i:
            continue
        input_file = os.path.join(test_dir_path, i)
        output_file = os.path.join(test_dir_path, i[: -2] + "out")

        # cmd = COMLINE_PY_RUN % (src_file_path, input_file, temp_output_file % (file_short_path))
        # try:
        #     os.system(cmd)
        # except:
        #     print('crashed')
        #     continue
        cover_lines, missing_lines = get_python_cover_line(temp_py_src_file, input_file)
        res = is_correct(temp_output_file, output_file)
        if res == True:
            passed_test_num += 1
        else:
            failed_test_num += 1
        for i in cover_lines:
            if res == True:
                lines_passed[i] += 1
            else:
                lines_failed[i] += 1

    os.chdir('../..')
    return passed_test_num, failed_test_num, lines_passed, lines_failed

def get_cpp_cover_line(src_file_path, input_file):

    cmd = COMLINE_CPP_COV % (src_file_path)
    os.system(cmd)
    cover_lines = []
    missing_lines = []

    with open('temp.cpp.gcov', 'r') as f:
        lines = f.readlines()
    for line in lines:
        items = line.replace(' ', '').split(':')
        if items[1] == '0':
            continue
        if items[0] == '#####':
            missing_lines.append(int(items[1]))
        else:
            cover_lines.append(int(items[1]))
    
    return cover_lines, missing_lines

def get_cpp_cov_info(src_file_path, test_dir_path):

    if not os.path.exists('log/'):
        os.makedirs('log')

    if sys.platform == "linux":
        file_short_path = 'log/' + src_file_path.split('/')[-1] + '/'
    else:
        file_short_path = 'log/' + src_file_path.split('\\')[-1] + '/'
    shutil.copy(src_file_path, file_short_path + temp_cpp_src_file)
    os.chdir(file_short_path)
    test_dir_path = '../../' + test_dir_path
    failed_test_num = 0
    passed_test_num = 0
    lines_failed = []
    lines_passed = []
    with open(temp_cpp_src_file, 'r') as f:
        line_num = len(f.readlines())
        for i in range(line_num + 1):
            lines_failed.append(0)
            lines_passed.append(0)

    test_files = os.listdir(test_dir_path)
    cmd1 = COMLINE_CPP_COM % (temp_cpp_src_file, temp_compile_file)
    os.system(cmd1)
    for i in test_files:
        if ".in" not in i:
            continue
        input_file = os.path.join(test_dir_path, i)
        output_file = os.path.join(test_dir_path, i[: -2] + "out")

        try:
            cmd2 = COMLINE_CPP_RUN % (temp_compile_file, input_file, temp_output_file)
            os.system(cmd2)
        except:
            print('crashed')
            continue
        cover_lines, missing_lines = get_cpp_cover_line(temp_cpp_src_file, input_file)
        # print(cover_lines, missing_lines)
        res = is_correct(temp_output_file, output_file)
        if res == True:
            passed_test_num += 1
        else:
            failed_test_num += 1
        for i in cover_lines:
            if res == True:
                lines_passed[i] += 1
            else:
                lines_failed[i] += 1
    
    os.chdir('../..')
    return passed_test_num, failed_test_num, lines_passed, lines_failed

if __name__ == "__main__":
    
    # src_file_path = r'..\TCG\data\3899\WA_py\498232.py'
    # test_dir_path = r'..\TCG\data\3899\TEST_DATA'

    src_file_path = r'..\oj数据集\data_cpp\1933\WA\2134.cpp'
    test_dir_path = r'..\oj数据集\data_cpp\1933\TEST_DATA'
    
    # passed_test_num, failed_test_num, lines_passed,  lines_failed = get_python_cov_info(src_file_path, test_dir_path)
    passed_test_num, failed_test_num, lines_passed, lines_failed = get_cpp_cov_info(src_file_path, test_dir_path)
    # print(passed_test_num, failed_test_num, lines_passed,  lines_failed)