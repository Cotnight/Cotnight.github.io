---
title: 对偶与范式
goal: 按一套固定动作把公式化成主析取范式与主合取范式，读出成真赋值，并写出任意公式的对偶式。
---

## 这一课要交什么

这一节对应教材第一章 1.7，分三块：对偶式与对偶原理（1.7.1）、析取范式与合取范式（1.7.2）、主析取范式与主合取范式（1.7.3）。课上 1.1–1.6 的命题、五个联结词、真值表、等值演算在本课当工具用，不重讲；公式一律按教材写法用 $P$、$Q$、$R$，小写 $p$、$q$、$r$ 同义。

试卷对这一节有三种问法：

- 求某公式的析取范式与合取范式；
- 求某公式的主析取范式与主合取范式，并写出成真赋值、成假赋值，或判断公式类型；
- 判断两个公式是否等价。

三种问法共用一个产出：公式唯一的标准形，以及它的编号表。本课练的就是把任意公式推到那个标准形，编号一个不漏。推理证明属于 1.8，本课不涉及。

这一节还有第二重用处：1.8 判定"推理有效"靠的是"前提合取蕴含结论是重言式"，而认重言式最省事的工具就是主范式。编号写对，判有效才落得下去。

::: svg
alt: 从原式到主范式的四步流程
caption: 四步固定动作，各自的产出与最终编号

<svg viewBox="0 0 560 380" role="img" aria-hidden="true">
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <rect x="24" y="16" width="196" height="48" rx="8"/>
    <rect x="24" y="116" width="196" height="48" rx="8"/>
    <rect x="24" y="216" width="196" height="48" rx="8"/>
    <rect x="24" y="316" width="196" height="48" rx="8"/>
    <path d="M122 64v36"/>
    <path d="M122 164v36"/>
    <path d="M122 264v36"/>
  </g>
  <g fill="currentColor" stroke="none">
    <polygon points="122,114 116,100 128,100"/>
    <polygon points="122,214 116,200 128,200"/>
    <polygon points="122,314 116,300 128,300"/>
  </g>
  <g fill="currentColor" font-size="16" text-anchor="middle">
    <text x="122" y="46">原式</text>
    <text x="122" y="146">范式（不唯一）</text>
    <text x="122" y="246">主范式（唯一）</text>
    <text x="122" y="346">编号与赋值</text>
  </g>
  <g fill="currentColor" font-size="16">
    <text x="240" y="80">① 化归 ② 否号内移</text>
    <text x="240" y="104">③ 拆括号定向</text>
    <text x="240" y="192">④ 补缺变元</text>
    <text x="240" y="292">按编号写 m 或 M</text>
  </g>
</svg>
:::

## 六条主干，其余现推

教材 1.4 的命题定律表（P15 表1-4.8）有二十多条式子。范式演算里真正反复用到的只有下面六条，其余条目现推，不必背表。

| 主干 | 式子 |
| --- | --- |
| ① 蕴含消除 | $A\to B\Leftrightarrow\neg A\vee B$ |
| ② 等价消除 | $A\leftrightarrow B\Leftrightarrow(A\to B)\wedge(B\to A)$ |
| ③ 双重否定 | $\neg\neg A\Leftrightarrow A$ |
| ④ 德摩根 | $\neg(A\wedge B)\Leftrightarrow\neg A\vee\neg B$ |
| ⑤ 分配 | $C\wedge(A\vee B)\Leftrightarrow(C\wedge A)\vee(C\wedge B)$ |
| ⑥ 0 与 1 | $A\vee1\Leftrightarrow1$、$A\wedge0\Leftrightarrow0$、$A\vee0\Leftrightarrow A$、$A\wedge1\Leftrightarrow A$、$A\vee\neg A\Leftrightarrow1$、$A\wedge\neg A\Leftrightarrow0$ |

先推吸收律 $A\vee(A\wedge B)\Leftrightarrow A$：

$$
A\vee(A\wedge B)\Leftrightarrow(A\wedge1)\vee(A\wedge B)\Leftrightarrow A\wedge(1\vee B)\Leftrightarrow A\wedge1\Leftrightarrow A
$$

再推幂等律 $A\vee A\Leftrightarrow A$：

