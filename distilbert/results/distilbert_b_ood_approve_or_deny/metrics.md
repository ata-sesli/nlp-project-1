# ood_approve_or_deny (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 1448 | 0.8722 | 0.8721 | 0.1208 | 0.1340 | 0.9481 |
| length_bucket=long | 403 | 0.8635 | 0.8634 | 0.1040 | 0.1692 | 0.9413 |
| length_bucket=medium | 475 | 0.8674 | 0.8672 | 0.1472 | 0.1189 | 0.9392 |
| length_bucket=short | 570 | 0.8825 | 0.8815 | 0.1102 | 0.1234 | 0.9602 |
| difficulty=easy | 428 | 0.8855 | 0.8788 | 0.1258 | 0.1078 | 0.9498 |
| difficulty=hard | 521 | 0.8656 | 0.8651 | 0.1070 | 0.1640 | 0.9415 |
| difficulty=medium | 499 | 0.8677 | 0.8676 | 0.1323 | 0.1322 | 0.9484 |
| call_has_both_labels=False | 1448 | 0.8722 | 0.8721 | 0.1208 | 0.1340 | 0.9481 |
| framework=ci_agent | 75 | 0.8400 | 0.8400 | 0.1111 | 0.2051 | 0.9145 |
| framework=claude_code | 64 | 0.9375 | 0.9369 | 0.0690 | 0.0571 | 0.9803 |
| framework=codex_cli | 61 | 0.8852 | 0.8848 | 0.1212 | 0.1071 | 0.9589 |
| framework=computer_use | 111 | 0.9279 | 0.9253 | 0.0465 | 0.0882 | 0.9836 |
| framework=cursor_agent | 105 | 0.9143 | 0.9143 | 0.0755 | 0.0962 | 0.9448 |
| framework=data_agent | 80 | 0.9375 | 0.9367 | 0.1316 | 0.0000 | 0.9680 |
| framework=devops_agent | 93 | 0.9032 | 0.9021 | 0.0750 | 0.1132 | 0.9698 |
| framework=email_calendar | 89 | 0.7303 | 0.7303 | 0.1795 | 0.3400 | 0.8959 |
| framework=finance_agent | 94 | 0.9362 | 0.9362 | 0.0435 | 0.0833 | 0.9669 |
| framework=home_iot | 58 | 0.8103 | 0.8103 | 0.0400 | 0.3030 | 0.9539 |
| framework=langchain | 76 | 0.9474 | 0.9426 | 0.0208 | 0.1071 | 0.9769 |
| framework=mcp_browser | 100 | 0.8300 | 0.8300 | 0.1765 | 0.1633 | 0.9188 |
| framework=mcp_filesystem | 62 | 0.8065 | 0.8056 | 0.1562 | 0.2333 | 0.9104 |
| framework=mcp_github | 82 | 0.8537 | 0.8514 | 0.2105 | 0.0909 | 0.9522 |
| framework=mcp_postgres | 99 | 0.8283 | 0.8257 | 0.2391 | 0.1132 | 0.9471 |
| framework=mcp_slack | 76 | 0.8421 | 0.8421 | 0.1351 | 0.1795 | 0.9231 |
| framework=openai_functions | 83 | 0.8795 | 0.8713 | 0.1613 | 0.0962 | 0.9584 |
| framework=pkg_agent | 40 | 0.8500 | 0.8500 | 0.2273 | 0.0556 | 0.9268 |
