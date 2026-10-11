# test (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71613 | 0.8871 | 0.8871 | 0.1049 | 0.1209 | 0.9533 |
| length_bucket=long | 23526 | 0.8858 | 0.8858 | 0.1070 | 0.1209 | 0.9520 |
| length_bucket=medium | 23700 | 0.8855 | 0.8855 | 0.1118 | 0.1172 | 0.9527 |
| length_bucket=short | 24387 | 0.8898 | 0.8897 | 0.0964 | 0.1244 | 0.9549 |
| difficulty=easy | 24237 | 0.9215 | 0.9164 | 0.0637 | 0.0869 | 0.9779 |
| difficulty=hard | 21791 | 0.8466 | 0.8132 | 0.1234 | 0.2320 | 0.9041 |
| difficulty=medium | 25585 | 0.8890 | 0.8872 | 0.1109 | 0.1111 | 0.9537 |
| call_has_both_labels=False | 67412 | 0.9055 | 0.9055 | 0.0925 | 0.0964 | 0.9670 |
| call_has_both_labels=True | 4201 | 0.5910 | 0.5791 | 0.2888 | 0.5468 | 0.6112 |
| framework=ci_agent | 4723 | 0.8973 | 0.8973 | 0.1005 | 0.1049 | 0.9516 |
| framework=claude_code | 3806 | 0.9109 | 0.9106 | 0.1029 | 0.0767 | 0.9598 |
| framework=codex_cli | 3858 | 0.9189 | 0.9188 | 0.0836 | 0.0788 | 0.9714 |
| framework=computer_use | 2409 | 0.9074 | 0.9073 | 0.0872 | 0.0975 | 0.9643 |
| framework=cursor_agent | 3963 | 0.9134 | 0.9134 | 0.0839 | 0.0893 | 0.9670 |
| framework=data_agent | 4326 | 0.9041 | 0.9040 | 0.0899 | 0.1017 | 0.9572 |
| framework=devops_agent | 4497 | 0.9062 | 0.9062 | 0.0905 | 0.0972 | 0.9614 |
| framework=email_calendar | 4059 | 0.8689 | 0.8689 | 0.0952 | 0.1655 | 0.9487 |
| framework=finance_agent | 3887 | 0.8907 | 0.8907 | 0.0858 | 0.1316 | 0.9592 |
| framework=home_iot | 3767 | 0.8901 | 0.8900 | 0.0966 | 0.1221 | 0.9603 |
| framework=langchain | 3818 | 0.9146 | 0.9146 | 0.0889 | 0.0818 | 0.9679 |
| framework=mcp_browser | 4577 | 0.8523 | 0.8518 | 0.1212 | 0.1764 | 0.9410 |
| framework=mcp_filesystem | 4001 | 0.8408 | 0.8407 | 0.1690 | 0.1497 | 0.9200 |
| framework=mcp_github | 3494 | 0.8045 | 0.8044 | 0.1868 | 0.2035 | 0.8895 |
| framework=mcp_postgres | 4308 | 0.8765 | 0.8758 | 0.1014 | 0.1483 | 0.9388 |
| framework=mcp_slack | 4384 | 0.8844 | 0.8843 | 0.0961 | 0.1356 | 0.9472 |
| framework=openai_functions | 3768 | 0.9106 | 0.9105 | 0.0917 | 0.0872 | 0.9675 |
| framework=pkg_agent | 3968 | 0.8795 | 0.8795 | 0.1199 | 0.1210 | 0.9504 |
