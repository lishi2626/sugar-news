# Sugar News Excel Prompt

你正在执行 `Sugar News` 独立任务。请严格遵守 `AGENTS.md` 的长期规则，最终生成 Excel 文件，而不是 Markdown 日报。

## 目标日期

- 根据系统当前日期自动确定目标新闻日期：当前日期减一天。
- 新闻发布日期按照新闻所涉及国家或地区的当地时间判断。
- 原则上只整理目标日期当天发布或发生的新闻。
- 临近日期消息只有在继续对目标日期市场产生重要影响时才能采用，并必须在新闻正文中标注原始发布日期。

## 必须联网检索

必须使用联网检索，不得仅依靠历史知识、本地旧数据或模型记忆。

在 VSCode Codex 中，使用 `web.run` 的搜索和网页打开能力进行检索核验。每次执行必须保存：

```text
logs/YYYY/MM/search_log_YYYY-MM-DD.json
data/verified_news/YYYY/MM/sugar_news_YYYY-MM-DD.json
```

`search_log` 必须记录国家、关键词、语言、目标日期、检索工具、请求状态、保留结果数量、保留链接、过滤结果及过滤原因。

## 多语言检索

巴西不得只依赖英文检索。判断巴西当天无新闻前，必须完成政府部门、行业媒体、主流媒体和葡萄牙语关键词检索。

巴西关键词至少覆盖：

```text
Brazil sugar industry news July 19 2026
Brazil sugarcane ethanol export July 19 2026
Brasil açúcar etanol 19 julho 2026
Brasil setor sucroenergético 19 de julho de 2026
usinas cana açúcar etanol 19/07/2026
tarifa exportação clima incêndio Centro-Sul São Paulo
```

印度关键词至少覆盖：

```text
India sugar industry news July 19 2026
India sugarcane ethanol mills July 19 2026
India sugar news 19 July 2026
India sugar production July 19 2026
India sugar stocks July 19 2026
India sugar prices July 19 2026
India sugar ex-mill price July 19 2026
India sugar export policy July 19 2026
India sugar import July 19 2026
India sugar sales quota July 19 2026
India sugar shortage July 19 2026
India sugar mills July 19 2026
India sugarcane production July 19 2026
India sugarcane acreage July 19 2026
India sugarcane FRP July 19 2026
India ethanol policy July 19 2026
India ethanol blending July 19 2026
India E20 petrol July 19 2026
India E20 ethanol target July 19 2026
India ethanol above 20 percent July 19 2026
India sugarcane ethanol July 19 2026
India molasses ethanol July 19 2026
India sugar syrup ethanol July 19 2026
India grain ethanol July 19 2026
India maize ethanol July 19 2026
India ethanol feedstock July 19 2026
India oil ministry ethanol July 19 2026
India OMC ethanol tender July 19 2026
India cane-based distillery July 19 2026
site:reuters.com India sugar July 19 2026
site:reuters.com India ethanol July 19 2026
site:reuters.com India E20 July 19 2026
site:reuters.com India sugarcane July 19 2026
site:reuters.com India molasses July 19 2026
India sugarcane rainfall
India sugar belt rainfall forecast
Uttar Pradesh sugarcane rain forecast
Maharashtra sugarcane rainfall
Karnataka sugarcane rainfall
India monsoon sugar production
IMD rainfall forecast sugarcane states
heavy rainfall sugarcane India
excess rainfall cane crop India
deficient rainfall sugarcane India
भारत चीनी उद्योग 19 जुलाई 2026
गन्ना चीनी मिल इथेनॉल 19 जुलाई 2026
भारत चीनी उत्पादन 19 जुलाई 2026
भारत चीनी कीमत 19 जुलाई 2026
ई20 पेट्रोल 19 जुलाई 2026
भारत इथेनॉल ब्लेंडिंग 19 जुलाई 2026
मक्के से इथेनॉल 19 जुलाई 2026
शीरा इथेनॉल 19 जुलाई 2026
उत्तर प्रदेश गन्ना बारिश
महाराष्ट्र गन्ना बारिश
कर्नाटक गन्ना बारिश
```