$$
A\vee A\Leftrightarrow(A\vee A)\wedge1\Leftrightarrow(A\vee A)\wedge(A\vee\neg A)\Leftrightarrow A\vee(A\wedge\neg A)\Leftrightarrow A\vee0\Leftrightarrow A
$$

两个推导的每一步都只用上表六条之一，其中 $A\wedge(1\vee B)$ 与 $A\vee(A\wedge\neg A)$ 两处把 ⑤ 反着用。这么推出来的式子不用记，要用时重推一次。对偶（下一节）再送两条：把上两式各取对偶，得到 $A\wedge(A\vee B)\Leftrightarrow A$ 与 $A\wedge A\Leftrightarrow A$。一条主干配一次对偶，抵两条公式。

::: practice 练习 | 第 1 步 · 只用主干推一次

下面三条里任选两条，各写一行推导链，每一步标出用的是第几条主干（1.6 里 $\uparrow$、$\downarrow$ 的定义可以当辅助）：

- $A\wedge(A\vee B)\Leftrightarrow A$
- $\neg(A\to B)\Leftrightarrow A\wedge\neg B$
- $(A\wedge B)\vee A\Leftrightarrow A$

写完抽一组取值自查，例如 $A=1$、$B=0$，两侧结果必须相同。

:::

## 对偶：∧ 与 ∨ 对调

教材 1.7.1 开头给了来由：1.4 的命题定律表里，多数等价式成对出现，每一对只差把 ∧ 与 ∨ 互换。把这个规律固定成定义，就得到对偶式。

定义 1.7.1（教材原文）：设命题公式 $A$ 仅含联结词 $\neg$、$\wedge$、$\vee$，在 $A$ 中将 $\vee$、$\wedge$、$1$、$0$ 分别换以 $\wedge$、$\vee$、$0$、$1$ 得出公式，则此公式称为 $A$ 的对偶公式，记作 $A^{\ast}$。

替换共三组；命题变元、括号、否定号一概不动：

- $\wedge$ 与 $\vee$ 互换；
- $1$ 与 $0$ 互换；
- 公式里出现与非 $\uparrow$ 或 或非 $\downarrow$ 时，$\uparrow$ 与 $\downarrow$ 互换。依据是 1.6 的两条定义 $P\uparrow Q\Leftrightarrow\neg(P\wedge Q)$ 与 $P\downarrow Q\Leftrightarrow\neg(P\vee Q)$，教材 1.7.1 由此给出 $(P\uparrow Q)^{\ast}=P\downarrow Q$。

取两次对偶回到原式。

教材 1.7.1 的三个例子：

- $(\neg P\vee(Q\wedge R))^{\ast}=\neg P\wedge(Q\vee R)$；
- $((P\wedge Q)\wedge1)^{\ast}=(P\vee Q)\vee0$；
- $(P\wedge Q)\uparrow R$ 的对偶式是 $(P\vee Q)\downarrow R$。

两个结论（教材定理 1.7.2 与 1.7.3，只记用法，不证）：

- 对偶原理：若两个公式等价，则它们的对偶式也等价。用法是定律表里成对的式子只记一条，另一条取对偶即得。
- 若 $A\Rightarrow B$，则 $B^{\ast}\Rightarrow A^{\ast}$：蕴含式的对偶要把方向倒过来。

对偶写错能当场查出来。把 $\uparrow$、$\downarrow$ 先折成 $\neg$、$\wedge$、$\vee$，取对偶，再折回去，两条路必须一致。以 $(P\wedge Q)\uparrow R$ 为例：

$$
(P\wedge Q)\uparrow R\;\Leftrightarrow\;\neg((P\wedge Q)\wedge R)\;=\;\neg(P\wedge Q\wedge R)
$$

取对偶后 ∧ 全变 ∨，得 $\neg(P\vee Q\vee R)$，再由 $\downarrow$ 的定义折回 $(P\vee Q)\downarrow R$。

::: warn 只换 ∧ 与 ∨ 会漏
对偶要换的是三组符号。公式里有 $\uparrow$ 或 $\downarrow$ 时漏掉这一组的互换，写出来的是另一个公式，而且它照样能算到底，错得不容易被发现。
:::

