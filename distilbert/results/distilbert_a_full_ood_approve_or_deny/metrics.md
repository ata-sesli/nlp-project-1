# ood_approve_or_deny (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 1448 | 0.8764 | 0.8763 | 0.0946 | 0.1498 | 0.9518 |
| length_bucket=long | 403 | 0.8685 | 0.8684 | 0.1139 | 0.1493 | 0.9501 |
| length_bucket=medium | 475 | 0.8821 | 0.8821 | 0.0909 | 0.1434 | 0.9552 |
| length_bucket=short | 570 | 0.8772 | 0.8768 | 0.0827 | 0.1551 | 0.9518 |
| difficulty=easy | 428 | 0.8785 | 0.8734 | 0.0881 | 0.1413 | 0.9609 |
| difficulty=hard | 521 | 0.8426 | 0.8412 | 0.0996 | 0.2200 | 0.9283 |
| difficulty=medium | 499 | 0.9098 | 0.9098 | 0.0934 | 0.0868 | 0.9649 |
| call_has_both_labels=False | 1448 | 0.8764 | 0.8763 | 0.0946 | 0.1498 | 0.9518 |
| framework=ci_agent | 75 | 0.7867 | 0.7863 | 0.1389 | 0.2821 | 0.8362 |
| framework=claude_code | 64 | 0.9531 | 0.9528 | 0.0345 | 0.0571 | 0.9842 |
| framework=codex_cli | 61 | 0.9180 | 0.9179 | 0.1212 | 0.0357 | 0.9805 |
| framework=computer_use | 111 | 0.9640 | 0.9623 | 0.0233 | 0.0441 | 0.9911 |
| framework=cursor_agent | 105 | 0.9524 | 0.9524 | 0.0566 | 0.0385 | 0.9913 |
| framework=data_agent | 80 | 0.9625 | 0.9624 | 0.0526 | 0.0238 | 0.9925 |
| framework=devops_agent | 93 | 0.8817 | 0.8790 | 0.1500 | 0.0943 | 0.9613 |
| framework=email_calendar | 89 | 0.8202 | 0.8200 | 0.1026 | 0.2400 | 0.9349 |
| framework=finance_agent | 94 | 0.8404 | 0.8395 | 0.0652 | 0.2500 | 0.9339 |
| framework=home_iot | 58 | 0.7759 | 0.7753 | 0.1600 | 0.2727 | 0.9236 |
| framework=langchain | 76 | 0.9342 | 0.9298 | 0.0625 | 0.0714 | 0.9836 |
| framework=mcp_browser | 100 | 0.8300 | 0.8300 | 0.1961 | 0.1429 | 0.9104 |
| framework=mcp_filesystem | 62 | 0.8226 | 0.8203 | 0.0938 | 0.2667 | 0.9177 |
| framework=mcp_github | 82 | 0.8415 | 0.8414 | 0.1053 | 0.2045 | 0.9492 |
| framework=mcp_postgres | 99 | 0.8586 | 0.8586 | 0.0870 | 0.1887 | 0.9467 |
| framework=mcp_slack | 76 | 0.8158 | 0.8146 | 0.0811 | 0.2821 | 0.8843 |
| framework=openai_functions | 83 | 0.9398 | 0.9360 | 0.0645 | 0.0577 | 0.9770 |
| framework=pkg_agent | 40 | 0.7750 | 0.7679 | 0.1364 | 0.3333 | 0.8283 |
