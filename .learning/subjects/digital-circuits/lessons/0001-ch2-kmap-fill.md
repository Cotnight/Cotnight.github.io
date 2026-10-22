---
title: 卡诺图：真值表排成的方格
goal: 能把真值表或表达式按正确的格位填进卡诺图，三变量、四变量都做到逐格无误。
---

## 先补齐两块底子

本课直接进入卡诺图。填图要用到的两件工具——真值表的列法与最小项编号——在这里一次性补到够用为止；布尔代数的定律与化简规则不在这里展开，用到时随讲随给。

### 真值表按二进制数递增列行

$n$ 个变量的取值组合共有 $2^n$ 种。列真值表时先把变量的次序排定（例如 $A$、$B$、$C$），行按这几个变量接成的二进制数由小到大排：二变量是 00、01、10、11，三变量是 000、001、010、011、100、101、110、111。行序一旦固定，行号与取值就一一对应，最小项编号与卡诺图格位才不会错位。

### 最小项编号：原变量记 1，反变量记 0

$n$ 个变量的一个乘积项中，每个变量恰好出现一次（取原变量或反变量），这样的乘积项称为**最小项**。把乘积项里的原变量记 1、反变量记 0，按变量次序读成一个二进制数，它的十进制值就是最小项的编号，记作 $m_i$。

- $A\bar B C$ 的取值组合是 101，编号为 $m_5$。
- $\bar A\bar B\bar C$ 是 000，编号为 $m_0$。
- $\bar A B\bar C$ 是 010，编号为 $m_2$。

反过来读同样常用：$m_5$ 指的就是 $A=1$、$B=0$、$C=1$ 这一组取值，该最小项在这组取值上为 1，在其余组合上全为 0。函数写成 $\sum m(3,5,6,7)$，表示这几个最小项相或。

## 为什么排成方格

真值表把 $2^n$ 种组合排成一列。三变量的真值表里，000 与 100 只差第一个变量，两行分别落在第 1 行与第 5 行；000 与 001 只差第三个变量，两行挨着。哪些行可以合并，只看它们是否只差一个变量，与两行在表里隔多远无关，所以单看真值表只能逐对去比。

只差一个变量的两项可以合并，依据是 $A+\bar A=1$。设这两项的其余变量取值为 $X$，则

$$X\cdot A+X\cdot\bar A=X(A+\bar A)=X$$

合并后 $X$ 比原来少一个变量；三变量的两项若只差 $A$，合并一次就降到两个变量。

卡诺图的做法是把 $2^n$ 个最小项按"相邻两格只差一个变量"铺成方格：每格代表一个最小项，格内填该最小项的值，可以合并的格子因此在图上相邻，扫一遍图就能找全。这种方格图 1953 年由贝尔实验室的卡诺（Maurice Karnaugh）提出，称为**卡诺图**。

## 行列为什么是格雷码

卡诺图的行、列各标一组变量的取值组合，那组有几个变量，标号就是几位。三变量图常把 $A$ 放在行、$BC$ 放在列；四变量图把 $AB$ 放行、$CD$ 放列。

标号序列要满足一条：轴上相邻的两个标号只差一位。图上的两格相邻，当且仅当它们对应的取值只差一个变量，而这件事完全由标号序列决定。一个变量的轴只有 0 与 1，天然满足。两个变量的轴要按 00、01、11、10 排：00 与 01 只差最低位，01 与 11 只差最高位，11 与 10 又只差最低位，末位的 10 绕回开头的 00 也只差最高位。这种相邻两个码只差一位的编码顺序以贝尔实验室的格雷（Frank Gray）命名，称为格雷码。

若按二进制顺序排成 00、01、10、11，01 与 10 相邻却差两位，两格之间找不到可以消去的公共变量；00 与 11 落在轴的两端，按格雷码本该相邻，却隔了整行。

::: note 两端也是相邻的
按格雷码排，左右两端、上下两端同样只差一位：列标 10 与 00 在图上分处两端，取值只差最高位。这一条在下一课圈组时要用，填图这一步还不依赖它。
:::

## 方格与最小项对应

每一格的位置由行标号与列标号共同确定：把两个标号接成一个二进制数，它的十进制值就是这一格的最小项编号。三变量图里行为 $A$、列为 $BC$，$A=0$ 且 $BC=01$ 的那一格是 001，即 $m_1$。

