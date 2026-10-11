# val (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71626 | 0.8882 | 0.8882 | 0.1044 | 0.1192 | 0.9542 |
| length_bucket=long | 23604 | 0.8818 | 0.8817 | 0.1163 | 0.1200 | 0.9507 |
| length_bucket=medium | 23710 | 0.8912 | 0.8912 | 0.1045 | 0.1131 | 0.9561 |
| length_bucket=short | 24312 | 0.8914 | 0.8913 | 0.0932 | 0.1244 | 0.9556 |
| difficulty=easy | 24128 | 0.9244 | 0.9192 | 0.0608 | 0.0838 | 0.9790 |
| difficulty=hard | 21784 | 0.8479 | 0.8146 | 0.1224 | 0.2302 | 0.9067 |
| difficulty=medium | 25714 | 0.8882 | 0.8865 | 0.1125 | 0.1112 | 0.9538 |
| call_has_both_labels=False | 67300 | 0.9071 | 0.9071 | 0.0903 | 0.0955 | 0.9681 |
| call_has_both_labels=True | 4326 | 0.5939 | 0.5869 | 0.3104 | 0.5119 | 0.6117 |
| framework=ci_agent | 4757 | 0.8777 | 0.8775 | 0.1183 | 0.1267 | 0.9436 |
| framework=claude_code | 3893 | 0.9163 | 0.9162 | 0.0868 | 0.0809 | 0.9682 |
| framework=codex_cli | 3772 | 0.9210 | 0.9209 | 0.0903 | 0.0683 | 0.9710 |
| framework=computer_use | 2490 | 0.9116 | 0.9115 | 0.0879 | 0.0888 | 0.9681 |
| framework=cursor_agent | 4098 | 0.9161 | 0.9158 | 0.0957 | 0.0734 | 0.9702 |
| framework=data_agent | 4301 | 0.9047 | 0.9047 | 0.0877 | 0.1030 | 0.9597 |
| framework=devops_agent | 4613 | 0.9113 | 0.9113 | 0.0803 | 0.0971 | 0.9657 |
| framework=email_calendar | 3958 | 0.8737 | 0.8736 | 0.0934 | 0.1590 | 0.9478 |
| framework=finance_agent | 3894 | 0.8901 | 0.8900 | 0.0869 | 0.1306 | 0.9583 |
| framework=home_iot | 3710 | 0.8895 | 0.8894 | 0.0883 | 0.1307 | 0.9607 |
| framework=langchain | 3833 | 0.9097 | 0.9097 | 0.0971 | 0.0838 | 0.9643 |
| framework=mcp_browser | 4397 | 0.8635 | 0.8632 | 0.1108 | 0.1635 | 0.9427 |
| framework=mcp_filesystem | 4232 | 0.8627 | 0.8625 | 0.1538 | 0.1215 | 0.9325 |
| framework=mcp_github | 3452 | 0.8079 | 0.8079 | 0.1676 | 0.2158 | 0.8888 |
| framework=mcp_postgres | 4242 | 0.8706 | 0.8701 | 0.1109 | 0.1498 | 0.9403 |
| framework=mcp_slack | 4255 | 0.8820 | 0.8819 | 0.0954 | 0.1408 | 0.9489 |
| framework=openai_functions | 3773 | 0.9070 | 0.9069 | 0.1048 | 0.0815 | 0.9644 |
| framework=pkg_agent | 3956 | 0.8756 | 0.8756 | 0.1189 | 0.1298 | 0.9499 |