::: quiz 理解 锚点：对偶式要换哪三组符号
empty_reason: 三组符号已并入「(P∧Q)↑R 的对偶式」那道排错题的判分要点，单出一题只剩背诵
:::

::: quiz 排错 锚点：(P∧Q)↑R 的对偶式
:::

## 文字与两种范式

定义 1.7.2（教材原文）：命题变元及其否定统称文字；仅有有限个文字组成的析取式称为简单析取式，组成的合取式称为简单合取式。

定义 1.7.3（教材原文）：一个命题公式称为析取范式，当且仅当它具有形式 $A_1\vee A_2\vee\cdots\vee A_n$，其中每个 $A_i$ 都是简单合取式；称为合取范式，当且仅当它具有形式 $A_1\wedge A_2\wedge\cdots\wedge A_n$，其中每个 $A_i$ 都是简单析取式。析取范式与合取范式统称范式。

范式存在定理 1.7.4：任一个命题公式都存在着与之等价的析取范式与合取范式。

两条立刻能用的性质：

- 一个析取范式是矛盾式，当且仅当它的每一个简单合取式都是矛盾式（即同时含有某个变元及其否定）；
- 一个合取范式是重言式，当且仅当它的每一个简单析取式都是重言式。

范式的问题是它不唯一。对同一个公式，$P\vee(Q\wedge\neg R)$ 与 $P\vee(P\wedge\neg R)\vee(Q\wedge\neg R)$ 都是析取范式。判等价要求等价的公式有同一张标准形，主范式就是为这件事引入的（1.7.3 开头）。

## 小项、大项与编号

定义 1.7.4（教材原文）：在含有 $n$ 个命题变元的简单合取式中，若每个命题变元和它的否定不同时出现，而二者之一必出现且仅出现一次，称这样的简单合取式为小项。定义 1.7.6 把同一条用于简单析取式，称大项。

编号规则（教材 P33 表1-7.1）：

- 变元按字母顺序排位：$P$ 记 4、$Q$ 记 2、$R$ 记 1，第一个变元占最高位；
- 小项 $m_i$ 的 $i$ 是这个式子取真值时 $P,Q,R$ 的二进制值（真记 1）；
- 大项 $M_i$ 的 $i$ 是它取假值时的二进制值。

于是同一行赋值上 $m_i$ 为真、$M_i$ 为假，两者编号相同。三个变元的八个小项：

| 小项 | 编号 | 成真赋值 |
| --- | --- | --- |
| $\neg P\wedge\neg Q\wedge\neg R$ | $m_0$ | 000 |
| $\neg P\wedge\neg Q\wedge R$ | $m_1$ | 001 |
| $\neg P\wedge Q\wedge\neg R$ | $m_2$ | 010 |
| $\neg P\wedge Q\wedge R$ | $m_3$ | 011 |
| $P\wedge\neg Q\wedge\neg R$ | $m_4$ | 100 |
| $P\wedge\neg Q\wedge R$ | $m_5$ | 101 |
| $P\wedge Q\wedge\neg R$ | $m_6$ | 110 |
| $P\wedge Q\wedge R$ | $m_7$ | 111 |

大项不用另记表：小项整体取反就是同编号的大项。$m_5=P\wedge\neg Q\wedge R$ 取反得 $M_5=\neg P\vee Q\vee\neg R$，它在 101 上取假，编号与对照表一致。

小项的三条性质（教材 1.7.3）：没有两个小项等价，每个小项有且仅有一个成真赋值；任意两个不同小项的合取为矛盾式；全体小项的析取为永真式。大项的三条性质逐条与它们对偶：每个大项有且仅有一个成假赋值；任意两个不同大项的析取为永真式；全体大项的合取为矛盾式。

定义 1.7.5 与 1.7.7：析取范式中每一个简单合取式都是小项，称主析取范式；合取范式中每一个简单析取式都是大项，称主合取范式。定理 1.7.5：任何命题公式都存在着与之等价的主析取范式与主合取范式，并且唯一。

::: quiz 理解 锚点：小项编号与变元位序
:::

## 四步求出主范式

四步固定动作。前三步是教材的"求命题公式的范式的基本步骤"，第四步是教材"求主析取范式的推演步骤"的第 (4) 条，两处合成一套动作：