三变量图是 2 行 4 列，四变量图是 4 行 4 列。下面两张图把格内编号直接写了出来，填图时对着编号找位置。

::: svg
alt: 三变量卡诺图，行标 A 取 0 与 1，列标 BC 按 00、01、11、10 排列，八格内依次标出 m0 至 m7 的编号
caption: 三变量卡诺图：2 行 4 列，格内是最小项编号

<svg viewBox="0 0 250 120" role="img" aria-hidden="true">
  <rect x="4" y="6" width="230" height="82" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M34 6V88" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M84 6V88" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M134 6V88" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M184 6V88" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 28H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 58H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 28L34 6" stroke="currentColor" stroke-width="1" fill="none"/>
  <text x="9" y="17" font-size="8" fill="currentColor">A</text>
  <text x="19" y="26" font-size="8" fill="currentColor">BC</text>
  <text x="59" y="21" font-size="9" text-anchor="middle" fill="currentColor">00</text>
  <text x="109" y="21" font-size="9" text-anchor="middle" fill="currentColor">01</text>
  <text x="159" y="21" font-size="9" text-anchor="middle" fill="currentColor">11</text>
  <text x="209" y="21" font-size="9" text-anchor="middle" fill="currentColor">10</text>
  <text x="19" y="47" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="19" y="77" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <text x="59" y="47" font-size="9" text-anchor="middle" fill="currentColor">m0</text>
  <text x="109" y="47" font-size="9" text-anchor="middle" fill="currentColor">m1</text>
  <text x="159" y="47" font-size="9" text-anchor="middle" fill="currentColor">m3</text>
  <text x="209" y="47" font-size="9" text-anchor="middle" fill="currentColor">m2</text>
  <text x="59" y="77" font-size="9" text-anchor="middle" fill="currentColor">m4</text>
  <text x="109" y="77" font-size="9" text-anchor="middle" fill="currentColor">m5</text>
  <text x="159" y="77" font-size="9" text-anchor="middle" fill="currentColor">m7</text>
  <text x="209" y="77" font-size="9" text-anchor="middle" fill="currentColor">m6</text>
</svg>
:::

三变量图的四列依次是 $BC=00$、01、11、10，两行依次是 $A=0$、1。

::: svg
alt: 四变量卡诺图，行标 AB 与列标 CD 都按 00、01、11、10 排列，十六格内依次标出 m0 至 m15 的编号
caption: 四变量卡诺图：4 行 4 列，行标 AB、列标 CD

<svg viewBox="0 0 250 190" role="img" aria-hidden="true">
  <rect x="4" y="6" width="230" height="160" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M34 6V166" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M84 6V166" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M134 6V166" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M184 6V166" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 30H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 64H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 98H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 132H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 30L34 6" stroke="currentColor" stroke-width="1" fill="none"/>
  <text x="6" y="16" font-size="8" fill="currentColor">AB</text>
  <text x="18" y="28" font-size="8" fill="currentColor">CD</text>
  <text x="59" y="23" font-size="9" text-anchor="middle" fill="currentColor">00</text>
  <text x="109" y="23" font-size="9" text-anchor="middle" fill="currentColor">01</text>
  <text x="159" y="23" font-size="9" text-anchor="middle" fill="currentColor">11</text>
  <text x="209" y="23" font-size="9" text-anchor="middle" fill="currentColor">10</text>
  <text x="19" y="51" font-size="9" text-anchor="middle" fill="currentColor">00</text>
  <text x="19" y="85" font-size="9" text-anchor="middle" fill="currentColor">01</text>
  <text x="19" y="119" font-size="9" text-anchor="middle" fill="currentColor">11</text>
  <text x="19" y="153" font-size="9" text-anchor="middle" fill="currentColor">10</text>
  <text x="59" y="51" font-size="9" text-anchor="middle" fill="currentColor">m0</text>
  <text x="109" y="51" font-size="9" text-anchor="middle" fill="currentColor">m1</text>
  <text x="159" y="51" font-size="9" text-anchor="middle" fill="currentColor">m3</text>
  <text x="209" y="51" font-size="9" text-anchor="middle" fill="currentColor">m2</text>
  <text x="59" y="85" font-size="9" text-anchor="middle" fill="currentColor">m4</text>
  <text x="109" y="85" font-size="9" text-anchor="middle" fill="currentColor">m5</text>
  <text x="159" y="85" font-size="9" text-anchor="middle" fill="currentColor">m7</text>
  <text x="209" y="85" font-size="9" text-anchor="middle" fill="currentColor">m6</text>
  <text x="59" y="119" font-size="9" text-anchor="middle" fill="currentColor">m12</text>
  <text x="109" y="119" font-size="9" text-anchor="middle" fill="currentColor">m13</text>
  <text x="159" y="119" font-size="9" text-anchor="middle" fill="currentColor">m15</text>
  <text x="209" y="119" font-size="9" text-anchor="middle" fill="currentColor">m14</text>
  <text x="59" y="153" font-size="9" text-anchor="middle" fill="currentColor">m8</text>
  <text x="109" y="153" font-size="9" text-anchor="middle" fill="currentColor">m9</text>
  <text x="159" y="153" font-size="9" text-anchor="middle" fill="currentColor">m11</text>
  <text x="209" y="153" font-size="9" text-anchor="middle" fill="currentColor">m10</text>
