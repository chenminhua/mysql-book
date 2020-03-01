# 左右子树递归套路

这种题基本都是白送，需要能够在 30s 内做出来的。很多题目都是在这些套路上改造的。

```python
寻找二叉树中最大值
max(root.val, maxval(root.left), maxval(root.right)) if root else 负无穷

树的最大深度
max(maxDepth(root.left), maxDepth(root.right)) + 1 if root else 0;

树的最小深度
def minDepth(root):
    if not root: return 0
    if root为叶子节点: return 1
    l = minDepth(root.left)
    r = minDepth(root.right)
    if (not root.left): return r + 1
    if (not root.right): return l + 1
    return min(l + r) + 1

判断两棵树是否相同
def sameTree(p, q):
    if (p空 且 q空) return true;
    if (p空 或 q空) return false;
    return p.val == q.val and sameTree(p.left, q.left) and sameTree(p.right, q.right)

判断两棵树是否互为镜像
def ismirror(p, q):
    if (p空 且 q空) return true;
    if (p空 或 q空) return false;
    return p.val == q.val and ismirror(p.left, q.right) and ismirror(p.right, q.left)

判断一个树是否为对称树
ismirror(root.p, root.q)

判断一棵树是否平衡
def isBalanced(root):
    if not root: return true;
    return isBalanced(root.left) and isBalanced(root.right) and
           (getHeight(root.left) - getHeight(root.right) <= 1)
def getHeight(root):
    return 1 + max(getHeight(root.left), getHeight(root.right)) if root else 0

二叉树中两个节点的最低公共祖先
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if(root == null || root.val == p.val || root.val == q.val) return root;
    TreeNode l = lowestCommonAncestor(root.left, p, q);
    TreeNode r = lowestCommonAncestor(root.right, p, q);
    if (l != null && r != null) return root;
    if(l == null) return r;
    return l;
}

BST的最近公共祖先
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root.val<p.val && root.val<q.val)
        root=lowestCommonAncestor(root.right,p,q);
    else if (root.val>p.val && root.val>q.val)
        root=lowestCommonAncestor(root.left,p,q);
    return root;
}

合并两个二叉树 LC617
public TreeNode mergeTrees(TreeNode t1, TreeNode t2) {
    if (t1 == null) return t2;
    if (t2 == null) return t1;
    t1.val += t2.val;
    t1.left = mergeTrees(t1.left, t2.left);
    t1.right = mergeTrees(t1.right, t2.right);
    return t1;
}

填充每一个节点的下一个右侧节点 LC 116
if (root == null || root.left == null) return root;
root.left.next = root.right;
if (root.next != null) root.right.next = root.next.left;
connect(root.left);
connect(root.right);
return root;
```

# BST

```java
// LC 98 校验一棵二叉树是否为BST
public boolean isValidBST(TreeNode root) {
    return isValid(root, null, null);
}
private boolean isValid(TreeNode root, Integer max, Integer min) {
    if (root == null) return true;
    if (max != null && root.val >= max) return false;
    if (min != null && root.val <= min) return false;
    return isValid(root.left, root.val, min) && isValid(root.right, max, root.val);
}

// LC 669 剪裁二叉树，将树中大于R或者小于L的部分全部剪掉并返回。
// 还是那句话，树的问题想到递归，而且树的递归有个特点就是只有LocalView。
// 对每个节点共有三种情况。
// 如果这个节点的值比上限还大，那么这个节点和它左边的整个子树都要全部砍掉。
// 如果这个节点的值比下限还小，那么这个节点和它右边整个子树要全部砍掉。
// 如果这个节点在上下线之间，则这个节点还是作为根节点保留，但是我们就要去剪裁它的左右子树了。
public TreeNode trimBST(TreeNode root, int L, int R) {
    if (root == null) return root;
    if (root.val > R) return trimBST(root.left, L, R);
    if (root.val < L) return trimBST(root.right, L, R);
    root.left = trimBST(root.left, L, R);
    root.right = trimBST(root.right, L, R);
    return root;
}

// LC 530 BST的最小距离
// 思路：BST的中序遍历是有序的。
// 一种方法是先中序遍历并将所有数值存入数组，然后再遍历一遍数组。
// 一种优化的技巧是在遍历过程中始终保存着上一个访问的节点。
TreeNode pre = null;
int res = Integer.MAX_VALUE;
public int getMinimumDifference(TreeNode root) {
    if (root == null) return 0;
    helper(root);
    return res;
}
private void helper(TreeNode root) {
    if (root == null) return;
    helper(root.left);
    if (pre != null) {
        res = Math.min(res, root.val - pre.val);
    }
    pre = root;
    helper(root.right);
}

// 二叉搜索树迭代器 LC 173
// 思路一：直接先中序遍历了，把所有值全存下来。
// 思路二：用个辅助栈。
public int next() {
    if (stack.isEmpty()) return -1;  // should throw an exception()
    TreeNode n = stack.pop();
    int res = n.val;
    if (n.right != null) {
        stack.push(n.right);
        n = n.right;
        while(n.left != null) {
            stack.push(n.left);
            n = n.left;
        }
    }
    return res;
}
```

