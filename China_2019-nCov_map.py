from fake_useragent import UserAgent
import requests
import json
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.commons.utils import JsCode
import os
class nCov_2019:
    #  伪造随机的User-Agent
    ua = UserAgent()
    def __init__(self):
        #  伪造随机的User-Agent
        ua = UserAgent()
        #  设置了一个headers，在构建request时传入，在请求时，就加入了headers传送，服务器若识别了是浏览器发来的请求，就会得到响应。
        self.headers = {
            #  伪造Chrome浏览器用户代理
            'User-Agent':ua.chrome
        }
        #  腾讯新闻网站疫情数据接口
        self.url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    #  解析接口数据
    def parse_url(self):
        response = requests.get(self.url,headers=self.headers)
        # 将请求到的数据转化为字典类型
        list_json = json.loads(response.text)
        #  返回接口数据信息
        return list_json

    def getDateList(self,list_json):
        #将data数据类型str，转成dict类型 方便操作数据
        #  当字典中，有键值为True或则False这种bool类型时，使用eval会报错NameError: name 'false' is not defined
        global false,null,true
        false = null = true = ""
        jo = list_json['data']
        # 将jo字符串数据转换为dict类型方便数据操作
        data = eval(jo)
        return data

    def main(self):
        list_json = self.parse_url()
        data = self.getDateList(list_json)
        return data

nCov_2019 = nCov_2019()
data = nCov_2019.main()
#  数据最新更新时间
lastUpdateTime = data['lastUpdateTime']
#  地区
area = []
#  现存确诊
nowConfirm = []
#  累积确诊
confirm = []
#  死亡人数
dead = []
#  治愈人数
heal = []
for i in range(34):
    #  获取添加中国各个省份名称
    area.append(data['areaTree'][0]['children'][i]['name'])
    #  获取添加中国各个省份现存确诊人数
    nowConfirm.append(data['areaTree'][0]['children'][i]['total']['nowConfirm'])
    #  获取添加中国各个省份累积确诊人数
    confirm.append(data['areaTree'][0]['children'][i]['total']['confirm'])
    #  获取添加中国各个省份死亡人数
    dead.append(data['areaTree'][0]['children'][i]['total']['dead'])
    #  获取添加中国各个省份治愈人数
    heal.append(data['areaTree'][0]['children'][i]['total']['heal'])
#  将数据封装成[‘北京’，[325,923,9,589]]这样的形式方便于数据可视化
data_pair = []
for i in range(34):
    x = []
    #  添加该省的累积确诊人数
    x.append(confirm[i])
    #  添加该省的死亡人数
    x.append(dead[i])
    #  添加该省的治愈人数
    x.append(heal[i])
    #  添加该省的现存确诊人数
    x.append(nowConfirm[i])
    #  将中国各省疫情数据添加到data_pair数组里
    data_pair.append(x)

testv = []

for i in range(34):
    # 向中国各省与该省疫情数据匹配
    testMap = [area[i],data_pair[i]]
    #获取整理各个省份确诊人数的信息
    testv.append(testMap)

c=(
    Map()
    #主要方法，用于添加图表的数据和设置各种配置项
    .add(
        #这个参数必须有，必须写，哪怕你传递一个空字符串，也要写，因为不写这个参数，会报错
        series_name = "",
        ## 数据项
        data_pair = testv,
        # mapType显示地图范围,为china,显示中国地图
        maptype = "china",
        #  去掉地图标识小红点
        is_map_symbol_show=False,
        #  是否显示标签
        label_opts =opts.LabelOpts(is_show = True),
        )

    #设置全局配置项
    .set_global_opts(

                        title_opts = opts.TitleOpts(
                                                        title="2020中国疫情地图",
                                                        subtitle = "XinXinM"+"\n\n\n全国各省份确诊人数分布\n\n截至: "+lastUpdateTime,

                                                    ),
                        visualmap_opts = opts.VisualMapOpts(
                                                                # 是否为分段型
                                                                is_piecewise=True,
                                                                # 自定义的每一段的范围，以及每一段的文字，以及每一段的特别的样式
                                                                pieces= [
                                                                          # 不指定 max，表示 max 为无限大（Infinity）。
                                                                          {"max": 0,"label":"0","color":"#ffffff"},
                                                                          {"min": 1, "max": 10,"color":"#ebb4a8"},
                                                                          {"min": 10, "max": 100,"color":"#e09694"},
                                                                          {"min": 100, "max": 500,"color":"#cb8382"},
                                                                          {"min": 500, "max": 1000,"color":"#b27372"},
                                                                          {"min": 1000, "color":"#976461"},
                                                                         ],
                                                                # 是否反转 visualMap 组件
                                                                is_inverse=True,
                                                                # visualMap 组件离容器右侧的距离
                                                                pos_right='right',
                                                            ),
                        tooltip_opts=opts.TooltipOpts(
                                                         # 提示框浮层的背景颜色。
                                                         background_color='white',
                                                         # 提示框浮层的边框宽。
                                                         border_width=1,
                                                         # 文字样式配置项，参考 `series_options.TextStyleOpts`
                                                         textstyle_opts=opts.TextStyleOpts(color='#00C791'),
                                                         # 回调函数，回调函数格式：
                                                         # (params: Object|Array) => string
                                                         # 参数 params 是 formatter 需要的单个数据集。
                                                         formatter=(JsCode(
                                                                             """
                                                                            
                                                                            function(params){
                                                                        
                                                                                                return params.name + ' : ' 
                                                                                                + '<br/>'
                                                                                                + '现存确诊：'+params.data.value[3] 
                                                                                                + '<br/>'
                                                                                                + '累积确诊：'+params.data.value[0] 
                                                                                                + '<br/>'
                                                                                                + '死亡人数：'+params.data.value[1] 
                                                                                                + '<br/>'
                                                                                                + '治愈人数：'+params.data.value[2];
                                                                            }
                                                                       """
                                                                            )
                                                                    )
                                                     )

                    )
    #   默认将会在根目录下生成一个 render.html 的文件，支持 path 参数，设置文件保存位置
    .render("China_2019-nCov_map.html"),

  )
#system函数可以将字符串转化成命令在服务器上运行，其会创建一个子进程在系统上执行命令行，子进程的执行结果无法影响主进程；
os.system("China_2019-nCov_map.html")











