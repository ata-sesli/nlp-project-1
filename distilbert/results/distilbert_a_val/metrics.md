# val (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71626 | 0.8983 | 0.8983 | 0.1025 | 0.1009 | 0.9601 |
| length_bucket=long | 23604 | 0.8924 | 0.8922 | 0.1146 | 0.1011 | 0.9571 |
| length_bucket=medium | 23710 | 0.9008 | 0.9008 | 0.1031 | 0.0953 | 0.9614 |
| length_bucket=short | 24312 | 0.9016 | 0.9016 | 0.0907 | 0.1062 | 0.9614 |
| difficulty=easy | 24128 | 0.9373 | 0.9326 | 0.0595 | 0.0644 | 0.9825 |
| difficulty=hard | 21784 | 0.8551 | 0.8242 | 0.1205 | 0.2089 | 0.9153 |
| difficulty=medium | 25714 | 0.8983 | 0.8965 | 0.1102 | 0.0953 | 0.9596 |
| call_has_both_labels=False | 67300 | 0.9179 | 0.9179 | 0.0873 | 0.0771 | 0.9733 |
| call_has_both_labels=True | 4326 | 0.5941 | 0.5887 | 0.3254 | 0.4949 | 0.6134 |
| framework=ci_agent | 4757 | 0.8938 | 0.8938 | 0.1151 | 0.0965 | 0.9522 |
| framework=claude_code | 3893 | 0.9255 | 0.9254 | 0.0820 | 0.0673 | 0.9719 |
| framework=codex_cli | 3772 | 0.9268 | 0.9267 | 0.0854 | 0.0616 | 0.9744 |
| framework=computer_use | 2490 | 0.9157 | 0.9154 | 0.0896 | 0.0796 | 0.9721 |
| framework=cursor_agent | 4098 | 0.9283 | 0.9281 | 0.0777 | 0.0664 | 0.9745 |
| framework=data_agent | 4301 | 0.9068 | 0.9068 | 0.0905 | 0.0960 | 0.9644 |
| framework=devops_agent | 4613 | 0.9178 | 0.9178 | 0.0704 | 0.0940 | 0.9683 |
| framework=email_calendar | 3958 | 0.8891 | 0.8891 | 0.0964 | 0.1253 | 0.9557 |
| framework=finance_agent | 3894 | 0.8955 | 0.8954 | 0.0885 | 0.1189 | 0.9646 |
| framework=home_iot | 3710 | 0.9008 | 0.9007 | 0.0872 | 0.1101 | 0.9663 |
| framework=langchain | 3833 | 0.9163 | 0.9162 | 0.0923 | 0.0756 | 0.9693 |
| framework=mcp_browser | 4397 | 0.8763 | 0.8763 | 0.1348 | 0.1121 | 0.9505 |
| framework=mcp_filesystem | 4232 | 0.8748 | 0.8746 | 0.1364 | 0.1145 | 0.9389 |
| framework=mcp_github | 3452 | 0.8285 | 0.8285 | 0.1553 | 0.1872 | 0.9072 |
| framework=mcp_postgres | 4242 | 0.8805 | 0.8801 | 0.1082 | 0.1320 | 0.9451 |
| framework=mcp_slack | 4255 | 0.8926 | 0.8926 | 0.1159 | 0.0988 | 0.9560 |
| framework=openai_functions | 3773 | 0.9123 | 0.9122 | 0.1032 | 0.0727 | 0.9687 |
| framework=pkg_agent | 3956 | 0.8908 | 0.8908 | 0.1087 | 0.1097 | 0.9570 |