### LC 124 二叉树中的最大路径和

思路：对于每个节点来说，通过其的最大路径和有两种可能，一种是 node.val + node.left.单边最大路径和 + node.right.单边最大路径和。一种是 node.单边最大路径和 + 其祖先 + 其祖先的右子树的单边最大路径和。

**这里有个技巧，我们 max_gain 方法中，计算了上面讨论的第一种情况，但是返回的是单边的最大路径和。**

这个技巧在 LC 543 和 LC 687 中也有应用。

```java
int ans = Integer.MIN_VALUE;
public int maxPathSum(TreeNode root) {
    max_gain(root);
    return ans;
}
public int max_gain(TreeNode node) {
    if (node == null) return 0;
    int left_gain = Math.max(max_gain(node.left), 0);
    int right_gain = Math.max(max_gain(node.right), 0);
    int price_newpath = node.val + left_gain + right_gain;
    max_sum = Math.max(max_sum, price_newpath);
    return node.val + Math.max(left_gain, right_gain);
}
```

### LC 543 树的直径

树的直径的定义是树中两个节点最远的距离（显然是两个叶子节点）。通过画图我们可以发现，这个最远路径不一定通过根节点。

因此在遍历这个树的过程中，每个节点都有可能是这个最长路径的最高节点。如果是，那么最长路径就是 node.left.depth + node.right.depth +1。如果不是，我们至少先知道了这个节点的 depth，然后再往上看。

这样我们在递归计算树的各个节点的 depth 的过程中，就可以找到所有潜在的 longest distance.

```java
int ans = 1;
public int diameterOfBinaryTree(TreeNode root) {
    depth(root);
    return ans - 1;
}
public int depth(TreeNode node) {
    if (node == null) return 0;
    int L = depth(node.left);
    int R = depth(node.right);
    ans = Math.max(ans, L+R+1);
    return Math.max(L, R) + 1;
}
```

### LC 687 最长同值路径

这题和前两题有着类似的解题框架。

在遍历到每个节点的时候，我们只有一个 LocalView，但是我们知道如果当前节点包含在这个最优解中，那只有两种情况，要么就是以这个节点为最高的节点，结果为这个节点的两边之和加它自己；要么就是这个节点作为部分和，只能取比较好的一边。

```java
int ans;
public int longestUnivaluePath(TreeNode root) {
    ans = 0;
    arrowLength(root);
    return ans;
}
public int arrowLength(TreeNode node) {
    if (node == null) return 0;
    int left = arrowLength(node.left);
    int right = arrowLength(node.right);
    int arrowLeft = 0, arrowRight = 0;
    if (node.left != null && node.left.val == node.val) arrowLeft = left + 1;
    if (node.right != null && node.right.val == node.val) arrowRight = right + 1;
    ans = Math.max(ans, arrowLeft + arrowRight);
    return Math.max(arrowLeft, arrowRight);
}
```

### LC 654 最大二叉树

此题要求根据一个数组来构建二叉树，满足如下条件：1. 二叉树的根是数组中的最大元素。2. 左子树是通过数组中最大值左边部分构造出的最大二叉树。3. 右子树是通过数组中最大值右边部分构造出的最大二叉树。

