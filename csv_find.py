import logging


class Solution:
    # array 二维列表
    def Find(self, target, array):
        find_list =[]
        # write code here
        if not array or not array[0] or target is None:
            return False,''
        # if array[0][0] > target or array[-1][-1] < target:
        #     return False
        rows, cols = len(array), len(array[0])
        # 从左到右依次遍历
        r, c = 0, 0
        for r in range(rows):
            for c in range(cols):
                try:
                    if array[r][c] == target:
                        # 2021-11-5修改:匹配成功后,将所在行数保存至列表中
                        find_list.append(r)
                except IndexError as e:
                    break
                else:
                    continue
        if len(find_list) == 0:              
            return False,''
        else :
            return True,find_list

if __name__ == '__main__':
    target = '127.0.0.1:22'
    array = [['IP', '端口', '主机端口', '协议', 'state', '服务'], ['127.0.0.1', '22', '127.0.0.1:22', 'tcp', 'closed', 'unknown'], ['127.0.0.1', '22', '127.0.0.1:22', 'tcp', 'closed', '1234']]
    s = Solution()
    # return  T/F 目标所在行数
    tmp = s.Find(target, array)
    print(tmp)