印度新闻必须纳入糖业间接影响识别：标题没有 `sugar` 但正文涉及 E20、乙醇掺混比例、油销公司乙醇采购、玉米/碎米等粮食乙醇、甘蔗汁、糖浆、B 重糖蜜、C 重糖蜜或制醇原料替代时，仍须作为印度糖业候选新闻核验。不得因其位于能源、石油或燃料政策栏目就排除；影响判断应说明其如何改变甘蔗制醇需求、食糖供应和糖价预期。

印度新闻数量不设固定上限。政策、乙醇、价格、库存、天气、行业协会声明等不同主题的重要新闻均须按重要性保留，不得因已经收录若干条而截断。

泰国关键词至少覆盖英文、泰语、公历和佛历：

```text
Thailand sugar industry news July 19 2026
Thailand sugarcane mills ethanol July 19 2026
Thailand sugar news 19 July 2026
ประเทศไทย น้ำตาล อ้อย 19 กรกฎาคม 2569
ข่าวอ้อย น้ำตาล 19 กรกฎาคม 2569
อุตสาหกรรมอ้อยและน้ำตาล 19 กรกฎาคม 2569
โรงงานน้ำตาล เอทานอล 19 กรกฎาคม 2569
```

2026 年对应泰国佛历 2569 年，必须支持佛历到公历转换。

中国必须作为独立重点国家检索和展示，不得归入其他国家。中国检索不得只使用英文关键词，中文关键词至少覆盖：

```text
中国糖业新闻 2026年7月19日
中国食糖 2026年7月19日
中国白糖 2026年7月19日
中国甘蔗 2026年7月19日
中国甜菜糖 2026年7月19日
食糖产销数据 2026年7月19日
食糖进口 2026年7月19日
食糖进口配额 2026年7月19日
糖浆预混粉进口 2026年7月19日
广西糖业 2026年7月19日
云南糖业 2026年7月19日
郑州白糖期货 2026年7月19日
郑糖主力合约 2026年7月19日
白糖现货价格 2026年7月19日
制糖集团公告 2026年7月19日
```

中国英文补充关键词至少覆盖：

```text
China sugar industry July 19 2026
China sugar production July 19 2026
China sugar imports July 19 2026
China sugarcane beet sugar July 19 2026
China white sugar futures July 19 2026
China sugar syrup imports July 19 2026
```

中国重点来源包括中国政府网、国家发展和改革委员会、农业农村部、商务部、海关总署、国家统计局、郑州商品交易所、中国糖业协会、广西糖业协会及广西相关政府部门、云南省糖业协会及云南相关政府部门、中国气象局和主要甘蔗产区气象部门、制糖企业公告、权威期货/农业/财经媒体。

完成巴西、印度、泰国、中国检索后，必须继续执行全球糖业新闻发现，不得只检索重点国家。全球英文检索至少覆盖：

```text
global sugar industry news July 19 2026
sugar production export policy July 19 2026
sugarcane ethanol mills July 19 2026
sugar import export tariff quota July 19 2026
sugar price government policy July 19 2026
sugar industry news 19 July 2026
sugarcane news 19 July 2026
ethanol sugar mills 19 July 2026
```

全球检索发现某个国家后，必须使用该国名称、当地语言和当地日期格式继续搜索。重点补充检索路径包括但不限于巴基斯坦、菲律宾、越南、俄罗斯和印度尼西亚，且必须覆盖英文及当地语言关键词。这些国家不是固定输出名单；每日继续根据实际发现检索可能影响全球糖业供需或 ICE 原糖价格的其他国家和地区。

## 日期核验

必须核对新闻实际发布日期和事件发生日期，不得把网页当前日期、访问日期、页眉日期或版权日期误认为新闻发布日期。

必须识别：

- `July 19, 2026`
- `19 July 2026`
- `19/07/2026`
- `2026-07-19`
- `19 de julho de 2026`
- `19 जुलाई 2026`
- `19 กรกฎาคม 2569`
- `19 جولائی 2026`
- `Hulyo 19 2026`
- `ngày 19 tháng 7 năm 2026`
- `19 июля 2026`
- `19 Juli 2026`

日期无法确认时，先记录为待核验；未完成来源和日期核验的新闻不得写入 Excel。

