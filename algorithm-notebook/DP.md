## 一维 DP

[LC 70](https://leetcode-cn.com/problems/climbing-stairs/) 送分题，直接写出 dp[i] = dp[i-1] + dp[i-2]，搞定。

[LC 746](https://leetcode-cn.com/problems/min-cost-climbing-stairs/) 稍微复杂一点，给每个台阶增加了 cost，但还是很容易写出状态转移方程 dp[i] = Math.min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]);

[198. 打家劫舍](https://leetcode-cn.com/problems/house-robber/) 也是送分题，直接写出 dp[i] = Math.max(dp[i-1], dp[i-2] + nums[i-1])，搞定。

[213 打家劫舍变形题](https://leetcode-cn.com/problems/house-robber-ii/)，说的是这个数组是个环，其实说白了就是第一家和最后一家不能一块儿偷，所以其实就是把第一家去掉后走一遍 dp，把最后一家去掉后走一遍 dp，然后两个结果取大的那个就行了。

[LC 1218](https://leetcode-cn.com/problems/longest-arithmetic-subsequence-of-given-difference/) 最长等差子序列，也是一维 DP，可以很容易写出 dp[x] = dp[x-d] + 1; 但是要利用一下 hashMap 辅助状态转移方程。

这种题都是一维状态的动态规划，相对比较简单。难点往往在于想到用 dp，以及写出状态转移方程。

[LC 139 ](https://leetcode-cn.com/problems/word-break/)，word break，给定一个字符串和一个字典（字符串数组），问该字符串是否能用字典里面的词组合而成。这题的代码非常简洁，难点在于想到用 dp[i]表示 s[:i]是否能用字典内单词组成。

```java
for (int i = 1; i<=s.length; i++) {
    for (int j = i - 1; j >=0; j--) {
        if(dp[j] && wordDict.contains(s.substring(j, i))) {
            dp[i] = true; break;
        }
    }
}
```

## 二维状态的 DP (不同路径数，最小路径和)

[LC 62](https://leetcode-cn.com/problems/unique-paths/), [LC 63](https://leetcode-cn.com/problems/unique-paths-ii/), [LC 64](https://leetcode-cn.com/problems/minimum-path-sum/)

这三题其实是一模一样的路子，也都是送分题。就是把状态从一维变成二维罢了。上面三道题看起来比较容易想到二维 DP，因为本身题目中就有一个二维对象存在。

[LC72](https://leetcode-cn.com/problems/edit-distance/),
[LC97](https://leetcode-cn.com/problems/interleaving-string/),
[LC115](https://leetcode-cn.com/problems/distinct-subsequences/),
[LC712](https://leetcode-cn.com/problems/minimum-ascii-delete-sum-for-two-strings/)
这一类题也非常常见，但是不太容易想到二维 DP，这类题目看上去是在两个一维数组中查找某个最优解，因此有时不太容易想到二维 DP。但是事实上，两个一维数组一交叉不就变成二维了么。这种问题的关键就是想到 dp[i][j] = solution for (A[:i], B[:j])。

72 题是两个词的编辑距离，比如 horse 和 ros，可以通过将 ros 的 r 改成 h，然后添加 r 和 e，一共三步来完成转移。定义 dp[i][j]为 w1[:i]和 w2[:j]的编辑距离。

```java
if (w1[i] == w2[j]) dp[i][j] = dp[i-1][j-1]
else dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
```

97 给定三个字符串 s1, s2, s3，判断 s3 是否由 s1 和 s2 交错而成。

```java
dp[i][j] = (dp[i-1][j] && s3[i+j-1] == s1[i-1]) ||
           (dp[i][j-1] && s3[i+j-1] == s2[j-1])
```

115 给定一个字符串 s 和一个字符串 t，计算 t 在 s 中出现的个数。比如 s = "rabbbit"，t = "rabbit"，t 在 s 中算出现了三次(三个 b 中选两个 b，一共有三种)。

```java
if t[i] == s[j] dp[i][j] = dp[i-1][j-1] + dp[i][j-1]
else dp[i][j] = dp[i][j-1]
```

712 给定两个字符串，找到使两个字符串相等所需删除字符的 ASCII 值的最小和。比如 s1 = sea，s2 = eat，删除 s 和 t 可使两个字符串相等。

**这道题其实可以反过来看，只要将两个字符串的 ASCII 和相加再减去两倍的最大共同子序列和就得到了答案。我们可以定义 dp[i][j] 为 s1[:i]和 s2[:j]的最大公共子序列和。**

```java
if (s1[i] == s2[j])
    dp[i][j] = dp[i-1][j-1] + ASCII(s1[i])
else
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

# 多个状态的动态规划

多个状态的动态规划和二维 DP 还是不一样的，我觉得其更接近一维 DP，只是状态数和状态转移方程要稍微复杂一点，其解法通常类似一维 DP，只是在遍历过程中更新多个状态，最终结果也需要组合多个最终状态。

LC 790 铺两种类型的瓷砖 Domino and Tromino Tiling

这道题很有意思，我们用 dp[i][0]表示到 2 i 的地面被铺满的方式总数，用 dp[i][1]表示 2 i 地面被铺满还差一格的方式数。我们可以写出下面的转移方程代码。

```java
dp[i][0] = dp[i-1][0]+dp[i-2][0] + 2 * dp[i-1][1]
dp[i][1] = dp[i-2][0]+dp[i-1][1];
```

LC 801 使序列递增的最小交换次数，其实这题和 790 有点像。

https://leetcode-cn.com/problems/minimum-swaps-to-make-sequences-increasing/

DP 的一个思想就是：如果你不知道咋做，你就想假设你已经做好了，再扩展一下这个问题规模怎么办？也就是说，如果我们已经通过交换让这两个数组递增了，这时候两个数组后面又多了两个元素，怎么办？

```
if (A[i] > A[i-1] && B[i] > B[i-1])
    keep[i] = keep[i-1]
    swap[i] = swap[i-1] + 1
if (A[i] > B[i-1] && B[i] > A[i-1])
    swap[i] = Math.min(swap[i], keep[i-1]+1)
    keep[i] = Math.min(keep[i], swap[i-1])

最后 return Math.min(keep[n-1], swap[n-1])
```

LC 1220 统计元音字母 permutation 的数目，这题更进一步，有五个状态，但其实还是一个套路。

```java
a, e, i, o ,u = (i+e+u), (i+a), (e+o), (i), (i + o)
```

# 双向动态规划

LC 926 将字符串翻转为单调递增

```java
ldp[i] = ldp[i-1] + s[i] - '0';   // 在 i 左边有多少个 1
rdp[i] = rdp[i+1] + '1' - s[i];   // 在 i 右边有多少个 0
for (int i = 1; i < n; i++) ans = min(ans, ldp[i-1] + rdp[i])
```

LC 845 数组中最长的山脉

```java
if (arr[i] > arr[i-1]) incdp[i] = incdp[i-1] + 1
if (arr[i] > arr[i+1]) decdp[i] = decdp[i+1] + 1
ans = min(ans, incdp[i] + decdp[i] + 1)
```

# 背包问题

对于一组不同重量、不可分割的物品，我们需要选择一些装入背包，在满足背包最大重量限制的前提下，背包中物品总重量的最大值是多少呢？

```java
// 假设背包容量为w，总共有n个商品，我们用dp[i]表示是否可以带走重量为i的物品
boolean[] dp = new boolean[w+1];
dp[0] = true;
if (items[0] <= w) { dp[items[0]] = true; }
for (int i = 1; i < n; ++i) {
    for (int j = w-items[i]; j >= 0; --j) {//把第i个物品放入背包
        if (dp[j]==true) dp[j+items[i]] = true;
```

如果每个商品有价格，我们希望背包中物品总价格最大

```java
// int[] weight, int[] value, int n, int w
// 用dp[i][j]来表示前0-i个商品，容量为w的情况下能达到的最大值。
for (int i = 1; i < n; ++i) {
    for (int j = 0; j <= w; ++j) { // 不选择第i个物品
        if (dp[i-1][j] >= 0) dp[i][j] = dp[i-1][j];
    }
    for (int j = 0; j <= w-weight[i]; ++j) { // 选择第i个物品
        if (dp[i-1][j] >= 0) {
            int v = dp[i-1][j] + value[i];
            if (v > dp[i][j+weight[i]]) {
                dp[i][j+weight[i]] = v;
            }
        }
    }
}
```

# 卡特兰数

LC 96 给定一个 n，问以 1 到 n 这 n 个数组成的 BST 有多少

```java
dp[i] = sum{dp[j]*dp[i-j-1]} while j in [0, i)
```

# LC 312 戳气球

https://leetcode-cn.com/problems/burst-balloons/

这也是我特别喜欢的一题，因为这道题让我明白了一个道理，背动态规划模板是没有用的，重要的不是记住一个算法套路，而是解决问题的能力。

我们用 dp[i][j]表示当问题只包含 i->j 的气球时候的解。还是那句话，如果你不知道怎么解，可以假设自己已经解完了，然后想象如果多了两个气球怎么办？这可不是开玩笑，我做这题的时候就是这么想的，这能帮你更快地写出状态转移方程。如果我已经知道了 dp[i][j]的值，也就是如果只有从 i 到 j 的气球时的解，这时候我在前面或者后面又加了一个气球怎么办？

这时候我需要多戳一次气球了，也就是我能多得一次的分。但是我把哪些气球留到最后呢？这里有一个很简单但是很牛逼的技巧，就是在原来的气球组两侧各加入一个分数为 1 的气球，这样问题就变成了最后留下三个气球，并且两边的气球都留下的问题。我们可以据此写出下面的状态转移方程，其中 k 为(i -> j)间的每一个气球。

```java
dp[i][j] = max(dp[i][j], dp[i][k]+dp[k][j]+nums[i]*nums[k]*nums[j]);
```

这里还有一个很关键的点，当计算 dp[i][j]的时候 dp[i][k]和 dp[k][j]必须都已经被计算完成了。这意味着什么呢？

意味着 dp[i][j]这个数组中 j-i 比较小的元素要被先计算。也就意味着这个二维状态的计算并非「从左到右，从上到下」，而是沿着对角线方向计算。所以，迭代的第一层，应该是 i 到 j 的距离。

```java
for (int len = 2; len < nums.length; len++) {
    for (int i = 0; i < nums.length - len; i++) {
        int j = i+len;
        for (int k = i + 1; k < j; k++) {
            dp[i][j] = Math.max(dp[i][j], dp[i][k]+dp[k][j]+nums[i]*nums[k]*nums[j]);
        }
    }
}
return dp[0][newNums.length - 1];
```

LC 10 正则表达式匹配

给你一个字符串 s 和一个字符规律 p，请你来实现一个支持'.' 和 '\*' 的正则表达式匹配。这题可以用动态规划的关键在于：1. 想到用 dp[i][j]表示 s[i:]与 p[j:]是否能匹配。

```java
int tlen = text.length(), plen = pattern.length();
for (int i = tlen; i >= 0; i--)
    for (int j = plen - 1; j >= 0; j--)
        boolean first_match = (i < tlen &&
                               (pattern.charAt(j) == text.charAt(i) ||
                               pattern.charAt(j) == '.'));
        if (j + 1 < plen && pattern.charAt(j+1) == '*'){
            dp[i][j] = dp[i][j+2] || (first_match && dp[i+1][j]);
        } else {
            dp[i][j] = first_match && dp[i+1][j+1];
        }
```

LC 32 最长有效括号序列

```java
if s[i] == ')':
    if (s[i-1] == '('):
        dp[i] = dp[i-2] + 2
    else if (s[i - dp[i-1] - 1] == '('):
        dp[i] = dp[i-1] + dp[i-dp[i-1]-2] + 2
```