1. 化归：把 $\to$、$\leftrightarrow$、$\uparrow$、$\downarrow$ 全换成只含 $\neg$、$\wedge$、$\vee$ 的式子。
2. 否号内移：用 $\neg\neg A\Leftrightarrow A$ 与德摩根，把每个否定号推到单个变元前面。
3. 拆括号定向：要析取范式，把 ∧ 分配进 ∨；要合取范式，把 ∨ 分配进 ∧。顺手删掉恒假支（析取范式里含 $X\wedge\neg X$ 的支）或恒真项（合取范式里含 $X\vee\neg X$ 的项），并掉重复支与重复文字。
4. 补缺变元：某一支缺某个变元 $P_i$，就按 $B\Leftrightarrow B\wedge(P_i\vee\neg P_i)$ 展开，合取路线用它的对偶 $B\Leftrightarrow B\vee(P_i\wedge\neg P_i)$，补到每个变元都在，再按上一节的位序查编号。

第 4 步是两条路线唯一分开的地方，前三步完全相同。这也是对偶在演算里最实际的用处：两条路线只需练一条。

教材 1.7.2 例1：求 $((P\vee Q)\to R)\to P$ 的析取范式与合取范式。

$$
\begin{aligned}
((P\vee Q)\to R)\to P &\Leftrightarrow \neg(\neg(P\vee Q)\vee R)\vee P \\
&\Leftrightarrow ((P\vee Q)\wedge\neg R)\vee P \\
&\Leftrightarrow (P\wedge\neg R)\vee(Q\wedge\neg R)\vee P \quad(\text{析取范式}) \\
&\Leftrightarrow P\vee(Q\wedge\neg R) \\
&\Leftrightarrow (P\vee Q)\wedge(\neg R\vee P) \quad(\text{合取范式})
\end{aligned}
$$

对 $P\vee(Q\wedge\neg R)$ 做第 4 步（缺几个变元就连补几次）：

$$
\begin{aligned}
P &\Leftrightarrow P\wedge(Q\vee\neg Q)\wedge(R\vee\neg R) \Leftrightarrow m_7\vee m_6\vee m_5\vee m_4 \\
Q\wedge\neg R &\Leftrightarrow (P\vee\neg P)\wedge Q\wedge\neg R \Leftrightarrow m_6\vee m_2
\end{aligned}
$$

合起来并掉重复的 $m_6$：主析取范式为 $m_2\vee m_4\vee m_5\vee m_6\vee m_7$。主合取范式取补集即得 $M_0\wedge M_1\wedge M_3$，教材在例1 之后给出的正是这一对。

::: quiz 改造 锚点：缺变元补成小项
empty_reason: 这步是机械动作，lab 第 2 步的 expand_term 断言已逐支验过，页内不再占一道题
:::

## 真值表路线

定理 1.7.6 与 1.7.7 把同一件事说成真值表上的两行话：真值为 1 的指派所对应的小项的析取，就是主析取范式；真值为 0 的指派所对应的大项的合取，就是主合取范式。

于是第二条路线是列 $2^n$ 行真值表，真值为 1 的行记编号写 $m$，真值为 0 的行记同一个编号写 $M$。变元多时这条路线更稳，每行只算一次真假，不必展开。

教材 1.7.3 例2：$(P\to Q)\leftrightarrow R$。

| P | Q | R | 原式 |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 1 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 |

真值为 1 的行是 001、011、100、111，对应 $m_1$、$m_3$、$m_4$、$m_7$，主析取范式为 $m_1\vee m_3\vee m_4\vee m_7$。真值为 0 的行是 000、010、101、110，对应 $M_0\wedge M_2\wedge M_5\wedge M_6$。两组编号正好互补，这一条对任何公式都成立。

::: svg
alt: 成真行取小项、成假行取大项的编号对照
caption: 同一张真值表上，1 的行给 m、0 的行给 M，两组编号互补