思路：我们需要先找到数组中的最大元素，将其作为根节点。然后对这个元素左侧的剩余数组递归调用生成左子树，右侧数组生成右子树。

```java
private TreeNode makeMBT(int[] nums, int start, int end) {
    int maxPos = maxPos(nums, start, end);
    if (maxPos == -1) return null;
    TreeNode root = new TreeNode(nums[maxPos]);
    root.left = makeMBT(nums, start, maxPos);
    root.right = makeMBT(nums, maxPos+1, end);
    return root;
}
private int maxPos(int[] nums, int start, int end) {
    if (nums.length == 0 || start >= end) return -1;
    int pos = start, max = nums[start];
    for (int i = start + 1; i < end; i++) {
        if (max <= nums[i]) {
            pos = i;
            max = nums[i];
        }
    }
    return pos;
}
```

### 序列化二叉树

LLC 297 序列化和反序列化二叉树。序列化比较简单，就是先序遍历。我们用空格来分隔节点，用#表示 null。反序列化稍微麻烦一点，我采用了一个 iterator 来简化代码。

```java
public String serialize(TreeNode root) {
    StringBuilder sb = new StringBuilder();
    serializeHelper(root, sb);
    return sb.toString();
}
private void serializeHelper(TreeNode root, StringBuilder sb) {
    if (root == null) {sb.append("# "); return;}
    sb.append(root.val).append(" ");
    serializeHelper(root.left, sb);
    serializeHelper(root.right, sb);
}
public TreeNode deserialize(String data) {
    List<String> strs = Arrays.asList(data.trim().split(" "));
    return deserializeHelper(strs.iterator());
}
private TreeNode deserializeHelper(Iterator<String> str_iter) {
    String val = str_iter.next();
    if (val.equals("#")) return null;
    TreeNode node = new TreeNode(Integer.parseInt(val));
    node.left = deserializeHelper(str_iter);
    node.right = deserializeHelper(str_iter);
    return node;
}
```

### LC 449 序列化和反序列化 BST

这题和 297 题其实差不多，但是由于是 BST，所以我们其实可以更压缩一下空间，在 297 题中，我们给每个空节点都插入了 # 来明确表明树的叶子节点。而对于 BST，我们只需要知道 BST 的先序遍历，就可以完整的复原 BST。

因为对于 BST 来说，先序遍历的第一个元素肯定就是根节点，而其左子树的所有值都小于根节点，右子树都大于根节点。比如 [5, 2, 1, 7, 6, 9]，显然[2,1]是左子树，而[7,6,9]是右子树。

直接递归调用就可以从先序遍历的数组中复原二叉树。

```java
private TreeNode builder(String[] arr, int lo, int hi) {
    if (lo > hi) return null;
    TreeNode root = new TreeNode(Integer.valueOf(arr[lo]));
    //找到第一个比首元素大的元素位置
    int index = hi + 1;
    for (int i = lo + 1; i <= hi; i++) {
        if (Integer.valueOf(arr[i]) > root.val) {
            index = i;break;
        }
    }
    root.left = builder(arr, lo + 1, index - 1);
    root.right = builder(arr, index, hi);
    return root;
}
```

### 重建二叉树

LC889 从先序和后序构建二叉树。

先序遍历的第一个节点肯定是根节点，而先序遍历的第二个节点肯定是左子树的根节点。我们就可以分别在前序遍历中和后序遍历中找到左子树的范围和右子树的范围，递归调用这个重建方法即可。

```java
public TreeNode constructFromPrePost(int[] pre, int[] post) {
    int N = pre.length;
    if (N == 0) return null;
    TreeNode root = new TreeNode(pre[0]);
    if (N == 1) return root;
    int mid = 0;
    for (int i = 0; i < N; ++i)
        if (post[i] == pre[1])
            mid = i+1;
    root.left = constructFromPrePost(Arrays.copyOfRange(pre, 1, mid+1),
                                         Arrays.copyOfRange(post, 0, L));
    root.right = constructFromPrePost(Arrays.copyOfRange(pre, mid+1, N),
                                          Arrays.copyOfRange(post, mid, N-1));
    return root;
}
```