</svg>
:::

四变量图的四行依次是 $AB=00$、01、11、10，四列依次是 $CD=00$、01、11、10。两个轴都用格雷码，所以每一格与它上下左右的邻居都只差一个变量。

::: quiz 理解 锚点：卡诺图的格号与最小项编号怎样对应
:::

## 从真值表填图

真值表与卡诺图记录的是同一份信息，填图就是把每一行的取值抄到对应的格子里：读一行的变量取值，写成最小项编号，找到编号相同的那一格，把这行的输出值填进去。输出为 0 的格填 0，也有人留空，图上的空位按 0 读。

以三变量的多数表决为例：三台设备各有启动开关 $A$、$B$、$C$，任意两台及以上启动时报警输出 $Y=1$。真值表与填好的卡诺图如下。

::: svg
alt: 左边是三变量真值表，八行列出 A、B、C 的取值、输出 Y 与最小项编号；右边是同一函数填好的卡诺图，四格填 1、四格填 0
caption: 同一张真值表落进方格：输出为 1 的四行各占一格

<svg viewBox="0 0 380 180" role="img" aria-hidden="true">
  <rect x="6" y="8" width="112" height="152" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M62 8V160" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M86 8V160" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 24H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 41H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 58H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 75H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 92H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 109H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 126H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M6 143H118" stroke="currentColor" stroke-width="1" fill="none"/>
  <text x="34" y="20" font-size="9" text-anchor="middle" fill="currentColor">ABC</text>
  <text x="74" y="20" font-size="9" text-anchor="middle" fill="currentColor">Y</text>
  <text x="102" y="20" font-size="9" text-anchor="middle" fill="currentColor">编号</text>
  <text x="34" y="36" font-size="9" text-anchor="middle" fill="currentColor">000</text>
  <text x="74" y="36" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="102" y="36" font-size="9" text-anchor="middle" fill="currentColor">m0</text>
  <text x="34" y="53" font-size="9" text-anchor="middle" fill="currentColor">001</text>
  <text x="74" y="53" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="102" y="53" font-size="9" text-anchor="middle" fill="currentColor">m1</text>
  <text x="34" y="70" font-size="9" text-anchor="middle" fill="currentColor">010</text>
  <text x="74" y="70" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="102" y="70" font-size="9" text-anchor="middle" fill="currentColor">m2</text>
  <text x="34" y="87" font-size="9" text-anchor="middle" fill="currentColor">011</text>
  <text x="74" y="87" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <text x="102" y="87" font-size="9" text-anchor="middle" fill="currentColor">m3</text>
  <text x="34" y="104" font-size="9" text-anchor="middle" fill="currentColor">100</text>
  <text x="74" y="104" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="102" y="104" font-size="9" text-anchor="middle" fill="currentColor">m4</text>
  <text x="34" y="121" font-size="9" text-anchor="middle" fill="currentColor">101</text>
  <text x="74" y="121" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <text x="102" y="121" font-size="9" text-anchor="middle" fill="currentColor">m5</text>
  <text x="34" y="138" font-size="9" text-anchor="middle" fill="currentColor">110</text>
  <text x="74" y="138" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <text x="102" y="138" font-size="9" text-anchor="middle" fill="currentColor">m6</text>
  <text x="34" y="155" font-size="9" text-anchor="middle" fill="currentColor">111</text>
  <text x="74" y="155" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <text x="102" y="155" font-size="9" text-anchor="middle" fill="currentColor">m7</text>
  <rect x="132" y="8" width="230" height="90" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M162 8V98" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M212 8V98" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M262 8V98" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M312 8V98" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M132 30H362" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M132 64H362" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M132 30L162 8" stroke="currentColor" stroke-width="1" fill="none"/>
  <text x="137" y="17" font-size="8" fill="currentColor">A</text>
  <text x="147" y="28" font-size="8" fill="currentColor">BC</text>
  <text x="187" y="23" font-size="9" text-anchor="middle" fill="currentColor">00</text>
  <text x="237" y="23" font-size="9" text-anchor="middle" fill="currentColor">01</text>
  <text x="287" y="23" font-size="9" text-anchor="middle" fill="currentColor">11</text>
  <text x="337" y="23" font-size="9" text-anchor="middle" fill="currentColor">10</text>
  <text x="147" y="51" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="147" y="85" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <rect x="262" y="30" width="50" height="34" fill="currentColor" opacity="0.14"/>
  <rect x="212" y="64" width="50" height="34" fill="currentColor" opacity="0.14"/>
  <rect x="262" y="64" width="50" height="34" fill="currentColor" opacity="0.14"/>
  <rect x="312" y="64" width="50" height="34" fill="currentColor" opacity="0.14"/>
  <text x="166" y="42" font-size="8" fill="currentColor" opacity="0.65">m0</text>
  <text x="216" y="42" font-size="8" fill="currentColor" opacity="0.65">m1</text>
  <text x="266" y="42" font-size="8" fill="currentColor" opacity="0.65">m3</text>
  <text x="316" y="42" font-size="8" fill="currentColor" opacity="0.65">m2</text>
  <text x="166" y="76" font-size="8" fill="currentColor" opacity="0.65">m4</text>
  <text x="216" y="76" font-size="8" fill="currentColor" opacity="0.65">m5</text>
  <text x="266" y="76" font-size="8" fill="currentColor" opacity="0.65">m7</text>
  <text x="316" y="76" font-size="8" fill="currentColor" opacity="0.65">m6</text>
  <text x="187" y="58" font-size="12" text-anchor="middle" fill="currentColor">0</text>
  <text x="237" y="58" font-size="12" text-anchor="middle" fill="currentColor">0</text>
  <text x="287" y="58" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <text x="337" y="58" font-size="12" text-anchor="middle" fill="currentColor">0</text>
  <text x="187" y="92" font-size="12" text-anchor="middle" fill="currentColor">0</text>
  <text x="237" y="92" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <text x="287" y="92" font-size="12" text-anchor="middle" fill="currentColor">1</text>
  <text x="337" y="92" font-size="12" text-anchor="middle" fill="currentColor">1</text>