<svg viewBox="0 0 640 200" role="img" aria-hidden="true">
  <g fill="currentColor" font-size="16">
    <text x="12" y="24">真值为 1 的行：取小项 m</text>
    <text x="12" y="98">真值为 0 的行：取大项 M</text>
  </g>
  <g stroke="currentColor" fill="none" stroke-width="1">
    <rect x="12" y="36" width="64" height="40" rx="6"/>
    <rect x="88" y="36" width="64" height="40" rx="6"/>
    <rect x="164" y="36" width="64" height="40" rx="6"/>
    <rect x="240" y="36" width="64" height="40" rx="6"/>
    <rect x="316" y="36" width="64" height="40" rx="6"/>
    <rect x="392" y="36" width="64" height="40" rx="6"/>
    <rect x="468" y="36" width="64" height="40" rx="6"/>
    <rect x="544" y="36" width="64" height="40" rx="6"/>
    <rect x="12" y="110" width="64" height="40" rx="6"/>
    <rect x="88" y="110" width="64" height="40" rx="6"/>
    <rect x="164" y="110" width="64" height="40" rx="6"/>
    <rect x="240" y="110" width="64" height="40" rx="6"/>
    <rect x="316" y="110" width="64" height="40" rx="6"/>
    <rect x="392" y="110" width="64" height="40" rx="6"/>
    <rect x="468" y="110" width="64" height="40" rx="6"/>
    <rect x="544" y="110" width="64" height="40" rx="6"/>
  </g>
  <g stroke="currentColor" stroke-width="2.5" fill="currentColor" fill-opacity="0.12">
    <rect x="88" y="36" width="64" height="40" rx="6"/>
    <rect x="240" y="36" width="64" height="40" rx="6"/>
    <rect x="316" y="36" width="64" height="40" rx="6"/>
    <rect x="544" y="36" width="64" height="40" rx="6"/>
    <rect x="12" y="110" width="64" height="40" rx="6"/>
    <rect x="164" y="110" width="64" height="40" rx="6"/>
    <rect x="392" y="110" width="64" height="40" rx="6"/>
    <rect x="468" y="110" width="64" height="40" rx="6"/>
  </g>
  <g fill="currentColor" font-size="16" text-anchor="middle">
    <text x="44" y="62">m0</text>
    <text x="120" y="62">m1</text>
    <text x="196" y="62">m2</text>
    <text x="272" y="62">m3</text>
    <text x="348" y="62">m4</text>
    <text x="424" y="62">m5</text>
    <text x="500" y="62">m6</text>
    <text x="576" y="62">m7</text>
    <text x="44" y="136">M0</text>
    <text x="120" y="136">M1</text>
    <text x="196" y="136">M2</text>
    <text x="272" y="136">M3</text>
    <text x="348" y="136">M4</text>
    <text x="424" y="136">M5</text>
    <text x="500" y="136">M6</text>
    <text x="576" y="136">M7</text>
    <text x="320" y="182">同一行上 m 与 M 编号相同，两组编号合起来正好把全部编号占满</text>
  </g>
</svg>
:::

用四步法做同一题，得到的是大项那一组：$(P\to Q)\leftrightarrow R$ 化到合取范式 $(P\vee R)\wedge(\neg Q\vee R)\wedge(\neg P\vee\neg R\vee Q)$，三项分别补成 $M_0\wedge M_2$、$M_2\wedge M_6$ 与 $M_5$，合起来 $M_0\wedge M_2\wedge M_5\wedge M_6$，与真值表一致。教材 1.7.3 例2 同时给出 $m_1\vee m_3\vee m_4\vee m_7$ 与 $M_0\wedge M_2\wedge M_5\wedge M_6$，两条路线的答案互相盖章。

::: practice 上手做 | 第 2 步 · 两条路线各做一题

真值表路线：求 $(P\vee Q)\to R$ 的主析取范式与主合取范式。列八行表，真值 1 的行写 $m$、真值 0 的行写 $M$，最后写出全部成真赋值。

四步路线：取上面这道教材例2 的 $(P\to Q)\leftrightarrow R$，按四步从头写一遍（合取路线），与真值表给的两组编号对账。

两题做完各写一句：哪条路线在手上步数更少；哪一步最容易写错。

:::

::: quiz 应用 锚点：由主范式读出成真赋值与公式类型
:::

## 主范式读出的三件事

有了主范式，教材 1.7.3 第 4 小节的三类问法都变成查编号：

