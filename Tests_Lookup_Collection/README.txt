https://pytest-c-testrunner.readthedocs.io/conftest.html


https://paragkamble.medium.com/understanding-hooks-in-pytest-892e91edbdb7



root
└── pytest_cmdline_main
 ├── pytest_plugin_registered
 ├── pytest_configure
 │ └── pytest_plugin_registered
 ├── pytest_sessionstart
 │ ├── pytest_plugin_registered
 │ └── pytest_report_header
 ├── pytest_collection
 │ ├── pytest_collectstart
 │ ├── pytest_make_collect_report
 │ │ ├── pytest_collect_file
 │ │ │ └── pytest_pycollect_makemodule
 │ │ └── pytest_pycollect_makeitem
 │ │ └── pytest_generate_tests
 │ │ └── pytest_make_parametrize_id
 │ ├── pytest_collectreport
 │ ├── pytest_itemcollected
 │ ├── pytest_collection_modifyitems
 │ └── pytest_collection_finish
 │ └── pytest_report_collectionfinish
 ├── pytest_runtestloop
 │ └── pytest_runtest_protocol
 │ ├── pytest_runtest_logstart
 │ ├── pytest_runtest_setup
 │ │ └── pytest_fixture_setup
 │ ├── pytest_runtest_makereport
 │ ├── pytest_runtest_logreport
 │ │ └── pytest_report_teststatus
 │ ├── pytest_runtest_call
 │ │ └── pytest_pyfunc_call
 │ ├── pytest_runtest_teardown
 │ │ └── pytest_fixture_post_finalizer
 │ └── pytest_runtest_logfinish
 ├── pytest_sessionfinish
 │ └── pytest_terminal_summary
 └── pytest_unconfigure