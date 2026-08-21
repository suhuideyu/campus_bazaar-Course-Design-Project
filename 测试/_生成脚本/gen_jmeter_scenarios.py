# -*- coding: utf-8 -*-
"""
生成 JMeter 并发压测场景配置文件（.jmx）。
5 个场景：
  01_登录并发压测     150 用户 / 30s 爬坡 / 5min
  02_首页浏览压测     150 用户 / 30s 爬坡 / 5min
  03_搜索压测         100 用户 / 20s 爬坡 / 5min
  04_下单流程压测     80 用户 / 30s 爬坡 / 5min（登录→商品列表→下单）
  05_混合业务压测     150 用户 / 40s 爬坡 / 10min（多接口混合）
运行：python gen_jmeter_scenarios.py
"""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "05_性能与自动化测试", "JMeter压测场景")

def body_arg(json_body):
    return ('<elementProp name="" elementType="HTTPArgument">'
            '<boolProp name="HTTPArgument.always_encode">false</boolProp>'
            '<stringProp name="Argument.value">%s</stringProp>'
            '<stringProp name="Argument.metadata">=</stringProp>'
            '</elementProp>' % escape(json_body))

def http_sampler(name, path, method="GET", json_body=None, extract=None, id=None):
    s = ['<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="%s" enabled="true">' % name]
    if json_body is not None:
        s.append('<elementProp name="HTTPsampler.Arguments" elementType="Arguments" '
                 'guiclass="HTTPArgumentsPanel" testclass="Arguments" testname="请求参数" enabled="true">')
        s.append('<collectionProp name="Arguments.arguments">')
        s.append(body_arg(json_body))
        s.append('</collectionProp></elementProp>')
    s += ['<stringProp name="HTTPSampler.domain">localhost</stringProp>',
          '<stringProp name="HTTPSampler.port">8080</stringProp>',
          '<stringProp name="HTTPSampler.protocol">http</stringProp>',
          '<stringProp name="HTTPSampler.path">%s</stringProp>' % path,
          '<stringProp name="HTTPSampler.method">%s</stringProp>' % method,
          '<boolProp name="HTTPSampler.follow_redirects">true</boolProp>',
          '<boolProp name="HTTPSampler.postBodyRaw">true</boolProp>' if json_body is not None else '',
          '<stringProp name="HTTPSampler.contentEncoding">UTF-8</stringProp>',
          '</HTTPSamplerProxy>']
    if extract:
        s.append('<RegexExtractor guiclass="RegexExtractorGui" testclass="RegexExtractor" '
                 'testname="%s" enabled="true">' % extract[0])
        s += ['<stringProp name="RegexExtractor.useHeaders">false</stringProp>',
              '<stringProp name="RegexExtractor.refname">%s</stringProp>' % extract[1],
              '<stringProp name="RegexExtractor.regex">%s</stringProp>' % escape(extract[2]),
              '<stringProp name="RegexExtractor.template">%s</stringProp>' % extract[3],
              '<stringProp name="RegexExtractor.match_number">1</stringProp>',
              '<stringProp name="RegexExtractor.default">%s</stringProp>' % extract[4],
              '</RegexExtractor>']
    return "\n".join(x for x in s if x)

COOKIE_MGR = ('<CookieManager guiclass="CookiePanel" testclass="CookieManager" '
              'testname="HTTP Cookie 管理器（登录态）" enabled="true">'
              '<collectionProp name="CookieManager.cookies"/>'
              '<boolProp name="CookieManager.clearEachIteration">false</boolProp>'
              '</CookieManager>')

AGG = ('<AggregateReport guiclass="AggregateReportGui" testclass="AggregateReport" '
       'testname="聚合报告" enabled="true"><stringProp name="filename"></stringProp>'
       '</AggregateReport>')

SUMMARY = ('<ResultCollector guiclass="SummaryReport" testclass="ResultCollector" '
           'testname="汇总报告" enabled="true"><boolProp name="ResultCollector.error_logging">false</boolProp>'
           '<objProp><name>saveConfig</name><value class="SampleSaveConfiguration">'
           '<time>true</time><latency>true</latency><timestamp>true</timestamp><success>true</success>'
           '<label>true</label><code>true</code><message>true</message>'
           '</value></objProp></ResultCollector>')

def thread_group(name, threads, ramp, duration, loops="1"):
    return ('<ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="%s" enabled="true">'
            '<stringProp name="ThreadGroup.on_sample_error">continue</stringProp>'
            '<elementProp name="ThreadGroup.main_controller" elementType="LoopController" '
            'guiclass="LoopControlPanel" testclass="LoopController" testname="循环控制器" enabled="true">'
            '<boolProp name="LoopController.continue_forever">false</boolProp>'
            '<stringProp name="LoopController.loops">%s</stringProp>'
            '</elementProp>'
            '<stringProp name="ThreadGroup.num_threads">%d</stringProp>'
            '<stringProp name="ThreadGroup.ramp_time">%d</stringProp>'
            '<boolProp name="ThreadGroup.scheduler">true</boolProp>'
            '<stringProp name="ThreadGroup.duration">%d</stringProp>'
            '<stringProp name="ThreadGroup.delay"></stringProp>'
            '</ThreadGroup>' % (name, loops, threads, ramp, duration))

