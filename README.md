# Dashboard

## 基本功能

* ssh keys 管理
* apps 管理，主要是 nginx 配置文件

## 高级功能

* 服务器运行状态

## 运行

    git clone git@github.com:ratazzi/dashboard.git
    virtualenv /opt/dashboard/runtime
    /opt/dashboard/runtime/bin/pip install -r dashboard/requirements.txt
    /opt/dashboard/runtime/bin/python dashboard/dashboard/app.py