```java
int[] inorder;
int[] preorder;
Map<Integer, Integer> idx_map = new HashMap<>();
public TreeNode buildTree(int[] preorder, int[] inorder) {
    if (preorder.length == 0) return null;
    this.preorder = preorder; this.inorder = inorder;
    for (int i = 0; i < inorder.length; i++) this.idx_map.put(inorder[i], i);
    return buildTree(0, inorder.length-1, 0, inorder.length-1);
}
// 记住这个函数签名
public TreeNode buildTree(int pstart, int pend, int istart, int iend) {
    if (pstart > pend) return null;
    int rootval = preorder[pstart];
    TreeNode root = new TreeNode(rootval);
    int in_index = idx_map.get(rootval); // 找到 inorder 中rootval的位置
    int leftsize = in_index - istart;
    root.left = buildTree(pstart + 1, pstart + leftsize, istart, in_index-1);
    root.right = buildTree(pstart + leftsize + 1, pend, in_index+1, iend);
    return root;
}
```

### 在二叉树内进行搜索

在二叉树内进行搜索也是一种很常见的题型。比如如何找到某个给定节点到根节点的路径，这其实就是一个最简单的 DFS，用个回溯法就可以搞定。再比如如何找到一个多叉树中两个节点的最低公共祖先，其实就可以通过两次二叉树内路径搜索后，转换为求链表的连接点问题。

```java
// LC 113 PATH SUM II
private void dfs(List<List<Integer>> res, List<Integer> tmp, TreeNode node, int rem) {
    如果是叶子节点，且rem = 0，将tmp加入 res;
    如果左子树非空，搜索左子树（并回溯）。
    如果右子树非空，搜索右子树（并回溯）。
}

// LC 652 寻找重复子树
// 此题的难点在于如何identify一个子树。
// 这里有一个很有趣的技巧，就是通过将子树序列化成字符串作为子树的id，并将其存入hashMap，
// 当这个id再次出现的时候，就说明出现了重复子树。
List<TreeNode> res = new ArrayList();
Map<String, Integer> map = new HashMap();
public List<TreeNode> findDuplicateSubtrees(TreeNode root) {
    dfs(root);
    return res;
}
public String dfs(TreeNode node){
    if(node == null) return "#";
    String str = node.val + dfs(node.left) + dfs(node.right);
    Integer val = map.get(str);
    if(val == null){
        map.put(str, 1);
    }else if(val == 1){
        res.add(node);
        map.put(str,++val);
    }
    return str;
}
```

### LC 1110 删点成林

这题说的是给你一棵二叉树和一些待删除的点，返回删除这些点后得到的森林。这里需要一个策略：先处理靠近叶子节点的子树，也就是一个 bottom up 的过程，因此考虑采取后序遍历。

```java
private Set<Integer> toDeleteSet = new HashSet();
public List<TreeNode> delNodes(TreeNode root, int[] to_delete) {
    List<TreeNode> forest = new ArrayList<>(16);
    if (null == root) return forest;
    for (int e : to_delete) toDeleteSet.add(e);
    root = delNodes(root, forest);
    if (root != null) forest.add(root);
    return forest;
}

public TreeNode delNodes(TreeNode root, List<TreeNode> forest) {
    if (null == root) return null;
    root.left = delNodes(root.left, forest);
    root.right = delNodes(root.right, forest);
    if (!toDeleteSet.contains(root.val)) return root;
    if (root.left != null) forest.add(root.left);
    if (root.right != null) forest.add(root.right);
    return null;
}
```

### LC 1145 二叉树着色游戏

https://leetcode-cn.com/problems/binary-tree-coloring-game

这是我很喜欢的一道题，这道题涉及到如何找到树中的某个节点，如何计算树中节点个数等基本的树操作。

### LC 979 在二叉树中分配硬币

https://leetcode-cn.com/problems/distribute-coins-in-binary-tree

