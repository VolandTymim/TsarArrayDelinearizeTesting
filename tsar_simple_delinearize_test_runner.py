import shlex
import json
import re
from ctestgen.runner import BasicTestRunner, TestRunResult


class TsarSimpleDelinearizeTestRunner(BasicTestRunner):
    def __init__(self, *args, **kwargs):
        super().__init__(shlex.split('tsar -print-only=array-subscript-delinearize -print-step=2'),
                         *args, **kwargs)

    def _process_program_response(self, test_dir, test_filename, program_response):
        tsar_output = program_response[1]
        tsar_json_search = re.findall(r'\{"Accesses":{.+},"Sizes":{.+},"IsDelinearized":\d+\}', tsar_output)
        if not tsar_json_search:
            return TestRunResult(TestRunResult.ResultType.FAIL, tsar_output, test_filename)
        tsar_results_description = ''
        for tsar_result_json in tsar_json_search:
            try:
                tsar_result = json.loads(tsar_result_json)
            except json.decoder.JSONDecodeError:
                if self.print_test_info:
                    print('\tTSAR JSON decode error')
                return TestRunResult(TestRunResult.ResultType.FAIL,
                                     'TSAR JSON decode error\n' + tsar_output,
                                     test_filename)
            tsar_results_description += '\tAccesses:\n'
            for array, accesses in tsar_result['Accesses'].items():
                tsar_results_description += '\t\t' + str(array) + ': ' + str(accesses) + '\n'
            tsar_results_description += '\tSizes:\n'
            for array, sizes in tsar_result['Sizes'].items():
                tsar_results_description += '\t\t' + str(array) + ': ' + str(sizes) + '\n'
            tsar_results_description += '\n'

        if self.print_test_info:
            print(tsar_results_description)
        return TestRunResult(TestRunResult.ResultType.SUCCESS, tsar_results_description)
