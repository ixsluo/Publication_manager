# 网站文献管理

本程序使用本地MongoDB数据库储存网站出版物。包含插入文献记录、更改文献记录、更新影响因子、常用查询，以及导出为HTML形式。

## 目录

- [文献格式](#文献格式)
- [使用说明](#使用说明)
    - [插入新数据](#插入新数据)
    - 
## 文献格式

导入文献格式为RIS([RIS wikipedia](https://en.wikipedia.org/wiki/RIS_(file_format)))，每一行为两大写字母的关键字、两个空格、连词符’-‘、内容。一个ris文件内可以包含多条文献记录，每条记录以’TY‘关键字起，’ER‘关键字止。
    
    key  - value

文件请使用UTF-8编码。本程序并不强制要求CRLF换行符（Unix等下通常为LF），但RIS标准为CRLF换行符。

关键字含义如下表：
|key|meaning|
|:-:| :----- |
|**TY**             |参考文献类型，必须是每一记录的第一行|
|**TI**             |标题|
|*T1*               |主标题，可写HTML格式|
|**AU**             |作者，每个作者单独一行，[lastname, firstname midname]或[firstname midname lastname]|
|**A1**             |第一作者，每个作者单独一行|
|**A0**<sup>1</sup> |非标准标签，通讯作者，每个作者单独一行|
|**JF**             |期刊名全称，必须包含在impact/impact_df.xlms<sup>2</sup>的所有期刊名中|
|C2                 |自定义标签2，影响因子。不推荐手动设定<sup>3</sup>|
|JA                 |期刊名标准缩写|
|**PY**             |出版年，写为YYYY|
|DA                 |日期|
|Y1                 |主要日期|
|Y2                 |访问日期|
|VL                 |卷|
|IS                 |期刊|
|SP                 |起始页码|
|EP                 |终止页码
|**DO**             |DOI，数字对象唯一标识符|
|*UR*               |URL，链接|
|SN                 |ISBN/ISSN|
|AB                 |摘要|
|N1                 |备注|
|N2                 |摘要|
|ID                 |Reference ID|
|**ER**             |记录终止，必须是每一记录的最后一行|
|||
**粗体**为必需字段，*斜体*为建议填写字段

</br>

<sup>1</sup> A0不是标准关键字，在此自定义为通讯作者

<sup>2</sup> 影响因子表格，pandas包DataFrame格式，建议通过`pd.ExeclWriter`生成。包括期刊全名和对应年的影响因子，默认序号为自动生成。若更新影响因子表格，请执行`python impact.py`确保读取正确。

|   |periodical|2019|...|
| - |   :-:    |:--:|:-:|
| 0 |p1        |1234|...|
| 1 |p2        |1234|...|
|...|...       |... |...|

<sup>3</sup> 当给定正确的期刊名**JF**后，影响因子将通过文件impact/impact_df.xlsx读取覆盖写入，依次查找与PY同年的影响因子、上一年影响因子，若两年都没有，则不进行任何修改。

## 使用说明

### 插入新数据



### MongoDB数据库

```
mongodb://<user>:<passwd>@<host>:<port>
```