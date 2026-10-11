# test (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71613 | 0.9142 | 0.9142 | 0.0879 | 0.0837 | 0.9685 |
| length_bucket=long | 23526 | 0.9131 | 0.9129 | 0.0932 | 0.0810 | 0.9674 |
| length_bucket=medium | 23700 | 0.9127 | 0.9127 | 0.0922 | 0.0824 | 0.9681 |
| length_bucket=short | 24387 | 0.9167 | 0.9167 | 0.0790 | 0.0877 | 0.9699 |
| difficulty=easy | 24237 | 0.9479 | 0.9440 | 0.0503 | 0.0531 | 0.9874 |
| difficulty=hard | 21791 | 0.8749 | 0.8476 | 0.1036 | 0.1817 | 0.9281 |
| difficulty=medium | 25585 | 0.9158 | 0.9142 | 0.0954 | 0.0757 | 0.9686 |
| call_has_both_labels=False | 67412 | 0.9335 | 0.9335 | 0.0729 | 0.0602 | 0.9804 |
| call_has_both_labels=True | 4201 | 0.6041 | 0.5971 | 0.3106 | 0.4936 | 0.6135 |
| framework=ci_agent | 4723 | 0.9246 | 0.9246 | 0.0856 | 0.0653 | 0.9707 |
| framework=claude_code | 3806 | 0.9304 | 0.9301 | 0.0840 | 0.0567 | 0.9725 |
| framework=codex_cli | 3858 | 0.9417 | 0.9417 | 0.0608 | 0.0559 | 0.9789 |
| framework=computer_use | 2409 | 0.9303 | 0.9301 | 0.0802 | 0.0602 | 0.9761 |
| framework=cursor_agent | 3963 | 0.9319 | 0.9319 | 0.0675 | 0.0688 | 0.9777 |
| framework=data_agent | 4326 | 0.9189 | 0.9188 | 0.0846 | 0.0778 | 0.9691 |
| framework=devops_agent | 4497 | 0.9277 | 0.9277 | 0.0663 | 0.0784 | 0.9741 |
| framework=email_calendar | 4059 | 0.8995 | 0.8994 | 0.1022 | 0.0989 | 0.9669 |
| framework=finance_agent | 3887 | 0.9125 | 0.9125 | 0.0842 | 0.0906 | 0.9712 |
| framework=home_iot | 3767 | 0.9196 | 0.9194 | 0.0821 | 0.0789 | 0.9736 |
| framework=langchain | 3818 | 0.9348 | 0.9348 | 0.0676 | 0.0628 | 0.9784 |
| framework=mcp_browser | 4577 | 0.8938 | 0.8937 | 0.1144 | 0.0973 | 0.9599 |
| framework=mcp_filesystem | 4001 | 0.8778 | 0.8777 | 0.1305 | 0.1142 | 0.9463 |
| framework=mcp_github | 3494 | 0.8558 | 0.8557 | 0.1364 | 0.1515 | 0.9327 |
| framework=mcp_postgres | 4308 | 0.8986 | 0.8981 | 0.0842 | 0.1207 | 0.9543 |
| framework=mcp_slack | 4384 | 0.9106 | 0.9106 | 0.0970 | 0.0816 | 0.9651 |
| framework=openai_functions | 3768 | 0.9318 | 0.9318 | 0.0689 | 0.0675 | 0.9774 |
| framework=pkg_agent | 3968 | 0.9196 | 0.9196 | 0.0845 | 0.0763 | 0.9683 |
