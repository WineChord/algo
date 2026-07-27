??? problem "LeetCode 2 · 两数相加"
    [打开原题 ↗](https://leetcode.cn/problems/add-two-numbers/){ .problem-source }

    **难度**：LeetCode 官方「中等」。

    **题意**：两个逆序链表表示两个非负整数，逐位相加并以相同形式返回结果。

    **思路**：同步扫描两条链，每轮把当前两位与旧进位相加。哑节点统一处理结果头，循环条件同时包含未读节点和最终进位。

    **复杂度**：时间 $O(\max(m,n))$，除结果链表外额外空间 $O(1)$。

    **C++ 实现**

    <!-- compile:leetcode-list -->
    ```cpp
    #include <bits/stdc++.h>
    using namespace std;
    class Solution {
    public:
      ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        ListNode dummy;
        ListNode* tail = &dummy;
        int carry = 0;
        while (l1 || l2 || carry) {
          int sum = carry;
          if (l1) {
            sum += l1->val;
            l1 = l1->next;
          }
          if (l2) {
            sum += l2->val;
            l2 = l2->next;
          }
          tail->next = new ListNode(sum % 10);
          tail = tail->next;
          carry = sum / 10;
        }
        return dummy.next;
      }
    };
    ```