```java
class Solution {
    int ans;
    public int distributeCoins(TreeNode root) {
        ans = 0;
        dfs(root);
        return ans;
    }

    public int dfs(TreeNode node) {
        if (node == null) return 0;
        int L = dfs(node.left);
        int R = dfs(node.right);
        ans += Math.abs(L) + Math.abs(R);
        return node.val + L + R - 1;
    }
}
```

### LC 894 所有可能的满二叉树

https://leetcode-cn.com/problems/all-possible-full-binary-trees/

```java
List<TreeNode> allPossibleFBT(int N) {
    List<TreeNode> ans = new ArrayList();
    if (N % 2 == 0) return ans;
    if (N == 1) {
        ans.add(new TreeNode(0));
        return ans;
    }
    for (int i = 1; i < N; i+=2){
        for (TreeNode l : allPossibleFBT(i)){
            for (TreeNode r : allPossibleFBT(N-i-1)){
                TreeNode root = new TreeNode(0);
                root.left = l;
                root.right = r;
                ans.add(root);}}}
    return ans;
}
```

### LC 865 具有所有最深节点的最小子树

https://leetcode-cn.com/problems/smallest-subtree-with-all-the-deepest-nodes/

```java
public Result dfs(TreeNode node) {
    if (node == null) return new Result(null, 0);
    Result L = dfs(node.left);
    Result R = dfs(node.right);
    if (L.dist > R.dist) return new Result(L.node, L.dist + 1);
    if (L.dist < R.dist) return new Result(R.node, R.dist + 1);
    return new Result(node, L.dist + 1);
}
```

### 变树为图

变图为树的题目通常来说忽略树的单向性，这时候可以考虑用邻接矩阵的方式存储这棵树，或者用 hashMap 存储每个节点的父节点。

LC 742 二叉树最近的叶子节点。

这题说实话我想了很久都没写出来，最后发现可以通过一种经典方法完成：dfs 建图 + bfs

LC 863 二叉树中所有离目标节点距离为 k 的节点。

这题也可以用类似的方法搞定了，建图+dfs。这里有两个技巧，第一是关于建图，其实只要整个 HashMap，存下每个节点的父节点就可以了。第二是关于 dfs，可以在达到 k 之后剪枝。

### LC 460 LFU Cache

思路 1： hashMap + balanced binary tree

思路 2： hashMap + 双向链表 + minFreq counter

## 其他

关于树还有一些高阶的数据结构一定要掌握，比如 Trie Tree, Segment Tree。后面我会另写文章来讲解它们的实现与使用场景。

## LC199 二叉树的右视图

```java
public List<Integer> rightSideView(TreeNode root) {
    List<Integer> res = new LinkedList<>();
    helper(root, 0, res);
    return res;
}

private void helper(TreeNode root, int level, List<Integer> res) {
    if (root == null) return;
    if (res.size() == level) res.add(root.val);
    helper(root.right, level+1, res);
    helper(root.left, level+1, res);
}
```

## 剑指 offer 32 锯齿形遍历二叉树

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res=new ArrayList<>();
    if(root==null) return res;
    Queue <TreeNode> queue=new LinkedList<TreeNode> ();
    queue.add(root);
    int dir = 1;
    while(!queue.isEmpty()) {
        int size = queue.size();
        List<Integer> list = new ArrayList<>();
        while(size >  0) {
            TreeNode n = queue.remove();
            if (dir > 0) {list.add(n.val);}
            else {list.add(0, n.val);}
            if (n.left != null) queue.add(n.left);
            if (n.right != null) queue.add(n.right);
            size--;
        }
        res.add(list);
        dir = -dir;
    }
    return res;
}
```

## 剑指 offer 33 验证二叉搜索树的后序遍历序列

```java
public boolean verifyPostorder(int [] postorder) {
    if (postorder.length <= 2) return true;
    return verifySeq(postorder, 0, postorder.length-1);
}
private boolean verifySeq(int[] postorder, int start, int end) {
    if (start >= end) return true;
    int idx = start;
    while (idx < end) {
        if (postorder[idx] > postorder[end]) break;
        idx++;
    }
    for (int j = idx; j < end; j++)
        if (postorder[j] < postorder[end]) return false;
    return verifySeq(postorder, start, idx-1) && verifySeq(postorder, idx, end-1);
}
```
