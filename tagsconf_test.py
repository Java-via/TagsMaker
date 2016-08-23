# _*_ coding: utf-8 _*_

config_tags_base = {
    "gender": {"show": "性别偏好", "value": {"male": "男", "female": "女", "unknown": "无偏向"}},
    "marital": {"show": "婚姻偏好", "value": {"unmarried": "未婚", "married": "已婚", "unknown": "无偏向"}},
    "havecar": {"show": "车辆偏好", "value": {"havecar": "有车", "nocar": "没车", "unknown": "无偏向"}},
    "age": {"show": "年龄偏好", "value": {"teen": "18岁以下", "youth": "18-24岁", "old_youth": "25-34岁",
                                      "earth_mid": "35-44岁", "over_mid": "45-54岁", "old": "55岁以上", "unknown": "无偏向"}},
    "degree": {"show": "学历偏好", "value": {"middle": "小学/初中", "high": "高中/中专/大专",
                                         "university": "大学及以上", "unknown": "无偏向"}},
}


config_tags_soft = {
    {"soft_classify": {"show": "应用类别", "value": {"shopping": "网上购物", "travelling": "旅游出行",
                                                "financial": "金融理财", "video": "视频", "music": "音乐",
                                                "photograph": "摄影摄像", "reading": "咨询阅读", "tools": "生活工具",
                                                "system": "系统工具", "decorate": "美化手机", "official": "效率办公",
                                                "social": "聊天社交", "telephony": "手机通讯", "map": "交通导航",
                                                "life": "生活服务", "sport": "运动健康", "education": "教育培训",
                                                "baby": "丽人母婴"}}},
    {"shopping": {"show": "网上购物", "value": {"shangcheng": "商城", "daogou": "导购", "haitao": "海淘",
                                           "tuangou_youhuiquan": "团购-优惠券", "wanggou": "网购",
                                           "gouwuyouhui": "购物优惠", "gouwu": "购物"}}} ,
    {"travelling": {"show": "旅游出行", "value": {"zonghelvyoufuwu": "综合旅游服务", "gonglue": "攻略"}}}
}.update(config_tags_base)


config_tags_base = [
    {
        "level": 1,
        "name": 人口属性
    }
]