## 筛选规则

新闻范围包括：

1. 甘蔗种植面积、单产、产量及天气影响；
2. 甘蔗压榨量、糖产量、出糖率和制糖比例；
3. 乙醇产量、价格、掺混政策和甘蔗制醇比例；
4. 糖出口、进口、配额、关税和贸易政策；
5. 国内糖价、国际糖价和主要糖厂报价；
6. 糖厂开榨、停榨、扩建、检修及经营情况；
7. 政府政策、行业协会声明和官方数据；
8. 可能影响全球糖业供需或 ICE 原糖价格的其他事件。

不得只按英文标题关键词判断相关性。正文中的 `açúcar`、`cana`、`etanol`、`चीनी`、`गन्ना`、`इथेनॉल`、`น้ำตาล`、`อ้อย`、`เอทานอล` 均应识别为糖业相关表达。

天气新闻只有在明确涉及主要甘蔗产区，并可能影响甘蔗生长、收割、压榨或运输时才能收录。

### 印度甘蔗产区降雨监测

每日印度检索必须覆盖昨日实际降雨和未来 7-15 天降雨预报；新闻发布日期可以是昨日或今日，但天气事件必须与昨日实况或最新预报有关，并按印度当地时间核对。

重点监测地区：

- 核心监测地区：北方邦（Uttar Pradesh）、马哈拉施特拉邦（Maharashtra）、卡纳塔克邦（Karnataka）。
- 其他主要产区：泰米尔纳德邦（Tamil Nadu）、古吉拉特邦（Gujarat）、比哈尔邦（Bihar）、旁遮普邦（Punjab）、哈里亚纳邦（Haryana）、北阿坎德邦（Uttarakhand）。

检索路径必须包括 IMD 每日降雨报告、季风报告、天气预警、扩展期预报和农业气象公告；印度各邦气象/农业/甘蔗管理部门；印度英文和印地语主流媒体；糖业、农业、季风及大宗商品专业媒体；必要时用可靠气象平台交叉验证未来降雨趋势。

如果昨日实况或未来预报涉及主要甘蔗产区，并可能影响甘蔗生长、单产、收割、压榨进度或糖产量，必须作为印度糖业相关新闻补充到报告中；不得因为已有其他印度新闻而省略天气新闻。

印度降雨影响判断：

- 甘蔗生长阶段适量降雨、预报降雨增多、强降雨或暴雨预报但未证实受灾、土壤墒情改善：偏空糖价：降雨有利于甘蔗生长和单产提升，可能增加未来甘蔗及食糖供应。
- 干旱、降雨不足、季风偏弱或未来降雨预报减少：偏多糖价：水分不足可能降低甘蔗单产和糖料供应。
- 已确认洪涝、农田被淹、甘蔗倒伏、道路中断、作物受损或预期减产：偏多糖价，并说明实际损失依据。
- 收割或压榨阶段降雨导致砍蔗、运输或糖厂开榨受阻：偏多糖价或短期偏多糖价。
- 降雨地区不属于主要甘蔗产区，或报道未说明其对甘蔗生产的影响：影响有限或不收录。

不得仅根据“强降雨”“暴雨”等词语机械判断，必须结合甘蔗所处生长阶段、产区位置以及是否已经造成实际损失。

### 泰国甘蔗产区天气判断

泰国主要甘蔗种植区名单：

- 东北部：乌隆他尼（Udon Thani）、孔敬（Khon Kaen）、呵叻/那空叻差是玛（Nakhon Ratchasima）、猜也蓬（Chaiyaphum）、加拉信（Kalasin）、黎府（Loei）。东北部是最核心产区。
- 北部：那空沙旺（Nakhon Sawan）、甘烹碧（Kamphaeng Phet）、素可泰（Sukhothai）、彭世洛（Phitsanulok）。
- 中部及西部：北碧（Kanchanaburi）、华富里（Lopburi）、素攀武里（Suphanburi）、猜纳（Chai Nat）。
- 东部：沙缴（Sa Kaeo）、春武里（Chonburi）。