- 成真赋值与成假赋值：主析取范式里的编号就是成真赋值，主合取范式里的编号就是成假赋值。含 $n$ 个变元、主析取范式有 $s$ 个小项，就有 $s$ 个成真赋值与 $2^n-s$ 个成假赋值。
- 公式类型：主析取范式含全部 $2^n$ 个小项，公式是重言式；一个小项都没有，记作 $0$，是矛盾式；至少含一个小项，是可满足式。对偶过来，主合取范式一个项都没有时公式是重言式，记作 $1$；含全部 $2^n$ 个大项时是矛盾式。
- 判等价：两个公式按同一组 $n$ 个变元各求主范式，相同则等价。求的时候变元取两式的并集，不能各按自己出现的变元算。

判等价的第一个例子（教材 1.7.3）：$(P\to Q)\wedge(P\to R)$ 与 $P\to(Q\wedge R)$。前式化成 $(\neg P\vee Q)\wedge(\neg P\vee R)$，两项补变元得 $M_4\wedge M_5\wedge M_6$；后式即 $\neg P\vee(Q\wedge R)$，再分配得同一个合取范式。主范式相同，两个公式等价。

第二个例子：$P\to(Q\wedge R)$ 与 $P\vee(Q\to R)$。前式是 $M_4\wedge M_5\wedge M_6$，即 $m_0\vee m_1\vee m_2\vee m_3\vee m_7$；后式 $P\vee\neg Q\vee R$ 只含一个大项 $M_2$，即 $m_0\vee m_1\vee m_3\vee m_4\vee m_5\vee m_6\vee m_7$。两组编号不同，两个公式不等价。

判蕴含放在 1.8：$A\Rightarrow B$ 当且仅当 $A\to B$ 是重言式，那时主范式与真值表都还是可用的工具。

::: quiz 应用 锚点：用主范式判定两个公式等值
empty_reason: 判等值在 lab 的 same_function 里由编号表逐题验，页内让位给「读出成真赋值与公式类型」
:::

## 一道完整的作业题

题目：求 $(P\to Q)\wedge(Q\to R)$ 的主析取范式与主合取范式，并写出全部成真赋值。

两个蕴涵连成合取，第 1 步几乎不用动，第 3 步也不用拆，直接进第 4 步。按合取路线求大项最短。

第 1 步 化归：$(P\to Q)\wedge(Q\to R)\Leftrightarrow(\neg P\vee Q)\wedge(\neg Q\vee R)$。两项都是简单析取式，这已经是一个合取范式。

第 4 步 补缺变元：

$$
\begin{aligned}
\neg P\vee Q &\Leftrightarrow (\neg P\vee Q\vee R)\wedge(\neg P\vee Q\vee\neg R) = M_4\wedge M_5 \\
\neg Q\vee R &\Leftrightarrow (P\vee\neg Q\vee R)\wedge(\neg P\vee\neg Q\vee R) = M_2\wedge M_6
\end{aligned}
$$

合起来：主合取范式 $M_2\wedge M_4\wedge M_5\wedge M_6$，成假赋值 010、100、101、110。取补集得主析取范式 $m_0\vee m_1\vee m_3\vee m_7$，成真赋值 000、001、011、111。

抽查两个大项：$M_2=P\vee\neg Q\vee R$ 在 010 上为 $0\vee0\vee0=0$，取假，编号对；$M_6=\neg P\vee\neg Q\vee R$ 在 110 上为 $0\vee0\vee0=0$，取假，编号对。

再用真值表对账两列中间结果：

| P | Q | R | $\neg P\vee Q$ | $\neg Q\vee R$ | 原式 |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 1 | 1 | 1 |
| 0 | 0 | 1 | 1 | 1 | 1 |
| 0 | 1 | 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 | 1 | 0 |
| 1 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 1 | 1 | 1 | 1 |

真值为 1 的行 000、001、011、111 正好是 $m_0$、$m_1$、$m_3$、$m_7$，与四步法的结果一致。两条路线互相盖章，是这类题最省事的自检。

代数展开也能到同一个答案，但展开时两支会重合：

$$
(\neg P\vee Q)\wedge(\neg Q\vee R)\Leftrightarrow(\neg P\wedge\neg Q)\vee(\neg P\wedge R)\vee(Q\wedge R)
$$

