import os
import easygui as g

choice  = g.ccbox(msg='选择文件夹,程序将遍历文件夹内的所有图片，然后将识别后的结果存入到当前文件夹下的excel文件当中。'+os.linesep+os.linesep+os.linesep, title='请选择文件夹', choices=('选择文件夹','放弃'), image=None,
      default_choice='选择文件夹', cancel_choice='放弃')

if(choice):
    path = os.getcwd()
    a = g.diropenbox(msg="选择文件夹", title="选择工作目录", default=path)
    print(a)