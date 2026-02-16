from tree_sitter import Language, Parser

Language.build_library(
  'my-languages2.so',
  [
    'vendor/tree-sitter-go',
    'vendor/tree-sitter-javascript',
    'vendor/tree-sitter-python',
    'vendor/tree-sitter-php/php',
    'vendor/tree-sitter-java',
    'vendor/tree-sitter-ruby',
    'vendor/tree-sitter-c-sharp'
  ]
)

print("\n✅ Parsers built successfully!")
