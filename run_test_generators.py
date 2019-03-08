import os
from dim_types_test_generator import DimTypesTestGenerator
from dim_types_c99_test_generator import DimTypesC99TestGenerator
from subscripts_test_generator import SubscriptsTestGenerator
from subscripts_c99_test_generator import SubscriptsC99TestGenerator
from subscripts_c99_with_standard_test_generator import SubscriptsC99WithStandardTestGenerator
from subscripts_with_casts_test_generator import SubscriptsWithCastsTestGenerator
from subscripts_with_standard_test_generator import SubscriptsWithStandardTestGenerator


generators = list()

dims_count_set = [2]
generators.append(DimTypesTestGenerator(os.path.join('tests', 'dim_types'), dims_count_set))
generators.append(DimTypesC99TestGenerator(os.path.join('tests', 'dim_types_c99'), dims_count_set))
generators.append(SubscriptsTestGenerator(os.path.join('tests', 'subscripts'), dims_count_set))
generators.append(SubscriptsC99TestGenerator(os.path.join('tests', 'subscripts_c99'), dims_count_set))
generators.append(SubscriptsC99WithStandardTestGenerator(os.path.join('tests', 'subscripts_c99_with_etalon'),
                                                         dims_count_set))
generators.append(SubscriptsWithCastsTestGenerator(os.path.join('tests', 'subscripts_with_casts'), dims_count_set))
generators.append(SubscriptsWithStandardTestGenerator(os.path.join('tests', 'subscripts_with_etalon'), dims_count_set))

for generator in generators:
    generator.run()
