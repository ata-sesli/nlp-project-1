# test (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71613 | 0.9564 | 0.9564 | 0.0500 | 0.0372 | 0.9912 |
| length_bucket=long | 23526 | 0.9543 | 0.9542 | 0.0511 | 0.0407 | 0.9903 |
| length_bucket=medium | 23700 | 0.9553 | 0.9553 | 0.0515 | 0.0380 | 0.9904 |
| length_bucket=short | 24387 | 0.9597 | 0.9597 | 0.0477 | 0.0327 | 0.9929 |
| difficulty=easy | 24237 | 0.9740 | 0.9719 | 0.0277 | 0.0250 | 0.9967 |
| difficulty=hard | 21791 | 0.9346 | 0.9202 | 0.0619 | 0.0748 | 0.9805 |
| difficulty=medium | 25585 | 0.9584 | 0.9576 | 0.0508 | 0.0346 | 0.9912 |
| call_has_both_labels=False | 67412 | 0.9614 | 0.9614 | 0.0453 | 0.0320 | 0.9931 |
| call_has_both_labels=True | 4201 | 0.8765 | 0.8760 | 0.1199 | 0.1277 | 0.9423 |
| framework=ci_agent | 4723 | 0.9555 | 0.9555 | 0.0545 | 0.0345 | 0.9914 |
| framework=claude_code | 3806 | 0.9661 | 0.9660 | 0.0467 | 0.0224 | 0.9930 |
| framework=codex_cli | 3858 | 0.9715 | 0.9715 | 0.0349 | 0.0224 | 0.9949 |
| framework=computer_use | 2409 | 0.9606 | 0.9605 | 0.0427 | 0.0365 | 0.9935 |
| framework=cursor_agent | 3963 | 0.9637 | 0.9637 | 0.0353 | 0.0375 | 0.9933 |
| framework=data_agent | 4326 | 0.9593 | 0.9593 | 0.0447 | 0.0369 | 0.9930 |
| framework=devops_agent | 4497 | 0.9660 | 0.9660 | 0.0322 | 0.0358 | 0.9934 |
| framework=email_calendar | 4059 | 0.9436 | 0.9435 | 0.0665 | 0.0468 | 0.9879 |
| framework=finance_agent | 3887 | 0.9511 | 0.9511 | 0.0476 | 0.0501 | 0.9898 |
| framework=home_iot | 3767 | 0.9562 | 0.9561 | 0.0527 | 0.0356 | 0.9908 |
| framework=langchain | 3818 | 0.9673 | 0.9673 | 0.0369 | 0.0285 | 0.9943 |
| framework=mcp_browser | 4577 | 0.9552 | 0.9552 | 0.0509 | 0.0382 | 0.9906 |
| framework=mcp_filesystem | 4001 | 0.9438 | 0.9438 | 0.0563 | 0.0561 | 0.9872 |
| framework=mcp_github | 3494 | 0.9428 | 0.9426 | 0.0830 | 0.0332 | 0.9854 |
| framework=mcp_postgres | 4308 | 0.9503 | 0.9502 | 0.0597 | 0.0384 | 0.9883 |
| framework=mcp_slack | 4384 | 0.9496 | 0.9496 | 0.0560 | 0.0447 | 0.9881 |
| framework=openai_functions | 3768 | 0.9567 | 0.9567 | 0.0423 | 0.0441 | 0.9932 |
| framework=pkg_agent | 3968 | 0.9584 | 0.9584 | 0.0577 | 0.0256 | 0.9927 |
