import shlex
import json
import re
import sys
import os
from ctestgen.runner import BasicTestRunner, TestRunResult, Metrics, decode_metrics


class TsarDelinearizeTestRunner(BasicTestRunner):
    def __init__(self, *args, baseline_results_file_path, print_failed_tests, **kwargs):
        super().__init__(shlex.split('tsar -print-only=delinearize -print-step=2'),
                         *args, **kwargs)
        self.baseline_results_file_path = baseline_results_file_path
        self.print_failed_tests = print_failed_tests

    @staticmethod
    def _filter_test_filenames(test_filenames):
        return [filename for filename in test_filenames]

    def _process_program_response(self, test_dir, test_filename, program_response):
        tsar_output = program_response[1]
        # Get last string in tsar output
        target_tsar_output = re.findall(r"for function 'foo':\s*\{.*\}", tsar_output)
        if not target_tsar_output:
            return TestRunResult(TestRunResult.ResultType.FAIL, tsar_output, test_filename)

        tsar_json_search = re.search(r'\{"Accesses":{.+},"Sizes":{.+}\}', target_tsar_output[-1])
        if not tsar_json_search:
            if self.print_test_info:
                print('\tTSAR JSON decode error')
            return TestRunResult(TestRunResult.ResultType.FAIL,
                                 'TSAR JSON decode error\n' + tsar_output, test_filename)

        tsar_result_json = tsar_json_search[0]
        # print(tsar_result_json)
        try:
            tsar_result = json.loads(tsar_result_json)
        except json.decoder.JSONDecodeError:
            if self.print_test_info:
                print('\tTSAR JSON decode error')
            return TestRunResult(TestRunResult.ResultType.FAIL,
                                 'TSAR JSON decode error\n' + tsar_output, test_filename)

        # print(tsar_result)
        assert len(tsar_result['Accesses'].values()) == 1 and len(tsar_result['Sizes'].values()) == 1, \
            'Test of more than one array not implemented. ' + test_filename + ' TSAR: ' + str(tsar_result)
        tsar_subscripts = list(tsar_result['Accesses'].values())[0]
        tsar_sizes = list(tsar_result['Sizes'].values())[0]

        test_answer_filename = '.'.join(test_filename.split('.')[:-1]) + '.ans'
        with open(os.path.join(test_dir, test_answer_filename), 'r') as test_answers:
            test_result = json.load(test_answers)
            assert len(test_result['Accesses'].values()) == 1 and len(test_result['Sizes'].values()) == 1, \
                'Test of more than one array not implemented'
            test_subscripts = list(test_result['Accesses'].values())[0]
            test_sizes = list(test_result['Sizes'].values())[0]
            tsar_results_description = 'TSAR Output:\n\tAccesses:\n\t' + str(tsar_subscripts) + '\n'
            tsar_results_description += '\tSizes:\n\t' + str(tsar_sizes) + '\n'

            was_subscript_mismatch = False
            was_size_mismatch = False
            if len(tsar_subscripts) == len(test_subscripts):
                for i in range(len(tsar_subscripts)):
                    if len(tsar_subscripts[i]) == len(test_subscripts[i]):
                        local_was_subscript_mismatch = False
                        for dim_idx in range(len(tsar_subscripts[i])):
                            if test_subscripts[i][dim_idx][0] != tsar_subscripts[i][dim_idx][0] and \
                                    not (tsar_subscripts[i][dim_idx][0] == '1' and dim_idx < len(tsar_subscripts) and
                                         test_subscripts[i][dim_idx][0] in tsar_sizes[dim_idx + 1]) and \
                                    (test_subscripts[i][dim_idx][0] not in tsar_subscripts[i][dim_idx][0] or
                                     (('*' in test_subscripts[i][dim_idx][0]) != (
                                             '*' in tsar_subscripts[i][dim_idx][0])) or
                                     (
                                             ('+' in test_subscripts[i][dim_idx][0] != '+' in
                                              tsar_subscripts[i][dim_idx][0]))):
                                # print('\t\tMultiply coefficients mismatch. TSAR: ' + tsar_subscripts[i][dim_idx][0] +
                                #       ' Test answer: ' + test_subscripts[i][dim_idx][0])
                                was_subscript_mismatch = True
                                local_was_subscript_mismatch = True
                                if self.print_failed_tests or self.print_test_info:
                                    if test_subscripts[i][dim_idx][0] == '0' or tsar_subscripts[i][dim_idx][0] == '0':
                                        print('\tSubscripts zero mismatch.')

                            if test_subscripts[i][dim_idx][1] != tsar_subscripts[i][dim_idx][1] and \
                                    not (tsar_subscripts[i][dim_idx][1] == '1' and dim_idx < len(tsar_subscripts) and
                                         test_subscripts[i][dim_idx][1] in tsar_sizes[dim_idx + 1]) and \
                                    (test_subscripts[i][dim_idx][1] not in tsar_subscripts[i][dim_idx][1] or
                                     (('*' in test_subscripts[i][dim_idx][1]) != (
                                             '*' in tsar_subscripts[i][dim_idx][1])) or
                                     (
                                             ('+' in test_subscripts[i][dim_idx][1] != '+' in
                                              tsar_subscripts[i][dim_idx][1]))):
                                # print('\t\tAdd coefficients mismatch. TSAR: ' + tsar_subscripts[i][dim_idx][1] +
                                #       ' Test answer: ' + test_subscripts[i][dim_idx][1])
                                was_subscript_mismatch = True
                                local_was_subscript_mismatch = True
                                if self.print_failed_tests or self.print_test_info:
                                    if test_subscripts[i][dim_idx][1] == '0' or tsar_subscripts[i][dim_idx][1] == '0':
                                        print('\tSubscripts zero mismatch.')
                        if not local_was_subscript_mismatch:
                            if self.print_test_info:
                                print('\tSubscripts: OK')
                        # else:
                        if self.print_test_info:
                            print('\tTSAR: ' + str(tsar_subscripts[i]))
                            print('\tTest: ' + str(test_subscripts[i]))
                    else:
                        was_subscript_mismatch = True
                        if self.print_failed_tests or self.print_test_info:
                            print('\tSubscripts dims count mismatch. TSAR: ' + str(len(tsar_subscripts)) +
                                  ' Test count: ' + str(len(test_subscripts)), file=sys.stderr)
            else:
                was_subscript_mismatch = True
                if self.print_failed_tests or self.print_test_info:
                    print('\tSubscripts count mismatch. TSAR: ' + str(len(tsar_subscripts)) +
                          ' Test count: ' + str(len(test_subscripts)), file=sys.stderr)

            if len(tsar_sizes) == len(test_sizes):
                for dim_idx in range(len(tsar_sizes)):
                    if test_sizes[dim_idx] != tsar_sizes[dim_idx] and \
                            test_sizes[dim_idx] != '***COULDNOTCOMPUTE***' and \
                            not (test_sizes[dim_idx] in tsar_sizes[dim_idx] and dim_idx > 0 and
                                 (test_subscripts[0][dim_idx - 1][0] in tsar_sizes[dim_idx] or
                                  test_subscripts[0][dim_idx - 1][1] in tsar_sizes[dim_idx])) and \
                            (test_sizes[dim_idx] not in tsar_sizes[dim_idx] or
                             (('*' in test_sizes[dim_idx]) != ('*' in tsar_sizes[dim_idx])) or
                             (('+' in test_sizes[dim_idx] != '+' in tsar_sizes[dim_idx]))):
                        # print('\t\tDimension sizes mismatch. TSAR: ' + tsar_sizes[dim_idx] +
                        #       ' Test answer: ' + test_sizes[dim_idx])
                        was_size_mismatch = True
                if not was_size_mismatch:
                    if self.print_test_info:
                        print('\tSizes: OK')
                # else:
                if self.print_test_info:
                    print('\tTSAR: ' + str(tsar_sizes))
                    print('\tTest: ' + str(test_sizes))
            else:
                was_size_mismatch = True
                if self.print_failed_tests or self.print_test_info:
                    print('\tDimensions count mismatch. TSAR: ' + str(len(tsar_sizes)) +
                          ' test count: ' + str(len(test_sizes)), file=sys.stderr)

            if not (was_size_mismatch | was_subscript_mismatch):
                return TestRunResult(TestRunResult.ResultType.SUCCESS, tsar_results_description, test_filename)
            else:
                if self.print_failed_tests or self.print_test_info:
                    print(test_filename + ':')
                    if was_subscript_mismatch:
                        print('\tSubscripts mismatch.')
                        if not self.print_test_info:
                            print('\tTSAR: ' + str(tsar_subscripts))
                            print('\tTest: ' + str(test_subscripts))
                    if was_size_mismatch:
                        print('\tDimension sizes mismatch.')
                        if not self.print_test_info:
                            print('\tTSAR: ' + str(tsar_sizes))
                            print('\tTest: ' + str(test_sizes))
                tsar_results_description += 'Reference results:\n\tAccesses:\n\t' + str(test_subscripts) + '\n'
                tsar_results_description += '\tSizes:\n\t' + str(test_sizes) + '\n'
                return TestRunResult(TestRunResult.ResultType.FAIL, tsar_results_description, test_filename)

    def _on_run_finish(self, tests, global_metrics):
        if self.baseline_results_file_path:
            print('Baseline file path: ' + self.baseline_results_file_path)
            try:
                with open(self.baseline_results_file_path, 'r') as baseline_results_file:
                    baseline_metrics: Metrics = decode_metrics(json.load(baseline_results_file))
                successful_tests_difference = list(set(self.global_metrics.successful_tests) -
                                                   set(baseline_metrics.successful_tests))
                successful_tests_difference.sort()
                fail_tests_difference = list(set(self.global_metrics.failed_tests) -
                                             set(baseline_metrics.failed_tests))
                fail_tests_difference.sort()
                print("Baseline successful tests: " + str(baseline_metrics.successful_count) +
                      "\nCurrent successful tests: " + str(self.global_metrics.successful_count))
                print('New successful: ' + str(successful_tests_difference))

                print("Baseline failed tests: " + str(baseline_metrics.failed_count) +
                      "\nCurrent failed tests: " + str(self.global_metrics.failed_count))
                print('New failed: ' + str(fail_tests_difference))
            except FileExistsError or FileNotFoundError:
                print("Baseline file not found")
            except json.decoder.JSONDecodeError:
                print("Can't decode json in baseline file")
