# ood_approve_or_deny (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 1448 | 0.9220 | 0.9216 | 0.0961 | 0.0618 | 0.9760 |
| length_bucket=long | 403 | 0.9107 | 0.9107 | 0.1040 | 0.0746 | 0.9799 |
| length_bucket=medium | 475 | 0.9326 | 0.9324 | 0.1039 | 0.0328 | 0.9689 |
| length_bucket=short | 570 | 0.9211 | 0.9202 | 0.0827 | 0.0759 | 0.9792 |
| difficulty=easy | 428 | 0.9416 | 0.9375 | 0.0755 | 0.0483 | 0.9832 |
| difficulty=hard | 521 | 0.9021 | 0.9020 | 0.0959 | 0.1000 | 0.9701 |
| difficulty=medium | 499 | 0.9259 | 0.9258 | 0.1089 | 0.0372 | 0.9762 |
| call_has_both_labels=False | 1448 | 0.9220 | 0.9216 | 0.0961 | 0.0618 | 0.9760 |
| framework=ci_agent | 75 | 0.8800 | 0.8800 | 0.0833 | 0.1538 | 0.9473 |
| framework=claude_code | 64 | 0.9688 | 0.9685 | 0.0345 | 0.0286 | 0.9892 |
| framework=codex_cli | 61 | 0.9180 | 0.9180 | 0.1515 | 0.0000 | 0.9751 |
| framework=computer_use | 111 | 0.9730 | 0.9714 | 0.0465 | 0.0147 | 0.9969 |
| framework=cursor_agent | 105 | 0.9333 | 0.9333 | 0.0755 | 0.0577 | 0.9811 |
| framework=data_agent | 80 | 0.9625 | 0.9622 | 0.0789 | 0.0000 | 0.9881 |
| framework=devops_agent | 93 | 0.8925 | 0.8888 | 0.1750 | 0.0566 | 0.9830 |
| framework=email_calendar | 89 | 0.8989 | 0.8955 | 0.1795 | 0.0400 | 0.9610 |
| framework=finance_agent | 94 | 0.9362 | 0.9362 | 0.0435 | 0.0833 | 0.9851 |
| framework=home_iot | 58 | 0.8966 | 0.8945 | 0.1200 | 0.0909 | 0.9648 |
| framework=langchain | 76 | 0.9342 | 0.9288 | 0.0417 | 0.1071 | 0.9844 |
| framework=mcp_browser | 100 | 0.8800 | 0.8798 | 0.1765 | 0.0612 | 0.9536 |
| framework=mcp_filesystem | 62 | 0.9032 | 0.9028 | 0.0625 | 0.1333 | 0.9760 |
| framework=mcp_github | 82 | 0.9024 | 0.9003 | 0.1842 | 0.0227 | 0.9719 |
| framework=mcp_postgres | 99 | 0.9091 | 0.9088 | 0.0870 | 0.0943 | 0.9705 |
| framework=mcp_slack | 76 | 0.9474 | 0.9473 | 0.0000 | 0.1026 | 0.9702 |
| framework=openai_functions | 83 | 0.9639 | 0.9611 | 0.0645 | 0.0192 | 0.9907 |
| framework=pkg_agent | 40 | 0.8500 | 0.8485 | 0.1364 | 0.1667 | 0.9419 |