def build_jmx(plan_name, scenario_name, threads, ramp, duration, samplers, extractor_extra=""):
    head = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<jmeterTestPlan version="1.2" properties="5.0" jmeter="5.6.3">\n<hashTree>\n'
            '<TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="%s" enabled="true">\n'
            '<stringProp name="TestPlan.comments">%s</stringProp>\n'
            '<boolProp name="TestPlan.functional_mode">false</boolProp>\n'
            '<boolProp name="TestPlan.serialize_threadgroups">false</boolProp>\n'
            '<elementProp name="TestPlan.user_defined_variables" elementType="Arguments" '
            'guiclass="ArgumentsPanel" testclass="Arguments" testname="用户定义变量" enabled="true">\n'
            '<collectionProp name="Arguments.arguments"/>\n</elementProp>\n</TestPlan>\n<hashTree>\n' % (plan_name, scenario_name))
    body = [thread_group(scenario_name, threads, ramp, duration), "<hashTree>", COOKIE_MGR]
    for s in samplers:
        body.append(s)
    body += [AGG, SUMMARY, "</hashTree>", "</hashTree>", "</hashTree>", "</jmeterTestPlan>"]
    return head + "\n".join(body)

# ============================================================
# 场景1：登录并发
# ============================================================
s1 = [
    http_sampler("登录 /api/users/login", "/api/users/login", "POST",
                 json_body='{"username":"zhangsan","password":"123456"}'),
]
jmx1 = build_jmx("CampusBazaar-登录并发压测", "登录并发（150并发/5min）", 150, 30, 300, s1)

# ============================================================
# 场景2：首页浏览
# ============================================================
s2 = [
    http_sampler("首页商品列表", "/api/items", "GET",
                 json_body='{"pageNum":1,"pageSize":10}'),
]
jmx2 = build_jmx("CampusBazaar-首页浏览压测", "首页商品列表浏览（150并发/5min）", 150, 30, 300, s2)

# ============================================================
# 场景3：商品搜索
# ============================================================
s3 = [
    http_sampler("商品搜索", "/api/items", "GET",
                 json_body='{"keyword":"%E6%95%99%E6%9D%90","pageNum":1,"pageSize":10}'),
]
jmx3 = build_jmx("CampusBazaar-搜索压测", "商品搜索（100并发/5min）", 100, 20, 300, s3)

# ============================================================
# 场景4：下单核心流程（登录→列表→下单）
# ============================================================
s4 = [
    http_sampler("登录", "/api/users/login", "POST",
                 json_body='{"username":"zhangsan","password":"123456"}'),
    http_sampler("获取在售商品", "/api/items", "GET",
                 json_body='{"pageNum":1,"pageSize":5}',
                 extract=("提取首个在售商品ID", "itemId",
                          '"list":\[\{"id":(\d+),', "$1$", "1")),
    http_sampler("提交订单", "/api/orders", "POST",
                 json_body='{"itemId":${itemId},"message":"JMeter压测下单","meetPlace":"第一食堂门口"}'),
]
jmx4 = build_jmx("CampusBazaar-下单流程压测", "下单核心流程（80并发/5min）", 80, 30, 300, s4)

# ============================================================
# 场景5：混合业务
# ============================================================
s5 = [
    http_sampler("登录", "/api/users/login", "POST",
                 json_body='{"username":"zhangsan","password":"123456"}'),
    http_sampler("首页列表", "/api/items", "GET", json_body='{"pageNum":1,"pageSize":10}'),
    http_sampler("商品详情", "/api/items/1", "GET"),
    http_sampler("商品搜索", "/api/items", "GET", json_body='{"keyword":"%E6%95%99%E6%9D%90"}'),
    http_sampler("分类列表", "/api/categories", "GET"),
    http_sampler("我的订单", "/api/orders/buy", "GET"),
]
jmx5 = build_jmx("CampusBazaar-混合业务压测", "混合业务（150并发/10min）", 150, 40, 600, s5)

SCENARIOS = [
    ("01_登录并发压测.jmx", jmx1),
    ("02_首页浏览压测.jmx", jmx2),
    ("03_商品搜索压测.jmx", jmx3),
    ("04_下单流程压测.jmx", jmx4),
    ("05_混合业务压测.jmx", jmx5),
]

for fname, content in SCENARIOS:
    path = os.path.join(OUT, fname)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("生成: %s (%d 字符)" % (fname, len(content)))
