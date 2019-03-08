from ctestgen.generator import *


class DimTypesC99TestGenerator(ArrayTestGenerator):
    def _generate_programs(self):
        generated_programs = list()

        for dim_sizes_names in self.dim_sizes_names_set:
            enum_constants = []
            var_sizes = []
            const_var_sizes = []
            define_sizes = []
            subscript_template_values = []

            constant_value = 40
            subscript_template_value = 3
            for dim_size_name in dim_sizes_names:
                enum_constants.append(('ENUM_' + dim_size_name, constant_value))
                define_sizes.append(Define('DEF_' + dim_size_name, str(constant_value)))
                const_var_sizes.append(ConstInt('CONST_' + dim_size_name, constant_value))
                constant_value += 10
                var_sizes.append(Int('VAR_' + dim_size_name))

                subscript_template_values.append((subscript_template_value, subscript_template_value + 2))
                subscript_template_value += 4

            array_sizes_enum = Enum(enum_constants)
            var_sizes_mask = BitVector(2)

            for var_sizes_mask.vector in range(var_sizes_mask.num_system_base ** len(var_sizes)):
                # A1 - foo argument, default sizes is enum
                foo_arguments = []
                current_dim_sizes = []
                for i in range(len(var_sizes)):
                    if var_sizes_mask.get_bit(i):
                        foo_arguments.append(var_sizes[i])
                        current_dim_sizes.append(var_sizes[i])
                    else:
                        current_dim_sizes.append(array_sizes_enum.constants[i])
                A1 = ArrayC99('A1', Int, current_dim_sizes)
                foo_arguments.append(A1)

                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values))))

                dim_sizes_program = Program(
                    'mixed_dim_sizes_c99_fun_arg_arr_enum_' + str(len(current_dim_sizes)) + 'd_' +
                    str(var_sizes_mask.vector))
                dim_sizes_program.add_enum(array_sizes_enum)
                dim_sizes_program.add_function(foo)
                write_arrays_to_json(dim_sizes_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(dim_sizes_program)

                # A1 - foo argument, default sizes is int constants
                foo_arguments = []
                current_dim_sizes = []
                for i in range(len(var_sizes)):
                    if var_sizes_mask.get_bit(i):
                        foo_arguments.append(var_sizes[i])
                        current_dim_sizes.append(var_sizes[i])
                    else:
                        current_dim_sizes.append(const_var_sizes[i])
                A1 = ArrayC99('A1', Int, current_dim_sizes)
                foo_arguments.append(A1)

                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values))))

                dim_sizes_program = Program('mixed_dim_sizes_c99_fun_arg_arr_const_int_' + str(len(current_dim_sizes)) +
                                            'd_' + str(var_sizes_mask.vector))
                for const_var_size in const_var_sizes:
                    dim_sizes_program.add_global_variable(const_var_size)
                dim_sizes_program.add_function(foo)
                write_arrays_to_json(dim_sizes_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(dim_sizes_program)

                # A1 - foo argument, default sizes from define
                foo_arguments = []
                current_dim_sizes = []
                for i in range(len(var_sizes)):
                    if var_sizes_mask.get_bit(i):
                        foo_arguments.append(var_sizes[i])
                        current_dim_sizes.append(var_sizes[i])
                    else:
                        current_dim_sizes.append(define_sizes[i])
                A1 = ArrayC99('A1', Int, current_dim_sizes)
                foo_arguments.append(A1)

                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values))))

                dim_sizes_program = Program('mixed_dim_sizes_c99_fun_arg_arr_define_' + str(len(current_dim_sizes)) +
                                            'd_' + str(var_sizes_mask.vector))
                for define_size in define_sizes:
                    dim_sizes_program.add_define(define_size)
                dim_sizes_program.add_function(foo)
                write_arrays_to_json(dim_sizes_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(dim_sizes_program)

                # A1 - local variable
                foo_arguments = []
                current_dim_sizes = []
                for i in range(len(var_sizes)):
                    if var_sizes_mask.get_bit(i):
                        foo_arguments.append(var_sizes[i])
                        current_dim_sizes.append(var_sizes[i])
                    else:
                        current_dim_sizes.append(array_sizes_enum.constants[i])
                A1 = ArrayC99('A1', Int, current_dim_sizes)

                foo = Function('foo', Pointer(Int), foo_arguments)
                foo.set_body(CodeBlock(Assignment(A1.get_declaration(), malloc(Mul(SizeOf(Int), *current_dim_sizes))),
                                       pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values)),
                                       Return(A1)))

                dim_sizes_program = Program('mixed_dim_sizes_c99_local_arr_' + str(len(current_dim_sizes)) + 'd_' +
                                            str(var_sizes_mask.vector))
                dim_sizes_program.add_include(Include('stdlib.h'))
                dim_sizes_program.add_enum(array_sizes_enum)
                dim_sizes_program.add_function(foo)
                write_arrays_to_json(dim_sizes_program.name, self.output_dir, A1)
                generated_programs.append(dim_sizes_program)
        return generated_programs
