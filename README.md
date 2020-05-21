## 邮件工具
本邮件工具可以直接发送邮件，或者启用监控服务，每当mail文件夹中有新的邮件文件时，发送新的邮件。  

### 文件夹结构
```text
 - data  # 邮件相关数据存放文件夹 
     - mail/         # 发送邮件存放文件夹
     - smtp-config/  # 发送邮箱的SMTP设置文件夹
     - template/     # 发送邮件HTML模板
     - sent-mail/    # 发送完成的邮件
     - mail.log      # mail-watcher的发送日志
- send_mail.py     # 发送邮件程序
- mail_watcher.py  # 监控并发送邮件程序
```

### 文件格式
#### SMTP配置文件
存放于smtp-config文件夹中，所有字段必填，**必须为json文件**  
**QQ_SMTP.json**
```json
{
    "host": "smtp.qq.com",  // smtp服务器
    "user": "abc@qq.com",  // 发送者邮箱名称
    "pwd": "xxxxxxxxx",   // 发送者smtp服务密码
    "port": 465,         // smtp ssl端口，不支持25端口
}
```

#### template的模板文件
**必须为html文件**   
待替换文本使用`{{text}}`表示，待替换图片使用`{{img}}`表示，并且可以使用css样式。  
后续传入的替换文本和图片的数量必须和模板中缺省的数量一致。  
**PRODUCT.html**
```html
<html>
    <body>
        产品: {{text}}
        图片: {{img}}
    </body>

    <style></style>
</html>
```

#### mail发送邮件格式
**必须为json文件**  
**普通文本邮件**  
```json
{
    "subject": "邮件主题",
    "msg": "邮件文本内容",
    "smtp": "QQ_SMTP",   // SMTP配置文件名，缺省.json后缀
    "receivers": ["xxxxx@163.com"]
}
```
  
**模板邮件**  
```json
{
    "subject": "邮件主题",
    "msg": "邮件文本内容",
    "smtp": "QQ_SMTP",      // SMTP配置文件名，缺省.json后缀
    "template": "PRODUCT",  // 模板文件名，缺省.html后缀
    "texts": ["xx"],        // 替换文本，数量需要和模板文件一致
    "imgs": ["xxx"],        // 替换图片的绝对路径，数量需要和模板文件一致
    "receivers": ["xxxxx@163.com"]
}
```

### 使用方法
首先至少配置一个smtp服务器配置文件，使用pip工具安装所需要的依赖`pip3 install -r requirement.txt`  

#### 使用send_mail发送邮件
按照上一章所提供的邮件模板编辑好要发送的邮件文件，使用`send_mail.py ...<邮件文件的绝对路径>`发送多个邮件，发送完成的邮件会被移动到`data/sent-mail/`文件夹中并且重命名为`<发送时间> <原文件名>`  

#### 使用mail_watcher监控data/mail文件夹并发送邮件
直接运行`mail_watcher.py`程序监控data/mail文件夹，按照格式编辑好要发送的邮件后直接将该邮件文件移动到data/mail文件夹中即可。