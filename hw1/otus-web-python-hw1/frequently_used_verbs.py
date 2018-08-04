import ast
import os
import collections

import helper


def main():
    """

    This program outputs most frequently used verbs
    and their occurrence as pair
    for python projects in a directory

    """

    TOP_SIZE = 200
    PROJECTS = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]

    top_verbs = []

    # iterate over all project folders
    for project in PROJECTS:
        path = os.path.join('.', project)
        top_verbs += get_top_verbs_in_path(path)
    print(f'total {len(top_verbs)} top_verbs, {len(set(top_verbs))} unique')
    most_common_words = top_verbs
    for top_word, occurence in most_common_words: 
        print(top_word, occurence)


def get_top_verbs_in_path(path, top_size=10):
    trees = [t for t in get_trees(path) if t]
    flattened_list = helper.transform_to_list(trees)
    functions = [f for f in flattened_list if not helper.is_special_function(f)]
    helper.log_to_file('functions extracted')
    verbs = helper.flatten([get_verbs_from_function_name(function_name)
                            for function_name in functions])
    return collections.Counter(verbs).most_common(top_size)


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if helper.is_verb(word)]


def get_trees(path):
    paths_to_python_files = find_python_files(path=path, limit=100)
    helper.log_to_file('total %s files' % len(paths_to_python_files))
    trees = generate_trees(paths_to_python_files=paths_to_python_files)
    helper.log_to_file('trees generated')
    return trees


def find_python_files(path, limit):
    paths_to_python_files = []
    for dirname, _, files in os.walk(path, topdown=True):
        if len(paths_to_python_files) >= limit:
            break
        python_files = helper.custom_file_path_filter(files=files,
                                                      dirname=dirname,
                                                      extension=".py")
        paths_to_python_files.extend(python_files)
    return paths_to_python_files[:limit]


def generate_trees(paths_to_python_files):
    trees = []
    for python_file_path in paths_to_python_files:
        with open(python_file_path, 'r', encoding='utf-8') as py_file:
            py_file_content = py_file.read()
        tree = ast.parse(py_file_content)
        trees.append(tree)
    return trees


if __name__== "__main__":
    main()
