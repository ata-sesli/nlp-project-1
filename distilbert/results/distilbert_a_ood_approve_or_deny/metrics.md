# ood_approve_or_deny (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 1448 | 0.8460 | 0.8460 | 0.1077 | 0.1958 | 0.9365 |
| length_bucket=long | 403 | 0.8511 | 0.8509 | 0.1139 | 0.1841 | 0.9388 |
| length_bucket=medium | 475 | 0.8421 | 0.8421 | 0.1169 | 0.1967 | 0.9374 |
| length_bucket=short | 570 | 0.8456 | 0.8454 | 0.0945 | 0.2025 | 0.9351 |
| difficulty=easy | 428 | 0.8481 | 0.8425 | 0.1132 | 0.1747 | 0.9449 |
| difficulty=hard | 521 | 0.8157 | 0.8128 | 0.0959 | 0.2800 | 0.9098 |
| difficulty=medium | 499 | 0.8758 | 0.8756 | 0.1167 | 0.1322 | 0.9537 |
| call_has_both_labels=False | 1448 | 0.8460 | 0.8460 | 0.1077 | 0.1958 | 0.9365 |
| framework=ci_agent | 75 | 0.7467 | 0.7467 | 0.2222 | 0.2821 | 0.8184 |
| framework=claude_code | 64 | 0.9375 | 0.9369 | 0.0690 | 0.0571 | 0.9616 |
| framework=codex_cli | 61 | 0.9344 | 0.9340 | 0.0606 | 0.0714 | 0.9913 |
| framework=computer_use | 111 | 0.9189 | 0.9156 | 0.0698 | 0.0882 | 0.9860 |
| framework=cursor_agent | 105 | 0.9238 | 0.9238 | 0.0943 | 0.0577 | 0.9811 |
| framework=data_agent | 80 | 0.9375 | 0.9373 | 0.0789 | 0.0476 | 0.9818 |
| framework=devops_agent | 93 | 0.8172 | 0.8158 | 0.1500 | 0.2075 | 0.9241 |
| framework=email_calendar | 89 | 0.7753 | 0.7753 | 0.1026 | 0.3200 | 0.9133 |
| framework=finance_agent | 94 | 0.8404 | 0.8389 | 0.0435 | 0.2708 | 0.9389 |
| framework=home_iot | 58 | 0.7241 | 0.7241 | 0.1600 | 0.3636 | 0.8836 |
| framework=langchain | 76 | 0.9342 | 0.9298 | 0.0625 | 0.0714 | 0.9807 |
| framework=mcp_browser | 100 | 0.7600 | 0.7599 | 0.2745 | 0.2041 | 0.8695 |
| framework=mcp_filesystem | 62 | 0.7581 | 0.7549 | 0.1562 | 0.3333 | 0.8833 |
| framework=mcp_github | 82 | 0.8537 | 0.8537 | 0.0789 | 0.2045 | 0.9426 |
| framework=mcp_postgres | 99 | 0.8485 | 0.8484 | 0.0652 | 0.2264 | 0.9446 |
| framework=mcp_slack | 76 | 0.8421 | 0.8411 | 0.0541 | 0.2564 | 0.8995 |
| framework=openai_functions | 83 | 0.8434 | 0.8388 | 0.0968 | 0.1923 | 0.9597 |
| framework=pkg_agent | 40 | 0.7500 | 0.7333 | 0.0909 | 0.4444 | 0.8485 |
