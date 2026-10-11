# test (threshold 0.5)

| group | rows | accuracy | macro_f1 | false_allow_rate | false_deny_rate | auroc |
|---|---:|---:|---:|---:|---:|---:|
| **overall** | 71613 | 0.9607 | 0.9607 | 0.0405 | 0.0381 | 0.9929 |
| length_bucket=long | 23526 | 0.9589 | 0.9589 | 0.0404 | 0.0417 | 0.9919 |
| length_bucket=medium | 23700 | 0.9597 | 0.9597 | 0.0414 | 0.0392 | 0.9925 |
| length_bucket=short | 24387 | 0.9633 | 0.9633 | 0.0398 | 0.0334 | 0.9943 |
| difficulty=easy | 24237 | 0.9776 | 0.9758 | 0.0211 | 0.0231 | 0.9976 |
| difficulty=hard | 21791 | 0.9422 | 0.9287 | 0.0484 | 0.0824 | 0.9832 |
| difficulty=medium | 25585 | 0.9603 | 0.9596 | 0.0447 | 0.0359 | 0.9927 |
| call_has_both_labels=False | 67412 | 0.9646 | 0.9646 | 0.0372 | 0.0337 | 0.9944 |
| call_has_both_labels=True | 4201 | 0.8976 | 0.8971 | 0.0905 | 0.1160 | 0.9553 |
| framework=ci_agent | 4723 | 0.9638 | 0.9638 | 0.0413 | 0.0312 | 0.9946 |
| framework=claude_code | 3806 | 0.9661 | 0.9660 | 0.0406 | 0.0279 | 0.9946 |
| framework=codex_cli | 3858 | 0.9717 | 0.9717 | 0.0296 | 0.0269 | 0.9959 |
| framework=computer_use | 2409 | 0.9664 | 0.9663 | 0.0340 | 0.0333 | 0.9946 |
| framework=cursor_agent | 3963 | 0.9652 | 0.9652 | 0.0338 | 0.0359 | 0.9947 |
| framework=data_agent | 4326 | 0.9628 | 0.9628 | 0.0371 | 0.0373 | 0.9944 |
| framework=devops_agent | 4497 | 0.9689 | 0.9689 | 0.0305 | 0.0318 | 0.9947 |
| framework=email_calendar | 4059 | 0.9515 | 0.9514 | 0.0569 | 0.0405 | 0.9897 |
| framework=finance_agent | 3887 | 0.9573 | 0.9573 | 0.0445 | 0.0410 | 0.9914 |
| framework=home_iot | 3767 | 0.9567 | 0.9566 | 0.0455 | 0.0412 | 0.9917 |
| framework=langchain | 3818 | 0.9696 | 0.9696 | 0.0296 | 0.0311 | 0.9959 |
| framework=mcp_browser | 4577 | 0.9600 | 0.9600 | 0.0370 | 0.0432 | 0.9929 |
| framework=mcp_filesystem | 4001 | 0.9518 | 0.9518 | 0.0431 | 0.0532 | 0.9892 |
| framework=mcp_github | 3494 | 0.9445 | 0.9444 | 0.0504 | 0.0603 | 0.9858 |
| framework=mcp_postgres | 4308 | 0.9591 | 0.9590 | 0.0417 | 0.0399 | 0.9914 |
| framework=mcp_slack | 4384 | 0.9500 | 0.9500 | 0.0555 | 0.0443 | 0.9899 |
| framework=openai_functions | 3768 | 0.9650 | 0.9649 | 0.0364 | 0.0337 | 0.9945 |
| framework=pkg_agent | 3968 | 0.9627 | 0.9627 | 0.0405 | 0.0342 | 0.9933 |
