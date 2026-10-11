# val (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71626 | 0.9614 | 0.9614 | 0.0415 | 0.0357 | 0.9927 |
| length_bucket=long | 23604 | 0.9579 | 0.9579 | 0.0472 | 0.0372 | 0.9912 |
| length_bucket=medium | 23710 | 0.9613 | 0.9613 | 0.0392 | 0.0382 | 0.9929 |
| length_bucket=short | 24312 | 0.9649 | 0.9649 | 0.0383 | 0.0318 | 0.9939 |
| difficulty=easy | 24128 | 0.9784 | 0.9765 | 0.0244 | 0.0201 | 0.9974 |
| difficulty=hard | 21784 | 0.9406 | 0.9266 | 0.0503 | 0.0835 | 0.9824 |
| difficulty=medium | 25714 | 0.9632 | 0.9625 | 0.0421 | 0.0327 | 0.9928 |
| call_has_both_labels=False | 67300 | 0.9654 | 0.9654 | 0.0379 | 0.0314 | 0.9940 |
| call_has_both_labels=True | 4326 | 0.8997 | 0.8994 | 0.0942 | 0.1071 | 0.9576 |
| framework=ci_agent | 4757 | 0.9577 | 0.9577 | 0.0446 | 0.0398 | 0.9920 |
| framework=claude_code | 3893 | 0.9697 | 0.9697 | 0.0326 | 0.0281 | 0.9957 |
| framework=codex_cli | 3772 | 0.9716 | 0.9716 | 0.0326 | 0.0243 | 0.9946 |
| framework=computer_use | 2490 | 0.9679 | 0.9678 | 0.0338 | 0.0306 | 0.9945 |
| framework=cursor_agent | 4098 | 0.9646 | 0.9645 | 0.0350 | 0.0357 | 0.9946 |
| framework=data_agent | 4301 | 0.9640 | 0.9640 | 0.0300 | 0.0422 | 0.9927 |
| framework=devops_agent | 4613 | 0.9712 | 0.9712 | 0.0341 | 0.0235 | 0.9942 |
| framework=email_calendar | 3958 | 0.9432 | 0.9431 | 0.0711 | 0.0428 | 0.9870 |
| framework=finance_agent | 3894 | 0.9605 | 0.9603 | 0.0494 | 0.0307 | 0.9916 |
| framework=home_iot | 3710 | 0.9580 | 0.9578 | 0.0504 | 0.0345 | 0.9924 |
| framework=langchain | 3833 | 0.9690 | 0.9689 | 0.0336 | 0.0286 | 0.9952 |
| framework=mcp_browser | 4397 | 0.9684 | 0.9684 | 0.0288 | 0.0346 | 0.9934 |
| framework=mcp_filesystem | 4232 | 0.9542 | 0.9541 | 0.0450 | 0.0467 | 0.9909 |
| framework=mcp_github | 3452 | 0.9438 | 0.9438 | 0.0576 | 0.0548 | 0.9855 |
| framework=mcp_postgres | 4242 | 0.9602 | 0.9601 | 0.0424 | 0.0371 | 0.9916 |
| framework=mcp_slack | 4255 | 0.9558 | 0.9558 | 0.0491 | 0.0392 | 0.9910 |
| framework=openai_functions | 3773 | 0.9661 | 0.9661 | 0.0360 | 0.0319 | 0.9947 |
| framework=pkg_agent | 3956 | 0.9601 | 0.9601 | 0.0417 | 0.0382 | 0.9935 |