整理泰国天气新闻时必须确认具体府名、是否为主产区、甘蔗生长阶段、降雨强度和实际影响。生长阶段不得仅凭“强降雨预报”推断甘蔗受灾，只有新闻明确指出严重洪涝、甘蔗倒伏、农田被淹、作物受损或预计减产时，才根据实际损失重新判断。

泰国天气影响判断：

- 甘蔗生长阶段，主产区实际出现强降雨、预报未来降雨量增加、提示可能出现强降雨，或多个主产区降雨范围/强度扩大：偏空糖价：降雨增加有助于改善土壤墒情和甘蔗生长，可能提高单产及未来糖料供应。
- 生长季降雨减少或持续干旱：偏多糖价：降雨不足可能抑制甘蔗生长并降低单产，增加未来糖产量下降风险。
- 新闻使用“强降雨”“暴雨预警”或“降雨明显增多”等表述时，只要处于甘蔗生长阶段且未明确造成作物损失，仍按偏空糖价处理。
- 只有明确已经造成严重洪涝、甘蔗倒伏、农田被淹、作物受损或预计减产时，才根据实际损失重新判断；不得仅凭风险预报改判为偏多。
- 收割及压榨期降雨增加：偏多糖价：收割及压榨期降雨可能影响甘蔗收割、运输和糖厂入榨进度，造成短期供应延迟。
- 降雨只出现在非甘蔗主产区：影响有限：降雨区域与泰国主要甘蔗种植区重合度较低，对全国甘蔗及糖产量影响有限。
- 低覆盖率、分散性阵雨且未说明明显增加或显著改善墒情：影响有限，不得把所有“有雨”机械写成偏空。

如果泰国东北部和中部主要甘蔗产区在甘蔗生长阶段出现降雨增加、强降雨预报或降雨范围/强度扩大，且未明确发生作物损失，影响统一写为：偏空糖价：降雨增加有助于改善土壤墒情和甘蔗生长，可能提高单产及未来糖料供应。

同一事件被多家媒体报道时，合并为一条，优先引用原始或权威来源。

## 新闻数量和顺序

新闻数量完全按照目标日期实际发生的重要糖业新闻确定，不规定各国家的新闻数量，不设最低数量和最高数量。

- 同一国家有多少条重要且不重复的新闻，就整理多少条；
- 每条新闻单独占一行；
- 某国没有重要新增信息时，不生成该国数据行；
- 不写“暂无新闻”“暂无最新数据”等占位文字；
- 不用旧闻、重复新闻或低相关性内容补数量。

国家整体顺序必须保持：

1. 中国；
2. 巴西；
3. 印度；
4. 泰国；
5. 其他国家。

“其他国家”在 A 列填写具体国家或地区名称，不要统一写“其他”。

其他国家新闻数量不受限制。每个具体国家必须保存在独立对象或独立数组中，不得用单个 `其他` 键覆盖多国新闻，不得只显示第一条其他国家新闻。

中国新闻数量不受限制。若目标日期没有中国重要新增信息，直接省略中国数据行，不写占位文字。结构化数据中中国必须使用独立对象和 `country_group=中国`，不得保存到“其他国家”。

## 摘要、分类和排除规则

每条新闻摘要使用 2-3 句中文糖业研究报告表达，提炼核心事件、关键数据或政策变化，以及对食糖供需、甘蔗生产、乙醇分流、进出口、库存或糖价的影响。不要逐句翻译英文标题，不要补充原文没有的数据，不要写宣传性背景或重复铺陈。页面已有报告日期时，正文不要机械重复“今日”“本日发布”“X月X日消息”；只有政策起止、榨季、配额、统计截止、降雨预报覆盖期、开榨停榨等影响判断需要的日期才保留。

国家归属以核心事件发生地和主要影响对象为准，不按来源网站、转载媒体所在地、文章语言、企业总部所在地或标题中出现次数最多的国家分类。某国进口另一国食糖时，进口政策、采购量和国内供应归进口国；出口销售、出口配额和生产安排归出口国；多国事件无明确主体时归“其他国家”下的实际国家或“全球”，不得重复发布。

