# val (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71626 | 0.9141 | 0.9141 | 0.0908 | 0.0810 | 0.9692 |
| length_bucket=long | 23604 | 0.9087 | 0.9085 | 0.1013 | 0.0820 | 0.9668 |
| length_bucket=medium | 23710 | 0.9162 | 0.9161 | 0.0905 | 0.0772 | 0.9695 |
| length_bucket=short | 24312 | 0.9175 | 0.9175 | 0.0812 | 0.0838 | 0.9708 |
| difficulty=easy | 24128 | 0.9503 | 0.9463 | 0.0497 | 0.0497 | 0.9877 |
| difficulty=hard | 21784 | 0.8727 | 0.8453 | 0.1075 | 0.1794 | 0.9293 |
| difficulty=medium | 25714 | 0.9153 | 0.9136 | 0.0989 | 0.0739 | 0.9693 |
| call_has_both_labels=False | 67300 | 0.9344 | 0.9344 | 0.0741 | 0.0573 | 0.9811 |
| call_has_both_labels=True | 4326 | 0.5987 | 0.5947 | 0.3347 | 0.4749 | 0.6195 |
| framework=ci_agent | 4757 | 0.9117 | 0.9117 | 0.0968 | 0.0791 | 0.9627 |
| framework=claude_code | 3893 | 0.9317 | 0.9316 | 0.0778 | 0.0593 | 0.9786 |
| framework=codex_cli | 3772 | 0.9374 | 0.9374 | 0.0740 | 0.0517 | 0.9810 |
| framework=computer_use | 2490 | 0.9293 | 0.9291 | 0.0820 | 0.0604 | 0.9792 |
| framework=cursor_agent | 4098 | 0.9383 | 0.9381 | 0.0710 | 0.0534 | 0.9817 |
| framework=data_agent | 4301 | 0.9214 | 0.9214 | 0.0780 | 0.0792 | 0.9702 |
| framework=devops_agent | 4613 | 0.9282 | 0.9282 | 0.0643 | 0.0792 | 0.9737 |
| framework=email_calendar | 3958 | 0.8999 | 0.8999 | 0.1137 | 0.0865 | 0.9645 |
| framework=finance_agent | 3894 | 0.9145 | 0.9143 | 0.0852 | 0.0858 | 0.9713 |
| framework=home_iot | 3710 | 0.9159 | 0.9158 | 0.0798 | 0.0880 | 0.9745 |
| framework=langchain | 3833 | 0.9309 | 0.9308 | 0.0725 | 0.0659 | 0.9755 |
| framework=mcp_browser | 4397 | 0.9018 | 0.9017 | 0.1028 | 0.0934 | 0.9616 |
| framework=mcp_filesystem | 4232 | 0.8934 | 0.8933 | 0.1161 | 0.0975 | 0.9531 |
| framework=mcp_github | 3452 | 0.8612 | 0.8612 | 0.1388 | 0.1387 | 0.9346 |
| framework=mcp_postgres | 4242 | 0.8970 | 0.8967 | 0.0969 | 0.1097 | 0.9584 |
| framework=mcp_slack | 4255 | 0.9126 | 0.9126 | 0.1043 | 0.0704 | 0.9670 |
| framework=openai_functions | 3773 | 0.9271 | 0.9271 | 0.0839 | 0.0622 | 0.9757 |
| framework=pkg_agent | 3956 | 0.9044 | 0.9044 | 0.0940 | 0.0971 | 0.9665 |
