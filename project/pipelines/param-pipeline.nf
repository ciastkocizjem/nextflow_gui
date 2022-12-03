
process printStuff {
  output:
    stdout

  """
  printf '${params.foo}'
  """
}

workflow {
  printStuff | view { it.trim() }
}
