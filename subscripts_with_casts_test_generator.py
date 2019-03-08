from ctestgen.generator import *


class SubscriptsWithCastsTestGenerator(ArrayTestGenerator):
    def _generate_programs(self):
        generated_programs = list()

        for dim_sizes_names in self.dim_sizes_names_set:
            enum_constants = []
            var_sizes = []

            constant_value = 40
            for dim_size_name in dim_sizes_names:
                enum_constants.append(('ENUM_' + dim_size_name, constant_value))
                constant_value += 10
                var_sizes.append(Int('VAR_' + dim_size_name))

            array_sizes_enum = Enum(enum_constants)

            var_a = Int('a')
            var_b = Int('b')
            subscripts_mask = BitVector(9)

            for subscripts_mask.vector in range(subscripts_mask.num_system_base ** len(dim_sizes_names)):
                subscript_template_values = []
                subscript_template_value = 3
                for subscript_idx in range(len(dim_sizes_names)):
                    current_mask = subscripts_mask.get_bit(subscript_idx)
                    if current_mask == 0:
                        subscript_template_values.append((0, 0))
                    if current_mask == 1:
                        subscript_template_values.append((subscript_template_value, 0))
                        subscript_template_value += 2
                    if current_mask == 2:
                        subscript_template_values.append((0, subscript_template_value))
                        subscript_template_value += 2
                    if current_mask == 3:
                        subscript_template_values.append((subscript_template_value, subscript_template_value + 2))
                        subscript_template_value += 4
                    if current_mask == 4:
                        subscript_template_values.append((var_a, var_b))
                    if current_mask == 5:
                        subscript_template_values.append((subscript_template_value, var_b))
                        subscript_template_value += 2
                    if current_mask == 6:
                        subscript_template_values.append((var_a, subscript_template_value))
                        subscript_template_value += 2
                    if current_mask == 7:
                        subscript_template_values.append((var_a, 0))
                    if current_mask == 8:
                        subscript_template_values.append((0, var_b))

                A1 = Array('A1', Long, array_sizes_enum[0], var_sizes[1],
                           *[array_sizes_enum[i] for i in range(2, len(dim_sizes_names))])
                foo_arguments = [var_sizes[1], A1, var_a, var_b]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values))))

                subscripts_program = Program('mixed_sizes_mixed_subscripts_casts1_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)

                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Long, *[array_sizes_enum[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [A1, var_a, var_b]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values))))

                subscripts_program = Program('enum_sizes_mixed_subscripts_casts1_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Long, *[var_sizes[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [*[var_sizes[i] for i in range(len(dim_sizes_names))], A1, var_a, var_b]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values))))

                subscripts_program = Program('var_sizes_mixed_subscripts_casts1_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Int, array_sizes_enum[0], var_sizes[1],
                           *[array_sizes_enum[i] for i in range(2, len(dim_sizes_names))])
                foo_arguments = [var_sizes[1], A1, Long('a'), Long('b')]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  iter_var_type=Long)))

                subscripts_program = Program('mixed_sizes_mixed_subscripts_casts2_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)

                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Int, *[array_sizes_enum[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [A1, Long('a'), Long('b')]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  iter_var_type=Long)))

                subscripts_program = Program('enum_sizes_mixed_subscripts_casts2_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Int, *[var_sizes[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [*[var_sizes[i] for i in range(len(dim_sizes_names))], A1, Long('a'), Long('b')]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  iter_var_type=Long)))

                subscripts_program = Program('var_sizes_mixed_subscripts_casts2_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Char, array_sizes_enum[0], var_sizes[1],
                           *[array_sizes_enum[i] for i in range(2, len(dim_sizes_names))])
                foo_arguments = [var_sizes[1], A1, UInt('a'), UInt('b')]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  iter_var_type=UInt)))

                subscripts_program = Program('mixed_sizes_mixed_subscripts_casts3_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)

                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Char, *[array_sizes_enum[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [A1, UInt('a'), UInt('b')]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  iter_var_type=UInt)))

                subscripts_program = Program('enum_sizes_mixed_subscripts_casts3_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Char, *[var_sizes[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [*[var_sizes[i] for i in range(len(dim_sizes_names))], A1, UInt('a'), UInt('b')]
                foo = Function('foo', Void, foo_arguments)
                foo.set_body(CodeBlock(pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  iter_var_type=UInt)))

                subscripts_program = Program('var_sizes_mixed_subscripts_casts3_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Char, array_sizes_enum[0], var_sizes[1],
                           *[array_sizes_enum[i] for i in range(2, len(dim_sizes_names))])
                foo_arguments = [var_sizes[1], A1, UInt('a'), UInt('b')]
                foo = Function('foo', Void, foo_arguments)
                assignment_source = Long('source')
                foo.set_body(CodeBlock(Assignment(assignment_source.get_declaration(), 40),
                                       pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  assignment_source, UInt)))

                subscripts_program = Program('mixed_sizes_mixed_subscripts_casts4_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)

                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Char, *[array_sizes_enum[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [A1, UInt('a'), UInt('b')]
                foo = Function('foo', Void, foo_arguments)
                assignment_source = Long('source')
                foo.set_body(CodeBlock(Assignment(assignment_source.get_declaration(), 40),
                                       pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  assignment_source, UInt)))

                subscripts_program = Program('enum_sizes_mixed_subscripts_casts4_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)


                A1 = Array('A1', Char, *[var_sizes[i] for i in range(len(dim_sizes_names))])
                foo_arguments = [*[var_sizes[i] for i in range(len(dim_sizes_names))], A1, UInt('a'), UInt('b')]
                foo = Function('foo', Void, foo_arguments)
                assignment_source = Long('source')
                foo.set_body(CodeBlock(Assignment(assignment_source.get_declaration(), 40),
                                       pass_array(A1, ArrayLinearSubscriptTemplate(subscript_template_values),
                                                  assignment_source, UInt)))

                subscripts_program = Program('var_sizes_mixed_subscripts_casts4_' + str(len(dim_sizes_names)) + 'd_' +
                                             str(subscripts_mask.vector))
                subscripts_program.add_enum(array_sizes_enum)
                subscripts_program.add_function(foo)
                write_arrays_to_json(subscripts_program.name, self.output_dir, A1, is_function_argument=True)
                generated_programs.append(subscripts_program)
        return generated_programs
