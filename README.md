# 网站文献管理

本程序使用本地MongoDB数据库储存网站出版物。包含插入文献记录、更改文献记录、更新影响因子、常用查询，以及导出为HTML形式。

下载

```bash
git clone https://github.com/ixsluo/Publication_manager.git ~/Publication_manager
```

## 目录

- [文献格式](#文献格式)
- [使用说明](#使用说明)
    - [插入新数据](#插入新数据)
    - [更新影响因子](#更新影响因子)
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
|**JF**             |期刊名全称，必须包含在`tables/impact_df.xlms`<sup>2</sup>的所有期刊名中|
|C1                 |自定义标签1，分区，包括中科院分区(CAS)、中信所分区(ISTIC)、校分区等，通过相应表格自动读取<sup>3</sup>|
|C2                 |自定义标签2，影响因子。不推荐手动设定<sup>4</sup>|
|JA                 |期刊名标准缩写|
|PR                 |非标准标签，是否为预发表，是：1，否：0或不填该字段|
|**PY**             |出版年，YYYY|
|MO                 |出版月，MM|
|DA                 |日期，DD|
|Y1                 |主要日期，YYYY/MM/DD|
|Y2                 |访问日期|
|VL                 |卷|
|IS                 |期刊|
|SP                 |起始页码|
|EP                 |终止页码
|**DO**             |DOI，数字对象唯一标识符，**重要！！！**，请确保正确|
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

<sup>2</sup> 影响因子表格，pandas包DataFrame格式，建议通过`pd.ExeclWriter`生成。包括期刊全名和对应年的影响因子，默认序号为自动生成。若更新影响因子表格，请执行`python read_tables.py`确保读取正确。

|   |periodical|2019|...|
| - |   :-:    |:--:|:-:|
| 0 |p1        |1234|...|
| 1 |p2        |1234|...|
|...|...       |... |...|

<sup>3</sup> 期刊分区表，中科院分区、中信所分区，分别保存在`tables/cas.xlsx`、`tables/istic.xlsx`。

<sup>4</sup> 当给定正确的期刊名**JF**后，影响因子将通过文件`tables/impact_df.xlsx`读取覆盖写入，依次查找与PY同年的影响因子、上一年影响因子，若两年都没有，则不进行任何修改。

## 使用说明

配置文件举例：

```
> cat ~/args.conf
-u=publication_manager
-p=******
-c=test
```

### 插入新数据

`insert.py`查看参数说明

```bash
python ~/Publication_manager/insert.py -h
```

从配置文件读取参数并执行插入，如

```bash
python ~/Publication_manager/insert.py @~/args.conf -f=[ris file pattern]
```

### 更新影响因子

通过`tables/impact_df.xlsx`表格更新指定年份的所有文献的影响因子。当表格中无指定年份的数据时抛出异常。

```bash
python ~/Publication_manager/update_if.py @~/args.conf -y=[year]
```

### 更新期刊分区

通过`tables/cas.xlsx`或`tables/istic.xlsx`表格更新所有文献的分区，`--partition`参数指定更新哪个机构的分区。

```bash
python ~/Publication_manager/update_partition.py @~/args.conf  --partition=[istic/cas]
```

### MongoDB数据库

```
mongodb://<user>:<passwd>@<host>:<port>
```