# test (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71613 | 0.9061 | 0.9061 | 0.0749 | 0.1125 | 0.9645 |
| length_bucket=long | 23526 | 0.9035 | 0.9035 | 0.0784 | 0.1133 | 0.9629 |
| length_bucket=medium | 23700 | 0.9055 | 0.9055 | 0.0786 | 0.1101 | 0.9645 |
| length_bucket=short | 24387 | 0.9093 | 0.9091 | 0.0681 | 0.1142 | 0.9660 |
| difficulty=easy | 24237 | 0.9363 | 0.9321 | 0.0454 | 0.0740 | 0.9840 |
| difficulty=hard | 21791 | 0.8746 | 0.8433 | 0.0875 | 0.2249 | 0.9229 |
| difficulty=medium | 25585 | 0.9044 | 0.9032 | 0.0802 | 0.1071 | 0.9652 |
| call_has_both_labels=False | 67412 | 0.9256 | 0.9256 | 0.0614 | 0.0871 | 0.9769 |
| call_has_both_labels=True | 4201 | 0.5939 | 0.5801 | 0.2745 | 0.5570 | 0.6032 |
| framework=ci_agent | 4723 | 0.9168 | 0.9168 | 0.0707 | 0.0956 | 0.9652 |
| framework=claude_code | 3806 | 0.9243 | 0.9241 | 0.0774 | 0.0742 | 0.9718 |
| framework=codex_cli | 3858 | 0.9352 | 0.9352 | 0.0571 | 0.0722 | 0.9766 |
| framework=computer_use | 2409 | 0.9166 | 0.9165 | 0.0689 | 0.0967 | 0.9744 |
| framework=cursor_agent | 3963 | 0.9301 | 0.9300 | 0.0576 | 0.0826 | 0.9752 |
| framework=data_agent | 4326 | 0.9142 | 0.9142 | 0.0723 | 0.0985 | 0.9674 |
| framework=devops_agent | 4497 | 0.9257 | 0.9257 | 0.0618 | 0.0869 | 0.9719 |
| framework=email_calendar | 4059 | 0.8886 | 0.8886 | 0.0780 | 0.1433 | 0.9607 |
| framework=finance_agent | 3887 | 0.9020 | 0.9020 | 0.0762 | 0.1186 | 0.9647 |
| framework=home_iot | 3767 | 0.9156 | 0.9155 | 0.0771 | 0.0911 | 0.9709 |
| framework=langchain | 3818 | 0.9345 | 0.9345 | 0.0588 | 0.0723 | 0.9770 |
| framework=mcp_browser | 4577 | 0.8829 | 0.8823 | 0.0795 | 0.1577 | 0.9560 |
| framework=mcp_filesystem | 4001 | 0.8738 | 0.8738 | 0.1137 | 0.1384 | 0.9422 |
| framework=mcp_github | 3494 | 0.8555 | 0.8555 | 0.1222 | 0.1654 | 0.9290 |
| framework=mcp_postgres | 4308 | 0.8651 | 0.8636 | 0.0821 | 0.1942 | 0.9344 |
| framework=mcp_slack | 4384 | 0.8889 | 0.8887 | 0.0727 | 0.1504 | 0.9582 |
| framework=openai_functions | 3768 | 0.9260 | 0.9260 | 0.0581 | 0.0893 | 0.9756 |
| framework=pkg_agent | 3968 | 0.9209 | 0.9209 | 0.0678 | 0.0904 | 0.9694 |
