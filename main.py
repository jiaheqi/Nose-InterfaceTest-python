import os
import sys

import click
import unittest
from BeautifulReport import BeautifulReport

from marmota import DingDing

DING_TOKEN = "8b2aee720f75e8e970b849663519d826907a8c6fc5815b6bdc7064de98f541ab"


def send_notification(option):
    if option == 'failure':
        color = '#FF0000'
    elif option == 'success':
        color = '#00FF00'
    else:
        color = '#FFA500'

    notifier = DingDing(DING_TOKEN)
    message = "### [Zeus 接口测试]: <font color={color}>{result}</font>\n " \
              "### 任务详情: {job_url} \n".format(color=color,
                                                  result=option,
                                                  job_url='{}{}/console'.format(
                                                      os.environ['JOB_URL'],
                                                      os.environ['BUILD_ID'])
                                                  )

    notifier.send_markdown("Test Results", message)


@click.group()
def cli():
    print("CI Cli")


@cli.command()
@click.option('-r', '--result',
              type=click.Choice(['success', 'failure', 'unstable']),
              required=True, help=u'发送消息选项')
def ding(result):
    send_notification(result)


@cli.command()
def run():
    test_suite = unittest.defaultTestLoader.discover('./tests', pattern='test*.py')
    result = BeautifulReport(test_suite)
    result.report(filename='index',
                  description='发行系统接口测试',
                  report_dir='report',
                  theme='theme_default')
    if result.fields.get("testFail"):
        print("失败的测试用例：")
        for r in result.fields.get('testResult'):
            if r.get("status") != "成功":
                print(f"{r['className']}\t{r['methodName']}\t{r['description']}\t{r['log']}")
    sys.exit(result.failure_count)


if __name__ == '__main__':
    cli()
