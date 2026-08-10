---
source_pdf: 计算机基础知识.pdf（希赛系统架构设计师讲义·第一章）
part: 0107-系统性能
keywords: [Web性能, 并发连接数, 响应延迟, 吞吐量, 系统监视, ps, last, netstat, Perfmon]
tags: [ruankao, performance, concept]
---

# Web 服务器性能评估与系统监视

## Web 服务器性能评估

反映 Web 服务器性能的主要指标：
- **最大并发连接数**
- **响应延迟**
- **吞吐量**

常见评测方法：**基准性能测试、压力测试、可靠性测试**。

> [!important] 真题
> - 反映 Web 服务器性能的指标**不包括**（　）→ **A（链接正确跳转）**
> - 常见评测方法有基准性能测试、压力测试和（　）→ **D（可靠性测试）**

## 系统监视三种方式

1. 通过**系统本身提供的命令**：UNIX/Linux 的 `W`、`ps`、`last`；Windows 的 `netstat`
2. 通过**系统记录文件**查阅特定时间的运行状态
3. 集成命令、文件记录和可视化技术的**监控工具**：如 Windows 的 **Perfmon**

> [!important] 真题
> 一是通过（　），如 UNIX/Linux 的 ps、last → **A（系统命令）**；
> 三是监控工具，如（　）→ **C（Windows 的 Perfmon）**

> [!warning] 易错点
> - `netstat` 是 **Windows** 例子中的命令（讲义口径），`ps/last/W` 是 UNIX/Linux
> - Linux 的 `top` 也是监控工具，但真题选项配对按讲义：命令→系统命令，工具→Perfmon

## Related Notes
- [[Exam-Traps]]
- [[性能评估方法与基准程序]]
- [[性能指标MIPS与阿姆达尔定律]]
