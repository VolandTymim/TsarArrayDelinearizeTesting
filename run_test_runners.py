import os
from tsar_simple_delinearize_test_runner import TsarSimpleDelinearizeTestRunner
from tsar_delinearize_test_runner import TsarDelinearizeTestRunner

# tsar_simple_runner = TsarSimpleDelinearizeTestRunner(test_base_dir='C:/Users/ForestBear/Documents/Specsem/Sapfor/test/polybench-all',
#                                                      runner_name='tsar_simple_delinearize')
# tsar_simple_runner.run()

tsar_runner = TsarDelinearizeTestRunner(test_base_dir='tests',
                                        print_test_info=False,
                                        test_filename_extensions=['.c'],
                                        runner_name='tsar_delinearize')
tsar_runner.run()
