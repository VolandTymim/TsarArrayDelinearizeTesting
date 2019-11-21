import sys
import argparse

from tsar_delinearize_test_runner import TsarDelinearizeTestRunner


def create_tsar_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--baseline')
    parser.add_argument('-p', '--print_test_info', action='store_const', const=True, default=False)
    parser.add_argument('-pf', '--print_failed_tests', action='store_const', const=True, default=False)
    parser.add_argument('-t', '--test_base_dir', default='tests')
    return parser


if __name__ == '__main__':
    tsar_parser = create_tsar_arg_parser()
    namespace = tsar_parser.parse_args(sys.argv[1:])
    tsar_runner = TsarDelinearizeTestRunner(baseline_results_file_path=namespace.baseline,
                                            print_failed_tests=namespace.print_failed_tests,
                                            print_test_info=namespace.print_test_info,
                                            test_base_dir=namespace.test_base_dir,
                                            test_filename_extensions=['.c'],
                                            runner_name='tsar_delinearize')
    tsar_runner.run()
