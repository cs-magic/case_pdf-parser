# Analysis

## Tips

### 字体颜色是不可靠的

14:18:53 | [6 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/9.9884_2024_ValTR_unep_gef_msp.pdf
14:19:04 | found table at page(71-78)

![img.png](../assets/unreliable-font-color.png)

### 表头是不可靠的

![img.png](../assets/unreliable-header.png)

## Bad Cases

### [Solved] 诡异重复

#### bugs

14:19:26 | [10 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/16.2023I_2024_TR_unep_UNDA_Cycling%20Policies.pdf
14:19:32 | [DUPLICATE], last table at page(92-93), current page at 94
![img.png](../assets/wield-refound.png)

14:19:32 | [11 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/17.2010_2024_ValTR_unep.pdf
14:19:39 | [DUPLICATE], last table at page(74-77), current page at 78
![img.png](../assets/wield-refound-2.png)

#### 解决方案

把含 col.. 的空列去掉就行了。

```
2024-11-15 15:08:09 | DEBUG |   page 92
2024-11-15 15:08:09 | DEBUG |   found table in page(92), header_names:
['Criterion', 'Col1', 'Col2', 'Summary Assessment', 'Rating', 'Col5', 'Col6']
2024-11-15 15:08:09 | DEBUG |   page 93
2024-11-15 15:08:09 | DEBUG |   found table in page(93), header_names:
['Criterion', 'Col1', 'Col2', 'Summary Assessment', 'Rating', 'Col5', 'Col6']
2024-11-15 15:08:09 | DEBUG |   page 94
2024-11-15 15:08:09 | DEBUG |   found table in page(94), header_names:
['Criterion', 'Col1', 'Col2', 'Summary Assessment', 'Col4', 'Rating', 'Col6', 'Col7']
2024-11-15 15:08:09 | WARNING | [DUPLICATE], last table at page(92-93), current page at 94
```

但是竟然还有单元格重复的……

![img.png](../assets/cell-duplication.png)

### 定义表误匹配

> 一般只有一级指标，以及两列，但也有三列的（122#10 加 ref.)等

```
Criterion Rating
Strategic Relevance Highly Satisfactory
Quality of Project Design Satisfactory
Nature of External Context Favorable
Effectiveness Highly Satisfactory
Financial Management Satisfactory
Efficiency Moderately Unsatisfactory
Monitoring and Reporting Moderately Unsatisfactory
Sustainability Moderately Unlikely
Factors Affecting Performance Satisfactory
Overall Project Performance Rating Satisfactory
```

14:06:22 | [3 / 444] parsing file:
///Users/mark/Documents/Terminal%20evaluation%20report/4.2007_2024_te_unep_spes_global_Enironment%20education%20Youth.pdf
14:06:26 | [DUPLICATE], last table at page(13-13), current page at 56
![img.png](../assets/definition-table.png)

14:19:12 | [8 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/12.5283_2024_te_unep_gef_sphpe_speg_Africa_LMO%20Testing.pdf
14:19:18 | [DUPLICATE], last table at page(15-15), current page at 79
![img.png](../assets/definition-table-2.png)

### 列在视觉上 ok，但解析出来有问题

17:40:01 | [153 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/190.4139_2021_te_unep_gef_msp_spcc_energy_efficient_lighting_in_Morocco.pdf
17:40:08 | page: 87, headers: ['criterion', 's ummary assessment', 'rating']
17:40:08 | page: 88, headers: ['criterion', 'summary assessment', 'rating']
![img.png](../assets/column-inconsistency.png)

### 列需要向下合并

> 这种一般是紧接着出错，即 56-59，然后 60 出错，但是不能直接连接，因为会有脏行
> 解决办法有二：
> 1. 【暴力】按照 顺序或者 sentiment 进行列对齐，然后删除 criterion 为空的行
> 2. 【推荐】先合并列，以\n合并编码，再对齐

16:50:37 | [44 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/57.01607_02088_2023_ValTR_unep_TTVC.pdf
16:50:42 | [DUPLICATE], last table at page(61-68), current page at 69
![img.png](../assets/merge-down-header.png)

16:51:27 | [71 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/90.9820_2023_ValTR_unep_gef_msp_CBIT%20Ghana.pdf
16:51:32 | [DUPLICATE], last table at page(42-45), current page at 46
![img.png](../assets/merge-down-header-2.png)

### 表格和表名连在了一起

17:06:41 | [89 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/117.PIMS%20Id%2001659%2002032_2023_Partnership_for%20Action_On_Green_Economy%20_PAGE_Op%20Strategy.pdf
17:06:49 | [DUPLICATE], last table at page(16-16), current page at 83
![img.png](../assets/name-join.png)

17:35:29 | [129 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/165.4934_2022_te_unep_gef_fsp_spcc_Global_EbA-South.pdf
2024-11-15 17:35:29 | DEBUG |   page 15
2024-11-15 17:35:30 | DEBUG | headers: ['key findings']
2024-11-15 17:35:30 | DEBUG |   page 16
2024-11-15 17:35:30 | INFO | page: 16, headers: ['criterion', 'summary assessment', 'rating']
2024-11-15 17:35:30 | DEBUG |   page 17
2024-11-15 17:35:30 | INFO | page: 17, headers: ['criterion', 'summary assessment', 'rating']
2024-11-15 17:35:30 | DEBUG |   page 18
2024-11-15 17:35:30 | INFO | page: 18, headers: ['criterion', 'summary assessment', 'rating']

### 表格重复

17:29:47 | [125 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/161.1215_5319_5615_unep_undp_gef_capacity_for_ldc_negotiators.pdf
17:29:48 | page: 10, headers: ['criterion', 'summary assessment', 'rating']
17:29:48 | page: 11, headers: ['criterion', 'summary assessment', 'rating']
17:29:48 | page: 12, headers: ['criterion', 'summary assessment', 'rating']
17:29:48 | page: 13, headers: ['criterion', 'summary assessment', 'rating']
17:29:51 | page: 64, headers: ['criterion', 'summary assessment', 'rating']
17:29:52 | page: 65, headers: ['criterion', 'summary assessment', 'rating']
17:29:52 | page: 66, headers: ['criterion', 'summary assessment', 'rating']
17:29:52 | page: 67, headers: ['criterion', 'summary assessment', 'rating']

### 两种不同目的的表格

17:36:58 | [136 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/173.01951_2021_te_unep_speg_Global_Illicit%20Trade%20in%20Wildlife.pdf
17:37:01 | page: 73, headers: ['criterion', 'summary assessment', 'rating']
17:37:02 | page: 74, headers: ['criterion', 'summary assessment', 'rating']
17:37:02 | page: 75, headers: ['criterion', 'summary assessment', 'rating']
17:37:02 | page: 76, headers: ['criterion', 'summary assessment', 'rating']
17:37:02 | page: 77, headers: ['criterion', 'summary assessment', 'rating']
17:37:05 | page: 117, headers: ['criterion', 'summary assessment/comments', 'rating']
17:37:05 | page: 118, headers: ['criterion', 'summary assessment/comments', 'rating']
17:37:05 | page: 119, headers: ['criterion', 'summary assessment/comments', 'rating']
17:37:05 | page: 120, headers: ['criterion', 'summary assessment/comments', 'rating']

![img.png](../assets/diff-table-1.png)

![img_1.png](../assets/diff-table-2.png)

### 表头不跨页（仅一页的一般也是有问题的）

17:42:13 | [162 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/199.4930_2020_te_unep-gef_global_bd_seagrass_eocystems_of_dugongs_Indian_and%20pacific%20oceans.pdf
17:42:17 | page: 76, headers: ['criterion', 'summary assessment', 'rating']
17:42:17 | page: 77, headers: ['criterion', 'summary assessment', 'rating']
17:42:17 | page: 78, headers: ['criterion', 'summary assessment', 'rating']
17:42:17 | page: 79, headers: ['criterion', 'summary assessment', 'rating']
17:42:19 | page: 99, headers: ['criterion', 'summary assessment', 'rating']
17:42:19 | page: 100, headers: ['criterion', 'summary assessment', 'rating']
17:42:19 | page: 101, headers: ['criterion', 'summary assessment', 'rating']
17:42:21 | page: 122, headers: ['criterion', 'summary assessment', 'rating'] <--
17:42:22 | page: 146, headers: ['criterion', 'summary assessment', 'rating']
17:42:23 | page: 167, headers: ['criterion', 'summary assessment', 'rating']
17:42:23 | page: 168, headers: ['criterion', 'summary assessment', 'rating']
17:42:23 | page: 169, headers: ['criterion', 'summary assessment', 'rating']
17:42:23 | page: 170, headers: ['criterion', 'summary assessment', 'rating']

17:43:36 | [167 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/204.4512_2020_te_spcc_fsp_asia_pacific_climate_technology_network_and_finance_centre_ctnfc.pdf
17:43:37 | page: 14, headers: ['criterion', 'rating']
17:43:38 | page: 15, headers: ['criterion', 'rating']
17:43:49 | page: 70, headers: ['criterion', 'summary assessment of the findings', 'rating']

### 多张表（不同区域的）

17:59:57 | [253 / 444] parsing file:///Users/mark/Documents/Terminal%20evaluation%20report/285.00609-1866_2017_te_unvironment_global_spcc_eba_mountain.pdf
17:59:58 | page: 19, headers: ['criterion', 'overall rating']
18:00:04 | page: 79, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:08 | page: 123, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:09 | page: 124, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:09 | page: 125, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:09 | page: 126, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:09 | page: 127, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:09 | page: 128, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:10 | page: 129, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:10 | page: 130, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:10 | page: 131, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:10 | page: 132, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:10 | page: 133, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:11 | page: 134, headers: ['criterion', 'summary assessment', 'ref.', 'rating']
18:00:11 | page: 135, headers: ['criterion', 'summary assessment', 'ref.', 'rating']