四支交叉相乘后 $(Q\wedge\neg Q)$ 那支恒假要删。补变元时 $(\neg P\wedge\neg Q)$ 给 $m_0$ 与 $m_1$，$(\neg P\wedge R)$ 给 $m_1$ 与 $m_3$，$(Q\wedge R)$ 给 $m_3$ 与 $m_7$：$m_1$ 与 $m_3$ 各出现两次。合并时若把重合的那一项当成"已经算过"，顺着就漏掉另一处来源，整组编号跟着错。四步法不经过这一步：第 4 步只按"缺哪个变元"拆，不跨支合并。

::: quiz 排错 锚点：展开时两支重合容易漏项
:::

## 三处错法与自检

作业里这一节有三处高频失分，改法各不相同。

错法一：编号整组对不上。根因是用代数展开硬推范式，交叉相乘后重合的支靠眼睛合并，漏一支编号就全错。改法是按四步走，第 3、4 步都是机械动作；写完用互补关系自查，主析取范式的编号与主合取范式的编号合起来必须正好是 $\{0,1,\dots,2^n-1\}$，不多、不少、不重。

错法二：否号进括号没换运算，把 $\neg P\vee\neg Q$ 写成 $\neg(P\vee Q)$。正确的对应是 $\neg P\vee\neg Q\Leftrightarrow\neg(P\wedge Q)$。抽一行就能看出来：取 $P=1$、$Q=0$，左边 $0\vee1=1$，而 $\neg(P\vee Q)=\neg1=0$，两式不等价。否定号进出括号，$\wedge$ 与 $\vee$ 都要换，进去一次是换，出来一次也是换。

错法三：对偶只换了一半，把 $(P\wedge Q)\uparrow R$ 的对偶式写成 $(P\vee Q)\uparrow R$。对偶换三组符号，$\uparrow$ 与 $\downarrow$ 必须一起翻，正确的是 $(P\vee Q)\downarrow R$。

交卷前三条自查：

- 主析取范式的编号与主合取范式的编号互补，合起来正好 $2^n$ 个；
- 每个小项里 $n$ 个变元各出现一次，取它本身或它的否定，恰好一次；
- 成真赋值的个数等于主析取范式里小项的个数，也等于真值表里真值为 1 的行数。

::: practice 回头改 | 第 3 步 · 把三处错法改对

1. 用四步法把 $(P\to Q)\wedge(Q\to R)$ 重做一遍，只写大项那一组，写完核对编号互补。
2. 把 $\neg P\vee\neg Q$ 化成只含 $\neg$ 与 $\wedge$ 的式子，再取 $P=1$、$Q=0$ 验一次。
3. 写出 $(P\wedge Q)\uparrow R$ 的对偶式，用"折成 $\neg$、$\wedge$、$\vee$ 再取对偶"的路子验一遍。

三题都写完，把每题的编号或结果与上面的自查三条逐条对一遍。

:::

::: practice 上手做 | 交 lab 用断言核对

载体是本机 Python 3.13，命令行跑 `python -m unittest`，不装任何东西。入口：[lab · 对偶与范式](../lab/README.md)。

这个 lab 干一件事：把你手算出来的范式结果交给断言逐行核对——成真赋值、小项编号、$\Sigma m$ 与 $\Pi M$ 是否互补，错在哪一行会直接报出来。

保底提示：先照上面的四步法自己手算一遍，再去跑断言对照；顺序反过来，错的就不只是计算，而是你看错了哪一行。

:::

::: quiz 排错 锚点：否号进括号要换运算
:::

::: note 后面的用法
这一套编号在后续内容里会反复出现：判等价、判推理有效（1.8）都按同一套编号走，实验一的真值表引擎也按它输出。本课不涉及程序。
:::

::: resources
- [老师课件 1 · 1.7 对偶与范式（第 101–146 页）](../reference/01-左孝凌课件1.html) | 本地课件 · 本节按它的小节顺序与原话组织，例题编号一致
- 左孝凌《离散数学》第一章 1.7 对偶与范式 | 书 · 小项真值表在 P33 表1-7.1，作业题在 P39
:::