必须排除人体血糖、糖尿病、医学健康、营养保健、胰岛素、降糖药、血糖仪、连续血糖监测、控糖饮食和代糖健康研究。英文检索和自动过滤必须排除 `blood sugar`、`glucose`、`diabetes`、`insulin`、`glycemic`、`hyperglycemia`、`hypoglycemia`、`glucose monitoring`、`diabetes treatment` 等语义。游戏、小说、影视、音乐、餐饮营销、菜谱甜点、文学作品或普通消费内容不得仅因标题包含 `sugar`、`palm sugar`、`burnt sugar` 等词进入报告。不得仅因标题包含 `sugar` 就判断为糖业新闻。

乙醇新闻只有在与甘蔗、糖蜜、糖浆、糖醇比、糖业自给或食糖供应存在直接关系时才能收录。一般能源、汽油、玉米乙醇或汽车燃料新闻不得仅因出现“乙醇”“E10”“E20”自动收录；印度乙醇政策按印度糖业间接影响规则处理。

## Excel 输出

必须以 `templates/新闻格式.xlsx` 作为固定模板，复制后填写，不得覆盖原始模板。

固定列：

- A 列：国家
- B 列：新闻
- C 列：影响

B 列新闻每条 2-3 句，并在末尾保留来源：

```text
来源：机构或媒体名称（原始链接）
```

C 列影响每条一句话，必须以以下之一开头：

```text
偏多糖价：
偏空糖价：
中性：
影响有限：
```

甘蔗、糖及进出口数量优先换算为“万吨”。例如 `273.90 LMT` 写成 `2739万吨`，不得保留 `LMT/lmt`。乙醇使用“万升”或“亿升”，同一日报保持统一。

当甘蔗收购价、最低支持价、FRP 或 SAP 提高时，如果主要作用是提高农户种植收益、刺激甘蔗面积扩张和增加未来糖产量，原则上判断为偏空糖价；如果同时存在明显的糖厂成本上升、停产或减产风险，则分别说明短期成本影响与中长期供应影响，不得直接判断为中性。

## 生成命令

核验清单完成后，运行：

```powershell
python scripts\run_sugar_news.py --date YYYY-MM-DD
```

脚本会生成：

```text
reports/YYYY/MM/Sugar News YYYY-MM-DD.xlsx
logs/YYYY/MM/write_log_YYYY-MM-DD.json
```

## 完成检查

生成后必须检查：

1. 目标日期正确；
2. 国家顺序正确；
3. 新闻数量完全依据实际情况；
4. 不存在重复、旧闻或无关内容；
5. 数据、单位和来源准确；
6. 新闻与影响简洁；
7. 新增行继承模板格式；
8. 文字完整显示；
9. 已核验新闻全部写入 Excel；
10. 保存后重新读取 Excel 的数量与核验清单一致；
11. 中国新闻是否在 Excel、结构化数据、本地看板和 Vercel 线上看板中一致；
12. 其他国家新闻是否全部用具体国家或地区名称展示；
13. Excel、结构化数据、本地看板和 Vercel 线上看板是否逐条一致；
14. 是否不存在血糖、糖尿病、胰岛素、医学健康或营养保健新闻；
15. 是否不存在按来源网站或转载媒体所在地误分国家的新闻。

最终只向用户汇报文件保存位置、目标新闻日期、各国家实际收录新闻数量及检查结果，不重复粘贴全部新闻内容。

## 看板发布

生成 Excel 后，还必须同步更新本项目内的 Sugar News 看板数据。Sugar News 必须发布到独立的 GitHub 仓库和独立的 Vercel 项目，不能依赖其他项目目录、域名或部署配置。

看板路由：

```text
/
/sugar-news
```

Excel 和网页必须使用同一份已核验新闻清单。运行：

```powershell
python scripts\sugar_news_pipeline.py --date YYYY-MM-DD --offline-only
```

该脚本会生成 Excel、网页 JSON、索引和状态文件，并核对已核验清单、Excel 与网页 JSON 的数量和内容是否一致。若检查失败，不得发布到 Vercel。

每日云端自动任务使用 GitHub Actions：

- 北京时间 06:00；
- 失败重试：北京时间 06:10、06:30；
- cron 对应 UTC：`0 22 * * *`、`10 22 * * *`、`30 22 * * *`；
- 日期计算必须使用 `Asia/Shanghai`。
