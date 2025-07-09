# 简介

> 本项目基于[ntwork](https://https://github.com/dev-kang/ntwork)
> 
> **本项目仅供学习和技术研究，请勿用于非法用途，如有任何人凭此做何非法事情，均于作者无关，特此声明。**

- 项目支持功能如下：

- [x] **WeCom** ：PC端的个微消息通道，依赖 [ntwork项目](https://https://github.com/dev-kang/ntwork) ，最高支持Python310环境版本，限[WeCom4.0.0.6027版本](https://dldir1.qq.com/wework/work_weixin/WeCom_4.0.8.6027.exe)，定时发送消息文本

# 快速开始

## 准备

### 1.运行环境

仅支持Windows 系统同时需安装 `Python`。

> 建议Python版本在 3.7.1~3.10 之间。编写时采用pythom3.10

**(1) 下载项目代码：**

```bash
git clone https://github.com/NKU-WIKI/nkuwiki-wework
cd nkuwiki-wework
```

**(2) 安装依赖 ：**

```bash
pip3 install -r requirements.txt
```

**(3) 安装指定版本的企业微信，并且在app.py中填写mysql的登录信息**

## 2.运行

### 本地运行（仅限window平台）

如果是开发机 **本地运行**，直接在项目根目录下执行：

```bash
python3 app.py
```