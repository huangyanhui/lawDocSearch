import os
import time
import multiprocessing
from parser import Parser
from composite_word import CompositeWord


def run(source_path, target_path):
    target_file = open(target_path, 'a+')
    p = Parser(path=source_path)
    p.analyze()
    for _, value in p.pack.items():
        if type(value) is list:
            for __ in value:
                c = CompositeWord(__)
                s = ' '.join(c.new_list)
                target_file.write(s + '\n')

    target_file.close()


def main():
    source_path = '/home/cowlog/Dropbox/Project/刑事/提取/'
    target_path = '/home/cowlog/Dropbox/Project/刑事/object.txt'
    save_path = '/home/cowlog/Dropbox/Project/刑事/save_path.txt'
    # target_paths = [
    #     '/home/cowlog/Dropbox/Project/刑事/object_1.txt',
    #     '/home/cowlog/Dropbox/Project/刑事/object_2.txt',
    #     '/home/cowlog/Dropbox/Project/刑事/object_3.txt',
    #     '/home/cowlog/Dropbox/Project/刑事/object_4.txt',
    #     '/home/cowlog/Dropbox/Project/刑事/object_5.txt',
    # ]
    # pool = multiprocessing.Pool(processes=4)
    cnt = 0
    print('***************(START)*******************')
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    dir_list = os.listdir(source_path)
    for path in dir_list:
        cnt += 1
        try:
            run(source_path + path, target_path)
        except Exception as e:
            print('Exception: ' + str(e))
            save_file = open(save_path, 'a+')
            save_file.write(path + '\n')
            save_file.close()

        # pool.apply(run_it, (
        #     source_path + path,
        #     target_paths[cnt % 5],
        # ))
        # pool.close()
        # pool.join()
        if cnt % 10 == 0:
            print(time.strftime('%H:%M:%S', time.localtime(time.time())))
            print(cnt)
    print('***************( END )*******************')


if __name__ == '__main__':
    main()
