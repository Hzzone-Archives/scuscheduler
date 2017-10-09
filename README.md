##### 四川大学课表生成ics文件, Python版本
###### 如何运行
需要先安装必要的依赖, 包括 requests, Beautifulsoup, ics, pytz.
以下命令进行安装：
```shell
pip3 install requests beautifulsoup4 ics pytz
```
具体执行如下：
* 替换config.py中的用户名和密码为自己的.
* 运行
```shell
python3 scheduler.py # 默认当前目录，生成courses.ics文件
python3 scheduler.py your_dir_path # 在指定目录，生成courses.ics文件
python3 scheduler.py your_file_path # 生成指定ics文件
```
* 目前只支持江安，望江华西和江安的作息差了十五分钟，判断一下校区就行，毕竟我四年江安，懒...
* 可能在解析课表的时候有错误，我自己测试非常完美，但是谢谢提issue.
* 先创建一个test日历再导入，如果正确则重命名，不然一个一个删挺麻烦的
* 最初的courses.ics是我的课表，别瞎导入...

###### 作用
ics文件是一种日历文件，包含一些行程安排把，比如地点，事件名，时间等信息。生成的ics文件可以导入Apple的日历，Google日历和Outlook日历等。     
更具体点的使用是：在 Mac上直接点击，在iOS上用日历打开，如果俩者都有，可以直接同步。对于Google日历，只需要把ics文件作为附件发送到邮箱里，会询问是否导入Google日历。    
在之后其他的日历应用都一个方法，更普及点，只需要订阅Apple日历或者Google日历就行了。     
个人更喜欢Apple和Google日历，因为原生集成在iOS或者android上，目前国内我觉得最好用的还是Apple日历。相对来说超级课程表和课程格子，太花哨，不喜。    
我想过分析超级课程表之类应用API，可以省去爬取课表的步骤，并且支持国内的大部分学校。懒，没时间，止步...

###### 效果截图
![](http://omoitwcai.bkt.clouddn.com/2017-10-09-IMG_1172.PNG)
![](http://omoitwcai.bkt.clouddn.com/2017-10-09-IMG_1173.PNG)