### 本地安装
1. clone一个其他仓库到自己的机器上
`git clone git@github.com:YapAmbition/contribution_draw.git` 

2. 打开`exec.py` ，把变量`git_repository_path` 修改为第1步仓库的路径，把变量`write_file` 修改为仓库中用来写入的文件名
3. 还是打开`exec.py` ，修改变量`templates` 数组，数字**`1`** 表示自动push，数字**`0`**表示什么都不做。`templates` 每个数组有7行，不能增多或者减少，因为这对应着contribution图的7行，列数可以随意增加减少。你可以用数组的数字绘制成一个图案
4. 想办法每天调用一次`exec.py` (这里我推荐用linux服务器中的crontab来调用)，传入三个参数，分别是调用这个脚本的开始年月日。例如我打算从今天开始调用这个脚本，那么我每天都这么调用这个脚本: 
`python3 exec.py 2022 10 9` 

### 原理
每天调用时根据传入的开始时间与当前时间做比较，在`templates` 中找到对应的数字，如果数字大于0就会自动push一下，目的是点亮github中今天的contribution活动图