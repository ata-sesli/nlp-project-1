# ood_approve_or_deny (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 1448 | 0.8467 | 0.8467 | 0.1063 | 0.1958 | 0.9296 |
| length_bucket=long | 403 | 0.8437 | 0.8433 | 0.1089 | 0.2040 | 0.9283 |
| length_bucket=medium | 475 | 0.8484 | 0.8483 | 0.1039 | 0.1967 | 0.9327 |
| length_bucket=short | 570 | 0.8474 | 0.8470 | 0.1063 | 0.1899 | 0.9282 |
| difficulty=easy | 428 | 0.8481 | 0.8425 | 0.1132 | 0.1747 | 0.9364 |
| difficulty=hard | 521 | 0.8234 | 0.8208 | 0.0923 | 0.2680 | 0.9072 |
| difficulty=medium | 499 | 0.8697 | 0.8695 | 0.1167 | 0.1446 | 0.9449 |
| call_has_both_labels=False | 1448 | 0.8467 | 0.8467 | 0.1063 | 0.1958 | 0.9296 |
| framework=ci_agent | 75 | 0.7067 | 0.7066 | 0.2778 | 0.3077 | 0.8031 |
| framework=claude_code | 64 | 0.9062 | 0.9059 | 0.0690 | 0.1143 | 0.9517 |
| framework=codex_cli | 61 | 0.9180 | 0.9177 | 0.0909 | 0.0714 | 0.9773 |
| framework=computer_use | 111 | 0.9279 | 0.9253 | 0.0465 | 0.0882 | 0.9867 |
| framework=cursor_agent | 105 | 0.9048 | 0.9048 | 0.0943 | 0.0962 | 0.9735 |
| framework=data_agent | 80 | 0.9500 | 0.9499 | 0.0526 | 0.0476 | 0.9850 |
| framework=devops_agent | 93 | 0.8495 | 0.8480 | 0.1250 | 0.1698 | 0.9217 |
| framework=email_calendar | 89 | 0.7865 | 0.7865 | 0.1026 | 0.3000 | 0.9105 |
| framework=finance_agent | 94 | 0.8298 | 0.8278 | 0.0435 | 0.2917 | 0.9384 |
| framework=home_iot | 58 | 0.7414 | 0.7413 | 0.1600 | 0.3333 | 0.8776 |
| framework=langchain | 76 | 0.9342 | 0.9307 | 0.0833 | 0.0357 | 0.9695 |
| framework=mcp_browser | 100 | 0.8200 | 0.8193 | 0.1373 | 0.2245 | 0.8868 |
| framework=mcp_filesystem | 62 | 0.7742 | 0.7721 | 0.1562 | 0.3000 | 0.8708 |
| framework=mcp_github | 82 | 0.8293 | 0.8292 | 0.0789 | 0.2500 | 0.9115 |
| framework=mcp_postgres | 99 | 0.8384 | 0.8384 | 0.0870 | 0.2264 | 0.9192 |
| framework=mcp_slack | 76 | 0.8158 | 0.8153 | 0.1081 | 0.2564 | 0.8891 |
| framework=openai_functions | 83 | 0.8554 | 0.8491 | 0.1290 | 0.1538 | 0.9541 |
| framework=pkg_agent | 40 | 0.7500 | 0.7396 | 0.1364 | 0.3889 | 0.8056 |
