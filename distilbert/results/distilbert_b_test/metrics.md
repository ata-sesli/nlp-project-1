# test (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71613 | 0.9399 | 0.9399 | 0.0605 | 0.0597 | 0.9846 |
| length_bucket=long | 23526 | 0.9396 | 0.9395 | 0.0578 | 0.0628 | 0.9846 |
| length_bucket=medium | 23700 | 0.9397 | 0.9397 | 0.0582 | 0.0623 | 0.9837 |
| length_bucket=short | 24387 | 0.9403 | 0.9403 | 0.0652 | 0.0540 | 0.9856 |
| difficulty=easy | 24237 | 0.9576 | 0.9545 | 0.0352 | 0.0464 | 0.9926 |
| difficulty=hard | 21791 | 0.9174 | 0.8989 | 0.0708 | 0.1135 | 0.9683 |
| difficulty=medium | 25585 | 0.9422 | 0.9411 | 0.0659 | 0.0516 | 0.9851 |
| call_has_both_labels=False | 67412 | 0.9454 | 0.9453 | 0.0566 | 0.0527 | 0.9870 |
| call_has_both_labels=True | 4201 | 0.8522 | 0.8510 | 0.1185 | 0.1814 | 0.9234 |
| framework=ci_agent | 4723 | 0.9430 | 0.9430 | 0.0592 | 0.0548 | 0.9862 |
| framework=claude_code | 3806 | 0.9493 | 0.9491 | 0.0568 | 0.0453 | 0.9879 |
| framework=codex_cli | 3858 | 0.9557 | 0.9557 | 0.0423 | 0.0462 | 0.9911 |
| framework=computer_use | 2409 | 0.9456 | 0.9455 | 0.0541 | 0.0547 | 0.9856 |
| framework=cursor_agent | 3963 | 0.9495 | 0.9495 | 0.0457 | 0.0554 | 0.9874 |
| framework=data_agent | 4326 | 0.9429 | 0.9428 | 0.0628 | 0.0517 | 0.9865 |
| framework=devops_agent | 4497 | 0.9473 | 0.9473 | 0.0384 | 0.0672 | 0.9879 |
| framework=email_calendar | 4059 | 0.9207 | 0.9207 | 0.0700 | 0.0883 | 0.9784 |
| framework=finance_agent | 3887 | 0.9419 | 0.9418 | 0.0524 | 0.0636 | 0.9829 |
| framework=home_iot | 3767 | 0.9366 | 0.9365 | 0.0538 | 0.0723 | 0.9836 |
| framework=langchain | 3818 | 0.9531 | 0.9531 | 0.0515 | 0.0422 | 0.9895 |
| framework=mcp_browser | 4577 | 0.9386 | 0.9385 | 0.0669 | 0.0555 | 0.9834 |
| framework=mcp_filesystem | 4001 | 0.9230 | 0.9230 | 0.0848 | 0.0694 | 0.9783 |
| framework=mcp_github | 3494 | 0.9210 | 0.9209 | 0.0765 | 0.0813 | 0.9738 |
| framework=mcp_postgres | 4308 | 0.9364 | 0.9363 | 0.0737 | 0.0522 | 0.9814 |
| framework=mcp_slack | 4384 | 0.9318 | 0.9318 | 0.0704 | 0.0660 | 0.9803 |
| framework=openai_functions | 3768 | 0.9456 | 0.9456 | 0.0489 | 0.0597 | 0.9890 |
| framework=pkg_agent | 3968 | 0.9375 | 0.9375 | 0.0769 | 0.0482 | 0.9857 |
