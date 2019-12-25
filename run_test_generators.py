import os
import argparse
from dim_types_test_generator import DimTypesTestGenerator
from dim_types_c99_test_generator import DimTypesC99TestGenerator
from subscripts_test_generator import SubscriptsTestGenerator
from subscripts_c99_test_generator import SubscriptsC99TestGenerator
from subscripts_c99_with_standard_test_generator import SubscriptsC99WithStandardTestGenerator
from subscripts_with_casts_test_generator import SubscriptsWithCastsTestGenerator
from subscripts_with_standard_test_generator import SubscriptsWithStandardTestGenerator


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dims_count', action='store_const', const=True, default=2)
    parser.add_argument('-t', '--test_base_dir', default='tests')
    return parser


if __name__ == '__main__':
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()

    dims_count_set = [args.dims_count]
    tests_base_dir = args.test_base_dir

    generators = list()

    generators.append(DimTypesTestGenerator(os.path.join(tests_base_dir, 'dim_types'), dims_count_set))
    generators.append(DimTypesC99TestGenerator(os.path.join(tests_base_dir, 'dim_types_c99'), dims_count_set))
    generators.append(SubscriptsTestGenerator(os.path.join(tests_base_dir, 'subscripts'), dims_count_set))
    generators.append(SubscriptsC99TestGenerator(os.path.join(tests_base_dir, 'subscripts_c99'), dims_count_set))
    generators.append(SubscriptsC99WithStandardTestGenerator(os.path.join(tests_base_dir, 'subscripts_c99_with_etalon'),
                                                             dims_count_set))
    generators.append(SubscriptsWithCastsTestGenerator(os.path.join(tests_base_dir, 'subscripts_with_casts'), dims_count_set))
    generators.append(SubscriptsWithStandardTestGenerator(os.path.join(tests_base_dir, 'subscripts_with_etalon'), dims_count_set))

    for generator in generators:
        generator.run()
