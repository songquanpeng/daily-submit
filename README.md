# 华南理工大学每日自动报平安

## 使用方法
1. 首先你必须手动填报并提交过一次。
2. clone 本项目：`git clone https://github.com/songquanpeng/daily-report`, 
服务器访问不了 Github 请使用：`git clone https://gitee.com/songquanpeng/daily-report` 。
3. 安装依赖（安装失败请见下面 Q&A）：
    ```shell script
    pip install playwright --user
    pip install requests
    python -m playwright install-deps
    python -m playwright install webkit
    ```
4. 给脚本执行权限：`chmod u+x ./main.py`
5. 手动运行一次脚本（务必在 `daily-report` 目录下运行）：`cd /path/to/daily-report/; ./main.py`，脚本将向你询问以下内容：
    1. 你的 ID，
    2. 统一认证密码，
    3. 消息推送 URL，该项可选，用于向你推送运行结果，详见下面 Q&A 第一项。
6. 设置 crontab 定时任务：
    1. 首先我们需要确定 Python 解释器的位置，终端执行命令 `which python`，输出可能为：`/home/user/anaconda3/bin/python`，
    1. 输入 `crontab -e`，
    2. 输入 `0 8 * * * cd /path/to/daily-report && /home/user/anaconda3/bin/python ./main.py`，
    注意，这里的项目路径和 Python 解释器的路径需要你根据你的情况进行修改，请使用绝对路径。
7. 一切 Okay，程序将在每日 8 点自动帮你报平安。

## Q&A
### 什么是消息推送 URL？
简而言之，就是一个 URL，在其后添加适当参数并发送 GET 请求访问后你将能收到消息。

你有两个选择：
1. 使用 [message-pusher](https://github.com/songquanpeng/message-pusher)，
则该项请填类似 `https://YOUR_DOMAIN.COM/PREFIX` 的内容；
2. 使用 [Server 酱](https://sct.ftqq.com/)，则该项请填类似 `https://sctapi.ftqq.com/<SENDKEY>.send` 的内容。

### 为什么一定要在 `daily-report` 目录下运行？
因为第一次运行后脚本将保存你的配置信息到工作目录，在 `daily-report` 目录下运行的目的就是确保脚本的工作目录是该目录。

### 依赖安装失败？报错：`cannot install dependencies for this linux distribution`
额，playwright 不支持你的发行版，目前无解。

### 为什么我手动执行可以成功运行，但是脚本并没有定时运行？
原因极有可能是 Python 环境的问题，你在终端运行的 Python 和 crontab 执行时用到的 Python 可能并不一样。

所以你需要用 `which python` 来找出你目前环境中的 Python，并在 crontab 的命令中指定使用该 Python 解释器来执行脚本。