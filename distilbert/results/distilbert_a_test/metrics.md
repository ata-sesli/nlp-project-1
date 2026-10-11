# test (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71613 | 0.8995 | 0.8995 | 0.0991 | 0.1018 | 0.9595 |
| length_bucket=long | 23526 | 0.8994 | 0.8993 | 0.1028 | 0.0985 | 0.9588 |
| length_bucket=medium | 23700 | 0.8980 | 0.8980 | 0.1041 | 0.0999 | 0.9588 |
| length_bucket=short | 24387 | 0.9011 | 0.9010 | 0.0911 | 0.1070 | 0.9608 |
| difficulty=easy | 24237 | 0.9349 | 0.9302 | 0.0593 | 0.0684 | 0.9820 |
| difficulty=hard | 21791 | 0.8569 | 0.8260 | 0.1171 | 0.2113 | 0.9135 |
| difficulty=medium | 25585 | 0.9024 | 0.9007 | 0.1049 | 0.0921 | 0.9601 |
| call_has_both_labels=False | 67412 | 0.9183 | 0.9183 | 0.0852 | 0.0783 | 0.9726 |
| call_has_both_labels=True | 4201 | 0.5987 | 0.5902 | 0.3048 | 0.5120 | 0.6134 |
| framework=ci_agent | 4723 | 0.9107 | 0.9106 | 0.1013 | 0.0775 | 0.9609 |
| framework=claude_code | 3806 | 0.9175 | 0.9171 | 0.0991 | 0.0677 | 0.9663 |
| framework=codex_cli | 3858 | 0.9266 | 0.9266 | 0.0788 | 0.0681 | 0.9737 |
| framework=computer_use | 2409 | 0.9191 | 0.9188 | 0.0907 | 0.0721 | 0.9684 |
| framework=cursor_agent | 3963 | 0.9235 | 0.9235 | 0.0680 | 0.0852 | 0.9717 |
| framework=data_agent | 4326 | 0.9096 | 0.9096 | 0.0903 | 0.0904 | 0.9616 |
| framework=devops_agent | 4497 | 0.9188 | 0.9188 | 0.0693 | 0.0931 | 0.9661 |
| framework=email_calendar | 4059 | 0.8832 | 0.8832 | 0.0997 | 0.1331 | 0.9558 |
| framework=finance_agent | 3887 | 0.8986 | 0.8986 | 0.0789 | 0.1226 | 0.9635 |
| framework=home_iot | 3767 | 0.9052 | 0.9051 | 0.0882 | 0.1008 | 0.9667 |
| framework=langchain | 3818 | 0.9188 | 0.9188 | 0.0863 | 0.0760 | 0.9718 |
| framework=mcp_browser | 4577 | 0.8739 | 0.8739 | 0.1350 | 0.1164 | 0.9478 |
| framework=mcp_filesystem | 4001 | 0.8585 | 0.8585 | 0.1457 | 0.1374 | 0.9319 |
| framework=mcp_github | 3494 | 0.8306 | 0.8305 | 0.1578 | 0.1803 | 0.9069 |
| framework=mcp_postgres | 4308 | 0.8877 | 0.8870 | 0.0908 | 0.1365 | 0.9449 |
| framework=mcp_slack | 4384 | 0.8969 | 0.8969 | 0.1101 | 0.0959 | 0.9555 |
| framework=openai_functions | 3768 | 0.9191 | 0.9190 | 0.0825 | 0.0794 | 0.9713 |
| framework=pkg_agent | 3968 | 0.8964 | 0.8964 | 0.1103 | 0.0969 | 0.9589 |