</svg>
:::

逐行走一遍：$m_3$ 在第 4 行（011），落 $A=0$、$BC=11$ 那一格；$m_5$（101）落 $A=1$、$BC=01$；$m_6$（110）落 $A=1$、$BC=10$；$m_7$（111）落 $A=1$、$BC=11$。其余四格填 0。图上的编号顺序与编号大小并不一致——这正是要用格雷码排标号的结果。

编号本身可以交给一小段程序验一遍，这也是后面 lab 的做法：

```python
for abc in ('000', '001', '010', '011'):
    print(abc, 'm' + str(int(abc, 2)))
```

```term
000 m0
001 m1
010 m2
011 m3
```

另四行同理：100 是 $m_4$、101 是 $m_5$、110 是 $m_6$、111 是 $m_7$。

::: quiz 改造 锚点：四变量图换一组行列变量后重填
:::

## 从表达式填图

表达式落到图上按乘积项逐项填 1。一项占一格还是占几格，取决于这项里有几个变量。

每一项都是最小项、各项之间相或的形式称为标准与或式；标准与或式的每一项占一格：

$$Y=\bar ABC+A\bar BC+AB\bar C+ABC$$

四项的编号依次是 011、101、110、111，把 $m_3$、$m_5$、$m_6$、$m_7$ 四格填 1，其余填 0。

