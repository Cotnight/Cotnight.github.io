# MIT OCW 6.004 Computation Structures —— 课程结构抓取稿

> 原址（课程主页）：https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/
> 原址（大纲页）：https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/syllabus/
> 抓取日期：2026-10-19。来源：MIT OpenCourseWare（官方开放课件）。
> 用途：**给“组合逻辑→时序逻辑→状态机”这条主线找一份讲法清楚、章节与本科目对得上的英文参照**；只取第 1、2、4、5、6 章。不挂科目主页。

## 已核对的课程信息（大纲页 Course Info 栏）

- 课程号：**6.004 Computation Structures**
- 开课学期：**Spring 2017**；级别：Undergraduate
- 授课教师：**Chris Terman**
- 院系：Electrical Engineering and Computer Science（MIT）
- 主题分类：Engineering → Electrical Engineering → **Digital Systems**
- 资源类型：Instructor Insights / Lecture Notes / Lecture Videos / Podcasts / Programming Assignments with Examples

## 章节结构（21 章，每章统一拆成三块）

每一章 `cN` 下固定三件：`cN s1 Annotated Slides`（带注释的讲义，PDF 形态）、`cN s2 Topic Videos`（分主题的视频）、`cN s3 Worksheet`（练习卷，部分章有）。第 10、20、21 章只有 Slides + Videos。

| 章 | 标题 | 与本科目的关系 |
|---|---|---|
| 1 | Basics of Information | **要**：比特、编码、数制——对应康华光第 1 章（学生“数制与编码够用但不熟”） |
| 2 | The Digital Abstraction | **要**：0/1 抽象、静态约束（static discipline）、噪声容限——对应康华光第 3 章的外部特性部分（**不碰内部管级电路**） |
| 3 | CMOS | **不取**：CMOS 门内部电路与版图思路，学生明确排除 |
| 4 | **Combinational Logic** | **核心**：组合逻辑、最简化的系统做法——对应康华光第 2 章（卡诺图化简）+ 第 4 章（组合电路分析与设计），**学生当前的真实卡点** |
| 5 | **Sequential Logic** | **核心**：锁存器/触发器、时序约束——对应康华光第 5 章（学生“没底”的那一块） |
| 6 | **Finite State Machines** | **核心**：状态机写法与设计流程——对应康华光第 6.1～6.3（同步时序分析与设计），也是“拿到功能要求判断组合还是时序”这条目标的直接训练 |
| 7 | Performance Measures | 选看：组合路径延时/时钟周期怎么估 |
| 8 | Design Tradeoffs | 选看：逻辑化简与实现代价的权衡（写“为什么这样划分模块”时有用） |
| 9–21 | 指令集、汇编、编译器、栈、Beta 处理器、Cache、流水线、虚拟内存、并发、系统级通信、并行 | **不取**：属于计算机体系结构，超出本科目范围 |

## 抓取留白（重要）

- 抓 `syllabus` 页只得“课程信息 + 左侧 21 章导航树”；抓 `c4` 等章节正文页**同样只返回导航外框**——章节正文与讲义是前端渲染/PDF，未取到。
- 因此本稿能确认的只有**章标题、每章三件套的命名规则、课程元信息**；**具体某一页讲了什么没有核实**。讲解若引用 6.004 的某个说法，需先在浏览器里点开对应 `cN s1` 的 Slides 核对，不要凭章名推断。
- 6.004 的实验用 MIT 自己的 BSim/硬件描述写法，**与学生的 Python 仿真载体不同**，只能借“讲法与章节顺序”，**不能照搬实验**。
