# val (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71626 | 0.9412 | 0.9412 | 0.0576 | 0.0600 | 0.9846 |
| length_bucket=long | 23604 | 0.9375 | 0.9374 | 0.0600 | 0.0649 | 0.9828 |
| length_bucket=medium | 23710 | 0.9420 | 0.9420 | 0.0539 | 0.0619 | 0.9850 |
| length_bucket=short | 24312 | 0.9441 | 0.9441 | 0.0589 | 0.0529 | 0.9861 |
| difficulty=easy | 24128 | 0.9572 | 0.9539 | 0.0341 | 0.0476 | 0.9925 |
| difficulty=hard | 21784 | 0.9193 | 0.9009 | 0.0679 | 0.1142 | 0.9679 |
| difficulty=medium | 25714 | 0.9447 | 0.9437 | 0.0611 | 0.0508 | 0.9859 |
| call_has_both_labels=False | 67300 | 0.9463 | 0.9463 | 0.0537 | 0.0537 | 0.9870 |
| call_has_both_labels=True | 4326 | 0.8627 | 0.8621 | 0.1140 | 0.1630 | 0.9288 |
| framework=ci_agent | 4757 | 0.9365 | 0.9364 | 0.0567 | 0.0708 | 0.9817 |
| framework=claude_code | 3893 | 0.9558 | 0.9558 | 0.0421 | 0.0462 | 0.9904 |
| framework=codex_cli | 3772 | 0.9576 | 0.9576 | 0.0435 | 0.0414 | 0.9895 |
| framework=computer_use | 2490 | 0.9454 | 0.9453 | 0.0558 | 0.0536 | 0.9836 |
| framework=cursor_agent | 4098 | 0.9534 | 0.9533 | 0.0458 | 0.0474 | 0.9900 |
| framework=data_agent | 4301 | 0.9430 | 0.9430 | 0.0549 | 0.0590 | 0.9843 |
| framework=devops_agent | 4613 | 0.9475 | 0.9475 | 0.0449 | 0.0601 | 0.9872 |
| framework=email_calendar | 3958 | 0.9209 | 0.9209 | 0.0751 | 0.0830 | 0.9762 |
| framework=finance_agent | 3894 | 0.9407 | 0.9405 | 0.0630 | 0.0560 | 0.9853 |
| framework=home_iot | 3710 | 0.9356 | 0.9355 | 0.0470 | 0.0803 | 0.9835 |
| framework=langchain | 3833 | 0.9549 | 0.9548 | 0.0437 | 0.0465 | 0.9905 |
| framework=mcp_browser | 4397 | 0.9416 | 0.9415 | 0.0607 | 0.0560 | 0.9847 |
| framework=mcp_filesystem | 4232 | 0.9355 | 0.9355 | 0.0658 | 0.0633 | 0.9829 |
| framework=mcp_github | 3452 | 0.9116 | 0.9116 | 0.0882 | 0.0885 | 0.9697 |
| framework=mcp_postgres | 4242 | 0.9397 | 0.9396 | 0.0685 | 0.0514 | 0.9815 |
| framework=mcp_slack | 4255 | 0.9337 | 0.9337 | 0.0626 | 0.0699 | 0.9827 |
| framework=openai_functions | 3773 | 0.9499 | 0.9499 | 0.0500 | 0.0502 | 0.9874 |
| framework=pkg_agent | 3956 | 0.9383 | 0.9383 | 0.0681 | 0.0553 | 0.9850 |