项里缺变量时，缺掉的那个变量取 0 取 1 都不改变这项的取值，所以这项要落 $2^k$ 格，$k$ 是缺掉的变量个数。定位仍靠剩下的变量：剩下的变量把落点限定在若干格上，缺的变量沿几个方向铺开。三变量图里的几种情形如下。

| 乘积项 | 缺的变量 | 落几格 | 落在哪几格 |
| --- | --- | --- | --- |
| $A\bar B$ | $C$ | 2 | $m_4$、$m_5$ |
| $A\bar C$ | $B$ | 2 | $m_4$、$m_6$ |
| $A$ | $B$、$C$ | 4 | $m_4$、$m_5$、$m_6$、$m_7$ |
| $C$ | $A$、$B$ | 4 | $m_1$、$m_3$、$m_5$、$m_7$ |
| $1$ | 三个都缺 | 8 | 全图八格 |

缺变量的项也可以先按 $A+\bar A=1$ 展开，再按最小项逐格填：$A\bar B=A\bar B(C+\bar C)=A\bar BC+A\bar B\bar C$，即 $m_5$ 与 $m_4$ 两格。展开只是说明为什么落这两格，填图时照上表直接落更快。

::: svg
alt: 两幅三变量卡诺图，上幅高亮 m4、m5 两格，下幅高亮 m4 到 m7 四格
caption: 缺变量的乘积项一次落多格：$A\bar B$ 落 m4、m5，$A$ 落 m4 至 m7

<svg viewBox="0 0 250 215" role="img" aria-hidden="true">
  <text x="4" y="14" font-size="9" fill="currentColor">（a）AB' 缺 C，落两格</text>
  <rect x="4" y="18" width="230" height="82" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M34 18V100" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M84 18V100" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M134 18V100" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M184 18V100" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 40H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 70H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 40L34 18" stroke="currentColor" stroke-width="1" fill="none"/>
  <text x="9" y="29" font-size="8" fill="currentColor">A</text>
  <text x="19" y="38" font-size="8" fill="currentColor">BC</text>
  <text x="59" y="34" font-size="9" text-anchor="middle" fill="currentColor">00</text>
  <text x="109" y="34" font-size="9" text-anchor="middle" fill="currentColor">01</text>
  <text x="159" y="34" font-size="9" text-anchor="middle" fill="currentColor">11</text>
  <text x="209" y="34" font-size="9" text-anchor="middle" fill="currentColor">10</text>
  <text x="19" y="59" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="19" y="89" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <rect x="34" y="70" width="50" height="30" fill="currentColor" opacity="0.16"/>
  <rect x="84" y="70" width="50" height="30" fill="currentColor" opacity="0.16"/>
  <text x="59" y="59" font-size="9" text-anchor="middle" fill="currentColor">m0</text>
  <text x="109" y="59" font-size="9" text-anchor="middle" fill="currentColor">m1</text>
  <text x="159" y="59" font-size="9" text-anchor="middle" fill="currentColor">m3</text>
  <text x="209" y="59" font-size="9" text-anchor="middle" fill="currentColor">m2</text>
  <text x="59" y="89" font-size="9" text-anchor="middle" fill="currentColor">m4</text>
  <text x="109" y="89" font-size="9" text-anchor="middle" fill="currentColor">m5</text>
  <text x="159" y="89" font-size="9" text-anchor="middle" fill="currentColor">m7</text>
  <text x="209" y="89" font-size="9" text-anchor="middle" fill="currentColor">m6</text>
  <text x="4" y="122" font-size="9" fill="currentColor">（b）A 缺 B、C，落四格</text>
  <rect x="4" y="126" width="230" height="82" fill="none" stroke="currentColor" stroke-width="1"/>
  <path d="M34 126V208" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M84 126V208" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M134 126V208" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M184 126V208" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 148H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 178H234" stroke="currentColor" stroke-width="1" fill="none"/>
  <path d="M4 148L34 126" stroke="currentColor" stroke-width="1" fill="none"/>
  <text x="9" y="137" font-size="8" fill="currentColor">A</text>
  <text x="19" y="146" font-size="8" fill="currentColor">BC</text>
  <text x="59" y="142" font-size="9" text-anchor="middle" fill="currentColor">00</text>
  <text x="109" y="142" font-size="9" text-anchor="middle" fill="currentColor">01</text>
  <text x="159" y="142" font-size="9" text-anchor="middle" fill="currentColor">11</text>
  <text x="209" y="142" font-size="9" text-anchor="middle" fill="currentColor">10</text>
  <text x="19" y="167" font-size="9" text-anchor="middle" fill="currentColor">0</text>
  <text x="19" y="197" font-size="9" text-anchor="middle" fill="currentColor">1</text>
  <rect x="34" y="178" width="200" height="30" fill="currentColor" opacity="0.16"/>
  <text x="59" y="167" font-size="9" text-anchor="middle" fill="currentColor">m0</text>
  <text x="109" y="167" font-size="9" text-anchor="middle" fill="currentColor">m1</text>
  <text x="159" y="167" font-size="9" text-anchor="middle" fill="currentColor">m3</text>
  <text x="209" y="167" font-size="9" text-anchor="middle" fill="currentColor">m2</text>
  <text x="59" y="197" font-size="9" text-anchor="middle" fill="currentColor">m4</text>
  <text x="109" y="197" font-size="9" text-anchor="middle" fill="currentColor">m5</text>
  <text x="159" y="197" font-size="9" text-anchor="middle" fill="currentColor">m7</text>
  <text x="209" y="197" font-size="9" text-anchor="middle" fill="currentColor">m6</text>
