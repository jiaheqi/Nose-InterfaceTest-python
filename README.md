# Nose-InterfaceTest-python
基于 nose 和 requests 的纯接口自动化，语言使用 python3
## 目录结构
1. tests 存放所有测试用例
2. test/components 存放所有公用组件
3. Jenkinsfile Jenkins 的自动测试任务配置
4. main.py 启动入口
## 快速开始
1. 依赖安装
    ```shell
        pip install -r requirements.txt
    ```
2. 运行测试
    ```shell
        python main.py 
   ```
3. 测试报告生成在 report 目录下
4. 钉钉发送消息通知（如果测试失败发送）