</svg>
:::

几项落在同一格时，这一格仍然是 1：$Y=A\bar B+A\bar BC$ 中后一项落 $m_5$，前一项已经包含 $m_5$，图上只填一个 1。

::: quiz 应用 锚点：缺变量的乘积项落几格
:::

## 填完先自查

填好的图要与真值表逐行对上，三步就能核完。

1. 数 1 的格数，应当等于真值表里输出为 1 的行数。
2. 抽两三格反查：指着一格报出它的编号，翻到真值表的同一行看输出，与图上填的值比一遍。
3. 念一遍轴的标号：三变量以上的轴应当是 00、01、11、10，中间两格是 11 与 10。

填图常错的地方：

- 轴的标号按二进制顺序写成 00、01、10、11。图看起来与教材相仿，相邻关系却变了，后面圈出来的项不成立。
- 缺变量的乘积项只填一格，漏掉 $2^k-1$ 格。
- 四变量图的行列顺序记成 00、01、10、11。
- 列的标号 $BC$ 写成 $CB$，$m_1$（001）与 $m_2$（010）落错列。

::: quiz 排错 锚点：行列标号按二进制顺序排的卡诺图
:::

::: note 卡诺图在数字钟里的两处用处
译码器要把 BCD 码换成七段段码，每一段都是一张小真值表；计数器的每一位触发器都要一张次态真值表。这两处都要经过卡诺图化简，分别在第 4 章和第 6 章回到它们。本课只负责把 1 放进正确的格子。
:::

## 上手：把图交给断言

格位对不对，可以交给程序核对：把卡诺图按格读成一串取值，再用编号对应到真值表的每一行，逐格比对。这样填错一格，立刻能定位到是哪一行的取值出错。

这一课的练手在 lab 里做，正文只给入口。

::: practice 上手做 | 三步填图，交 lab 逐格核对

- 载体：本机 Python 3.13，用 `python -m unittest` 跑断言，不装新的工具。
- 入口：[lab/0001 · 卡诺图填图](../lab/README.md)，任务、断言与卡壳顺序都在里面。
- 三步：给真值表填三变量图；给含缺变量项的表达式填四变量图；把一张填错的图改回来。
- 每步都有逐格断言，填错会指出是哪一行取值、错在哪个格号上。

:::

::: resources
- 康华光、张林《电子技术基础 数字部分》第 7 版 §2.4.1 用卡诺图表示逻辑函数 | 本课主来源：格位、行列标号与由表达式填图
- [MIT OCW 6.004 Computation Structures](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/) | 对照讲法：第 4 章 Combinational Logic 的最简化讲法（只借讲法，实验写法不同）
:::
